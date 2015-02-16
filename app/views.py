from datetime import datetime
from flask import (
    request,
    flash,
    url_for,
    redirect,
    render_template,
    g
)
from flask.ext.login import (
    login_user,
    logout_user,
    current_user,
    login_required
)
from . import app, db
from .models import (
    Address,
    Agency,
    Caregiver,
    CaregiverForm as CaregiverFormModel,
    Client,
    ClientForm as ClientFormModel,
    Service,
    ClientFormInstance
)
from .forms import (
    CaregiverForm,
    ClientForm,
    EmailForm,
    LoginForm,
    PasswordForm,
    RegisterForm,
    RoleForm,
    ServiceForm
)
from .util.security import ts

@app.route('/reset', methods=["GET", "POST"])
def reset():
    if current_user.is_authenticated():
        return redirect(url_for("index"))
    form = EmailForm()
    if form.validate_on_submit():
        agency = Agency.query.filter_by(email=form.email.data).first_or_404()

        subject = "Password reset requested."

        token = ts.dumps(agency.email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True
        )

        html = 'hello ' + recover_url

        from flask_mail import Mail, Message

        mail = Mail()
        mail.init_app(app)
        msg = Message(
            "hello",
            sender="staff@roberttstephens.com",
            recipients=["roberttstephens@gmail.com"]
        )
        msg.html = html
        mail.send(msg)
        flash('An email has been sent to ' + agency.email + ' with a password reset link.')
        return redirect(url_for("login"))
    return render_template('reset.html', form=form)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    if current_user.is_authenticated():
        return redirect(url_for("index"))
    try:
        email = ts.loads(token, salt="recover-key", max_age=86400)
    except:
        abort(404)

    form = PasswordForm()

    if form.validate_on_submit():
        agency = Agency.query.filter_by(email=email).first_or_404()

        agency.set_password(form.password.data)

        db.session.add(agency)
        db.session.commit()

        flash('Your password has been successfully changed.')

        return redirect(url_for('login'))

    return render_template('reset_with_token.html', form=form, token=token)


@app.route('/')
@app.route('/index', alias=True)
@app.route('/overview', alias=True)
@login_required
def index():
    agency = g.user
    return render_template(
        'index.html',
        caregiver_forms=agency.urgent_caregiver_form_instances(),
        client_forms=agency.urgent_client_form_instances()
    )

@app.route('/services/forms')
@login_required
def service_overview():
    return render_template('services_overview.html')

@app.route('/caregivers/forms')
@login_required
def caregiver_overview():
    agency = g.user
    return render_template(
        'caregiver_overview.html',
        urgent_forms=agency.urgent_caregiver_form_instances(),
        non_urgent_forms=agency.non_urgent_caregiver_form_instances()
    )

@app.route('/caregivers/add', methods=['GET', 'POST'])
@login_required
def caregiver_add():
    form = CaregiverForm()
    if form.validate_on_submit():
        caregiver = Caregiver()
        address = Address()
        form.populate_obj(address)
        form.populate_obj(caregiver)
        caregiver.address = address
        caregiver.status = True
        caregiver.agency = g.user
        db.session.add(caregiver)
        db.session.commit()
        return redirect(url_for("caregiver", caregiver_id=caregiver.id))
    return render_template(
        'caregiver_add.html',
        form=form,
    )

@app.route('/caregivers/<int:caregiver_id>/edit', methods=['GET', 'POST'])
@login_required
def caregiver_edit(caregiver_id):
    caregiver = Caregiver.query.filter_by(id=caregiver_id).first_or_404()
    form = CaregiverForm(obj=caregiver, **caregiver.address.data)
    if form.validate_on_submit():
        form.populate_obj(caregiver)
        form.populate_obj(caregiver.address)
        db.session.add(caregiver)
        db.session.commit()
        return redirect(url_for("caregiver", caregiver_id=caregiver.id))
    return render_template(
        'caregiver_edit.html',
        caregiver=caregiver,
        form=form,
    )


@app.route('/clients/add', methods=['GET', 'POST'])
@login_required
def client_add():
    form = ClientForm()
    if form.validate_on_submit():
        client = Client()
        address = Address()
        form.populate_obj(address)
        form.populate_obj(client)
        client.address = address
        client.status = True
        client.agency = g.user
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("client", client_id=client.id))
    return render_template(
        'client_add.html',
        form=form,
    )


