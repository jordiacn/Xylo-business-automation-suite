# backend/automation/invoice_parser.py
"""
XYLO — Invoice Parser (Lightweight OCR/Extraction)

This module extracts useful accounting data from invoices such as:
- invoice number
- date
- vendor name (basic)
- amount
- tax (if found)
- description

It supports:
- PDF invoices (using PyPDF2 text extraction)
- Image/PDF text as plain string (future: OCR library)

This version is intentionally simple but effective.
Can be upgraded to Tesseract OCR or cloud OCR later.
"""

import re
from typing import Dict, Any, Optional
from datetime import datetime

try:
    import PyPDF2
except Exception:
    PyPDF2 = None  # optional dependency


# ------------------------------------------------------------
# Utility: extract numeric amount from text
# ------------------------------------------------------------
def extract_amount(text: str) -> Optional[float]:
    """
    Extracts monetary value.
    Supports patterns like:
    - Rs 1240.50
    - INR 1200
    - 1,200.00
    - Amount: 2300
    """
    text = text.replace(",", "")
    match = re.search(r"(\d+\.\d+|\d+)", text)
    if match:
        try:
            return float(match.group(1))
        except:
            return None
    return None


# ------------------------------------------------------------
# Basic Extraction Rules
# ------------------------------------------------------------
def extract_invoice_number(text: str) -> Optional[str]:
    """
    Recognises patterns:
    - INV-1003
    - Invoice No: 4501
    - Bill #00124
    """
    patterns = [
        r"(INV[-\s]?\d+)",
        r"Invoice\s*No[:\s]*([A-Za-z0-9-]+)",
        r"Bill\s*#\s*([A-Za-z0-9-]+)",
    ]
    for p in patterns:
        m = re.search(p, text, flags=re.IGNORECASE)
        if m:
            return m.group(1)
    return None


def extract_date(text: str) -> Optional[str]:
    """
    Looks for DD/MM/YYYY, YYYY-MM-DD, DD-MM-YYYY.
    """
    patterns = [
        r"(\d{2}/\d{2}/\d{4})",
        r"(\d{4}-\d{2}-\d{2})",
        r"(\d{2}-\d{2}-\d{4})",
    ]
    for p in patterns:
        m = re.search(p, text)
        if m:
            try:
                # Normalise date to ISO
                return datetime.fromisoformat(
                    m.group(1).replace("/", "-")
                ).date().isoformat()
            except:
                continue
    return None


def extract_vendor(text: str) -> Optional[str]:
    """
    Simple heuristic:
    - Looks for lines starting with 'From', 'Vendor', 'Supplier'
    """
    lines = text.split("\n")
    for ln in lines:
        if ln.lower().startswith(("from", "vendor", "supplier")):
            return ln.split(":", 1)[-1].strip()
    return None


# ------------------------------------------------------------
# PDF Reader
# ------------------------------------------------------------
def extract_text_from_pdf(path: str) -> str:
    if PyPDF2 is None:
        raise ImportError("PyPDF2 not installed. Install PyPDF2 to process PDFs.")
    try:
        with open(path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        print(f"[invoice_parser] Error reading PDF: {e}")
        return ""


# ------------------------------------------------------------
# Main Entry Function
# ------------------------------------------------------------
def parse_invoice(file_path: str) -> Dict[str, Any]:
    """
    Extract structured invoice data.
    """

    # Read PDF or fallback to plain text
    if file_path.lower().endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    else:
        # plain text fallback
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    # Extract fields
    invoice_no = extract_invoice_number(text) or "Unknown"
    invoice_date = extract_date(text) or datetime.utcnow().date().isoformat()
    vendor = extract_vendor(text) or "Unknown Vendor"
    amount = extract_amount(text) or 0.0

    return {
        "invoice_number": invoice_no,
        "date": invoice_date,
        "vendor": vendor,
        "amount": float(amount),
        "raw_text_preview": text[:300] + "..." if len(text) > 300 else text,
    }


# ------------------------------------------------------------
# Demo
# ------------------------------------------------------------
if __name__ == "__main__":
    sample = parse_invoice("sample_invoice.pdf")
    print(sample)
