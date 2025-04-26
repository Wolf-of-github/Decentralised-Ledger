from flask import Blueprint, request, jsonify
import os
import json
import jwt
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

# Load from .env-defined paths
USERS_FILE = os.environ.get('USERS_FILE', 'data/users.json')
PASSWORDS_FILE = os.environ.get('PASSWORDS_FILE', 'data/user_passwords.json')
JWT_SECRET = os.environ.get('JWT_SECRET', 'changeme')
JWT_EXPIRATION_SECONDS = int(os.environ.get('JWT_EXPIRATION_SECONDS', 3600))

# Utility: load users and passwords from file
def load_users():
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def load_passwords():
    with open(PASSWORDS_FILE, 'r') as f:
        return json.load(f)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    username = data['username']
    password = data['password']

    users = load_users()
    passwords = load_passwords()

    if username not in passwords or passwords[username] != password:
        return jsonify({'error': 'Invalid username or password'}), 401

    user = next((u for u in users if u['username'] == username), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Create JWT payload
    payload = {
        'user_id': user['user_id'],
        'username': username,
        'role': user['role'],
        'exp': datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_SECONDS)
    }

    if user['role'] == 'patient':
        payload['patient_id'] = user['patient_id']

    token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')

    return jsonify({'token': token})