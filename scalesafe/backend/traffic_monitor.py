import sys
import os
from flask import Blueprint, Flask, request, jsonify, send_file
import psutil
import matplotlib.pyplot as plt
import io
import google.auth
from googleapiclient.discovery import build

# Add the directory containing the scalesafe module to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Import the traffic_monitor Blueprint
try:
    from scalesafe.backend.traffic_monitor_blueprint import traffic_monitor_bp
except ImportError:
    sys.path.append('path_to_traffic_monitor_blueprint_directory')
    from scalesafe.backend.traffic_monitor_blueprint import traffic_monitor_bp

traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

@traffic_monitor_bp.route('/status', methods=['GET'])
def server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 75:
        return jsonify({'message': 'Server capacity at 75% or higher. Consider scaling.'}), 200
    return jsonify({'message': 'Server capacity normal.'}), 200

app = Flask(__name__)

# Register the traffic_monitor Blueprint
app.register_blueprint(traffic_monitor_bp, url_prefix='/monitor')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
