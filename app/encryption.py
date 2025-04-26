import os
import base64
import json
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

# ───────────────────────────────
# Load RSA keys from PEM files
# ───────────────────────────────
def load_public_key(path='keys/public.pem'):
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read(), backend=default_backend())

def load_private_key(path='keys/private.pem'):
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())

# ───────────────────────────────
# Encrypt audit log entry
# ───────────────────────────────
def encrypt_log_record(log_data_dict):
    # Step 1: Convert log data to bytes
    data_bytes = json.dumps(log_data_dict).encode('utf-8')

    # Step 2: Generate AES key and nonce
    aes_key = AESGCM.generate_key(bit_length=128)
    aesgcm = AESGCM(aes_key)
    nonce = os.urandom(12)

    # Step 3: Encrypt the data with AES
    encrypted_data = aesgcm.encrypt(nonce, data_bytes, associated_data=None)

    # Step 4: Encrypt the AES key with RSA public key
    public_key = load_public_key()
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Step 5: Return base64-encoded bundle
    return {
        "encrypted_log": base64.b64encode(encrypted_data).decode('utf-8'),
        "nonce": base64.b64encode(nonce).decode('utf-8'),
        "encrypted_key": base64.b64encode(encrypted_key).decode('utf-8')
    }

# ───────────────────────────────
# Decrypt audit log entry
# ───────────────────────────────
def decrypt_log_record(enc_data, private_key_path='keys/private.pem'):
    private_key = load_private_key(private_key_path)

    # Step 1: Decode all base64 fields
    aes_key = private_key.decrypt(
        base64.b64decode(enc_data['encrypted_key']),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    nonce = base64.b64decode(enc_data['nonce'])
    encrypted_log = base64.b64decode(enc_data['encrypted_log'])

    # Step 2: Decrypt using AES-GCM
    aesgcm = AESGCM(aes_key)
    decrypted = aesgcm.decrypt(nonce, encrypted_log, associated_data=None)

    return json.loads(decrypted)
