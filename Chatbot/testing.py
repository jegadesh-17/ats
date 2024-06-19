from flask import Flask, jsonify, request, send_from_directory
from pymongo import MongoClient, errors,DESCENDING
from bson.json_util import dumps, ObjectId
from flask_cors import CORS
import logging

app = Flask(__name__, static_folder='Templates')
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
        # job_data = list(collection.find({})).sort("_id", DESCENDING)
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

# Route to serve job-details.html
@app.route('/job-details.html')
def job_details():
    return app.send_static_file('job-details.html')

if __name__ == '__main__':
    app.run(debug=True)


