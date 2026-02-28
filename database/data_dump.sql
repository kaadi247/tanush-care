-- SPECIALISATION TABLE
INSERT INTO Specialisation (specialisationName) VALUES
('Cardiology'),
('Dermatology'),
('Orthopedics'),
('Pediatrics'),
('Neurology'),
('Psychiatry'),
('ENT'),
('Gynecology'),
('General Medicine'),
('Ophthalmology');

-- HOSPITAL TABLE
INSERT INTO Hospital 
(hospitalName, address, city, state, contactEmail, contactPhone) VALUES

-- Bangalore
('Aster Prime Care', '14 Residency Road', 'Bangalore', 'Karnataka', 'contact@asterprime.com', '9845012345'),
('GreenLeaf Medical Center', '22 Indiranagar 2nd Stage', 'Bangalore', 'Karnataka', 'info@greenleafmed.com', '9845098761'),
('Nova Specialty Hospital', '3 Koramangala 5th Block', 'Bangalore', 'Karnataka', 'admin@novaspecialty.com', '9845123476'),
('Harmony Health Institute', '77 Jayanagar 4th Block', 'Bangalore', 'Karnataka', 'support@harmonyhealth.com', '9845234567'),
('CityCare Multispeciality', '19 Whitefield Main Road', 'Bangalore', 'Karnataka', 'help@citycaremulti.com', '9845345678'),

-- Mumbai
('Western Horizon Hospital', '21 Bandra West', 'Mumbai', 'Maharashtra', 'contact@westernhorizon.com', '9820012345'),
('OceanView Medical', '9 Marine Drive', 'Mumbai', 'Maharashtra', 'info@oceanviewmed.com', '9820098761'),
('SilverLine Healthcare', '44 Powai Lake Road', 'Mumbai', 'Maharashtra', 'admin@silverlinehc.com', '9820123456'),
('LifeBridge Hospital', '12 Andheri East', 'Mumbai', 'Maharashtra', 'support@lifebridge.com', '9820234567'),
('Trinity Advanced Clinic', '8 Dadar TT', 'Mumbai', 'Maharashtra', 'help@trinityclinic.com', '9820345678'),

-- Delhi
('NorthStar Hospital', 'Sector 10 Rohini', 'Delhi', 'Delhi', 'contact@northstarhosp.com', '9810012345'),
('Medisphere Institute', 'Lajpat Nagar II', 'Delhi', 'Delhi', 'info@medisphere.com', '9810098761'),
('Zenith Care Centre', 'Karol Bagh', 'Delhi', 'Delhi', 'admin@zenithcare.com', '9810123456'),
('PrimePulse Hospital', 'Dwarka Sector 6', 'Delhi', 'Delhi', 'support@primepulse.com', '9810234567'),
('HealWell Medical Hub', 'Greater Kailash I', 'Delhi', 'Delhi', 'help@healwellhub.com', '9810345678'),

-- Hyderabad
('Sapphire Health', 'Jubilee Hills Road 36', 'Hyderabad', 'Telangana', 'contact@sapphirehealth.com', '9390012345'),
('MedAxis Hospital', 'Gachibowli IT Corridor', 'Hyderabad', 'Telangana', 'info@medaxis.com', '9390098761'),
('Sunline Specialty', 'Kukatpally Housing Board', 'Hyderabad', 'Telangana', 'admin@sunlinespecialty.com', '9390123456'),
('CareSpring Institute', 'Begumpet Main Road', 'Hyderabad', 'Telangana', 'support@carespring.com', '9390234567'),
('Nizam Lifecare', 'Secunderabad Market Road', 'Hyderabad', 'Telangana', 'help@nizamlifecare.com', '9390345678'),

