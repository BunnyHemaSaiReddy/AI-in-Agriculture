# AI-in-Agriculture

🏥 Agriculture Disease Diagnosis & Consultation System
This project is a Flask-based web application that connects pathologists (agriculture doctors) with farmers to diagnose crop diseases and provide recommendations. Pathologists can log in, view farmer requests, accept or reject cases, and provide solutions, while farmers can submit disease reports for expert consultation.

✨ Features
🔐 Authentication System
User signup with OTP verification via email

Secure login/logout functionality for doctors

Session management to keep users logged in

🏥 Doctor Dashboard
View profile details (name, specialization, contact)

If details are missing, prompt for profile completion

See farmer requests for disease diagnosis

Accept or reject disease reports from farmers

🌱 Farmer Requests & Disease Diagnosis
Farmers submit crop disease reports

Requests include farmer name, disease details, and status

If no requests are available, show "No requests found"

📊 Database Integration
Stores doctor details, farmer requests, and disease reports

Uses MySQL for structured data storage

Automatically fetches pending disease reports for doctors

🎨 UI & Styling
Login & Signup Pages with a background image

Semi-transparent form (30% opacity) over the background

Responsive design for different devices

🛠️ Technologies Used
Python (Flask) - Backend framework

MySQL - Database management

HTML, CSS - Frontend design

Bootstrap - UI styling

SMTP (Gmail) - Email verification for OTP

🚀 Installation & Setup
Prerequisites
Install Python (>= 3.8)

Install MySQL and create a database named agriculture

Steps to Run the Project
Clone the repository:

bash
Copy
Edit
git clone https://github.com/yourusername/agriculture-doctor-system.git
cd agriculture-doctor-system
Install dependencies:

bash
Copy
Edit
pip install flask mysql-connector-python
Set up the MySQL database:

sql
Copy
Edit
CREATE DATABASE agriculture;

CREATE TABLE doctordetails ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    specialization VARCHAR(100),
    contact VARCHAR(15)
);

CREATE TABLE requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    doctor_email VARCHAR(100),
    farmer_name VARCHAR(100),
    disease_details TEXT,
    status ENUM('Pending', 'Accepted', 'Rejected') DEFAULT 'Pending',
    FOREIGN KEY (doctor_email) REFERENCES doctordetails(email)
);
Run the Flask app:

bash
Copy
Edit
python app.py
Open the browser and go to:

cpp
Copy
Edit
http://127.0.0.1:8000
📧 Contact
If you have any questions or issues, feel free to contact:
📧 Email: hsr.bunny.2004@gmail.com
