from flask import Flask, render_template, request, jsonify, session, send_from_directory
from flask_session import Session  # For server-side session management
from pymongo import MongoClient, errors, DESCENDING
from bson.json_util import dumps, ObjectId
from flask_cors import CORS
import logging

app = Flask(__name__, static_folder='Templates')
app.config["SECRET_KEY"] = "your_secret_key_here"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# MongoDB configuration
try:
    client = MongoClient('mongodb+srv://ssdev:ssdev123@ssdev.us8prjv.mongodb.net/test')
    db = client['job_data']  # Replace with your database name
    collection = db['job']  # Replace with your collection name
    logging.debug("Connected to MongoDB successfully")
except errors.ConnectionError as e:
    logging.error(f"Failed to connect to MongoDB: {e}")

# Database connection for chatbot
client = MongoClient('mongodb://localhost:27017/')
db = client['job_database']
jobs_collection = db['jobs']

# Initial job data
job_data = {
    "job_title": "python",
    "assigned_to": [],
    "status": "Open",
    "no_of_positions": "2",
    "priority": "Low",
    "client": "maersk",
    "job_description": "<p>test java developer</p>",
    "additional_details": "<p></p>",
    "due_date": "2024-06-14T18:30:00.000Z",
    "notice_period": "< 15 Days",
    "minimum_experience": 26,
    "maximum_experience": 39,
    "mode_of_hire": "Permanent",
    "vendor_name": "",
    "poc_vendor": "",
    "job_rr_id": "",
    "skillset": [{"skill": "java", "exp": 53}]
}

# Insert initial data into MongoDB
try:
    collection.insert_one(job_data)
    logging.debug("Initial job data inserted successfully")
except errors.PyMongoError as e:
    logging.error(f"Failed to insert initial job data: {e}")

# Route to serve index.html
@app.route('/')
def index():
    session.clear()  # Start fresh each time the main page is loaded
    session['stage'] = 'welcome'  # Set the initial stage to 'welcome'
    return send_from_directory('Templates', 'index.html')

# API endpoint to add a new job
@app.route('/api/job', methods=['POST'])
def add_job():
    try:
        data = request.get_json()
        # Insert new job data into MongoDB
        result = collection.insert_one(data)
        return jsonify({"success": True, "message": f"Job added with ID: {result.inserted_id}"}), 201
    except errors.PyMongoError as e:
        return jsonify({"success": False, "message": f"Failed to add job: {e}"}), 500

# API endpoint to retrieve all jobs
@app.route('/api/job', methods=['GET'])
def get_jobs():
    try:
        # Retrieve all job data from MongoDB
        job_data = list(collection.find({}).sort("_id", DESCENDING))
        if job_data:
            return dumps(job_data), 200
        else:
            return jsonify({"error": "No job data available"}), 404
    except errors.PyMongoError as e:
        return jsonify({"error": f"Failed to retrieve jobs: {e}"}), 500

# API endpoint to retrieve a specific job by ID
@app.route('/api/job/<job_id>', methods=['GET'])
def get_job(job_id):
    try:
        logging.debug(f"Fetching job with ID: {job_id}")
        job = collection.find_one({"_id": ObjectId(job_id)})
        if job:
            logging.debug(f"Job details found: {job}")
            return dumps(job), 200  # Return job details as JSON
        else:
            logging.debug(f"Job with ID {job_id} not found")
            return jsonify({"error": "Job not found"}), 404
    except errors.PyMongoError as e:
        logging.error(f"Failed to retrieve job: {e}")
        return jsonify({"error": f"Failed to retrieve job: {e}"}), 500

# API endpoint to handle job application
@app.route('/api/apply/<job_id>', methods=['POST'])
def apply_job(job_id):
    try:
        # Update job status to "Applied"
        result = collection.update_one(
            {"_id": ObjectId(job_id)},
            {"$set": {"status": "Applied"}}
        )
        if result.matched_count > 0:
            session.clear()  # Clear session data when application starts
            session['stage'] = 'welcome'  # Set initial stage for chatbot
            return jsonify({"success": True, "message": "Job application successful"}), 200
        else:
            return jsonify({"error": "Job not found"}), 404
    except errors.PyMongoError as e:
        return jsonify({"error": f"Failed to apply for job: {e}"}), 500