-- Chennai
('Marina Medical Center', 'Anna Salai Mount Road', 'Chennai', 'Tamil Nadu', 'contact@marinamed.com', '9444012345'),
('CoralCare Hospital', 'T Nagar Usman Road', 'Chennai', 'Tamil Nadu', 'info@coralcare.com', '9444098761'),
('Velachery Health Hub', 'Velachery Main Road', 'Chennai', 'Tamil Nadu', 'admin@velacheryhub.com', '9444123456'),
('Bayview Specialty', 'Adyar LB Road', 'Chennai', 'Tamil Nadu', 'support@bayviewspecialty.com', '9444234567'),
('Sri Ram Advanced Clinic', 'Porur Arcot Road', 'Chennai', 'Tamil Nadu', 'help@sriramclinic.com', '9444345678'),

-- Pune
('Crestview Medical', 'Shivajinagar FC Road', 'Pune', 'Maharashtra', 'contact@crestviewmed.com', '9765012345'),
('Lifetree Hospital', 'Hinjewadi Phase 2', 'Pune', 'Maharashtra', 'info@lifetreehosp.com', '9765098761'),
('BluePeak Health', 'Kothrud Paud Road', 'Pune', 'Maharashtra', 'admin@bluepeakhealth.com', '9765123456'),
('WellSpring Institute', 'Viman Nagar', 'Pune', 'Maharashtra', 'support@wellspringinst.com', '9765234567'),
('Unity Care Center', 'Camp MG Road', 'Pune', 'Maharashtra', 'help@unitycare.com', '9765345678'),

-- Kolkata
('Eastern Care Hospital', 'Salt Lake Sector V', 'Kolkata', 'West Bengal', 'contact@easterncare.com', '9830012345'),
('Howrah Medical Institute', 'Howrah Station Road', 'Kolkata', 'West Bengal', 'info@howrahmed.com', '9830098761'),
('Lotus Bengal Clinic', 'Ballygunge Circular Road', 'Kolkata', 'West Bengal', 'admin@lotusbengal.com', '9830123456'),
('Medinova Kolkata', 'Park Street', 'Kolkata', 'West Bengal', 'support@medinovakolkata.com', '9830234567'),
('GangaLife Hospital', 'New Town Action Area I', 'Kolkata', 'West Bengal', 'help@gangalife.com', '9830345678');

-- PATIENT TABLE
INSERT INTO Patient (name, email, phone, dob, gender) VALUES
('Rohit Mehra', 'rohit.mehra21@gmail.com', '9988123456', '1998-03-12', 'Male'),
('Ananya Iyer', 'ananya.iyer89@gmail.com', '9123456723', '1989-11-04', 'Female'),
('Karan Verma', 'karanv.dev@gmail.com', '9812345678', '2001-07-22', 'Male'),
('Megha Reddy', 'megha.reddy@gmail.com', '9345678912', '1995-09-30', 'Female'),
('Arjun Nair', 'arjun.nair@gmail.com', '9001122334', '1993-02-18', 'Male'),
('Priya Sharma', 'priya.sharma07@gmail.com', '9098765432', '2004-06-10', 'Female'),
('Faizan Ali', 'faizan.ali88@gmail.com', '8877665544', '1988-12-25', 'Male'),
('Sneha Patil', 'sneha.patil@gmail.com', '9011223344', '1999-01-14', 'Female'),
('Dev Malhotra', 'dev.malhotra@gmail.com', '9191919191', '2012-08-19', 'Male'),
('Ishita Sen', 'ishita.sen@gmail.com', '8800112233', '1996-05-03', 'Female'),
('Aditya Kulshreshtha', 'aditya.kul@gmail.com', '8734562190', '1991-10-27', 'Male'),
('Nikita Rao', 'nikita.rao24@gmail.com', '9023456712', '2003-04-16', 'Female'),
('Vivek Anand', 'vivek.anand@gmail.com', '8866123490', '1985-01-08', 'Male'),
('Tanvi Desai', 'tanvi.desai@gmail.com', '9172345601', '1997-09-11', 'Female'),
('Rehan Siddiqui', 'rehan.sid@gmail.com', '8956234710', '1992-07-19', 'Male');

-- DOCTOR TABLE
INSERT INTO Doctor 
(doctorName, experience, fees, appointmentDuration, specialisationID, hospitalID) VALUES

-- Bangalore (Hospital 1–5) → 2 each

