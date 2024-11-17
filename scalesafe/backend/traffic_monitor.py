from flask import Blueprint, request, jsonify, send_file
import matplotlib.pyplot as plt
import io

# Define the traffic_monitor blueprint
traffic_monitor_bp = Blueprint('traffic_monitor', __name__)

@traffic_monitor_bp.route('/analyze', methods=['POST'])
def analyze_traffic():
    url = request.form.get('url')
    if not url:
        return jsonify({'error': 'URL parameter is missing.'}), 400

    # Sample data (replace with actual analysis logic)
    dates = ['2024-10-01', '2024-10-02', '2024-10-03']
    sessions = [10, 20, 15]
    pageviews = [15, 25, 18]

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
    plt.close(fig)

    return send_file(img, mimetype='image/png')
