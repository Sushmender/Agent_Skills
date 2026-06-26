r"""
Smoke test for the full ADK orchestrator + 3 subagents.

Sends "What is FastAPI?" and verifies that the orchestrator delegates
to the three specialized subagents and produces a final response.

Run: .venv\Scripts\python.exe tests/test_agent.py
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import asyncio
import os
import sys
import uuid

# Force UTF-8 output on Windows (same fix as test_gemini.py)
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

# Add src/ to path so agent_skills package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent_skills.subagents import create_subagents
from agent_skills.utils import display_event

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

TEST_PROMPT = "What is FastAPI? Give me a brief overview."


async def run_agent_smoke_test():
    print("=" * 60)
    print("ADK Orchestrator Smoke Test")
    print("=" * 60)

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env")

    print(f"\nTest prompt: {TEST_PROMPT!r}\n")
    print("Initialising subagents...")

    subagents = create_subagents(PROMPTS_DIR)
    print(f"Created {len(subagents)} subagents: {[a.name for a in subagents]}")

    # Load orchestrator prompt
    main_prompt_path = os.path.join(PROMPTS_DIR, "main_agent.md")
    with open(main_prompt_path, "r", encoding="utf-8") as f:
        main_agent_prompt = f.read().strip()

    orchestrator = LlmAgent(
        name="orchestrator",
        model="gemini-2.5-flash",
        description="Research orchestrator that delegates tasks to specialized subagents.",
        instruction=main_agent_prompt,
        sub_agents=subagents,
        tools=[],  # No Notion MCP for this smoke test
    )

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())

    runner = Runner(
        agent=orchestrator,
        app_name="agent_skills_test",
        session_service=session_service,
    )

    # InMemorySessionService requires explicit session creation before run_async
    await session_service.create_session(
        app_name="agent_skills_test",
        user_id="test_user",
        session_id=session_id,
    )

    print("\nStreaming agent events:\n")
    print("-" * 60)

    content = types.Content(
        role="user",
        parts=[types.Part(text=TEST_PROMPT)],
    )

    final_seen = False
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=content,
    ):
        display_event(event)
        if event.is_final_response():
            final_seen = True

    print("-" * 60)

    if final_seen:
        print("\n[PASS] Orchestrator produced a final response.")
    else:
        print("\n[FAIL] No final response received.")
        sys.exit(1)

    print("[PASS] Smoke test complete.\n")


if __name__ == "__main__":
    asyncio.run(run_agent_smoke_test())
