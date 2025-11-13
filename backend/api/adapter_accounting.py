# backend/api/adapter_accounting.py
"""
Adapter layer: API ↔ Accounting Engine

This module provides small wrapper functions that the FastAPI endpoints can import and call.
It isolates the accounting implementation (stubs or full engine) so the API stays clean.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import backend.accounting_engine.stubs as acct
import csv
import io

# Initialize / ensure schema and seed demo accounts
acct._ensure_schema()
acct.seed_default_accounts()


def create_transaction_and_post(
    user_id: Optional[str],
    date: datetime,
    amount: float,
    description: Optional[str] = None,
    source: str = "manual",
    reference: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Convenience function: creates a transaction record, then creates a basic journal entry.
    For demo purposes: posts a simple debit to Bank (1100) and credit to Sales (4000) when amount > 0.
    Replace this logic with the production rules engine later.
    """
    tx_id = acct.create_transaction(user_id=user_id, amount=amount, description=description or "", source=source, reference=reference)

    # Build a simple journal entry: Debit Bank (1100) / Credit Sales (4000)
    entry_date = date.date().isoformat()
    lines = [
        {"account_code": "1100", "debit": float(amount), "credit": 0.0},
        {"account_code": "4000", "debit": 0.0, "credit": float(amount)},
    ]

    je_id = acct.create_journal_entry(transaction_id=tx_id, entry_date=entry_date, description=description or "Auto-posted", lines=lines)

    return {"transaction_id": tx_id, "journal_entry_id": je_id}


def get_trial_balance(from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns a packaged trial balance with totals.
    """
    tb = acct.compute_trial_balance(from_date, to_date)
    total_debit = sum(row["total_debit"] for row in tb)
    total_credit = sum(row["total_credit"] for row in tb)
    return {"trial_balance": tb, "total_debit": round(total_debit, 2), "total_credit": round(total_credit, 2)}


def get_profit_and_loss(from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns profit/loss summary.
    """
    pnl = acct.compute_profit_and_loss(from_date, to_date)
    return pnl


def get_balance_sheet(as_of: Optional[str] = None) -> Dict[str, Any]:
    """
    Returns balance sheet top-level totals.
    """
    bs = acct.compute_balance_sheet(as_of)
    return bs


def import_transactions_from_csv_bytes(csv_bytes: bytes, user_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Import transactions from uploaded CSV content (bytes), create transactions, and optionally post them.
    Returns a summary of created transaction IDs.
    Expected CSV headers: date,description,amount,currency,source,reference
    """
    text = csv_bytes.decode("utf-8")
    reader = csv.DictReader(io.StringIO(text))
    created = []
    for row in reader:
        try:
            date_str = row.get("date") or datetime.utcnow().date().isoformat()
            date = datetime.fromisoformat(date_str) if "T" in date_str else datetime.fromisoformat(date_str + "T00:00:00")
            amount = float(row.get("amount", "0") or "0")
            description = row.get("description") or ""
            source = row.get("source") or "csv_import"
            reference = row.get("reference")
            tx_id = acct.create_transaction(user_id=user_id, amount=amount, description=description, source=source, reference=reference)
            created.append(tx_id)
        except Exception as e:
            # skip malformed rows but continue
            print(f"[adapter_accounting] skipping row due to error: {e}")
            continue

    return {"created_transactions": created, "count": len(created)}


# Expose a small convenience to be used by API main
__all__ = [
    "create_transaction_and_post",
    "get_trial_balance",
    "get_profit_and_loss",
    "get_balance_sheet",
    "import_transactions_from_csv_bytes",
]
