
from werkzeug.utils import redirect
from app import app, db
from app.models import Doctor
from flask import json, render_template, request, session, url_for, jsonify, flash

@app.route('/')
def index():
    if 'doctor' in session.keys():
        return render_template('patients.html')
    else:
        return render_template('main.html')

@app.route('/register-doctor', methods=['POST'])
def register_doctor():
    form = request.form
    doctor = Doctor(
        name=form['name'],
        email=form['email-address'],
        phone_number=form['phone-number'],
        government_id=form['government-id'])
    doctor.set_password(form['password'])
    db.session.add(doctor)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/validate-doctor', methods=['POST'])
def validate_doctor():
    if request.method == "POST":
        email_address = request.get_json()['email']
        doctor = Doctor.query.filter_by(email=email_address).first()
        if doctor:
            return jsonify({'user_exists': 'true'})
        else:
            return jsonify({'user_exists': 'false'})

@app.route('/validate-password', methods=['POST'])
def validate_password():
    if request.method == "POST":
        email_address = request.get_json()['email']
        password = request.get_json()['password']
        userFound = 'false'
        passwordCorrect = 'false'
        doctor = Doctor.query.filter_by(email=email_address).first()
        if doctor:
            userFound = 'true'
            if doctor.check_password(password):
                passwordCorrect = 'true'
        
        return jsonify({'user_exists': userFound, 'passwordCorrect': passwordCorrect})
        
@app.route('/login-doctor', methods=['POST'])
def login_doctor():
    form = request.form
    doctor = Doctor.query.filter_by(email=form['email-address']).first()
    print(doctor.check_password(form['password']))
    if doctor.check_password(form['password']):
        # if not, redirect to index and give flask message (don't worry about javascript validation)
        session['doctor'] = doctor.id
        return redirect(url_for('patients'))
    else:
        flash("Password was incorrect.")
        return redirect(url_for('index'))

@app.route('/logout-doctor', methods=['POST', 'GET'])
def logout_doctor():
    session.pop('doctor', None)
    return redirect(url_for('index'))


@app.route('/patients', methods=['POST', 'GET'])
def patients():
    doctor = None
    if session['doctor']:
        doctor = session['doctor']
    return render_template('patients.html')

@app.route('/patient')
def individual_patient():
    return 'Individual patient'

