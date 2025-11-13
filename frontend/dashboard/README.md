# XYLO Dashboard — Frontend Specification  
### XYLO Business Automation Suite

The XYLO Dashboard is the main user interface for business owners.  
It provides access to accounting reports, automation features, AI assistant, and business data visualization.

This document outlines the layout, UI components, page structure, and API integration points.

---

# 🎯 Core Goals

- Simple, clean, business-friendly UI  
- Fast navigation  
- Immediate access to financial insights  
- Integrated AI assistant  
- Responsive layout (works on desktop/mobile)  
- Stateless, API-driven frontend  

Recommended stack:  
- **HTML/CSS/JS** (simple) or **React** (preferred)  
- **Fetch / Axios** for API calls  

---

# 🧩 1. Dashboard Layout (High-Level)
+-------------------------------------------------------------+
| Sidebar (Navigation) | Main Area (Graphs, Reports, Actions) |
+-------------------------------------------------------------+
| AI Assistant Panel (Collapsible) |
+-------------------------------------------------------------+

### Sidebar Sections:
- Dashboard Home  
- Transactions  
- Ledgers  
- Reports  
- Automations  
- Invoices  
- AI Assistant  
- Settings  
- Logout  

---

# 📊 2. Pages & Features

## 2.1 Dashboard Home
Shows key business metrics:

- **Total Revenue (current month)**  
- **Total Expenses**  
- **Net Profit**  
- **Cash Flow Overview**  
- Graph: Revenue vs Expense (line/bar chart)  
- Quick actions:
  - Add Transaction  
  - Generate Report  
  - Open Assistant  

API Calls Used:
GET /accounting/profit_loss
GET /accounting/trial_balance

---

## 2.2 Transactions Page

### Features:
- List view of all transactions  
- Search by date, amount, keyword  
- Add new transaction modal  
- Edit/delete transaction (optional)  

API Calls:
GET /transactions
POST /accounting/add_transaction


---

## 2.3 Ledger Viewer

Displays individual ledgers:

- Cash  
- Bank  
- Sales  
- Expenses  
- Payables  
- Equity  

Columns:
Date | Description | Debit | Credit | Balance

API:
GET /accounting/ledger/{account_code}

---

## 2.4 Reports Section

Reports available:
- Trial Balance  
- Profit & Loss  
- Balance Sheet  
- Monthly Summary  
- Expense Breakdown  

Download formats:
- JSON  
- CSV  
- PDF (future)

API:
GET /accounting/trial_balance
GET /accounting/profit_loss
GET /accounting/balance_sheet

---

## 2.5 Automation Settings

Features:
- Toggle automatic daily summary  
- Add scheduling rules (cron-like)  
- View past automation task history  
- Payment reminder manager  

API:
GET /automation/tasks
POST /automation/run_daily_summary
POST /automation/send_payment_reminder

---

## 2.6 Invoice Upload Page

Allows:
- Upload invoice PDFs/images  
- OCR/extraction results preview  
- Auto transaction creation  

API:
POST /invoices/upload

---

## 2.7 AI Assistant Panel

Floating or docked panel.

### Capabilities:
- Ask queries:
  - “Show today’s sales.”  
  - “Generate balance sheet.”  
  - “Total expenses this month?”  
- Get instant answers  
- Use shortcuts/buttons for common queries  
- Maintains conversation context  

API:
POST /chatbot/message

---

# 🧱 3. UI Components

### Shared Components:
- `<SidebarNav />`
- `<TopBar />`
- `<Card />`
- `<Table />`
- `<Graph />`
- `<Modal />`
- `<Loader />`
- `<Toast />`
- `<AIChatBox />`

### Style Recommendations:
- Flat, clean UI  
- Blue/white theme  
- Icons for each sidebar item  
- Use simple CSS grid for layout  

---

# 🔌 4. API Integration Strategy

Each page communicates with backend:

- `fetch(url)` or Axios request  
- JSON payloads  
- Error handling & loading states  
- Central config file for all API endpoints  

Example (pseudo-code):

```js
async function getProfitLoss() {
  const res = await fetch('/accounting/profit_loss');
  return await res.json();
}
