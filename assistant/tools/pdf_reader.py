import os
import pdfplumber

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Contracts")


def list_contracts() -> list[str]:
    """Lists all PDF contract files available in the Contracts folder."""
    files = [f for f in os.listdir(CONTRACTS_DIR) if f.lower().endswith(".pdf")]
    return files


def read_contract_pdf(filename: str) -> str:
    """Reads a contract PDF file and returns its full text content.

    Args:
        filename: The PDF filename (e.g. 'contract.pdf') inside the Contracts folder.

    Returns:
        The extracted text from the PDF.
    """
    path = os.path.join(CONTRACTS_DIR, filename)
    if not os.path.exists(path):
        return f"Error: File '{filename}' not found in Contracts folder."

    text_parts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {i + 1} ---\n{page_text}")

    if not text_parts:
        return "Error: No text could be extracted from this PDF."

    return "\n\n".join(text_parts)
