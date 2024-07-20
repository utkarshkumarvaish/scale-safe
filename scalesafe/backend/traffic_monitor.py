from flask import Blueprint, jsonify
import psutil

traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

@traffic_monitor_bp.route('/status', methods=['GET'])
def server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 75:
        return jsonify({'message': 'Server capacity at 75% or higher. Consider scaling.'}), 200
    return jsonify({'message': 'Server capacity normal.'}), 200
