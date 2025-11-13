# API Backend — Technical Specification  
### XYLO Business Automation Suite

The API Backend acts as the central communication layer of XYLO.  
It connects the frontend dashboard, automation engine, accounting engine, AI chatbot, and database into a unified system.

This document explains the responsibilities, architecture, endpoints, and communication flow of the backend.

---

# 🧩 1. Core Responsibilities

### ✔ Routing & Request Handling
Handles all REST API endpoints:
- User authentication  
- Uploading invoices  
- Adding transactions  
- Fetching ledgers and reports  
- Chatbot message handling  
- Automation triggers  

### ✔ Business Logic Aggregation
API does **not** contain heavy logic.  
It forwards requests to:
- Accounting Engine  
- Automation Engine  
- Chatbot Engine  
- Database Layer  

### ✔ Data Validation
Ensures inputs are safe and clean:
- Required fields  
- Valid amounts  
- Correct formatting  

### ✔ Response Packaging
Uniform JSON responses:
{
"status": "success",
"data": { ... },
"timestamp": "2025-01-01T10:30:10"
}


---

# ⚙️ 2. Technology Stack

Recommended stack:

- Python  
- FastAPI or Flask  
- Pydantic (for validation)  
- SQLite / PostgreSQL  
- Uvicorn (for local server)  

Structure lives in:
backend/api/

---

# 🛠 3. Internal Architecture (Backend Layering)

      +-------------------------------+
      |           Frontend            |
      +-------------------------------+
                      |
                      v
      +-------------------------------+
      |           API Backend         |
      |  (routes, auth, validators)   |
      +-------------------------------+
          |             |           |
          |             |           |
          v             v           v
 +-------------+ +-------------+ +-------------+
 | Accounting  | | Automation  | | AI Chatbot  |
 |   Engine    | |   Engine    | |   Engine    |
 +-------------+ +-------------+ +-------------+
          \             |           /
           \            |          /
            v           v         v
                 +-------------+
                 |   Database   |
                 +-------------+

---

# 🔌 4. Core API Modules
backend/api/
auth.py
accounting_routes.py
automation_routes.py
chatbot_routes.py
database_interface.py

---

# 📚 5. Example Endpoint Categories

## 1. Authentication
POST /auth/register
POST /auth/login
GET /auth/me

## 2. Accounting
POST /accounting/add_transaction
GET /accounting/ledger/{account_name}
GET /accounting/trial_balance
GET /accounting/profit_loss
GET /accounting/balance_sheet

## 3. Automation
POST /automation/run_daily_summary
POST /automation/send_payment_reminder
GET /automation/tasks

## 4. Chatbot
POST /chatbot/message
Request:
{ "query": "What are today's expenses?" }
Response:
{ "reply": "Today's expenses are ₹3,250." }


## 5. Invoice Upload
POST /invoices/upload
Backend:
- Extract text  
- Categorize expense  
- Add to ledger  

---

# 🔐 6. Authentication & Security

### JWT-based login
- Issues access tokens  
- Validates each request  
- Protects private endpoints  

### Role support (Future)
- Admin  
- Staff  
- Viewer  

---

# 💾 7. Database Interface Layer

API uses a unified database helper:
database_interface.py


Responsibilities:
- Fetch user info  
- Insert ledger entries  
- Retrieve reports  
- Log chatbot interactions  
- Read automation tasks  

Database types supported:
- SQLite (simple)  
- PostgreSQL (production)  

---

# 🧠 8. Why This API Design Works

### ✔ Clean boundaries  
Logic stays in modules, not in API.

### ✔ Expandable  
More services can be added later.

### ✔ Easy to maintain  
Single responsibility per route.

### ✔ Professional  
Matches modern backend architecture.

---

# 📌 Summary

The API Backend serves as the **central controller** of XYLO:

- Routes requests  
- Validates data  
- Connects modules  
- Controls workflow  
- Sends uniform responses  

It keeps XYLO modular, scalable, and maintainable.