# API endpoint to retrieve all jobs for chatbot
@app.route('/api/jobs')
def get_jobs_for_chatbot():
    jobs = list(jobs_collection.find())
    for job in jobs:
        job['_id'] = str(job['_id'])  # Convert ObjectId to string for JSON serialization
    return jsonify(jobs)

# API endpoint for chatbot message handling
@app.route('/message', methods=['POST'])
def message():
    data = request.get_json()
    user_input = data['message']
    stage = session.get('stage', 'welcome')  # Use 'welcome' as the default stage if not set
    response, next_stage = process_chat(stage, user_input)
    session['stage'] = next_stage  # Update stage in session
    return jsonify({'message': response, 'stage': next_stage})

def process_chat(stage, user_input):
    """Process the chat based on the current stage and user input, including validation."""
    # Validation messages
    if stage == "email" and "@" not in user_input:
        return ("It seems there was an error with the email address you provided. Please enter a valid email address:", "email")
    if stage == "phone_number" and (not user_input.isdigit() or len(user_input) != 10):
        return ("It seems there was an error with the phone number you provided. Please enter a valid 10-digit phone number:", "phone_number")

    # Response handling
    responses = {
        "welcome": ("Thank you for showing interest in the Management Consultant position at maersk . Let's get started with your application. Can you please provide your first name?", "start"),
        "start": ("Great! Now, can you provide your last name?", "last_name"),
        "last_name": (f"Thank you, {user_input}. What's your email address?", "email"),
        "email": ("Got it. Can you also provide your phone number?", "phone_number"),
        "phone_number": ("Perfect. Can you please provide your current address? Start with your house number and street name.", "address"),
        "address": ("Thank you. Now, can you provide your city or town?", "city"),
        "city": ("Thanks. Can you provide your postal code?", "postal_code"),
        "postal_code": ("Great. And finally, can you provide your country?", "country"),
        "country": ("Excellent. Now, let's move on to your employment history. Please provide the name of your most recent employer.", "employer"),
        "employer": (f"Thank you. What was your job title at {user_input}?", "job_title"),
        "job_title": ("Great. How long did you work there? (Please specify in months or years)", "job_duration"),
        "job_duration": ("Got it. Can you briefly describe your responsibilities in this role?", "responsibilities"),
        "responsibilities": ("Thank you. Let's move on to your educational background. Please provide the name of the institution where you obtained your highest degree.", "education"),
        "education": ("Great. What was your degree?", "degree"),
        "degree": ("When did you graduate? (Please specify the month and year)", "graduation_date"),
        "graduation_date": ("Thank you. Can you also provide any additional qualifications or certifications relevant to the Management Consultant position?", "qualifications"),
        "qualifications": ("Excellent. Can you list your top three skills relevant to this position?", "skills"),
        "skills": ("Thank you. Do you have any specific competencies or experiences that make you a strong fit for this role? (e.g., project management, data analysis, etc.)", "competencies"),
        "competencies": ("Great. Is there anything else you would like us to know about your application or experience?", "additional_info"),
        "additional_info": ("Thank you for all the information. Can you please upload your CV/resume? You can simply drag and drop the file here.", "cv"),
        "cv": ("Thank you. Do you have a cover letter to upload as well?", "cover_letter"),
        "cover_letter": ("Thank you. Your application is almost complete. Please review the information you've provided. Type 'yes' to confirm and submit your application or 'no' to make any changes.", "confirmation"),
        "confirmation": (f"Thank you, {session.get('first_name', 'Applicant')}. Your application for the Management Consultant position has been submitted successfully. You will receive a confirmation email shortly. Have a great day!", "end")
    }

    response, next_stage = responses.get(stage, ("Thank you for chatting with us.", "end"))
    return response, next_stage

# Route to serve job-details.html
@app.route('/listingdesign.html')
def job_details():
    return app.send_static_file('listingdesign.html')

if __name__ == '__main__':
    app.run(debug=True)
