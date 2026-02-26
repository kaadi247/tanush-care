from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Put this near the top of app.py, right under app = Flask(__name__)
MOCK_DOCTORS = [
    {"id": 1, "name": "Dr. Priya Sharma", "specialisation": "Cardiologist", "hospital": "City General", "rating": 4.8},
    {"id": 2, "name": "Dr. Rohan Mehta", "specialisation": "Neurologist", "hospital": "Sunrise Medical", "rating": 4.6}
]



# --- PAGE ROUTES ---

@app.route('/')
def home():
    return render_template('home.html')

# Update the doctors route to send this data to the template
@app.route('/doctors')
def doctors():
    return render_template('doctors.html', doctors=MOCK_DOCTORS)

@app.route('/appointments')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Logic to check email/password will go here
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Grab the data using the exact 'name' attributes Team C wrote
        name = request.form.get('patient_name')
        email = request.form.get('patient_email')
        phone = request.form.get('patient_phone')
        dob = request.form.get('patient_dob')
        sex = request.form.get('patient_sex')
        password = request.form.get('patient_password')
        
        # Print it to the terminal to prove we caught it
        print(f"SUCCESS! Received new patient: {name}, {email}, {dob}, {sex}")
        
        # Send them to the login page after registering
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/book', methods=['GET', 'POST'])
def book_appointment():
    if request.method == 'POST':
        # Logic to save the appointment will go here
        return redirect(url_for('dashboard'))
    return render_template('book_appointment.html')

if __name__ == '__main__':
    app.run(debug=True)