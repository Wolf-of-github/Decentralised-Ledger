from flask import Blueprint, request, jsonify, current_app
import jwt
from app.chain import load_chain, append_to_chain
from app.encryption import decrypt_log_record
from datetime import datetime

audit_bp = Blueprint('audit', __name__)

def verify_jwt(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET'], algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

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
            raw_ts = entry.get("timestamp", "")
            formatted_ts = ""
            try:
                formatted_ts = datetime.fromisoformat(raw_ts).strftime("%Y-%m-%d, %H:%M:%S")
            except Exception:
                formatted_ts = raw_ts  # fallback if parsing fails

            matching_records.append({
                **decrypted,
                "timestamp": formatted_ts
            })
        else:
            if decrypted.get('actor_user_id') == patient_id:
                raw_ts = entry.get("timestamp", "")
                formatted_ts = ""
                try:
                    formatted_ts = datetime.fromisoformat(raw_ts).strftime("%Y-%m-%d, %H:%M:%S")
                except Exception:
                    formatted_ts = raw_ts  # fallback if parsing fails

                matching_records.append({
                    **decrypted,
                    "timestamp": formatted_ts
                })

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
            raw_ts = entry.get("timestamp", "")
            formatted_ts = ""
            try:
                formatted_ts = datetime.fromisoformat(raw_ts).strftime("%Y-%m-%d, %H:%M:%S")
            except Exception:
                formatted_ts = raw_ts  # fallback if parsing fails

            matching_records.append({
                **decrypted,
                "timestamp": formatted_ts
            })
        else:
            if decrypted.get('actor_user_id') == auditor_id:
                raw_ts = entry.get("timestamp", "")
                formatted_ts = ""
                try:
                    formatted_ts = datetime.fromisoformat(raw_ts).strftime("%Y-%m-%d, %H:%M:%S")
                except Exception:
                    formatted_ts = raw_ts  # fallback if parsing fails

                matching_records.append({
                    **decrypted,
                    "timestamp": formatted_ts
                })

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

@audit_bp.route('/audit/my-access', methods=['GET'])
def get_my_audit_access():
    from datetime import datetime

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
                raw_ts = entry.get("timestamp", "")
                formatted_ts = ""
                try:
                    formatted_ts = datetime.fromisoformat(raw_ts).strftime("%Y-%m-%d, %H:%M:%S")
                except Exception:
                    formatted_ts = raw_ts  # fallback if parsing fails

                matching_records.append({
                    **decrypted,
                    "timestamp": formatted_ts
                })
        except Exception:
            continue  # skip corrupted or tampered entries

    return jsonify({
        "patient_id": patient_id,
        "records": matching_records,
        "count": len(matching_records)
    })