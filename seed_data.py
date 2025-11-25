from sqlalchemy.orm import sessionmaker
from models import (
    Base,
    init_db,
    User,
    Administrator,
    Doctor,
    Patient,
    Appointment,
    Room,
    Treatment,
    MedicalRecord,
    Bill,
    Department,
)
from datetime import date, time

# Creates a connection to database
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

def ensure_user(email, password, user_type):
    user = session.query(User).filter(User.Email == email).first()
    if user:
        return user
    user = User(Email=email, Password=password, User_Type=user_type)
    session.add(user)
    session.flush()
    return user


def ensure_admin(user, first_name, last_name, dept_id=None):
    admin = session.query(Administrator).filter(Administrator.Admin_ID == user.User_ID).first()
    if admin:
        return admin
    admin = Administrator(
        Admin_ID=user.User_ID,
        First_Name=first_name,
        Last_Name=last_name,
        Dept_ID=dept_id,
    )
    session.add(admin)
    session.flush()
    return admin


def ensure_doctor(user, first_name, last_name, specialization):
    doctor = session.query(Doctor).filter(Doctor.Doctor_ID == user.User_ID).first()
    if doctor:
        return doctor
    doctor = Doctor(
        Doctor_ID=user.User_ID,
        First_Name=first_name,
        Last_Name=last_name,
        Specialization=specialization,
    )
    session.add(doctor)
    session.flush()
    return doctor


def ensure_patient(user, first_name, last_name, address, phone, condition, admission=None, discharge=None):
    patient = session.query(Patient).filter(Patient.Patient_ID == user.User_ID).first()
    if patient:
        return patient
    patient = Patient(
        Patient_ID=user.User_ID,
        First_Name=first_name,
        Last_Name=last_name,
        Address=address,
        Phone=phone,
        Admission_Date=admission,
        Discharge_Date=discharge,
        Condition=condition,
    )
    session.add(patient)
    session.flush()
    return patient


def ensure_department(name, head, doctor_id=None):
    dept = session.query(Department).filter(Department.Dept_name == name).first()
    if dept:
        return dept
    dept = Department(
        Dept_name=name,
        Dept_head=head,
        Doctor_ID=doctor_id,
    )
    session.add(dept)
    session.flush()
    return dept


def ensure_appointment(doctor_id, patient_id, appt_date, appt_time):
    appt = (
        session.query(Appointment)
        .filter(
            Appointment.Doctor_ID == doctor_id,
            Appointment.Patient_ID == patient_id,
            Appointment.Date == appt_date,
            Appointment.Time == appt_time,
        )
        .first()
    )
    if appt:
        return appt
    appt = Appointment(
        Doctor_ID=doctor_id,
        Patient_ID=patient_id,
        Date=appt_date,
        Time=appt_time,
    )
    session.add(appt)
    session.flush()
    return appt


def ensure_room(appt_id, room_type):
    room = session.query(Room).filter(Room.Appt_ID == appt_id).first()
    if room:
        return room
    room = Room(Appt_ID=appt_id, room_type=room_type)
    session.add(room)
    session.flush()
    return room


def ensure_medical_record(patient_id, doctor_id, diagnosis):
    record = (
        session.query(MedicalRecord)
        .filter(
            MedicalRecord.Patient_ID == patient_id,
            MedicalRecord.Doctor_ID == doctor_id,
            MedicalRecord.Diagnosis == diagnosis,
        )
        .first()
    )
    if record:
        return record
    record = MedicalRecord(
        Patient_ID=patient_id,
        Doctor_ID=doctor_id,
        Diagnosis=diagnosis,
    )
    session.add(record)
    session.flush()
    return record


def ensure_treatment(record_id, medicine, prescription):
    treatment = (
        session.query(Treatment)
        .filter(
            Treatment.Record_ID == record_id,
            Treatment.Medicine == medicine,
            Treatment.Prescription == prescription,
        )
        .first()
    )
    if treatment:
        return treatment
    treatment = Treatment(
        Record_ID=record_id,
        Medicine=medicine,
        Prescription=prescription,
    )
    session.add(treatment)
    session.flush()
    return treatment


