from flask import Blueprint, request, jsonify, send_file
import matplotlib.pyplot as plt
import io
import google.auth
from googleapiclient.discovery import build

traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

@traffic_monitor_bp.route('/status', methods=['GET'])
def server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > 75:
        return jsonify({'message': 'Server capacity at 75% or higher. Consider scaling.'}), 200
    return jsonify({'message': 'Server capacity normal.'}), 200

# Google Analytics setup
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
CLIENT_SECRETS_FILE = 'path_to_client_secrets.json'

def get_google_analytics_service():
    """Authenticate and build the Google Analytics service."""
    creds, _ = google.auth.default(scopes=SCOPES)
    service = build('analytics', 'v3', credentials=creds)
    return service

def get_analytics_data(url):
    """Fetch analytics data for the specified URL."""
    service = get_google_analytics_service()
    VIEW_ID = 'your_view_id'  # Replace with your Google Analytics View ID
    response = service.data().ga().get(
        ids=f'ga:{VIEW_ID}',
        start_date='7daysAgo',
        end_date='today',
        metrics='ga:sessions,ga:pageviews',
        dimensions='ga:date'
    ).execute()
    return response

@traffic_monitor_bp.route('/analyze', methods=['POST'])
def analyze_traffic():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing.'}), 400

    analytics_data = get_analytics_data(url)

    dates = [item['dimensions'][0] for item in analytics_data['rows']]
    sessions = [int(item['metrics'][0]['values'][0]) for item in analytics_data['rows']]
    pageviews = [int(item['metrics'][0]['values'][1]) for item in analytics_data['rows']]

    fig, ax = plt.subplots()
    ax.plot(dates, sessions, label='Sessions', marker='o')
    ax.plot(dates, pageviews, label='Pageviews', marker='x')
    ax.set_title('Traffic Analysis')
    ax.set_xlabel('Date')
    ax.set_ylabel('Counts')
    ax.legend()
    ax.grid(True)

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')