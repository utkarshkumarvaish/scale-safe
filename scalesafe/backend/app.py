from flask import Flask
from auth import auth_bp  # Ensure this is implemented
from file_checker import file_checker_bp  # Ensure this is implemented
from traffic_monitor import traffic_monitor_bp  # Ensure this is implemented

app = Flask(__name__)
app.config.from_object('config.Config')  # Load your configuration

# Registering Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(file_checker_bp, url_prefix='/file')  # Assuming you have a file_checker.py
app.register_blueprint(traffic_monitor_bp, url_prefix='/traffic')  # Updated to include traffic_monitor

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

