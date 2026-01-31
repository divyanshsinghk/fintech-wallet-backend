
# Fintech Wallet Backend (FastAPI + MongoDB)

A production-grade **Fintech Wallet Backend** built using **FastAPI** and **MongoDB**, implementing real-world banking rules such as atomic transactions, idempotency, balance integrity, and secure authorization.

---

## Features

- User Authentication (JWT)
- One User → One Wallet
- Wallet Balance Management
- Atomic Credit / Debit / Transfer
- Transaction History & Statements
- Date-range Transaction Statements
- Transaction Summary & Analytics
- Idempotent Transfers
- Read-only Ledger (No edits/deletes)
- Secure Authorization & Access Control

---

## Architecture

The system follows a **clean layered architecture**:



Routes → Services → Database
→ Schemas
→ Utils (Auth, Security)


 **Detailed architecture and core business rules are documented here:**  
`ARCHITECTURE.md`


---

## Project Structure



app/
├── routes/ # API endpoints
├── services/ # Business logic
├── schemas/ # Pydantic models
├── utils/ # Security, auth helpers
├── database.py # MongoDB connection
├── config.py # Environment config
└── main.py # FastAPI entry point


---

##  Core Business Rules

- One User → One Wallet
- No negative balances
- MongoDB transactions for atomicity
- Transactions are immutable
- Authorization required for all wallet operations
- Frozen wallets cannot transact

(See `ARCHITECTURE.md` for full rules)

---

##  Tech Stack

- **FastAPI**
- **MongoDB**
- **PyMongo**
- **JWT Authentication**
- **Pydantic**
- **Uvicorn**

---

##  Run Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt

2. Set environment variables

Create .env:

MONGO_URI=your_mongodb_uri
JWT_SECRET=your_secret

3. Start server
uvicorn app.main:app --reload

4. Open API Docs
http://127.0.0.1:8000/docs

API Highlights

POST /auth/register

POST /auth/login

GET /wallet/me

POST /wallet/credit

POST /wallet/debit

POST /transfer

GET /transactions/me

GET /transactions/statement

GET /transactions/statement/summary