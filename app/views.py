
from werkzeug.utils import redirect
from app import app, db
from app.models import Doctor, Patient, Vaccine_Dose
from flask import json, render_template, request, session, url_for, jsonify, flash
from fpdf import FPDF
import qrcode
import os

@app.route('/')
def index():
    if 'doctor' in session.keys():
        return redirect(url_for('patients'))
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

    if doctor and doctor.check_password(form['password']):
        # if not, redirect to index and give flask message (don't worry about javascript validation)
        session['doctor'] = doctor.id
        return redirect(url_for('patients'))
    else:
        flash("Password was incorrect or user doesn't exist.")
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
        patients = Patient.query.filter_by(doctor_id=doctor)
        return render_template('patients.html', patients=patients)
    return render_template('patients.html')

@app.route('/register-patient', methods=['POST', 'GET'])
def register_patient():
    form = request.form
    email = form['email-address']
    patient = Patient.query.filter_by(email=email).first()
    if not patient:
        patient = Patient(
            name=form['name'],
            email=email,
            phone_number=form['phone-number'],
            doctor_id=session['doctor'])
        db.session.add(patient)
        db.session.commit()
        flash('Patient successfully registered')
        return redirect(url_for('patients'))
    else:
        flash('Patient already exists')
        return redirect(url_for('patients'))

@app.route('/vaccine-record/<patient_id>', methods=['GET', 'POST'])
def vaccine_record(patient_id):
    if not patient_id:
        return redirect(url_for('patients'))
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient:
        vaccine_doses = Vaccine_Dose.query.filter_by(patient_id=patient_id)
        return render_template('vaccine_record.html', vaccine_doses=vaccine_doses, patient_id=patient_id)
    return render_template('vaccine_record.html')

@app.route('/add-vaccine-record/<patient_id>', methods=['POST', 'GET'])
def add_vaccine_record(patient_id):
    form = request.form
    dose_id = form['dose-id']
    dose_number = form['dose-number']
    vaccine_dose = Vaccine_Dose.query.filter_by(patient_id=patient_id, dose_no=dose_number).first()
    if vaccine_dose:
        flash('This dose number has already been entered.')
        return redirect(url_for('vaccine_record', patient_id=patient_id))
    vaccine_dose = Vaccine_Dose.query.filter_by(dose_id=dose_id).first()
    if vaccine_dose:
        flash('A dose with this serial number already exists in the database')
        return redirect(url_for('vaccine_record', patient_id=patient_id))
    vaccine_dose = Vaccine_Dose(
        type=form['type'],
        volume=form['volume'],
        dose_no=form['dose-number'],
        dose_id=dose_id,
        patient_id=patient_id
    )
    db.session.add(vaccine_dose)
    db.session.commit()
    flash('Vaccine dose successfully added.')
    return redirect(url_for('vaccine_record', patient_id=patient_id))
    
@app.route('/delete-vaccine-record/<patient_id>/<vaccine_id>', methods=['GET'])
def delete_vaccine_record(patient_id, vaccine_id):
    Vaccine_Dose.query.filter_by(id=vaccine_id).delete()
    db.session.commit()
    flash('Vaccine dose successfully deleted.')
    return redirect(url_for('vaccine_record', patient_id=patient_id))

def generate_qr_code(link, user_id):
    #Creating an instance of qrcode
    qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    file_name = "qr_code-"+str(user_id)+".png"
    path = os.path.join("app/static", file_name)
    img.save(path)
    return path

def generate_pdf(patient):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    name_string = "Name: "+ patient.name
    id_string = "ID: " + str(patient.id)
    email_string = "Email: " + patient.email
    doctor_id_string = "Doctor ID: " + str(patient.doctor_id)
    pdf.cell(40, 10, name_string, ln=2, align="L")
    pdf.cell(40, 10, id_string, ln=2, align="L")
    pdf.cell(40, 10, email_string, ln=2, align="L")
    pdf.cell(40, 10, doctor_id_string, ln=2, align="L")
    verification_path = url_for('verify_vaccination_status', patient_id=patient.id, _external=True)
    img_path = generate_qr_code(verification_path, patient.id)
    pdf.cell(40, 10, "Scan QR Code to verify: ")
    pdf.image(img_path, x=50, y=100)
    pdf.output('vaccine_passport.pdf', 'F')
    return True

@app.route('/send-certificate/<patient_id>', methods=['GET'])
def send_certificate(patient_id):
    if not patient_id:
        return redirect(url_for('patients'))
    patient = Patient.query.filter_by(id=patient_id).first()
    if patient:
        generate_pdf(patient)
        flash("Certificate generated")
        return redirect(url_for('patients'))
    else:
        flash("Error generating certificate")
        return redirect(url_for('patients'))

@app.route('/verify-vaccination-status/<patient_id>', methods=['GET'])
def verify_vaccination_status(patient_id):
    if not patient_id:
        return redirect(url_for('patients'))
    patient = Patient.query.filter_by(id=patient_id).first()
    if(len(patient.vaccine_doses) >= 2):
        return "Fully Vaccinated"
    else:
        return "Not Fully Vaccinated"

