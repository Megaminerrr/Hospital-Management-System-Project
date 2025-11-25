from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import User, Patient, Doctor, Administrator, Appointment, Room, Treatment, session as db_session


app = Flask(__name__)
app.secret_key = "muuta_tähän_turvallinen_salaisuus"

# --- LOGIN API (POST) ---
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    user = db_session.query(User).filter(User.Email == email).first()
    if not user or user.Password != password:
        return render_template("index.html", error="Email or password is incorrect")

    session["user_id"] = user.User_ID
    session["user_type"] = user.User_Type

    if user.User_Type.lower() == "patient":
        patient = db_session.query(Patient).filter(Patient.Patient_ID == user.User_ID).first()
        session["patient_id"] = patient.Patient_ID
        return redirect(url_for("patient_page", patient_id=patient.Patient_ID))
    elif user.User_Type.lower() == "doctor":
        doctor = db_session.query(Doctor).filter(Doctor.Doctor_ID == user.User_ID).first()
        session["doctor_id"] = doctor.Doctor_ID
        return redirect(url_for("doctor_page", doctor_id=user.User_ID))
    elif user.User_Type.lower() == "admin":
        admin = db_session.query(Administrator).filter(Administrator.Admin_ID == user.User_ID).first()
        session["admin_id"] = admin.Admin_ID
        return redirect(url_for("admin_page", admin_id=user.User_ID))
    return "User logged in: " + user.User_Type

# --- MAIN PAGE ---
@app.route("/")
def index():
    return render_template("index.html", error=None)

# --- SIGN UP PAGE ---

@app.route("/signup", methods=["GET"])
def signup_page():
    return render_template("signup.html")

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json 

    email = data.get("email")
    password = data.get("password")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    address = data.get("address")
    phone = data.get("phone")

    # Check if email exists
    existing = db_session.query(User).filter_by(Email=email).first()
    if existing:
        return jsonify({"status": "error", "message": "Email already exists"}), 400

    # Create user (ALWAYS patient)
    new_user = User(
        Email=email,
        Password=password,
        User_Type="patient"
    )
    db_session.add(new_user)
    db_session.commit()

    # Create patient profile
    profile = Patient(
        Patient_ID=new_user.User_ID,
        First_Name=first_name,
        Last_Name=last_name,
        Address=address,
        Phone=phone
    )
    db_session.add(profile)
    db_session.commit()

    return jsonify({"status": "ok"})

# --- EDIT PROFILE PAGE ---
@app.route("/edit_profile")
def edit_profile():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user_type = session.get("user_type", "").lower()

    user = db_session.query(User).filter(User.User_ID == user_id).first()

    if user_type == "patient":
        patient = db_session.query(Patient).filter(Patient.Patient_ID == user_id).first()
        return render_template("editProfile.html", user=user, patient=patient)
    
    return redirect(url_for("profile"))


# --- PATIENT PAGE ---
@app.route("/patient/<int:patient_id>")
def patient_page(patient_id):
    if "patient_id" not in session or session["patient_id"] != patient_id:
        return redirect(url_for("index"))

    patient = db_session.query(Patient).filter(Patient.Patient_ID == patient_id).first()
    if not patient:
        return "Patient not found", 404

    return render_template("patient.html", patient=patient)

# --- USER PROFILE PAGES ---
@app.route("/profile")
def profile():
    if "user_id" not in session:
        return redirect("/")

    user_id = session["user_id"]
    user_type = session.get("user_type", "").lower()

    user = db_session.query(User).filter(User.User_ID == user_id).first()

    if user_type == "patient":
        patient = db_session.query(Patient).filter(Patient.Patient_ID == user_id).first()
        return render_template("patientFrontPage.html", user=user, patient=patient)
    elif user_type == "doctor":
        doctor = db_session.query(Doctor).filter(Doctor.Doctor_ID == user_id).first()
        return render_template("doctorFrontPage.html", user=user, doctor=doctor)

    return redirect("/")

# --- DOCTOR PAGE --- 
@app.route("/doctor/<int:doctor_id>")
def doctor_page(doctor_id):
    if "doctor_id" not in session or session["doctor_id"] != doctor_id:
        return redirect(url_for("index"))

    # get doctor from database
    doctor = db_session.query(Doctor).filter(Doctor.Doctor_ID == doctor_id).first()
    if not doctor:
        return "Doctor not found", 404
    return render_template("doctor.html", doctor=doctor)

