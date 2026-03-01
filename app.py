from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, flash, session       
from db_connect import get_db_connection
import mysql.connector

import os
from dotenv import load_dotenv

load_dotenv() # This wakes up the .env file!

import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages"

def send_notification_email(recipient_email, subject, body):
    # Grab the credentials from your .env file
    sender_email = os.getenv('MAIL_USERNAME')
    sender_password = os.getenv('MAIL_PASSWORD')
    
    if not sender_email or not sender_password:
        print("⚠️ Email credentials missing in .env! Email skipped.")
        return

    try:
        # Construct the email
        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = f"TanushCare Hospital Network <{sender_email}>"
        msg['To'] = recipient_email

        # Connect to Gmail's secure server and send it!
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"📧 Email successfully sent to {recipient_email}!")
    except Exception as e:
        print(f"❌ Failed to send email to {recipient_email}. Error: {e}")

@app.route('/')
def home():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    
    cursor = conn.cursor(dictionary=True)
    
    # Fetch unique cities and all specialisations for the dropdowns
    cursor.execute("SELECT DISTINCT city FROM Hospital ORDER BY city ASC")
    cities = cursor.fetchall()
    
    cursor.execute("SELECT specialisationName FROM Specialisation ORDER BY specialisationName ASC")
    specialisations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('home.html', cities=cities, specialisations=specialisations)

@app.route('/doctors', methods=['GET'])
def doctors():
    # 1. Grab all parameters from the URL
    selected_city = request.args.get('city')
    selected_spec = request.args.get('specialisation')
    selected_hospital = request.args.get('hospital_id')
    sort_by = request.args.get('sort')
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    
    # 2. Dynamic Query Building (Preserving Team A's Logic)
    # We use "WHERE 1=1" so we can easily append AND conditions
    query = """
        SELECT d.doctorID, d.doctorName, d.experience, d.fees, 
               h.hospitalName, h.city, s.specialisationName
        FROM Doctor d
        JOIN Hospital h ON d.hospitalID = h.hospitalID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
        WHERE 1=1
    """
    params = []

    if selected_city:
        query += " AND h.city = %s"
        params.append(selected_city)
    if selected_spec:
        query += " AND s.specialisationName = %s"
        params.append(selected_spec)
    if selected_hospital:
        query += " AND h.hospitalID = %s"
        params.append(selected_hospital)

    # Team A's Availability Logic (EXISTS / NOT EXISTS)
    query += """
        AND (
            NOT EXISTS (SELECT 1 FROM DoctorSlots ds WHERE ds.doctorID = d.doctorID)
            OR
            EXISTS (
                SELECT 1 FROM DoctorSlots ds
                LEFT JOIN Appointment a ON ds.slotID = a.slotID
                WHERE ds.doctorID = d.doctorID
                AND (a.appointmentID IS NULL OR a.status = 'Cancelled')
            )
        )
    """

    # 3. Apply Sorting
    if sort_by == 'fees_asc':
        query += " ORDER BY d.fees ASC"
    elif sort_by == 'fees_desc':
        query += " ORDER BY d.fees DESC"
    elif sort_by == 'exp_desc':
        query += " ORDER BY d.experience DESC"
    else:
        query += " ORDER BY d.doctorName ASC"

    cursor.execute(query, tuple(params))
    real_doctors = cursor.fetchall()

    # 4. THE FIX: Fetch hospitals that actually have doctors for this search
    # This ensures the dropdown is populated and only shows "valid" choices
    hosp_query = """
        SELECT DISTINCT h.hospitalID, h.hospitalName 
        FROM Hospital h
        JOIN Doctor d ON h.hospitalID = d.hospitalID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
        WHERE 1=1
    """
    hosp_params = []
    if selected_city:
        hosp_query += " AND h.city = %s"
        hosp_params.append(selected_city)
    if selected_spec:
        hosp_query += " AND s.specialisationName = %s"
        hosp_params.append(selected_spec)
    
    hosp_query += " ORDER BY h.hospitalName ASC"
    cursor.execute(hosp_query, tuple(hosp_params))
    hospital_list = cursor.fetchall()
        
    cursor.close()
    conn.close()
    
    return render_template('doctors.html', 
                           doctors=real_doctors, 
                           hospitals=hospital_list, 
                           city=selected_city if selected_city else "", 
                           spec=selected_spec if selected_spec else "",
                           current_sort=sort_by,
                           current_hospital=selected_hospital)

