from flask import Blueprint, request, jsonify
import boto3
import hashlib

file_checker_bp = Blueprint('file_checker', __name__)

def check_file_integrity(file):
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: file.read(4096), b""):
        hash_md5.update(chunk)
    file.seek(0)
    return hash_md5.hexdigest()

@file_checker_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    integrity_hash = check_file_integrity(file)
    # Check hash against a database or list of known vulnerabilities (not implemented here)
    # Assume a function `is_vulnerable` that checks the file against known issues
    if is_vulnerable(integrity_hash):
        return jsonify({'status': 'bad file', 'message': 'File is corrupted or vulnerable'}), 400
    s3 = boto3.client('s3')
    s3.upload_fileobj(file, 'your-bucket-name', file.filename)
    return jsonify({'status': 'good file', 'message': 'File uploaded successfully'}), 200
