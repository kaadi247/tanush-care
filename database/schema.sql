CREATE DATABASE IF NOT EXISTS vital_link_db;
USE vital_link_db;

CREATE TABLE IF NOT EXISTS Patient (
    patientID INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone CHAR(10) NOT NULL,
    dob DATE NOT NULL,
    gender ENUM('Male', 'Female', 'Other') NOT NULL,
    -- Removed CHECK with CURDATE() - this should be handled at application level
    -- or use a trigger if absolutely needed
    CONSTRAINT email_format CHECK (email REGEXP '^[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT phone_format CHECK (phone REGEXP '^[0-9]{10}$')
    -- Note: The backslashes in REGEXP need to be escaped in MySQL
);

CREATE TABLE IF NOT EXISTS Hospital (
    hospitalID INT AUTO_INCREMENT PRIMARY KEY,
    hospitalName VARCHAR(150) NOT NULL,
    address VARCHAR(255) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    contactEmail VARCHAR(100) NOT NULL UNIQUE,
    contactPhone CHAR(10) NOT NULL UNIQUE,
    CONSTRAINT hospital_email_format CHECK (contactEmail REGEXP '^[A-Za-z0-9.%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$'),
    CONSTRAINT hospital_phone_format CHECK (contactPhone REGEXP '^[0-9]{10}$')
);

CREATE TABLE IF NOT EXISTS Specialisation (
    specialisationID INT AUTO_INCREMENT PRIMARY KEY,
    specialisationName VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS Doctor (
    doctorID INT AUTO_INCREMENT PRIMARY KEY,
    doctorName VARCHAR(100) NOT NULL,
    experience INT NOT NULL,
    fees INT NOT NULL,
    appointmentDuration INT NOT NULL,
    specialisationID INT NOT NULL,
    hospitalID INT NOT NULL,
    CONSTRAINT experience_positive CHECK (experience >= 0),
    CONSTRAINT fees_positive CHECK (fees > 0),
    CONSTRAINT duration_range CHECK (appointmentDuration BETWEEN 5 AND 60),
    FOREIGN KEY (specialisationID) REFERENCES Specialisation (specialisationID) ON DELETE RESTRICT ON UPDATE CASCADE,
    FOREIGN KEY (hospitalID) REFERENCES Hospital (hospitalID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS DoctorSlots (
    slotID INT AUTO_INCREMENT PRIMARY KEY,
    doctorID INT NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    -- Added constraint to prevent past dates
    -- CONSTRAINT future_or_present_date CHECK (date >= CURRENT_DATE),
    UNIQUE (doctorID, date, time),
    FOREIGN KEY (doctorID) REFERENCES Doctor (doctorID) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS Appointment (
    appointmentID INT AUTO_INCREMENT PRIMARY KEY,
    slotID INT NOT NULL UNIQUE,
    patientID INT NOT NULL,
    status ENUM('Booked', 'Cancelled') DEFAULT 'Booked',
    bookingTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (slotID) REFERENCES DoctorSlots (slotID) ON DELETE CASCADE ON UPDATE RESTRICT,
    FOREIGN KEY (patientID) REFERENCES Patient (patientID) ON DELETE CASCADE ON UPDATE RESTRICT
);

select * from patient;