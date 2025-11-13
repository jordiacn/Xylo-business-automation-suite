# backend/utils/pdf_generator.py
"""
XYLO — PDF Report Generator (ReportLab)

This module generates professional PDF reports for:
- Daily summaries
- Profit & Loss
- Balance sheet snapshots
- Trial balance tables

These PDFs can be:
- Downloaded via API
- Emailed via email_service.py
- Auto-generated via automation scheduler
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from typing import Dict, Any, List

import backend.accounting_engine.stubs as acct


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------

styles = getSampleStyleSheet()
TITLE = styles["Title"]
HEADER = styles["Heading2"]
NORMAL = styles["BodyText"]


def _timestamp():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _save_pdf(path: str, elements: List[Any]):
    """
    Builds the PDF document at the provided path.
    """
    doc = SimpleDocTemplate(path, pagesize=A4)
    doc.build(elements)
    return path


# ------------------------------------------------------------
# 1. Daily Summary PDF
# ------------------------------------------------------------

def create_daily_summary_pdf(output_path: str) -> str:
    today = datetime.utcnow().date().isoformat()
    pnl = acct.compute_profit_and_loss(today, today)
    tb = acct.compute_trial_balance(today, today)

    elements = []
    elements.append(Paragraph("XYLO — Daily Summary Report", TITLE))
    elements.append(Paragraph(f"Date: {today}", NORMAL))
    elements.append(Paragraph(f"Generated at: {_timestamp()}", NORMAL))
    elements.append(Spacer(1, 12))

    # P&L Section
    elements.append(Paragraph("Profit & Loss", HEADER))
    elements.append(Paragraph(f"Income: ₹{pnl['income']:.2f}", NORMAL))
    elements.append(Paragraph(f"Expenses: ₹{pnl['expense']:.2f}", NORMAL))
    elements.append(Paragraph(f"Net Profit: ₹{pnl['profit']:.2f}", NORMAL))
    elements.append(Spacer(1, 12))

    # Trial Balance Section
    elements.append(Paragraph("Trial Balance", HEADER))

    tb_data = [["Account Code", "Account Name", "Type", "Debit", "Credit"]]
    for row in tb:
        tb_data.append([
            row["account_code"],
            row["account_name"],
            row["type"],
            f"{row['total_debit']:.2f}",
            f"{row['total_credit']:.2f}",
        ])

    tb_table = Table(tb_data)
    tb_table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(tb_table)

    return _save_pdf(output_path, elements)


# ------------------------------------------------------------
# 2. Profit & Loss PDF
# ------------------------------------------------------------

def create_pnl_pdf(output_path: str) -> str:
    pnl = acct.compute_profit_and_loss()

    elements = [
        Paragraph("XYLO — Profit & Loss Report", TITLE),
        Paragraph(f"Generated: {_timestamp()}", NORMAL),
        Spacer(1, 12),
        Paragraph(f"Income: ₹{pnl['income']:.2f}", NORMAL),
        Paragraph(f"Expenses: ₹{pnl['expense']:.2f}", NORMAL),
        Paragraph(f"Net Profit: ₹{pnl['profit']:.2f}", NORMAL),
    ]

    return _save_pdf(output_path, elements)


# ------------------------------------------------------------
# 3. Balance Sheet PDF
# ------------------------------------------------------------

def create_balance_sheet_pdf(output_path: str) -> str:
    bs = acct.compute_balance_sheet()

    elements = [
        Paragraph("XYLO — Balance Sheet", TITLE),
        Paragraph(f"Generated: {_timestamp()}", NORMAL),
        Spacer(1, 12),
        Paragraph(f"Assets: ₹{bs['assets']:.2f}", NORMAL),
        Paragraph(f"Liabilities: ₹{bs['liabilities']:.2f}", NORMAL),
        Paragraph(f"Equity: ₹{bs['equity']:.2f}", NORMAL),
        Paragraph(f"Reconciliation Value: {bs['reconciles']}", NORMAL),
    ]

    return _save_pdf(output_path, elements)


# ------------------------------------------------------------
# 4. Trial Balance PDF
# ------------------------------------------------------------

def create_trial_balance_pdf(output_path: str) -> str:
    tb = acct.compute_trial_balance()

    elements = [
        Paragraph("XYLO — Trial Balance", TITLE),
        Paragraph(f"Generated: {_timestamp()}", NORMAL),
        Spacer(1, 12),
    ]

    tb_data = [["Account Code", "Account Name", "Type", "Debit", "Credit"]]
    for row in tb:
        tb_data.append([
            row["account_code"],
            row["account_name"],
            row["type"],
            f"{row['total_debit']:.2f}",
            f"{row['total_credit']:.2f}",
        ])

    table = Table(tb_data)
    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ])
    )

    elements.append(table)

    return _save_pdf(output_path, elements)


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------

if __name__ == "__main__":
    print(create_daily_summary_pdf("daily_summary.pdf"))
    print(create_pnl_pdf("pnl_report.pdf"))
    print(create_balance_sheet_pdf("balance_sheet.pdf"))
    print(create_trial_balance_pdf("trial_balance.pdf"))
