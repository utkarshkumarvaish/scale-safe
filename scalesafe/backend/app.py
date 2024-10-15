from flask import Flask
from flask_cors import CORS
from auth import auth_bp
from file_checker import file_checker_bp
from traffic_monitor import traffic_monitor_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Registering Blueprints with URL prefixes
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_checker_bp, url_prefix='/file')
app.register_blueprint(traffic_monitor_bp, url_prefix='/traffic')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
