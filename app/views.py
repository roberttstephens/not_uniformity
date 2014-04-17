from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from app import db
from app.models import Agency, Caregiver, Client
from app.forms import LoginForm, RegisterForm

@app.route('/')
@app.route('/index', alias=True)
@app.route('/overview', alias=True)
@login_required
def index():
    return render_template('index.html')

@app.route('/caregivers')
@login_required
def caregiver_index():
    caregivers = Caregiver.query.all()
    return render_template('role_index.html', role='caregiver',
        items=caregivers)

@app.route('/caregiver/<int:id>')
@login_required
def caregiver(id):
    return render_template('caregiver.html', caregiver=Caregiver.query.get(id))

@app.route('/clients')
@login_required
def client_index():
    clients = Client.query.all()
    return render_template('role_index.html', role='client',
        items=clients)

@app.route('/client/<int:id>')
@login_required
def client(id):
    return render_template('caregiver.html', caregiver=Client.query.get(id))

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

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/caregiver_form')
def caregiver_form():
    return render_template('role_form.html', role='caregiver')

@app.route('/client_form')
def client_form():
    return render_template('role_form.html', role='client')

@app.before_request
def before_request():
    g.user = current_user
