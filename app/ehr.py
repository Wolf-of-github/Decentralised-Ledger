from flask import Blueprint, request, jsonify, current_app
import os
import json
import jwt
from app.chain import append_to_chain

ehr_bp = Blueprint('ehr', __name__)

def verify_jwt(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def load_ehr_data():
    with open('data/EHR_data.json', 'r') as f:
        return json.load(f)

@ehr_bp.route('/my-ehr', methods=['GET'])
def get_my_ehr():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if payload['role'] != 'patient':
        return jsonify({'error': 'Only patients can access their EHR'}), 403

    patient_id = payload['user_id']
    ehr_data = load_ehr_data()
    patient_records = [entry for entry in ehr_data if entry['patient_id'] == patient_id]

    append_to_chain({
        "actor_user_id": payload["user_id"],
        "actor_username": payload["username"],
        "actor_role": payload["role"],
        "target_user_id": patient_id,
        "action": "query"
    })

    return jsonify({
        "patient_id": patient_id,
        "records": patient_records
    })