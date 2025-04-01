from flask import Flask, render_template, request, redirect, session, flash, jsonify
import mysql.connector
import smtplib
import google.generativeai as genai
import random
from datetime import datetime
from pytube import Search
from googletrans import Translator,LANGUAGES
import os
#import dotenv

api_key = os.getenv("API_KEY")

# Get database configuration from environment variables
db_config = {
    "host": os.getenv("DB_HOST"),
    "port": 13214,
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
    "auth_plugin": os.getenv("DB_AUTH_PLUGIN")
}
#dotenv.load_dotenv()
translator = Translator()

def lang():
    return LANGUAGES  # Keeps full language names

languages = lang()

from deep_translator import GoogleTranslator

def translate_text(text, target_lang="en"):
    """Translate text to the specified target language. Skips translation if target is English."""
    if target_lang.lower() == "en":  # No need to translate if target is English
        return text  
    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated_text
    except Exception as e:
        return f"Translation failed: {e}"

def fetch_youtube_links(query, num_results=3):
    search = Search(query)
    results = search.results
    video_links = [result.watch_url for result in results[:num_results]]    
    return video_links
# API Key for Gemini AI
API_KEY = "AIzaSyCEn5YfcEEUnKFTRhLYXO-ebLrAmSW6AUE"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)

app.secret_key=os.getenv("sec")
# Required for session handling

# Database Configuration
# db_config = {
#     "host": "localhost",
#     "user": "root",
#     "password": "bunny",
#     "database": "agriculture",
#     "auth_plugin": "mysql_native_password"
# }



# Email Credentials
SENDER_EMAIL = "hsr.bunny.2004@gmail.com"
SENDER_PASSWORD = "epjm sgyq fpvu uwlr"



# Function to send OTP
def send_otp(email, otp):
    subject = "OTP Verification"
    message = f"Your OTP for registration is: {otp}"
    msg = f"Subject: {subject}\n\n{message}"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, email, msg)
        server.quit()
        return True
    except Exception as e:
        print("Error sending email:", e)
        return False

# Home Route
@app.route("/")
def home():
    if "email" in session:
        return render_template("index.html",languages=lang())
    return redirect("/login")


@app.route('/diseases')
def diseases():
    return render_template('diseases.html')

# About Us route
@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

# Contact Us route
@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

# AI Text Generation Route
# @app.route("/generate", methods=["POST"])
# def generate_text():
#     try:
#         data = request.json
#         prompt = data.get("prompt", "")

#         if not prompt:
#             return jsonify({"error": "Prompt is required"}), 400

#         response = model.generate_content(prompt)
#         return jsonify({"response": response.text})

#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session["email"] = email
                return redirect("/")
            else:
                flash("Invalid email or password!", "danger")

        except Exception as e:
            flash(f"Database error: {str(e)}", "danger")

    return render_template("login.html")

# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        otp = str(random.randint(100000, 999999))

        # Send OTP to user email
        if send_otp(email, otp):
            session["otp"] = otp
            session["signup_email"] = email
            session["signup_password"] = password
            return redirect("/verify_otp")
        else:
            flash("Failed to send OTP. Try again!", "danger")

    return render_template("signup.html")

# OTP Verification Route
@app.route("/verify_otp", methods=["GET", "POST"])
def verify_otp():
    if request.method == "POST":
        user_otp = request.form["otp"]

        if "otp" in session and session["otp"] == user_otp:
            email = session.pop("signup_email", None)
            password = session.pop("signup_password", None)

            try:
                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
                conn.commit()
                cursor.close()
                conn.close()

                flash("Account created successfully! Please login.", "success")
                return redirect("/login")

            except Exception as e:
                flash(f"Database error: {str(e)}", "danger")

        else:
            flash("Invalid OTP! Try again.", "danger")

    return render_template("verify_otp.html")

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    query = data.get("query")
    
    if not query:
        return jsonify({"error": "Query is missing"}), 400

    links = fetch_youtube_links(query)
    return jsonify({"links": links})

@app.route("/set_language", methods=["POST"])
def set_language():
    data = request.get_json()
    selected_lang_code = data.get("language", "en")  # Default to English if not provided

    session["selected_lang_code"] = selected_lang_code
    return jsonify({"message": f"Language set to {selected_lang_code}"})

@app.route("/generate", methods=["POST"])
def generate_text():
    try:
        data = request.json
        prompt = data.get("prompt", "")
        selected_lang_code = session.get("selected_lang_code", "en")  # Get selected language

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate response in English
        response = model.generate_content(prompt)
        generated_text = response.text if hasattr(response, "text") else str(response)

        # Translate response if needed
        translated_text = translate_text(generated_text, selected_lang_code)

        return jsonify({"response": translated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Logout Route
@app.route("/logout")
def logout():
    session.pop("email", None)
    return redirect("/login")

@app.route("/get_messages")
def get_messages():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor
    cursor.execute("SELECT user_email, message, timestamp FROM messages ORDER BY timestamp ASC")
    messages = cursor.fetchall()
    
    cursor.close()
    conn.close()

    return jsonify(messages)


# Handle new messages
@app.route("/send_message", methods=["POST"])
def send_message():
    data = request.get_json()
    user_email = session.get("email")  # Get user email from session
    message = data.get("message")

    if not user_email or not message:
        return jsonify({"error": "Invalid request"}), 400

    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO messages (user_email, message, timestamp) VALUES (%s, %s, %s)",
            (user_email, message, datetime.now())
        )
        conn.commit()
    except mysql.connector.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({"success": True})

@app.route('/index/requests')
def requests():
    try:
        # Connect to MySQL Database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # Query to get pathologists from the new 'Pathologists' table
        cursor.execute("SELECT Name, Specialization, Phone_Number, Clinic_Name, ID FROM Pathologists")
        pathologists = cursor.fetchall()

        cursor.close()
        conn.close()

        # Check if pathologists were found
        if not pathologists:
            print("No pathologists found!")
        else:
            print(f"Pathologists Retrieved: {pathologists}")

        # Return the rendered template with pathologists data
        return render_template('requests.html', pathologists=pathologists)
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return "Database Error occurred!", 500

@app.route('/submit_request', methods=['POST'])
def submit_request():
    try:
        # Retrieving form data
        farmer_name = request.form['farmer_name']
        phone_number = request.form['phone_number']
        place = request.form['place']
        explanation = request.form['explanation']
        doctor_id = request.form['doctor_id']

        # Connect to MySQL Database and insert the request data
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Insert data into 'pathologist_requests' table
        cursor.execute("""
            INSERT INTO pathologist_requests (farmer_name, phone_number, place, explanation, doctor_id, status)
            VALUES (%s, %s, %s, %s, %s, 'Pending')
        """, (farmer_name, phone_number, place, explanation, doctor_id))

        conn.commit()  # Commit the changes
        cursor.close()
        conn.close()

        # Redirect to the requests page after submitting the request
        return redirect('/index/requests')
    
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        return "Database Error occurred!", 500
    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred while processing your request!", 500


# Run Flask App
if __name__ == "__main__":
    app.run(debug=True)
