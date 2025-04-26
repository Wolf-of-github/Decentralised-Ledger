from flask import Blueprint, request, jsonify, current_app
import jwt
from app.chain import load_chain, append_to_chain
from app.encryption import decrypt_log_record

audit_bp = Blueprint('audit', __name__)

# ───────────────────────────────
# Utility: Verify JWT token
# ───────────────────────────────
def verify_jwt(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

# ───────────────────────────────
# Route: POST /audit/patient-records
# ───────────────────────────────
@audit_bp.route('/audit/patient-records', methods=['POST'])
def get_patient_records():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if payload['role'] != 'auditor':
        return jsonify({'error': 'Only auditors can access patient audit logs'}), 403

    request_data = request.get_json()
    patient_id = request_data.get('patient_id', '*')

    chain = load_chain()
    matching_records = []

    for entry in chain:
        try:
            decrypted = decrypt_log_record(entry['encrypted_data'])
        except Exception:
            continue  # skip any corrupted entries safely

        # Only consider records where action was performed by a patient
        if decrypted.get('actor_role') != 'patient':
            continue

        if patient_id == '*':
            matching_records.append(decrypted)
        else:
            if decrypted.get('actor_user_id') == patient_id:
                matching_records.append(decrypted)

    access_log = {
        "actor_user_id": payload["user_id"],
        "actor_username": payload["username"],
        "actor_role": payload["role"],
        "target_user_id": patient_id,
        "action": "query_patient_records"
    }
    append_to_chain(access_log)

    return jsonify({
        "records": matching_records,
        "count": len(matching_records)
    })

# ───────────────────────────────
# Route: POST /audit/auditor-records
# ───────────────────────────────
@audit_bp.route('/audit/auditor-records', methods=['POST'])
def get_auditor_records():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if payload['role'] != 'auditor':
        return jsonify({'error': 'Only auditors can access auditor audit logs'}), 403

    request_data = request.get_json()
    auditor_id = request_data.get('auditor_id', '*')

    chain = load_chain()
    matching_records = []

    for entry in chain:
        try:
            decrypted = decrypt_log_record(entry['encrypted_data'])
        except Exception:
            continue  # skip any corrupted entries safely

        if decrypted.get('actor_role') != 'auditor':
            continue

        if auditor_id == '*':
            matching_records.append(decrypted)
        else:
            if decrypted.get('actor_user_id') == auditor_id:
                matching_records.append(decrypted)

    access_log = {
        "actor_user_id": payload["user_id"],
        "actor_username": payload["username"],
        "actor_role": payload["role"],
        "target_user_id": auditor_id,
        "action": "query_auditor_records"
    }
    append_to_chain(access_log)

    return jsonify({
        "records": matching_records,
        "count": len(matching_records)
    })

# ───────────────────────────────
# Route: GET /audit/my-access
# ───────────────────────────────
@audit_bp.route('/audit/my-access', methods=['GET'])
def get_my_audit_access():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if payload['role'] != 'patient':
        return jsonify({'error': 'Only patients can access their audit records'}), 403

    patient_id = payload['user_id']

    chain = load_chain()
    matching_records = []

    for entry in chain:
        try:
            decrypted = decrypt_log_record(entry['encrypted_data'])
            target_user_ids = decrypted.get('target_user_id', '').split(",")
            if patient_id in target_user_ids:
                matching_records.append(decrypted)
        except Exception:
            continue  # skip corrupted or tampered entries

    return jsonify({
        "patient_id": patient_id,
        "records": matching_records,
        "count": len(matching_records)
    })