from datetime import datetime
from app import db
from werkzeug.security import check_password_hash, generate_password_hash

class Doctor(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    government_id = db.Column(db.String(6), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    patients = db.relationship('Patient', backref='doctor', lazy=True)



    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Patient(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone_number = db.Column(db.String(12), unique=True, nullable=False)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    vaccine_doses = db.relationship('Vaccine_Dose', backref='patient')


class Vaccine_Dose(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(120), nullable=False)
    volume = db.Column(db.Numeric, nullable=False)
    dose_no = db.Column(db.Integer, nullable=False)
    dose_id = db.Column(db.String(6), nullable=False)
    dose_date = db.Column(db.DateTime(timezone=True), default=datetime.now)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))  

