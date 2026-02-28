# Secure Decentralized Electronic Health Record Audit System

A cryptographically secure and decentralized audit system for Electronic Health Records (EHR), developed as part of the CSCI 531 Semester Project.

---

## Overview

This project addresses the growing need for privacy-preserving and tamper-evident audit logging in modern Electronic Health Record systems.

It enables:
- Patients to view access logs on their medical data  
- Auditors to track and verify data access  
- A decentralized, verifiable ledger to ensure audit integrity  

---

## Key Features

- **Secure Audit Logs** – Immutable, encrypted logs using AES-GCM and RSA  
- **Decentralized Architecture** – Multi-node system with peer discovery  
- **Role-Based Access Control** – Patients and auditors have distinct permissions  
- **Tamper Detection** – Merkle tree verification and chained hash logs  
- **React Frontend** – Intuitive interface for patients and auditors  
- **JWT Authentication** – Token-based stateless user sessions  

---

## Technologies Used

### Backend
- Python (Flask)  
- JWT Authentication  
- AES-GCM Encryption  
- RSA Public-Key Cryptography  
- SHA-256 Hashing  

### Frontend
- React.js  
- Bootstrap  

### Ledger & Communication
- Append-only JSON chain with cryptographic linkage  
- REST APIs over HTTP  
  (Can be upgraded to HTTPS for production security)

---

## System Modules

| Module | Description |
|--------|------------|
| `auth.py` | User authentication and JWT token issuance |
| `ehr.py` | Patient EHR data retrieval and audit logging |
| `audit.py` | Querying and managing audit records |
| `chain.py` | Ledger creation, hashing, and verification |
| `encryption.py` | AES-GCM + RSA envelope encryption logic |
| `sync.py` | Peer discovery and node health checks |

---

## How to Run

### 1. Configure Environment Files

Create `.env.nodeX` files for each node.

### 2. Launch Backend Nodes

```bash
set -o allexport; source .env.nodeX; set +o allexport && python run.py
