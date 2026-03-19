import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Contracts")


def write_contract_metadata(filename: str, fields: dict) -> str:
    """Writes the extracted contract metadata to a JSON file in the Contracts folder.

    The output filename matches the source PDF (e.g. 'contract.pdf' -> 'contract.json').

    Args:
        filename: The source PDF filename (e.g. 'contract.pdf').
        fields: The complete extracted contract fields as a dict.

    Returns:
        A confirmation message with the path of the written file.
    """
    base = os.path.splitext(filename)[0]
    output_path = os.path.join(CONTRACTS_DIR, f"{base}.json")

    fields["responsible_email"] = os.getenv("RESPONSIBLE_EMAIL", "")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=2, ensure_ascii=False)

    return f"Metadata written to {output_path}"
