from flask import Blueprint, jsonify
import json
import os
import requests
import threading
import time
from app.chain import verify_chain

sync_bp = Blueprint('sync', __name__)

@sync_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@sync_bp.route('/audit/verify', methods=['GET'])
def audit_verify():
    is_valid, message = verify_chain()
    return jsonify({
        'valid': is_valid,
        'message': message
    })

def load_known_nodes():
    try:
        with open('data/nodes.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Failed to load nodes.json: {e}")
        return []

def ping_peers():
    nodes = load_known_nodes()
    my_node_id = os.environ.get("NODE_ID", "1")

    print(f"\nDiscovering peers from nodes.json (I am node {my_node_id})...")
    for node in nodes:
        if node['node_id'] == my_node_id:
            continue  # Skip self

        try:
            response = requests.get(f"{node['url']}/health", timeout=2)
            if response.status_code == 200:
                print(f"✅ Node {node['node_id']} reachable at {node['url']}")
            else:
                print(f"⚠️ Node {node['node_id']} responded with status {response.status_code}")
        except Exception as e:
            print(f"❌ Node {node['node_id']} unreachable at {node['url']}: {e}")

def start_peer_monitor(interval=5):
    def monitor():
        while True:
            print("\nPeriodic peer check:")
            ping_peers()
            time.sleep(interval)

    thread = threading.Thread(target=monitor, daemon=True)
    thread.start()