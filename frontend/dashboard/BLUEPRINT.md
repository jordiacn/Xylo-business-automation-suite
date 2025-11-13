# XYLO Dashboard — Full UI/UX Blueprint  
### Product-Level Design for the XYLO Business Automation Suite

This blueprint defines the complete user interface, navigation flow, and user experience for the XYLO dashboard.  
It is intended for implementers, reviewers, and designers to understand how the system works visually and interactively.

---

# 🎯 Objectives

- Provide a clean, professional experience for small business users  
- Offer fast, simple access to financial insights  
- Integrate intelligent workflows (AI, automation, invoice parsing)  
- Keep layout predictable, efficient, and mobile-friendly  
- Mirror real ERP systems but with a lightweight UI  

---

# 🧭 **1. Global Navigation Structure**
Sidebar (Left)
Dashboard
Transactions
Ledgers
Reports
Automations
Invoices
AI Assistant
Settings
Logout

### Navigation Behavior
- Sidebar collapses on small screens  
- Icons + labels  
- Active page highlighted  

---

# 🏠 **2. Dashboard Screen (Home)**

### Components:

#### A. **Top Stats Row**
- **Total Revenue (This Month)**  
- **Total Expenses (This Month)**  
- **Net Profit**  
- **Cash on Hand**  
- **Pending Receivables** (future)

Visual: 4–5 clickable cards.

#### B. **Graphs Section**
- Revenue vs Expenses (bar/line chart)  
- Cash flow timeline  
- Expense category split (pie chart)

#### C. **Quick Actions**
- Add Transaction  
- Upload Invoice  
- Generate Report  
- Open AI Assistant  

#### D. **Notifications Pane**
- Overdue payments  
- Automation tasks  
- Alert messages  

---

# 📄 **3. Transactions Page**

### A. Filters Panel
- Date range  
- Amount range  
- Source (manual / invoice / bank)  
- Text search  

### B. Transactions Table
Columns:
Date | Description | Amount | Source | Reference | Actions


### C. Add Transaction Modal
Inputs:
- Date  
- Amount  
- Description  
- Source  
- Reference  

Posts to:
POST /accounting/add_transaction

---

# 📓 **4. Ledger Viewer**

Each ledger (Cash, Bank, Sales, Expenses, etc.) shows:

Date | Description | Debit | Credit | Running Balance


Features:
- Select ledger from dropdown  
- Export Ledger (CSV/PDF)  
- Filter by date  

API:
GET /accounting/ledger/{account}


---

# 📊 **5. Reports Section**

### Reports Offered:
- **Trial Balance**  
- **Profit & Loss**  
- **Balance Sheet**  
- **Daily Summary**  
- **Monthly Summary**  
- **Custom Period Report**  

### Layout:
- Date selectors  
- Generate Button  
- Display area (cards + tables)  
- Download buttons: JSON / CSV / PDF  

APIs:
GET /accounting/profit_loss
GET /accounting/balance_sheet
GET /accounting/trial_balance

Uses:
- pdf_generator  
- report_generator  

---

# 🤖 **6. Automations Page**

### A. Automation Overview
Displays current automation rules:
- Daily summary at 10PM  
- Weekly backup  
- Payment reminders  
- Custom task schedules  

### B. Task History Table
Task | Status | Run Time | Duration | Result

### C. Create Custom Automation (future)
- Cron-like selector  
- Actions: “Generate report”, “Send email”, “Trigger reminder”  

APIs:
GET /automation/tasks
POST /automation/run_daily_summary
POST /automation/send_payment_reminder

Scheduler integration:
- daily@HH:MM  
- weekly@sun@03:00  
- interval@300  

---

# 🧾 **7. Invoice Upload Page**

### Workflow:
1. Upload invoice file  
2. Preview extracted text  
3. Show parsed fields:
   - Invoice Number  
   - Date  
   - Vendor  
   - Amount  
4. Auto-create transaction  
5. Auto-post journal entry  
6. Provide result summary

API:
POST /invoices/upload

Uses:
- invoice_adapter  
- invoice_parser  
- accounting_engine  

---

# 🤖💬 **8. AI Assistant Panel**

Floating panel as defined in `AIChatBox.md`.

Capabilities:
- Ask natural-language finance queries  
- Trigger automation  
- Ask for reports  
- Ask invoice questions  

API:
POST /chatbot/message

Handles:
- intent detection  
- entity extraction  
- accounting lookups  
- reminder triggers  

---

# ⚙️ **9. Settings Page**

Options:
- Company profile  
- Currency format  
- Email settings (SMTP / notifications)  
- Automation toggles  
- Dark/Light mode (future)  
- Manage users (future)  

---

# 🔐 **10. Authentication Flow (Frontend)**

### Screens:
- Login  
- Register  
- Forgot password (future)

### JWT Handling:
- Store token in memory  
- Auto-refresh (future)  
- Logout wipes token  

---

# 📱 **11. Mobile Responsibilities**

Mobile layout:
- Sidebar collapses into hamburger menu  
- Cards stack vertically  
- Tables become scrollable horizontally  
- ChatBox becomes full-screen modal  

---

# 🧠 **12. Future Enhancements**

- Predictive analytics dashboard  
- Cashflow forecasting  
- Inventory module  
- Payroll module  
- Multi-user roles  
- Invoice templates  
- Webhooks  
- Real AI (transformer-based model) instead of rules  

---

# 📌 Summary

The XYLO dashboard is designed as a complete, modern financial automation environment:

- Clean professional UI  
- AI-assisted workflows  
- OCR-powered invoice ingestion  
- Full accounting view  
- Automation + reporting pipeline  
- Production-ready architecture  

This blueprint guides the full UI/UX development of XYLO.
