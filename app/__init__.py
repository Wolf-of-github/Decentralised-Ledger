from flask import Flask
import os
from .auth import auth_bp
from .ehr import ehr_bp
from .sync import sync_bp, ping_peers, start_peer_monitor
from .audit import audit_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)

    CORS(app)

    # Load config from environment
    app.config['JWT_SECRET'] = os.environ.get('JWT_SECRET', 'changeme')
    app.config['USERS_FILE'] = os.environ.get('USERS_FILE', 'data/users.json')
    app.config['PASSWORDS_FILE'] = os.environ.get('PASSWORDS_FILE', 'data/user_passwords.json')
    app.config['AUDIT_LOG_FILE'] = os.environ.get('AUDIT_LOG_FILE', 'instance/audit_node1.json')
    app.config['PRIVATE_KEY_PATH'] = os.environ.get('PRIVATE_KEY_PATH', 'keys/private.pem')
    app.config['PUBLIC_KEY_PATH'] = os.environ.get('PUBLIC_KEY_PATH', 'keys/public.pem')
    app.config['JWT_EXPIRATION_SECONDS'] = int(os.environ.get('JWT_EXPIRATION_SECONDS', 3600))

    # Register blueprints inside the factory
    app.register_blueprint(auth_bp)
    app.register_blueprint(ehr_bp)
    app.register_blueprint(sync_bp)
    app.register_blueprint(audit_bp)   # ✅ Add this!

    # Initial peer ping
    ping_peers()

    # Periodic peer health monitoring
    start_peer_monitor(interval=10)

    return app