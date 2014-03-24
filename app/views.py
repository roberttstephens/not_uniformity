from flask import Flask, session, request, flash, url_for, redirect, render_template, abort, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app
from app.models import Agency

@app.route('/')
@app.route('/index', alias=True)
@login_required
def index():
    return render_template('index.html')

@app.route('/caregiver')
def caregiver_index():
    return render_template('role_index.html', role='caregiver')

@app.route('/client')
def client_index():
    return render_template('role_index.html', role='client')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    username = request.form['username']
    password = request.form['password']
    registered_user = Agency.query.filter_by(name=username, password=password).first()
    if registered_user is None:
        flash('Username or Password is invalid' , 'error')
        return redirect(url_for('login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['username'] , request.form['password'],request.form['email'])
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('login'))

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
