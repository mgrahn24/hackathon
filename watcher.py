"""
File watcher that triggers the contract agent when a new PDF is added to Contracts/.

Usage:
    python watcher.py

Requires:
    pip install watchdog
"""

import os
import sys
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

CONTRACTS_DIR = os.path.join(os.path.dirname(__file__), "Contracts")


class ContractHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".pdf"):
            filename = os.path.basename(event.src_path)
            print(f"New contract detected: {filename}")
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

    initial_message = Content(
        role="user",
        parts=[Part(text=f"Please process the contract file: {filename}")]
    )

    print(f"Running extraction for {filename}...")
    async for event in runner.run_async(
        user_id="watcher",
        session_id=session.id,
        new_message=initial_message,
    ):
        if event.content and event.content.parts:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text)


if __name__ == "__main__":
    print(f"Watching {CONTRACTS_DIR} for new PDF files...")
    observer = Observer()
    observer.schedule(ContractHandler(), path=CONTRACTS_DIR, recursive=False)
    observer.start()
    try:
        while True:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
