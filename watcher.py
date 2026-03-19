"""
File watcher that triggers the contract extractor when a new PDF is added to Contracts/.

Usage:
    python watcher.py

Requires:
    pip install watchdog
"""

import asyncio
import logging
import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s — %(message)s",
)
log = logging.getLogger(__name__)

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "Contracts")

HEADLESS_PROMPT = (
    "Process the contract file: {filename}\n\n"
    "IMPORTANT: This is a headless automated run. Do NOT ask the user for missing fields. "
    "Extract everything you can from the PDF. For any fields you cannot find, set them to null. "
    "Call write_contract_metadata() with whatever you have extracted and then stop."
)


class ContractHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".pdf"):
            filename = os.path.basename(event.src_path)
            log.info("New PDF detected: %s", filename)
            asyncio.run(process_contract(filename))


async def process_contract(filename: str):
    from google.adk.runners import Runner
    from google.adk.sessions import InMemorySessionService
    from google.genai.types import Content, Part
    from assistant.agent import root_agent

    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="contract_watcher",
        user_id="watcher",
    )
    runner = Runner(
        agent=root_agent,
        app_name="contract_watcher",
        session_service=session_service,
    )

    log.info("Starting extraction for: %s", filename)
    message = Content(
        role="user",
        parts=[Part(text=HEADLESS_PROMPT.format(filename=filename))],
    )

    async for event in runner.run_async(
        user_id="watcher",
        session_id=session.id,
        new_message=message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    log.info("[agent] %s", part.text.strip())

    log.info("Extraction complete for: %s", filename)


if __name__ == "__main__":
    log.info("Watching %s for new PDF files...", CONTRACTS_DIR)
    observer = Observer()
    observer.schedule(ContractHandler(), path=CONTRACTS_DIR, recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