@app.route('/clients/<int:client_id>/edit', methods=['GET', 'POST'])
@login_required
def client_edit(client_id):
    client = Client.query.filter_by(id=client_id).first_or_404()
    form = ClientForm(obj=client, **client.address.data)
    if form.validate_on_submit():
        form.populate_obj(client)
        form.populate_obj(client.address)
        db.session.add(client)
        db.session.commit()
        return redirect(url_for("client", client_id=client.id))
    return render_template(
        'client_edit.html',
        client=client,
        form=form,
    )

@app.route('/services/add', methods=['GET', 'POST'])
@login_required
def service_add():
    form = ServiceForm(
        caregiver_id=request.args.get('caregiver_id'),
        client_id=request.args.get('client_id')
    )
    caregiver_disabled = False
    client_disabled = False
    if request.args.get('caregiver_id'):
        caregiver_disabled = True
        next_url = url_for('caregiver', caregiver_id=request.args.get('caregiver_id'))
    if request.args.get('client_id'):
        client_disabled = True
        next_url = url_for('client', client_id=request.args.get('client_id'))
    caregivers = Caregiver.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        order_by(Caregiver.name.asc()).\
        all()
    form.caregiver_id.choices = [(c.id, c.name) for c in caregivers]
    clients = Client.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        order_by(Client.name.asc()).\
        all()
    form.client_id.choices = [(c.id, c.name) for c in clients]
    if form.validate_on_submit():
        service = Service()
        form.populate_obj(service)
        service.status = True
        service.agency = g.user
        db.session.add(service)
        db.session.commit()
        flash('Successfully added ' + service.name)
        if next_url:
            return redirect(next_url)
    return render_template(
        'service_add_edit.html',
        form=form,
        caregiver_disabled=caregiver_disabled,
        client_disabled=client_disabled,
    )

@app.route('/services/<int:service_id>/edit', methods=['GET', 'POST'])
@login_required
def service_edit(service_id):
    service = Service.query.filter_by(id=service_id).first_or_404()
    form = ServiceForm(obj=service)
    caregivers = Caregiver.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        order_by(Caregiver.name.asc()).\
        all()
    form.caregiver_id.choices = [(c.id, c.name) for c in caregivers]
    clients = Client.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        order_by(Client.name.asc()).\
        all()
    form.client_id.choices = [(c.id, c.name) for c in clients]
    if form.validate_on_submit():
        form.populate_obj(service)
        db.session.add(service)
        db.session.commit()
        return redirect(url_for("service", service_id=service.id))
    return render_template(
        'service_add_edit.html',
        form=form
    )

@app.route('/caregivers/<int:caregiver_id>/forms/add', methods=['GET', 'POST'])
@login_required
def caregiver_form_add(caregiver_id):
    caregiver = Caregiver.\
        query.\
        filter(Caregiver.id == caregiver_id).\
        filter(Agency.id == g.user.id).\
        first_or_404()
    form = RoleForm()
    if form.validate_on_submit():
        caregiver_form = CaregiverFormModel()
        form.populate_obj(caregiver_form)
        caregiver_form.status = True
        caregiver_form.caregiver = caregiver
        db.session.add(caregiver_form)
        db.session.commit()
        flash('Successfully added ' + caregiver_form.name)
        next_url = url_for('caregiver', caregiver_id=caregiver_id)
        return redirect(next_url)
    return render_template(
        'caregiver_form_add.html',
        form=form
    )

@app.route('/clients/<int:client_id>/forms/add', methods=['GET', 'POST'])
@login_required
def client_form_add(client_id):
    client = Client.\
        query.\
        filter(Client.id == client_id).\
        filter(Agency.id == g.user.id).\
        first_or_404()
    form = RoleForm()
    if form.validate_on_submit():
        client_form = ClientFormModel()
        form.populate_obj(client_form)
        client_form.status = True
        client_form.client = client
        db.session.add(client_form)
        db.session.commit()
        flash('Successfully added ' + client_form.name)
        next_url = url_for('client', client_id=client_id)
        return redirect(next_url)
    return render_template(
        'client_form_add.html',
        form=form
    )

@app.route('/caregivers/<int:caregiver_id>/forms/<int:form_id>/edit')
@login_required
def caregiver_form_edit(caregiver_id, form_id):
    return render_template('role_form_add_edit.html')

