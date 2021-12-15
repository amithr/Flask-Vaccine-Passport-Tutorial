
from app import app
from flask import render_template, request

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/patients', methods=['POST'])
def patients():
    email_address = request.form['email-address']
    return email_address

@app.route('/patient')
def individual_patient():
    return 'Individual patient'

