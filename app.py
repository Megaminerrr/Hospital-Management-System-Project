from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from models import User, Patient, Doctor, Administrator, session as db_session

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

if __name__ == "__main__":
    app.run(debug=True)