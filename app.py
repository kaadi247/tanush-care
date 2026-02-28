from datetime import datetime, timedelta, date
from flask import Flask, render_template, request, redirect, url_for, flash
from db_connect import get_db_connection

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages" 

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
    # Grab the search parameters from the URL (e.g., /doctors?city=Mumbai&specialisation=Cardiology)
    selected_city = request.args.get('city')
    selected_spec = request.args.get('specialisation')
    
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
        
    cursor = conn.cursor(dictionary=True)
    
    if selected_city and selected_spec:
        # Implementing Team A's EXACT Search Results Query
        query = """
            SELECT 
                d.doctorID, d.doctorName, d.experience, d.fees, 
                h.hospitalName, h.city, s.specialisationName
            FROM Doctor d
            JOIN Hospital h ON d.hospitalID = h.hospitalID
            JOIN Specialisation s ON d.specialisationID = s.specialisationID
            WHERE h.city = %s 
            AND s.specialisationName = %s
            AND (
                -- Case 1: Doctor has no slots at all (slots will be generated later)
                NOT EXISTS (
                    SELECT 1 FROM DoctorSlots ds WHERE ds.doctorID = d.doctorID
                )
                OR
                -- Case 2: Doctor has at least one available slot
                EXISTS (
                    SELECT 1 FROM DoctorSlots ds
                    LEFT JOIN Appointment a ON ds.slotID = a.slotID
                    WHERE ds.doctorID = d.doctorID
                    AND (a.appointmentID IS NULL OR a.status = 'Cancelled')
                )
            )
        """
        cursor.execute(query, (selected_city, selected_spec))
        real_doctors = cursor.fetchall()
    else:
        # Fallback if they just click "Find a Doctor" without searching: Show all doctors
        query = """
            SELECT d.doctorID, d.doctorName, d.experience, d.fees, 
                   h.hospitalName, h.city, s.specialisationName
            FROM Doctor d
            JOIN Hospital h ON d.hospitalID = h.hospitalID
            JOIN Specialisation s ON d.specialisationID = s.specialisationID
        """
        cursor.execute(query)
        real_doctors = cursor.fetchall()
        
    cursor.close()
    conn.close()
    
    return render_template('doctors.html', doctors=real_doctors)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # We are intentionally skipping the database insertion here for now!
        # Tomorrow, we will move the Patient INSERT logic to the booking route.
        flash("Registration simulated! Patient insertion will happen during booking tomorrow.", "info")
        return redirect(url_for('login'))
            
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/appointments')
def dashboard():
    return render_template('dashboard.html')

@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        flash("Appointment booked successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('book_appointment.html')

@app.route('/doctor/<int:doctor_id>', methods=['GET'])
def doctor_profile(doctor_id):
    # Get the date from the URL (e.g., ?date=2026-03-05). 
    # If no date is provided, default to tomorrow.
    target_date_str = request.args.get('date')
    if not target_date_str:
        target_date = date.today() + timedelta(days=1)
        target_date_str = target_date.strftime('%Y-%m-%d')
        
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
    
    # QUERY 3: Dynamic Slot Generation (if count is 0)
    if slot_count == 0:
        duration = doctor['appointmentDuration']
        
        # Let's simulate a clinic shift from 9:00 AM to 5:00 PM
        current_time = datetime.strptime('09:00:00', '%H:%M:%S')
        end_time = datetime.strptime('17:00:00', '%H:%M:%S')
        
        # While loop to generate slots
        while current_time + timedelta(minutes=duration) <= end_time:
            time_str = current_time.strftime('%H:%M:%S')
            
            cursor.execute("""
                INSERT INTO DoctorSlots (doctorID, date, time)
                VALUES (%s, %s, %s)
            """, (doctor_id, target_date_str, time_str))
            
            current_time += timedelta(minutes=duration)
            
        conn.commit() # Save the newly generated slots!

    # QUERY 4: Fetch Available Slots
    cursor.execute("""
        SELECT ds.slotID, ds.time
        FROM DoctorSlots ds
        LEFT JOIN Appointment a ON ds.slotID = a.slotID
        WHERE ds.doctorID = %s AND ds.date = %s
        AND (a.appointmentID IS NULL OR a.status = 'Cancelled')
        ORDER BY ds.time ASC
    """, (doctor_id, target_date_str))
    available_slots = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template('doctor_profile.html', doctor=doctor, slots=available_slots, selected_date=target_date_str)

if __name__ == '__main__':
    app.run(debug=True)