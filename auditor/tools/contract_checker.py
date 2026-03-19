import os
import json
import logging
import re
from datetime import date
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger(__name__)

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Contracts")


def _parse_termination(termination: str) -> relativedelta:
    """Parses a termination string like '3 months' or '1 year' into a relativedelta."""
    termination = termination.strip().lower()
    match = re.match(r"(\d+)\s*(month|months|year|years)", termination)
    if not match:
        raise ValueError(f"Cannot parse termination period: '{termination}'")
    amount = int(match.group(1))
    unit = match.group(2)
    if "month" in unit:
        return relativedelta(months=amount)
    return relativedelta(years=amount)


def get_contracts_due_for_audit() -> list[dict]:
    """Loads all contract JSON files, recalculates audit_date from valid_to minus
    termination period, and returns contracts where today >= audit_date.

    Returns:
        A list of contract dicts that are due (or overdue) for audit review.
    """
    today = date.today()
    log.info("Checking contracts for audit. Today: %s", today)
    due = []

    for fname in os.listdir(CONTRACTS_DIR):
        if not fname.lower().endswith(".json"):
            continue

        path = os.path.join(CONTRACTS_DIR, fname)
        with open(path, encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                log.warning("Skipping %s — invalid JSON", fname)
                continue

        valid_to = data.get("valid_to")
        termination = data.get("termination")

        if not valid_to or not termination:
            log.warning("Skipping %s — missing valid_to or termination (valid_to=%r, termination=%r)", fname, valid_to, termination)
            continue

        try:
            end_date = date.fromisoformat(valid_to)
            delta = _parse_termination(termination)
            audit_date = end_date - delta
        except (ValueError, TypeError) as e:
            log.warning("Skipping %s — could not calculate audit date: %s", fname, e)
            continue

        data["audit_date"] = audit_date.isoformat()
        data["responsible_email"] = os.getenv("RESPONSIBLE_EMAIL", "")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        log.info("%s — valid_to=%s, termination=%s, audit_date=%s, due=%s", fname, valid_to, termination, audit_date, today == audit_date)

        if today == audit_date:
            due.append({**data, "source_file": fname})

    log.info("Contracts due for audit: %d", len(due))
    return due
