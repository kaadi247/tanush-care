from flask import Flask, render_template, request, redirect, url_for, flash
from db_connect import get_db_connection

app = Flask(__name__)
app.secret_key = "super_secret_key_for_flash_messages" 

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/doctors')
def doctors():
    # 1. Connect to the database
    conn = get_db_connection()
    if not conn:
        return "Database connection failed", 500
        
    cursor = conn.cursor(dictionary=True)
    
    # 2. Fetch real doctors using Team A's JOIN logic
    query = """
        SELECT d.doctorID, d.doctorName, d.experience, d.fees, d.appointmentDuration,
               h.hospitalName, h.address, h.city, h.state, s.specialisationName
        FROM Doctor d
        JOIN Hospital h ON d.hospitalID = h.hospitalID
        JOIN Specialisation s ON d.specialisationID = s.specialisationID
    """
    cursor.execute(query)
    real_doctors = cursor.fetchall()
    
    # 3. Close the connection
    cursor.close()
    conn.close()
    
    # 4. Send the real SQL data to the HTML template
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