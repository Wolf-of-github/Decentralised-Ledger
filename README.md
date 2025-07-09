Secure Decentralized Electronic Health Record Audit System
A cryptographically secure and decentralized audit system for Electronic Health Records (EHR), developed as part of the CSCI 531 Semester Project.

🧩 Overview

This project addresses the growing need for privacy-preserving, tamper-evident audit logging in modern Electronic Health Record systems. It enables patients to view access logs on their data and auditors to track and verify data access using a decentralized, verifiable ledger.

🔐 Key Features
	•	Secure Audit Logs: Immutable, encrypted logs using AES-GCM & RSA.
	•	Decentralized Architecture: Multi-node system with peer discovery.
	•	Role-Based Access: Patients and auditors have distinct permissions.
	•	Tamper Detection: Merkle tree verification and chained hash logs.
	•	React Frontend: Intuitive interface for patients and auditors.
	•	JWT Authentication: Token-based stateless user sessions.

⚙️ Technologies Used
	•	Backend: Python (Flask), JWT, AES-GCM, RSA, SHA-256
	•	Frontend: React.js, Bootstrap
	•	Audit Ledger: Append-only JSON chain with cryptographic linkage
	•	Communication: HTTP (can be upgraded to HTTPS), REST APIs

📁 System Modules
	•	auth.py – User authentication and JWT token issuance.
	•	ehr.py – Patient EHR data retrieval and audit logging.
	•	audit.py – Querying and managing audit records.
	•	chain.py – Ledger creation, hashing, and verification.
	•	encryption.py – AES-GCM + RSA envelope encryption logic.
	•	sync.py – Peer discovery and node health checks.

🧪 How to Run
	1.	Create .env.nodeX files for each node.
	2.	Launch backend nodes:

set -o allexport; source .env.nodeX; set +o allexport && python run.py


	3.	Update React frontend with node info in App.js.
	4.	Start frontend:

cd client && npm start


	5.	Visit: http://localhost:3000

🧑‍⚕️ User Roles

Patients
	•	View their own EHR
	•	View who accessed their records

Auditors
	•	Query patient/auditor access logs
	•	Verify audit chain integrity

📌 Limitations
	•	No consensus protocol (nodes assume identical behavior)
	•	Static user roles (no dynamic account creation)
	•	No real-time ledger sync or key management UI
	•	Vulnerable to replay attacks if not run over HTTPS