@app.route('/logout')
def logout():
    # This completely clears the VIP wristband!
    session.clear()
    flash("You have been securely logged out.", "info")
    return redirect(url_for('home'))

@app.route('/appointments')
def dashboard():
    # 1. Check if the system remembers the family email
    if 'family_email' not in session:
        flash("Please book an appointment or log in to view your dashboard.", "warning")
        return redirect(url_for('home'))
        
    family_email = session['family_email']
    primary_user = session['primary_user']
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
        
    cursor = conn.cursor(dictionary=True)
    
    # 2. Fetch all appointments linked to this EMAIL, and grab the patient's name!
    query = """
        SELECT a.appointmentID, a.status, ds.date, ds.time, 
               d.doctorID, d.doctorName, s.specialisationName, p.name AS patientName
        FROM Appointment a
        JOIN Patient p ON a.patientID = p.patientID
        JOIN DoctorSlots ds ON a.slotID = ds.slotID
        JOIN Doctor d ON ds.doctorID = d.doctorID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
        WHERE p.email = %s
        ORDER BY ds.date ASC, ds.time ASC
    """
    cursor.execute(query, (family_email,))
    family_appointments = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('dashboard.html', appointments=family_appointments, patient_name=primary_user)

@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)

    # --- POST REQUEST: Process the Booking ---
    if request.method == 'POST':
        slot_id = request.form.get('slot_id')
        name = request.form.get('patient_name')
        email = request.form.get('patient_email')
        phone = request.form.get('patient_phone')
        dob = request.form.get('patient_dob')
        gender = request.form.get('patient_sex')

        try:
            # 1. Start Transaction (Concurrency Control)
            conn.start_transaction()

            # 2. Check for existing patient
            cursor.execute("""
                SELECT patientID FROM Patient 
                WHERE name = %s AND email = %s AND phone = %s AND dob = %s
            """, (name, email, phone, dob))
            existing_patient = cursor.fetchone()

            if existing_patient:
                patient_id = existing_patient['patientID']
            else:
                # 3. Insert new patient if not found
                cursor.execute("""
                    INSERT INTO Patient (name, email, phone, dob, gender)
                    VALUES (%s, %s, %s, %s, %s)
                """, (name, email, phone, dob, gender))
                # Grab the ID of the patient we just inserted
                patient_id = cursor.lastrowid 
            
            # --- UPDATED SESSION LOGIC ---
            # We now track the family email instead of a single patient ID
            session['family_email'] = email
            session['primary_user'] = name

            # 4. Create the Appointment
            cursor.execute("""
                INSERT INTO Appointment (slotID, patientID)
                VALUES (%s, %s)
            """, (slot_id, patient_id))

            # If no errors occurred, commit the transaction!
            conn.commit()

            # SEND NEW BOOKING EMAIL
            email_body = f"Hello {name},\n\nYour appointment is confirmed!\n\nThank you for booking with us. You can manage your appointment anytime by logging into your patient dashboard.\n\nStay healthy!"
            send_notification_email(email, "Appointment Confirmed!", email_body)
            
            flash("Appointment booked successfully!", "success")
            return redirect(url_for('dashboard'))

        except mysql.connector.IntegrityError:
            # CONCURRENCY TRIGGERED! Another user took this exact slotID
            conn.rollback()
            flash("Sorry! This slot was just booked by someone else. Please pick another time.", "danger")
            return redirect(url_for('doctors'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Booking failed: Please ensure all details are correct. Error: {e}", "danger")
            return redirect(url_for('doctors'))
            
        finally:
            cursor.close()
            conn.close()

    # --- GET REQUEST: Show the Form ---
    slot_id = request.args.get('slot_id')
    if not slot_id:
        flash("Please select a valid time slot first.", "warning")
        return redirect(url_for('doctors'))

    # *** THE 1-CLICK RESCHEDULE MAGIC ***
    if 'reschedule_id' in session:
        try:
            reschedule_id = session['reschedule_id']
            
            # Instantly update the existing appointment to the new slot
            cursor.execute("""
                UPDATE Appointment 
                SET slotID = %s 
                WHERE appointmentID = %s
            """, (slot_id, reschedule_id))
            
            conn.commit()
            session.pop('reschedule_id', None) # Rip up the sticky note

            # --- THE FIX: Grab the email and name from their session wristband! ---
            email = session.get('family_email')
            name = session.get('primary_user', 'Patient')

            # SEND RESCHEDULE EMAIL
            if email:
                email_body = f"Hello {name},\n\nYour appointment has been successfully rescheduled.\n\nThank you for choosing our hospital network. You can view your updated timeline on your dashboard.\n\nStay healthy!"
                send_notification_email(email, "Appointment Rescheduled - Update", email_body)
            # ----------------------------------------------------------------------
            
            flash("Appointment successfully rescheduled to your new time!", "success")
            return redirect(url_for('dashboard'))
            
        except Exception as e:
            conn.rollback()
            flash(f"Failed to reschedule. Please try again. Error: {e}", "danger")
            return redirect(url_for('dashboard'))
        finally:
            cursor.close()
            conn.close()
    
    # Fetch the details of the slot so the user knows what they are booking
    cursor.execute("""
        SELECT ds.time, ds.date, d.doctorName, h.hospitalName 
        FROM DoctorSlots ds
        JOIN Doctor d ON ds.doctorID = d.doctorID
        JOIN Hospital h ON d.hospitalID = h.hospitalID
        WHERE ds.slotID = %s
    """, (slot_id,))
    slot_details = cursor.fetchone()
    
    cursor.close()
    conn.close()

    return render_template('book_appointment.html', slot_id=slot_id, details=slot_details)

@app.route('/doctor/<int:doctor_id>', methods=['GET'])
def doctor_profile(doctor_id):
    target_date_str = request.args.get('date')
    
    # 1. Change default to TODAY so it's easier to test!
    if not target_date_str:
        target_date_str = date.today().strftime('%Y-%m-%d')
        
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
        
    cursor = conn.cursor(dictionary=True)
    
    # QUERY 1: Fetch Doctor Details
    cursor.execute("""
        SELECT d.doctorID, d.doctorName, d.experience, d.fees, d.appointmentDuration,
               h.hospitalName, h.address, h.city, h.state, s.specialisationName
        FROM Doctor d
        JOIN Hospital h ON d.hospitalID = h.hospitalID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
        WHERE d.doctorID = %s
    """, (doctor_id,))
    doctor = cursor.fetchone()
    
    if not doctor:
        return "Doctor not found", 404

    # QUERY 2: Check if slots exist for this date
    cursor.execute("SELECT COUNT(*) as count FROM DoctorSlots WHERE doctorID = %s AND date = %s", (doctor_id, target_date_str))
    slot_count = cursor.fetchone()['count']
    
    # QUERY 3: Dynamic Slot Generation
    if slot_count == 0:
        duration = doctor['appointmentDuration']
        
       # The work hours are from 9-5 
        current_time = datetime.strptime('09:00:00', '%H:%M:%S') 
        end_time = datetime.strptime('17:00:00', '%H:%M:%S')
        
        while current_time + timedelta(minutes=duration) <= end_time:
            time_str = current_time.strftime('%H:%M:%S')
            cursor.execute("""
                INSERT INTO DoctorSlots (doctorID, date, time)
                VALUES (%s, %s, %s)
            """, (doctor_id, target_date_str, time_str))
            current_time += timedelta(minutes=duration)
            
        conn.commit()

    # 2. Get Python's exact clock right now
    now = datetime.now()
    current_date_val = now.strftime('%Y-%m-%d')
    current_time_val = now.strftime('%H:%M:%S')

    # QUERY 4: Fetch Available Slots (Using Python's Clock!)
    cursor.execute("""
        SELECT ds.slotID, ds.time
        FROM DoctorSlots ds
        LEFT JOIN Appointment a ON ds.slotID = a.slotID
        WHERE ds.doctorID = %s AND ds.date = %s
        AND (a.appointmentID IS NULL OR a.status = 'Cancelled')
        
        -- The Python Timecheck!
        AND (ds.date > %s OR (ds.date = %s AND ds.time > %s))
        
        ORDER BY ds.time ASC
    """, (doctor_id, target_date_str, current_date_val, current_date_val, current_time_val))
    available_slots = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('doctor_profile.html', doctor=doctor, slots=available_slots, selected_date=target_date_str)

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check against the secret .env variables
        if email == os.getenv('ADMIN_EMAIL') and password == os.getenv('ADMIN_PASSWORD'):
            session['is_admin'] = True # Hand them the God-mode wristband!
            flash("Welcome, Administrator. God-mode activated.", "success")
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Admin Credentials.", "danger")
            return redirect(url_for('admin_login'))
            
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    # SECURITY CHECK
    if not session.get('is_admin'):
        flash("Access Denied. Administrators only.", "danger")
        return redirect(url_for('home'))
        
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    cursor = conn.cursor(dictionary=True)
    
    # 1. Fetch all doctors for the master table
    cursor.execute("""
        SELECT d.doctorID, d.doctorName, d.experience, d.fees, d.appointmentDuration,
               h.hospitalName, s.specialisationName
        FROM Doctor d
        JOIN Hospital h ON d.hospitalID = h.hospitalID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
        ORDER BY d.doctorID DESC
    """)
    all_doctors = cursor.fetchall()
    
    # 2. Fetch lists for the "Add Doctor" dropdown menus
    cursor.execute("SELECT hospitalID, hospitalName FROM Hospital ORDER BY hospitalName ASC")
    hospitals = cursor.fetchall()
    
    cursor.execute("SELECT specialisationID, specialisationName FROM Specialisation ORDER BY specialisationName ASC")
    specialisations = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('admin_dashboard.html', doctors=all_doctors, hospitals=hospitals, specialisations=specialisations)

@app.route('/admin/doctor/add', methods=['POST'])
def add_doctor():
    if not session.get('is_admin'):
        return redirect(url_for('home'))
        
    name = request.form.get('name')
    experience = request.form.get('experience')
    fees = request.form.get('fees')
    duration = request.form.get('duration')
    specialisation_id = request.form.get('specialisation_id')
    hospital_id = request.form.get('hospital_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO Doctor (doctorName, experience, fees, appointmentDuration, specialisationID, hospitalID)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (name, experience, fees, duration, specialisation_id, hospital_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash(f"Dr. {name} successfully added to the network!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/doctor/delete/<int:doctor_id>', methods=['POST'])
def delete_doctor(doctor_id):
    if not session.get('is_admin'):
        return redirect(url_for('home'))
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Because Team A used 'ON DELETE CASCADE' in the schema, deleting the doctor 
    # here will automatically delete all their slots and appointments too!
    cursor.execute("DELETE FROM Doctor WHERE doctorID = %s", (doctor_id,))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Doctor and all associated slots deleted.", "info")
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/doctor/edit/<int:doctor_id>', methods=['POST'])
def edit_doctor(doctor_id):
    # SECURITY CHECK
    if not session.get('is_admin'):
        return redirect(url_for('home'))
        
    # Grab the updated values typed into the popup form
    experience = request.form.get('experience')
    fees = request.form.get('fees')
    hospital_id = request.form.get('hospital_id')
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Run the SQL UPDATE command!
    cursor.execute("""
        UPDATE Doctor 
        SET experience = %s, fees = %s, hospitalID = %s 
        WHERE doctorID = %s
    """, (experience, fees, hospital_id, doctor_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    flash("Doctor details successfully updated!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/appointment/cancel/<int:appointment_id>', methods=['POST'])
def cancel_appointment(appointment_id):
    # Security check: Make sure they are logged in
    if 'family_email' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
    cursor = conn.cursor()
    
    # Update the status to 'Cancelled'
    cursor.execute("""
        UPDATE Appointment 
        SET status = 'Cancelled' 
        WHERE appointmentID = %s
    """, (appointment_id,))
    
    conn.commit()
    
    # Grab the family email from the session to send the alert!
    family_email = session.get('family_email')
    if family_email:
        email_body = "Hello,\n\nThis is a confirmation that your appointment has been cancelled. The time slot has been freed up for other patients.\n\nIf this was a mistake, please visit the dashboard to book a new appointment."
        send_notification_email(family_email, "Appointment Cancelled", email_body)
    
    cursor.close()
    conn.close()
    
    flash("Appointment has been successfully cancelled. The slot is now open for others.", "info")
    return redirect(url_for('dashboard'))

@app.route('/appointment/reschedule/<int:appointment_id>/<int:doctor_id>')
def start_reschedule(appointment_id, doctor_id):
    if 'family_email' not in session:
        return redirect(url_for('login'))
        
    # 1. Attach the sticky note to their session memory!
    session['reschedule_id'] = appointment_id
    
    flash("Please select a new time slot to reschedule your appointment.", "info")
    # 2. Send them to the doctor's profile to pick a new time
    return redirect(f"/doctor/{doctor_id}")


if __name__ == '__main__':
    app.run(debug=True, port=5001)