('Dr. Vikram Rao', 12, 900, 20, 1, 1),
('Dr. Neha Kapoor', 6, 650, 15, 2, 1),

('Dr. Prakash Shetty', 22, 2000, 40, 3, 2),
('Dr. Alok Chatterjee', 3, 450, 10, 9, 2),

('Dr. Harini Subramanian', 11, 950, 25, 10, 3),
('Dr. Mohan Iyer', 15, 1100, 30, 7, 3),

('Dr. Shruti Deshmukh', 16, 1400, 35, 5, 4),
('Dr. Nikita Shah', 4, 500, 15, 2, 4),

('Dr. Rahul Batra', 10, 850, 20, 8, 5),
('Dr. Aishwarya Menon', 7, 700, 20, 4, 5),

-- Mumbai (6–10)

('Dr. Sandeep Kulkarni', 18, 1500, 30, 3, 6),
('Dr. Farah Khan', 9, 750, 20, 6, 7),
('Dr. Kavita Bansal', 5, 600, 15, 8, 8),
('Dr. Ritesh Jain', 20, 1800, 45, 5, 9),
('Dr. Manish Yadav', 13, 1000, 25, 9, 10),

-- Delhi (11–15)

('Dr. Lavanya Krishnan', 17, 1600, 40, 9, 11),
('Dr. Amitabh Roy', 2, 350, 10, 10, 12),
('Dr. Tania Dutta', 8, 780, 20, 6, 13),
('Dr. Gaurav Sinha', 14, 1200, 30, 3, 14),
('Dr. Rupal Arora', 6, 650, 20, 2, 15),

-- Hyderabad (16–20)

('Dr. Sameer Qureshi', 19, 1700, 35, 1, 16),
('Dr. Pooja Reddy', 7, 720, 15, 4, 17),
('Dr. Nikhil Varma', 12, 980, 25, 7, 18),
('Dr. Charan Teja', 4, 480, 15, 8, 19),
('Dr. Fatima Noor', 15, 1300, 30, 6, 20),

-- Chennai (21–25)

('Dr. Karthik Raman', 21, 1900, 40, 1, 21),
('Dr. Divya Iyer', 5, 550, 15, 2, 22),
('Dr. Anand Prakash', 9, 820, 20, 9, 23),
('Dr. Meenakshi Sundar', 18, 1550, 35, 5, 24),
('Dr. Arvind Narayanan', 11, 960, 25, 7, 25),

-- Pune (26–30)

('Dr. Rohan Deshpande', 6, 610, 15, 3, 26),
('Dr. Shalini Kulkarni', 14, 1250, 30, 8, 27),
('Dr. Tejas Patwardhan', 3, 400, 10, 10, 28),
('Dr. Mahesh Bendre', 16, 1450, 35, 1, 29),
('Dr. Snehal Joshi', 8, 750, 20, 4, 30),

-- Kolkata (31–35)

('Dr. Souvik Banerjee', 13, 1150, 25, 9, 31),
('Dr. Anindita Sen', 7, 700, 15, 2, 32),
('Dr. Kaustav Ghosh', 20, 1750, 40, 5, 33),
('Dr. Rituparna Das', 4, 480, 15, 6, 34),
('Dr. Debojyoti Roy', 10, 900, 20, 7, 35);

-- DOCTOR SLOTS TABLE
INSERT INTO DoctorSlots (doctorID, date, time) VALUES
(1,  '2030-01-15', '10:00:00'),
(7,  '2030-01-15', '14:30:00'),
(12, '2030-01-16', '09:45:00'),
(18, '2030-01-17', '16:15:00'),
(25, '2030-01-18', '11:00:00'),
(3,  '2030-01-18', '13:20:00');  -- extra unused slot

-- APPOINTMENTS TABLE
INSERT INTO Appointment (slotID, patientID, status) VALUES
(1, 4, 'Booked'),
(2, 9, 'Cancelled'),
(3, 2, 'Booked'),
(4, 11, 'Booked'),
(5, 6, 'Cancelled'),
(6, 14, 'Booked');
