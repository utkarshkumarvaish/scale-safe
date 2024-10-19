from flask import Blueprint, jsonify
import psutil
import requests

traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

@traffic_monitor_bp.route('/status', methods=['GET'])
def server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 75:
        return jsonify({'message': 'Server capacity at 75% or higher. Consider scaling.'}), 200
    return jsonify({'message': 'Server capacity normal.'}), 200

@traffic_monitor_bp.route('/traffic', methods=['GET'])
def traffic_data():
    try:
        url = 'example.com'  # Replace with the actual URL you want to query
        api_key = 'YOUR_API_KEY'  # Replace with your actual SimilarWeb API key
        endpoint = f'https://api.similarweb.com/v1/website/{url}/total-traffic-and-engagement'
        headers = {'Authorization': f'Bearer {api_key}'}

        response = requests.get(endpoint, headers=headers)

        if response.status_code == 200:
            traffic_data = response.json()
            return jsonify({
                'visits': traffic_data.get('visits', 'N/A'),
                'uniqueVisitors': traffic_data.get('uniqueVisitors', 'N/A')
            }), 200
        else:
            return jsonify({'error': 'Failed to fetch traffic data.'}), response.status_code

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error.'}), 500
 