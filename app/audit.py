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

        patient_match = ('*' in patients) or (decrypted['patient_id'] in patients)
        auditor_match = ('*' in auditors) or (decrypted['user_id'] in auditors)

        if patient_match or auditor_match:
            matching_records.append(decrypted)

    # 🔥 Log that auditor accessed records
    access_log = {
        "user_id": payload["user_id"],
        "patient_id": ",".join(patients),
        "action": "audit_query"
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

    patient_id = payload['patient_id']

    chain = load_chain()
    matching_records = []

    for entry in chain:
        try:
            decrypted = decrypt_log_record(entry['encrypted_data'])
            patient_ids = decrypted['patient_id'].split(",")
            if patient_id in patient_ids:
                matching_records.append(decrypted)
        except Exception:
            continue  # skip corrupted or tampered entries

    return jsonify({
        "patient_id": patient_id,
        "records": matching_records,
        "count": len(matching_records)
    })