import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set upload folder path
UPLOAD_FOLDER = r'C:\Users\HP\Desktop\scalesafegit\scale-safe\scalesafe\backend\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Set JSON file path for storing file metadata
JSON_FILE_PATH = r'C:\Users\HP\Desktop\scalesafegit\scale-safe\scalesafe\backend\file_metadata.json'

# Ensure uploads directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def ensure_json_file_exists():
    """Ensure the JSON file exists and is properly initialized."""
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump([], f)  # Initialize with an empty list


# File upload route
@app.route('/file/upload', methods=['POST'])
def upload_file():
    ensure_json_file_exists()  # Ensure JSON file exists before handling requests

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if not file or file.filename == '':
        return jsonify({'error': 'No file selected for upload'}), 400

    try:
        # Save the file to the upload folder
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        
        # Prevent overwriting by appending a numeric suffix if file exists
        base, extension = os.path.splitext(file.filename)
        counter = 1
        while os.path.exists(file_path):
            file_path = os.path.join(
                app.config['UPLOAD_FOLDER'],
                f"{base}_{counter}{extension}"
            )
            counter += 1

        file.save(file_path)

        # Example: Simple file status logic
        file_status = "Healthy"  # Replace with actual validation logic

        # Prepare metadata
        file_metadata = {
            'filename': os.path.basename(file_path),
            'status': file_status,
            'timestamp': datetime.now().isoformat()
        }

        # Append metadata to JSON file
        with open(JSON_FILE_PATH, 'r+') as f:
            data = json.load(f)
            data.append(file_metadata)
            f.seek(0)
            json.dump(data, f, indent=4)

        # Respond with success
        return jsonify(file_metadata)

    except Exception as e:
        return jsonify({'error': f"Failed to save file: {str(e)}"}), 500


# Route to fetch all uploaded files metadata
@app.route('/file/metadata', methods=['GET'])
def get_metadata():
    ensure_json_file_exists()  # Ensure JSON file exists before handling requests

    try:
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': f"Failed to read metadata: {str(e)}"}), 500


if __name__ == '__main__':
    ensure_json_file_exists()  # Ensure JSON file exists at server start
    app.run(host='0.0.0.0', port=5000, debug=True)
