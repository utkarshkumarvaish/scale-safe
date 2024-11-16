import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set upload folder path
UPLOAD_FOLDER = r'C:\Users\HP\Desktop\scalesafegit\scale-safe\scalesafe\backend\uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure uploads directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# File upload route
@app.route('/file/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save file to the specified folder
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Here, you'd process the file (e.g., check for corruption or health)
        # For now, we're just going to mock a result for demonstration.
        file_status = 'Healthy'  # Example, you can add your file validation logic here

        # Respond with the filename and its health status
        return jsonify({'filename': file.filename, 'status': file_status})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
