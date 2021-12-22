import sqlite3 as db
import os

def register_doctor(input_dict):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    SQLPATH = os.path.join(BASE_DIR, "vaccine_passport.db")
    conn = db.connect(SQLPATH)
    conn.execute("INSERT INTO DOCTORS (NAME, GOVERNMENT_ID, EMAIL_ADDRESS, PHONE_NUMBER, PASSWORD) \
    VALUES (?,?,?,?,?)", (input_dict['name'],input_dict['government-id'],input_dict['email-address'], input_dict['phone-number'], input_dict['password']))
    conn.commit()
    conn.close()

def is_doctor_login_valid(input_dict):
    conn = db.connect('vaccine_passport.db')
    results_array = []
    cursor = conn.execute("SELECT ID, PASSWORD from DOCTORS where EMAIL_ADDRESS = ? LIMIT 1) \
    VALUES (?)", (input_dict['email_address']))
    conn.close()
    for row in cursor:
        results_array = [row[0], row[1]]
    
    if results_array[1] == input_dict['password']:
        return results_array[0]

def get_doctor_by_id(id):
    conn = db.connect('vaccine_passport.db')
    results_array = []
    cursor = conn.execute("SELECT NAME, GOVERNMENT_ID, EMAIL_ADDRESS, PHONE_NUMBER from DOCTORS where ID = ? LIMIT 1) \
    VALUES (?)", (id))
    conn.close()
    for row in cursor:
        results_array = [row[0], row[1], row[2], row[3]]
    
    return results_array





