
from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes in the app

# Path to the JSON file where data will be saved
json_file_path = os.path.join(os.path.dirname(__file__), 'data.json')

# Function to load existing data from the JSON file
def load_data():
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as file:
                return json.load(file)
    except json.JSONDecodeError as jde:
        app.logger.error(f"Failed to decode JSON from the file: {jde}")
        return []
    except Exception as e:
        app.logger.error(f"Error loading data: {e}")
    return []

# Function to save data to the JSON file
def save_data(data):
    try:
        with open(json_file_path, 'w') as file:
            json.dump(data, file, indent=4)
            app.logger.info("Data successfully saved to JSON file.")
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")
        raise e

@app.route('/', methods=['POST', 'GET'])
def index():
    return "API"

@app.route('/submit', methods=['POST'])
def submit():
    try:
        if not request.is_json:
            app.logger.error("Request is not JSON.")
            return jsonify({"message": "Invalid JSON"}), 400

        data = request.get_json()
        app.logger.info("Received data: %s", data)

        name = data.get('name')
        phone_number = data.get('phone_number')
        date = data.get('date')
        time = data.get('time')

        if not all([name, phone_number, date, time]):
            app.logger.error("Missing data: %s", data)
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
        app.logger.error(f"Error in submit: {e}")
        return jsonify({"message": str(e)}), 500

@app.route('/data', methods=['GET'])
def get_data():
    try:
        data = load_data()
        return jsonify(data)
    except Exception as e:
        app.logger.error(f"Error retrieving data: {e}")
        return jsonify({"message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
