from flask import Blueprint, request, jsonify, send_file
import matplotlib.pyplot as plt
import io
import google.auth
from googleapiclient.discovery import build

# Define the traffic_monitor blueprint
traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

# Google Analytics Data API setup
SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
CLIENT_SECRETS_FILE = "C:\\Users\\HP\\Desktop\\scalesafegit\\scale-safe\\scalesafe\\backend\\scale-safe-29da45ad3ced.json"  # Ensure this path is correct
PROPERTY_ID = '462927062'  # Replace with your GA4 Property ID

def get_google_analytics_service():
    """Authenticate and build the Google Analytics Data API service."""
    creds, _ = google.auth.default(scopes=SCOPES)
    service = build('analyticsdata', 'v1beta', credentials=creds)
    return service

def get_analytics_data():
    """Fetch analytics data for the specified GA4 property."""
    service = get_google_analytics_service()
    request_body = {
        'dateRanges': [{'startDate': '7daysAgo', 'endDate': 'today'}],
        'metrics': [{'name': 'sessions'}, {'name': 'pageviews'}],
        'dimensions': [{'name': 'date'}]
    }
    response = service.properties().runReport(
        property=f'properties/{PROPERTY_ID}',
        body=request_body
    ).execute()
    return response

@traffic_monitor_bp.route('/analyze', methods=['POST'])
def analyze_traffic():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing.'}), 400

    analytics_data = get_analytics_data()

    # Prepare data for plotting
    dates = [row['dimensionValues'][0]['value'] for row in analytics_data['rows']]
    sessions = [int(row['metricValues'][0]['value']) for row in analytics_data['rows']]
    pageviews = [int(row['metricValues'][1]['value']) for row in analytics_data['rows']]

    # Generate the plot
    fig, ax = plt.subplots()
    ax.plot(dates, sessions, label='Sessions', marker='o', color='blue')
    ax.plot(dates, pageviews, label='Pageviews', marker='x', color='green')
    ax.set_title('Traffic Analysis')
    ax.set_xlabel('Date')
    ax.set_ylabel('Counts')
    ax.legend()
    ax.grid(True)

    # Save the plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close(fig)  # Close the figure to avoid memory issues

    return send_file(img, mimetype='image/png')
