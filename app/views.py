
from app import app
from flask import render_template

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/patients')
def patients():
    return 'Display patients'

@app.route('/patient')
def individual_patient():
    return 'Individual patient'

