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
# Route: POST /audit/chain
# ───────────────────────────────
@audit_bp.route('/audit/chain', methods=['POST'])
def get_audit_chain():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({'error': 'Missing or invalid Authorization header'}), 401

    token = auth_header.split(" ")[1]
    payload = verify_jwt(token)
    if not payload:
        return jsonify({'error': 'Invalid or expired token'}), 401

    if payload['role'] != 'auditor':
        return jsonify({'error': 'Only auditors can access audit logs'}), 403

    request_data = request.get_json()
    patients = request_data.get('patients', ['*'])
    auditors = request_data.get('auditors', ['*'])

    chain = load_chain()
    matching_records = []

    for entry in chain:
        try:
            decrypted = decrypt_log_record(entry['encrypted_data'])
        except Exception:
            continue  # skip any corrupted entries safely

        patient_match = ('*' in patients) or (decrypted.get('target_user_id') in patients)
        auditor_match = ('*' in auditors) or (decrypted.get('actor_user_id') in auditors)

        if ('*' in patients and '*' in auditors) or \
           ('*' in patients and auditor_match) or \
           ('*' in auditors and patient_match) or \
           (patient_match and auditor_match):
            matching_records.append(decrypted)

    
    access_log = {
        "actor_user_id": payload["user_id"],
        "actor_username": payload["username"],
        "actor_role": payload["role"],
        "target_user_id": ",".join(patients),
        "action": "query"
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