import os
import json
import logging
import smtplib
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

log = logging.getLogger(__name__)

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Contracts")


def _mark_email_sent(source_file: str):
    path = os.path.join(CONTRACTS_DIR, source_file)
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        data["audit_email_sent"] = date.today().isoformat()
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log.info("Flagged audit_email_sent in %s", source_file)
    except Exception as e:
        log.error("Failed to flag audit_email_sent in %s: %s", source_file, e)


def send_audit_email(
    to_email: str,
    supplier_name: str,
    valid_to: str,
    audit_date: str,
    source_file: str,
    alternatives_summary: str,
) -> str:
    """Sends an audit notification email with alternative supplier research.

    Args:
        to_email: Recipient email address.
        supplier_name: Name of the current supplier.
        valid_to: Contract expiry date (YYYY-MM-DD).
        audit_date: The date the review was triggered (YYYY-MM-DD).
        source_file: The JSON filename for reference.
        alternatives_summary: Researched alternative suppliers with cost, terms, and
            termination details formatted as plain text.

    Returns:
        A confirmation or error message.
    """
    smtp_host = "smtp.office365.com"
    smtp_port = 587
    smtp_user = os.getenv("OFFICE365_EMAIL", "")
    smtp_password = os.getenv("OFFICE365_PASSWORD", "")
    sender = smtp_user

    log.info("Sending audit email to=%s from=%s for supplier=%s", to_email, sender, supplier_name)

    if not smtp_user or not smtp_password:
        msg = "OFFICE365_EMAIL or OFFICE365_PASSWORD not set in environment"
        log.error(msg)
        return f"Failed: {msg}"

    subject = f"Contract Review Due: {supplier_name}"
    body = f"""
Hi,

The following contract is due for review — please decide whether to renew, renegotiate, or terminate before the expiry date.

CURRENT CONTRACT
  Supplier:    {supplier_name}
  Expires:     {valid_to}
  Review by:   {audit_date}
  Record file: {source_file}

ALTERNATIVE SUPPLIERS
{alternatives_summary}

This is an automated notification.
""".strip()

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_password)
            server.sendmail(sender, to_email, msg.as_string())
        result = f"Email sent to {to_email} for contract '{supplier_name}'."
        log.info(result)
        _mark_email_sent(source_file)
        return result
    except Exception as e:
        result = f"Failed to send email to {to_email}: {e}"
        log.error(result, exc_info=True)
        return result