# --- ADMINISTRATOR PAGE ---
@app.route("/admin/<int:admin_id>")
def admin_page(admin_id):
    if "admin_id" not in session or session["admin_id"] != admin_id:
        return redirect(url_for("index"))

    # get admin from database
    admin = db_session.query(Administrator).filter(Administrator.Admin_ID == admin_id).first()
    if not admin:
        return "Admin not found", 404
    return render_template("administrator.html", administrator=admin)

# --- LOGOUT ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

# --- Convenient 'back to home' function ---
@app.route("/home")
def home():
    user_type = session.get("user_type", "").lower()

    if user_type == "patient" and session.get("patient_id"):
        return redirect(url_for("patient_page", patient_id=session["patient_id"]))
    if user_type == "doctor" and session.get("doctor_id"):
        return redirect(url_for("doctor_page", doctor_id=session["doctor_id"]))
    if user_type == "admin" and session.get("admin_id"):
        return redirect(url_for("admin_page", admin_id=session["admin_id"]))

    # Fallback: not logged in or missing ids
    return redirect(url_for("index"))


# --- ViewRecords PAGE ---
@app.route("/ViewRecords")
def ViewRecords_self():
    if "admin_id" not in session:
        return redirect(url_for("index"))

    admin_id = session["admin_id"]
    admin = db_session.query(Administrator).filter(Administrator.Admin_ID == admin_id).first()
    if not admin:
        return "Admin not found", 404
    return render_template("ViewRecords.html", administrator=admin)

# --- Appointment View PAGE ---
@app.route("/AppointmentView/<int:user_id>")
def AppointmentView(user_id):
    if "user_id" not in session or session["user_id"] != user_id:
        return redirect("/")

    user_id = session["user_id"]
    user_type = session.get("user_type", "").lower()

    user = db_session.query(User).filter(User.User_ID == user_id).first()

    # Fetch appointments based on role
    appointments = []
    if user_type == "patient":
        appointments = db_session.query(Appointment).filter(Appointment.Patient_ID == user_id).all()
    elif user_type == "doctor":
        appointments = db_session.query(Appointment).filter(Appointment.Doctor_ID == user_id).all()
    elif user_type == "admin":
        # Admins see all appointments
        appointments = db_session.query(Appointment).all()

    return render_template("AppointmentView.html", user=user, user_type=user_type, appointments=appointments)

# --- Requests ---
@app.get("/api/patients")
def api_patients():
    patients = db_session.query(Patient).all()
    data = [
        {
            "Patient_ID": p.Patient_ID,
            "First_Name": p.First_Name,
            "Last_Name": p.Last_Name,
        }
        for p in patients
    ]
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/api/doctors")
def api_doctors():
    doctors = db_session.query(Doctor).all()
    data = [
        {
            "Doctor_ID": d.Doctor_ID,
            "First_Name": d.First_Name,
            "Last_Name": d.Last_Name,
            "Specialization": d.Specialization,
        }
        for d in doctors
    ]
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/api/appointments")
def api_appointments():
    appointments = db_session.query(Appointment).all()
    def serialize_dt(value):
        return str(value) if value is not None else None
    data = [
        {
            "Appt_ID": a.Appt_ID,
            "Doctor_ID": a.Doctor_ID,
            "Patient_ID": a.Patient_ID,
            "Date": serialize_dt(a.Date),
            "Time": serialize_dt(a.Time),
        }
        for a in appointments
    ]
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/api/rooms")
def api_rooms():
    rooms = db_session.query(Room).all()
    data = [
        {
            "Room_ID": r.Room_ID,
            "Appt_ID": r.Appt_ID,
            "room_type": r.room_type,
        }
        for r in rooms
    ]
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.get("/api/treatments")
def api_treatments():
    treatments = db_session.query(Treatment).all()
    # Note: frontend expects 'Perscription' (misspelling), so we output that key
    data = [
        {
            "Treatment_ID": t.Treatment_ID,
            "Medicine": t.Medicine,
            "Perscription": t.Prescription,
        }
        for t in treatments
    ]
    response = jsonify(data)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

if __name__ == "__main__":
    app.run(debug=True)