@app.route('/clients/<int:client_id>/forms/<int:form_id>/edit')
@login_required
def client_form_edit(client_id, form_id):
    return render_template('role_form_add_edit.html')


@app.route('/clients/forms')
@login_required
def client_overview():
    agency = g.user
    return render_template(
        'client_overview.html',
        urgent_forms=agency.urgent_client_form_instances(),
        non_urgent_forms=agency.non_urgent_client_form_instances()
    )

@app.route('/caregivers')
@login_required
def caregiver_index():
    caregivers = Caregiver.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        all()
    return render_template(
        'role_index.html',
        role='caregiver',
        items=caregivers
    )

@app.route('/caregivers/<int:caregiver_id>')
@login_required
def caregiver(caregiver_id):
    caregiver = Caregiver.query.filter_by(id=caregiver_id).first_or_404()
    return render_template(
        'caregiver.html',
        caregiver=caregiver,
        urgent=caregiver.urgent_form_instances(),
        non_urgent=caregiver.non_urgent_form_instances()
    )

@app.route('/clients')
@login_required
def client_index():
    clients = Client.query.\
        join(Agency).\
        filter(Agency.id == g.user.id).\
        all()
    return render_template(
        'role_index.html',
        role='client',
        items=clients
    )

@app.route('/clients/<int:client_id>')
@login_required
def client(client_id):
    client = Client.query.filter_by(id=client_id).first_or_404()
    return render_template(
        'client.html',
        client=client,
        urgent=client.urgent_form_instances(),
        non_urgent=client.non_urgent_form_instances()
    )

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        name = request.form['name']
        password = request.form['password']
        registered_user = Agency.query.filter_by(name=name).first()
        if registered_user is None:
            flash(
                'The name you entered does not belong to any account.<br>TODO link to a form where you input your email and it sends an email with the agency name.',
                'error'
            )
            return render_template('login.html', form=form)
        if not registered_user.check_password(password):
            flash(
                'The password you entered is incorrect. <br>'
                '<a href="' + url_for('reset', _external=True) + '">Click here'
                '</a> to reset your password.',
                'error'
            )
            return render_template('login.html', form=form)
        login_user(registered_user)
        registered_user.access = datetime.utcnow()
        db.session.add(registered_user)
        db.session.commit()
        flash('Welcome back, ' + registered_user.name)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        address = Address(
            address_1 = form.address_1.data,
            address_2 = form.address_2.data,
            city = form.city.data,
            state = form.state.data,
            zip_code = form.zip_code.data,
        )
        agency = Agency(
            name = form.name.data,
            email = form.email.data,
            contact_name = form.contact_name.data,
            contact_title = form.contact_title.data,
            phone_number = form.phone_number.data,
            phone_extension = form.phone_extension.data,
            status = True,
            address = address,
        )
        agency.set_password(form.password.data)
        db.session.add(agency)
        db.session.commit()
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('register.html', form=form)

@app.route('/styles')
def styles():
    return render_template('styles.html')

@app.route('/forms')
def form():
    return render_template('form.html')

@app.route('/caregivers/<int:caregiver_id>/forms/<int:form_id>')
def caregiver_form(caregiver_id, form_id):
    print(caregiver_id)
    caregiver = Caregiver.query.get(caregiver_id)
    return render_template('role_form.html', role='caregiver', item=caregiver)

@app.route('/clients/<int:client_id>/forms/<int:form_id>')
def client_form(client_id, form_id):
    print(client_id)
    client = Client.query.get(client_id)
    return render_template('role_form.html', role='client', item=client)

@app.route('/services/<int:service_id>/forms/<int:form_id>')
def service_form(service_id, form_id):
    print(service_id)
    service = Service.query.get(service_id)
    return render_template('service_form.html', item=service)

@app.route('/services/<int:service_id>')
def service(service_id):
    service = Service.query.filter_by(id=service_id).first_or_404()
    return render_template('service.html', service=service)

@app.route('/services/<int:service_id>/forms/<int:form_id>/edit')
def service_form_edit(service_id, form_id):
    service = Service.query.get(service_id)
    return render_template('service_form_add_edit.html', item=service)

@app.route('/services/<int:service_id>/forms/add')
def service_form_add(service_id):
    service = Service.query.get(service_id)
    return render_template('service_form_add_edit.html', item=service)

@app.before_request
def before_request():
    g.user = current_user
