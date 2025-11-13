# backend/api/adapter_chatbot.py
"""
Adapter layer: API ↔ AI Chatbot Engine

This module bridges the FastAPI chatbot endpoint and the internal chatbot logic.
It provides:
- Preprocessing of user queries
- Intent detection (rule-based)
- Entity extraction
- Command routing
- Response formatting

This keeps 'main.py' very clean and maintains a stable interface
whether using the simple rules engine or a future ML model.
"""

from typing import Dict, Any, Optional
import re
import backend.accounting_engine.stubs as acct
import backend.automation.scheduler as scheduler


# ------------------------------------------------------------
# 1. Preprocessing
# ------------------------------------------------------------
def preprocess(text: str) -> str:
    text = text.strip().lower()
    return re.sub(r"\s+", " ", text)


# ------------------------------------------------------------
# 2. Intent Detection (Rule-Based)
# ------------------------------------------------------------
def detect_intent(text: str) -> str:
    if "profit" in text or "p&l" in text:
        return "INTENT_PROFIT"
    if "balance sheet" in text:
        return "INTENT_BALANCE_SHEET"
    if "trial balance" in text:
        return "INTENT_TRIAL_BALANCE"
    if "expense" in text or "spending" in text:
        return "INTENT_EXPENSE_SUMMARY"
    if "sales" in text or "revenue" in text:
        return "INTENT_REVENUE_SUMMARY"
    if "reminder" in text or "follow up" in text:
        return "INTENT_SEND_REMINDER"
    if "hello" in text or "hi" in text:
        return "INTENT_SMALLTALK"
    return "INTENT_UNKNOWN"


# ------------------------------------------------------------
# 3. Entity Extraction (Simple Regex)
# ------------------------------------------------------------
def extract_entities(query: str) -> Dict[str, Any]:
    # numbers
    amounts = re.findall(r"\d+(?:\.\d+)?", query)
    
    # dates (very simple demo)
    date_keywords = []
    if "today" in query:
        date_keywords.append("today")
    if "yesterday" in query:
        date_keywords.append("yesterday")
    if "this month" in query:
        date_keywords.append("this_month")

    return {
        "amounts": amounts,
        "date_keywords": date_keywords,
    }


# ------------------------------------------------------------
# 4. Dispatcher (Routes Intent to Engine)
# ------------------------------------------------------------
def dispatch(intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    # Finance reports
    if intent == "INTENT_PROFIT":
        return {"reply": _format_profit(acct.compute_profit_and_loss())}

    if intent == "INTENT_BALANCE_SHEET":
        return {"reply": _format_balance(acct.compute_balance_sheet())}

    if intent == "INTENT_TRIAL_BALANCE":
        tb = acct.compute_trial_balance()
        return {"reply": f"Trial balance has {len(tb)} accounts. Total debit={sum(x['total_debit'] for x in tb):.2f}, total credit={sum(x['total_credit'] for x in tb):.2f}"}

    # Smalltalk
    if intent == "INTENT_SMALLTALK":
        return {"reply": "Hello! How can I assist you today?"}

    # Reminders
    if intent == "INTENT_SEND_REMINDER":
        # simple example
        scheduler.run_task_now("daily_summary")
        return {"reply": "Reminder task has been triggered."}

    # Fallback
    return {"reply": "I'm not fully sure what you mean, but I'm learning. Try asking about profit, balance sheet, reminders, or expenses."}


# ------------------------------------------------------------
# 5. Formatting Helpers
# ------------------------------------------------------------
def _format_profit(pnl: Dict[str, float]) -> str:
    return (
        f"Profit & Loss Summary:\n"
        f"- Income: ₹{pnl['income']:.2f}\n"
        f"- Expenses: ₹{pnl['expense']:.2f}\n"
        f"- Net Profit: ₹{pnl['profit']:.2f}"
    )


def _format_balance(bs: Dict[str, float]) -> str:
    return (
        f"Balance Sheet:\n"
        f"- Assets: ₹{bs['assets']:.2f}\n"
        f"- Liabilities: ₹{bs['liabilities']:.2f}\n"
        f"- Equity: ₹{bs['equity']:.2f}\n"
        f"- Reconciliation: {bs['reconciles']:.2f}"
    )


# ------------------------------------------------------------
# 6. Public Engine Entry Point
# ------------------------------------------------------------
def handle_chat_message(query: str, session_id: Optional[str] = None) -> Dict[str, Any]:
    cleaned = preprocess(query)
    intent = detect_intent(cleaned)
    entities = extract_entities(cleaned)
    result = dispatch(intent, entities)

    return {
        "query": query,
        "intent": intent,
        "entities": entities,
        "reply": result["reply"],
    }


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------
if __name__ == "__main__":
    print(handle_chat_message("What is my profit today?"))
    print(handle_chat_message("Show me the balance sheet"))
    print(handle_chat_message("Send a payment reminder"))
