from sqlalchemy.orm import sessionmaker
from models import Base, init_db, User, Administrator, Doctor, Patient

# Creates a connection to database
engine = init_db()
Session = sessionmaker(bind=engine)
session = Session()

# -----------------------------
# Add Admin
# -----------------------------
admin_user = User(
    Email='admin@hospital.com',
    Password='admin123',
    User_Type='admin'
)
session.add(admin_user)
session.flush()

admin_profile = Administrator(
    Admin_ID=admin_user.User_ID,
    First_Name='Anna',
    Last_Name='Admin',
    Dept_ID=None
)
session.add(admin_profile)

# -----------------------------
# Add Doctor
# -----------------------------
doctor_user = User(
    Email='dr.smith@hospital.com',
    Password='doc123',
    User_Type='doctor'
)
session.add(doctor_user)
session.flush()

doctor_profile = Doctor(
    Doctor_ID=doctor_user.User_ID,
    First_Name='John',
    Last_Name='Smith',
    Specialization='Cardiology'
)
session.add(doctor_profile)

# -----------------------------
# Add Patient
# -----------------------------
patient_user = User(
    Email='patient@hospital.com',
    Password='patient123',
    User_Type='patient'
)
session.add(patient_user)
session.flush()

patient_profile = Patient(
    Patient_ID=patient_user.User_ID,
    First_Name='Emily',
    Last_Name='Stone',
    Address='123 Health St',
    Phone='0401234567',
    Admission_Date=None,
    Discharge_Date=None,
    Condition='Healthy'
)
session.add(patient_profile)

# -----------------------------
# Save all
# -----------------------------
session.commit()