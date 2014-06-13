from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from app import db
from app.models import Agency, Caregiver, Client, Service, CaregiverForm, CaregiverFormInstance, ClientForm, ClientFormInstance
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index', alias=True)
@app.route('/overview', alias=True)
@login_required
def index():
    return render_template('index.html')

@app.route('/services/forms')
@login_required
def service_overview():
    return render_template('services_overview.html')

@app.route('/caregivers/forms')
@login_required
def caregiver_overview():
    return render_template('caregiver_overview.html')

@app.route('/caregivers/add')
@login_required
def caregiver_add_edit():
    return render_template('role_add_edit.html')

@app.route('/caregivers/<int:id>/edit')
@login_required
def caregiver_edit(id):
    return render_template('role_add_edit.html')


@app.route('/clients/add')
@login_required
def client_add_edit():
    return render_template('role_add_edit.html')


@app.route('/clients/<int:id>/edit')
@login_required
def client_edit(id):
    return render_template('role_add_edit.html')

@app.route('/services/add')
@login_required
def service_add_edit():
    return render_template('service_add_edit.html')

@app.route('/services/<int:id>/edit')
@login_required
def service_edit(id):
    return render_template('service_add_edit.html')

@app.route('/caregivers/<int:id>/forms/add')
@login_required
def caregiver_form_add(id):
    return render_template('role_form_add_edit.html')

@app.route('/clients/<int:id>/forms/add')
@login_required
def client_form_add(id):
    return render_template('role_form_add_edit.html')

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
    return render_template('client_overview.html')

@app.route('/caregivers')
@login_required
def caregiver_index():
    caregivers = Caregiver.query.all()
    return render_template('role_index.html', role='caregiver',
        items=caregivers)

@app.route('/caregivers/<int:id>')
@login_required
def caregiver(id):
    caregiver = Caregiver.query.get(id)
    expired_forms = caregiver.get_expired_forms()
    expiring_soon_forms = caregiver.get_expiring_soon_forms()
    non_urgent_forms = caregiver.get_non_urgent_forms()
    return render_template('caregiver.html',
            caregiver=caregiver,
            expired_forms = expired_forms,
            expiring_soon_forms = expiring_soon_forms,
            non_urgent_forms=non_urgent_forms)

@app.route('/clients')
@login_required
def client_index():
    clients = Client.query.all()
    return render_template('role_index.html', role='client',
        items=clients)

@app.route('/clients/<int:id>')
@login_required
def client(id):
    form_instances = db.session.query(ClientFormInstance).\
        join(ClientForm).\
        join(Client).\
        filter(Client.id==id).\
        order_by(ClientFormInstance.expiration_date.desc()).\
        all()
    return render_template('client.html',
            caregiver=Client.query.get(id),
            form_instances=form_instances)

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        name = request.form['name']
        password = request.form['password']
        registered_user = Agency.query.filter_by(name=name).first()
        if registered_user is None:
            flash('The name you entered does not belong to any account.<br>TODO link to a form where you input your email and it sends an email with the agency name.' , 'error')
            return render_template('login.html', form=form)
        if not registered_user.check_password(password):
            flash('The password you entered is incorrect.<br>TODO Forgot your password.' , 'error')
            return render_template('login.html', form=form)
        login_user(registered_user)
        flash('Welcome back, ' + registered_user.name)
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET','POST'])
def register():
    from flask.ext.wtf import Form
    from wtforms.ext.sqlalchemy.orm import model_form
    from .models import Agency
    RegisterForm = model_form(Agency, db_session=db.session, base_class=Form)
    model = Agency()
    form = RegisterForm(request.form, model)
    if form.validate_on_submit():
        form.populate_obj(model)
        flash('Please log in to continue.')
        return redirect(request.args.get('next') or url_for('index'))
    from pprint import pprint
    pprint(vars(form))
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
    service = Service.query.get(service_id)
    return render_template('service.html', item=service)

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
