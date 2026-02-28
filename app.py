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

if __name__ == '__main__':
    app.run(debug=True)