def ensure_bill(patient_id, bill_date, cost):
    bill = (
        session.query(Bill)
        .filter(
            Bill.Patient_ID == patient_id,
            Bill.Date == bill_date,
            Bill.Cost == cost,
        )
        .first()
    )
    if bill:
        return bill
    bill = Bill(
        Patient_ID=patient_id,
        Date=bill_date,
        Cost=cost,
    )
    session.add(bill)
    session.flush()
    return bill


# -----------------------------
# Seed Users and Profiles
# -----------------------------
admin_user = ensure_user('admin@hospital.com', 'admin123', 'admin')
admin_profile = ensure_admin(admin_user, 'Anna', 'Admin')

doctor1_user = ensure_user('dr.smith@hospital.com', 'doc123', 'doctor')
doctor1 = ensure_doctor(doctor1_user, 'John', 'Smith', 'Cardiology')

doctor2_user = ensure_user('dr.jones@hospital.com', 'doc123', 'doctor')
doctor2 = ensure_doctor(doctor2_user, 'Alice', 'Jones', 'Neurology')

doctor3_user = ensure_user('dr.lee@hospital.com', 'doc123', 'doctor')
doctor3 = ensure_doctor(doctor3_user, 'David', 'Lee', 'Pediatrics')

patient1_user = ensure_user('patient@hospital.com', 'patient123', 'patient')
patient1 = ensure_patient(patient1_user, 'Emily', 'Stone', '123 Health St', '0401234567', 'Healthy')

patient2_user = ensure_user('michael@hospital.com', 'patient123', 'patient')
patient2 = ensure_patient(patient2_user, 'Michael', 'Brown', '456 Wellness Ave', '0407654321', 'Allergic Rhinitis')

patient3_user = ensure_user('sara@hospital.com', 'patient123', 'patient')
patient3 = ensure_patient(patient3_user, 'Sara', 'Connor', '789 Care Rd', '0405550000', 'Asthma')

# -----------------------------
# Seed Departments and link them
# -----------------------------
cardiology = ensure_department('Cardiology', 'Dr. John Smith', doctor1.Doctor_ID)
neurology = ensure_department('Neurology', 'Dr. Alice Jones', doctor2.Doctor_ID)
pediatrics = ensure_department('Pediatrics', 'Dr. David Lee', doctor3.Doctor_ID)

# link admin to a department if not set
if admin_profile.Dept_ID is None:
    admin_profile.Dept_ID = cardiology.Dept_ID
    session.flush()

# -----------------------------
# Seed Appointments
# -----------------------------
appt1 = ensure_appointment(doctor1.Doctor_ID, patient1.Patient_ID, date.today(), time(10, 0))
appt2 = ensure_appointment(doctor1.Doctor_ID, patient2.Patient_ID, date.today(), time(11, 30))
appt3 = ensure_appointment(doctor2.Doctor_ID, patient1.Patient_ID, date.today(), time(14, 0))
appt4 = ensure_appointment(doctor3.Doctor_ID, patient3.Patient_ID, date.today(), time(9, 15))

# -----------------------------
# Seed Rooms for some appointments
# -----------------------------
ensure_room(appt1.Appt_ID, 'consultation')
ensure_room(appt3.Appt_ID, 'examination')

# -----------------------------
# Seed Medical Records and Treatments
# -----------------------------
rec1 = ensure_medical_record(patient1.Patient_ID, doctor1.Doctor_ID, 'Routine check-up')
ensure_treatment(rec1.Record_ID, 'Vitamin D', 'Take 1000 IU daily')

rec2 = ensure_medical_record(patient2.Patient_ID, doctor1.Doctor_ID, 'Cardiac screening')
ensure_treatment(rec2.Record_ID, 'Aspirin', '81 mg daily')

rec3 = ensure_medical_record(patient3.Patient_ID, doctor3.Doctor_ID, 'Pediatric consultation')
ensure_treatment(rec3.Record_ID, 'Albuterol', 'Two puffs as needed')

# -----------------------------
# Seed Bills
# -----------------------------
ensure_bill(patient1.Patient_ID, date.today(), 120.00)
ensure_bill(patient2.Patient_ID, date.today(), 250.00)
ensure_bill(patient3.Patient_ID, date.today(), 80.00)

# -----------------------------
# Save all
# -----------------------------
session.commit()