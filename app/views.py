from flask import render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/caregiver')
def caregiver_index():
    return render_template('role_index.html', role='caregiver')

@app.route('/client')
def client_index():
    return render_template('role_index.html', role='client')

@app.route('/styles')
def styles():
    return render_template('styles.html')
