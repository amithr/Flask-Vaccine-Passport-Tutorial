import sqlite3 as db

conn = db.connect('vaccine_passport.db')

create_doctor_table_query = (''' CREATE TABLE IF NOT EXISTS DOCTORS
                                (ID            INTEGER     PRIMARY KEY,
                                 NAME          TEXT     NOT NULL,
                                 GOVERNMENT_ID CHAR(6)  NOT NULL UNIQUE,
                                 EMAIL_ADDRESS TEXT     NOT NULL UNIQUE,
                                 PHONE_NUMBER  CHAR(20) NOT NULL,
                                 PASSWORD      TEXT     NOT NULL
                                 );''')

conn.execute(create_doctor_table_query)

create_patient_table_query = (''' CREATE TABLE IF NOT EXISTS PATIENTS
                                (ID           INTEGER      PRIMARY KEY,
                                NAME          TEXT     NOT NULL,
                                EMAIL_ADDRESS TEXT     NOT NULL UNIQUE,
                                PHONE_NUMBER  CHAR(20) NOT NULL,
                                DOCTOR_ID     INTEGER      NOT NULL,
                                FOREIGN KEY(DOCTOR_ID) REFERENCES DOCTORS(ID)
                                );''')

conn.execute(create_patient_table_query)

create_dose_table_query = (''' CREATE TABLE IF NOT EXISTS DOSES
                                (ID           INTEGER      PRIMARY KEY,
                                VACCINE_ID    CHAR(6)  NOT NULL,
                                TYPE          TEXT     NOT NULL,
                                VOLUME        REAL     NOT NULL,
                                DATE          INTEGER  NOT NULL,
                                DOSE_NO     INTEGER  NOT NULL,
                                PATIENT_ID     INTEGER      NOT NULL,
                                FOREIGN KEY(PATIENT_ID) REFERENCES PATIENTS(ID)
                                );''')

conn.execute(create_dose_table_query)
conn.close()