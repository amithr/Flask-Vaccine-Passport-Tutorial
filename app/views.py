
from werkzeug.utils import redirect
from app import app, db
from app.models import Doctor
from flask import render_template, request, session, url_for

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/register-doctor')
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
    return render_template('main.html')

@app.route('/validate-doctor')
def validate_doctor():
    return

@app.route('/login-doctor')
def login_doctor():
    form = request.form
    doctor = Doctor.query.filter_by(email_address=form['email-address']).first()
    if doctor.check_password(form['password']):
        session['doctor'] = doctor
        return redirect(url_for('patients'))




@app.route('/patients', methods=['POST'])
def patients():
    doctor = session['doctor']
    return 'Successfully submitted!'

@app.route('/patient')
def individual_patient():
    return 'Individual patient'

