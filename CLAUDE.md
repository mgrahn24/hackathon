# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Setup

Dependencies are managed via a `.venv` virtual environment. Activate it before running any commands:

```bash
source .venv/Scripts/activate  # Windows (bash)
```

API key goes in `.env`:
```
GOOGLE_API_KEY=...
```

## Running the Agent

```bash
# Browser dev UI (recommended for testing)
adk web .

# Interactive CLI
adk run .
```

Then open `http://localhost:8000`.

## Architecture

This is a **Google ADK** (Agent Development Kit) project using `gemini-2.5-flash`.

ADK requires agents to live in a **subfolder package** under the working directory. Each agent package must have:
- `__init__.py` — exports `root_agent`
- `agent.py` — defines `root_agent` as an `Agent` instance

Current agents:
- `assistant/` — general-purpose assistant agent

To add a new agent, create a new subfolder with the same `__init__.py` + `agent.py` pattern. ADK will auto-discover it when running `adk web .` from the project root.

## Key ADK Concepts

- **`Agent`** — single LLM agent with optional `tools`
- **`LlmAgent`** — alias for `Agent`, used in multi-agent setups with `sub_agents`
- Tools are passed as a list to the `tools=` parameter
- Multi-agent coordination is done by assigning `sub_agents` to a parent/coordinator agent
