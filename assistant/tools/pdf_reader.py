import os
import pdfplumber
import google.genai as genai

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Contracts")


def list_contracts() -> list[str]:
    """Lists all PDF contract files available in the Contracts folder."""
    files = [f for f in os.listdir(CONTRACTS_DIR) if f.lower().endswith(".pdf")]
    return files


def read_contract_pdf(filename: str) -> str:
    """Reads a contract PDF and returns its content using both text extraction
    and Gemini vision analysis, so image-based and scanned PDFs are handled.

    Args:
        filename: The PDF filename (e.g. 'contract.pdf') inside the Contracts folder.

    Returns:
        Combined text from pdfplumber extraction and Gemini visual analysis.
    """
    path = os.path.join(CONTRACTS_DIR, filename)
    if not os.path.exists(path):
        return f"Error: File '{filename}' not found in Contracts folder."

    # --- Text layer extraction ---
    text_parts = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {i + 1} ---\n{page_text}")

    text_content = "\n\n".join(text_parts) if text_parts else "(No text layer found)"

    # --- Vision analysis via Gemini Files API ---
    try:
        client = genai.Client()
        uploaded = client.files.upload(
            path=path,
            config={"mime_type": "application/pdf"},
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                uploaded,
                (
                    "Transcribe all content visible in this document in full detail. "
                    "Include all text, tables, dates, values, names, and any content "
                    "embedded in images or scanned sections. Do not summarize — "
                    "reproduce the data as completely as possible."
                ),
            ],
        )
        vision_content = response.text
        client.files.delete(name=uploaded.name)
    except Exception as e:
        vision_content = f"(Vision analysis unavailable: {e})"

    return (
        f"=== TEXT EXTRACTION ===\n{text_content}\n\n"
        f"=== VISION ANALYSIS ===\n{vision_content}"
    )
