from flask import Flask, request, jsonify, send_file, Response
import json
import os
from flask_cors import CORS

app = Flask(__name__)


CORS(app)  # Enable CORS for all routes in the app

# Path to the JSON file where data will be saved
json_file_path = "data.json"

# Function to load existing data from the JSON file
def load_data():
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            return json.load(file)
    return []

# Function to save data to the JSON file
def save_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['POST','GET'])
def index():
    return "API"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        if not request.is_json:
            return jsonify({"message": "Invalid JSON"}), 400
        
        data = request.get_json()
        
        name = data.get('name')
        phone_number = data.get('phone_number')
        date = data.get('date')
        time = data.get('time')

        if not all([name, phone_number, date, time]):
            return jsonify({"message": "Missing data!"}), 400

        # Load existing data
        existing_data = load_data()

        # Add new data to the existing data
        existing_data.append({
            'name': name,
            'phone_number': phone_number,
            'date': date,
            'time': time
        })

        # Save updated data back to the JSON file
        save_data(existing_data)

        return jsonify({"message": "Data saved successfully!"}), 201
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"message": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            return jsonify(data)
        else:
            return jsonify({"message": "File not found"}), 404
    except Exception as e:
        app.logger.error(f"Error: {e}")
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run()
