"""Runs the contract auditor agent headlessly. Intended for daily scheduled execution."""

import asyncio
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
)

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from auditor.agent import root_agent


async def main():
    session_service = InMemorySessionService()
    session = await session_service.create_session(
        app_name="contract_auditor",
        user_id="scheduler",
    )
    runner = Runner(
        agent=root_agent,
        app_name="contract_auditor",
        session_service=session_service,
    )
    async for event in runner.run_async(
        user_id="scheduler",
        session_id=session.id,
        new_message=Content(role="user", parts=[Part(text="Run audit")]),
    ):
        if event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text)


if __name__ == "__main__":
    asyncio.run(main())
