from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import psutil
import matplotlib.pyplot as plt
import io
import random
from traffic_monitor import traffic_monitor_bp  # Import the blueprint

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SECRET_KEY'] = 'your_secret_key'

# Register the traffic monitor blueprint
app.register_blueprint(traffic_monitor_bp, url_prefix='/traffic')

# Route to serve the main HTML page
@app.route('/')
def index():
    return render_template('index.html')

# Route to analyze CPU usage and traffic data
@app.route('/analyze', methods=['POST'])
def analyze_traffic():
    try:
        url = request.form.get('url')
        if not url:
            return jsonify({'error': 'URL parameter is missing.'}), 400

        # Simulate CPU usage and generate random traffic data
        cpu_usage = psutil.cpu_percent(interval=1)
        dates = ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05']
        sessions = [random.randint(100, 500) for _ in dates]
        pageviews = [random.randint(200, 600) for _ in dates]

        # Create a graph using matplotlib
        fig, ax = plt.subplots()
        ax.plot(dates, sessions, label='Sessions', marker='o')
        ax.plot(dates, pageviews, label='Pageviews', marker='x')
        ax.set_title(f'Traffic Analysis for {url}')
        ax.set_xlabel('Date')
        ax.set_ylabel('Counts')
        ax.legend()
        ax.grid(True)

        # Save the graph as a PNG in memory
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)

        return send_file(img, mimetype='image/png')

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error.'}), 500

# ===========================
# MAIN APPLICATION ENTRY POINT
# ===========================
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
