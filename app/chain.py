import json
import os
import hashlib
from datetime import datetime
from app.encryption import encrypt_log_record

LEDGER_PATH = os.environ.get("AUDIT_CHAIN_PATH", "shared/audit_chain.json")

def calculate_hash(entry):
    entry_copy = dict(entry)
    entry_copy.pop("current_hash", None)  # important!
    hash_str = json.dumps(entry_copy, sort_keys=True).encode('utf-8')
    return hashlib.sha256(hash_str).hexdigest()

def load_chain():
    if not os.path.exists(LEDGER_PATH):
        return []
    with open(LEDGER_PATH, 'r') as f:
        return json.load(f)

def save_chain(chain):
    os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
    with open(LEDGER_PATH, 'w') as f:
        json.dump(chain, f, indent=2)

def append_to_chain(log_data_dict):
    chain = load_chain()
    prev_hash = chain[-1]['current_hash'] if chain else "0" * 64

    encrypted_data = encrypt_log_record(log_data_dict)

    new_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "target_user_id": log_data_dict["target_user_id"],
        "actor_user_id": log_data_dict["actor_user_id"],
        "actor_username": log_data_dict["actor_username"],
        "actor_role": log_data_dict["actor_role"],
        "action": log_data_dict["action"],
        "encrypted_data": encrypted_data,
        "prev_hash": prev_hash,
    }
    new_entry["current_hash"] = calculate_hash(new_entry)
    chain.append(new_entry)
    save_chain(chain)

    return new_entry["current_hash"]

def verify_chain():
    chain = load_chain()
    for i in range(len(chain)):
        entry = chain[i]

        # Check if the prev_hash matches the previous entry's current_hash
        if i == 0:
            expected_prev = "0" * 64
        else:
            expected_prev = chain[i - 1]["current_hash"]

        if entry["prev_hash"] != expected_prev:
            return False, f"Tampering detected: bad prev_hash at index {i}"

        # Check if current_hash matches the recalculated hash
        expected_curr = calculate_hash(entry)
        if entry["current_hash"] != expected_curr:
            return False, f"Tampering detected: hash mismatch at index {i}"

    return True, "Chain is valid"

def get_latest_hash():
    chain = load_chain()
    if not chain:
        return None
    return chain[-1]["current_hash"]