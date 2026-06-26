r"""
Smoke test for Notion MCP connectivity.

Connects to the Notion MCP server via npx, then asks the orchestrator
to save a test note — verifying that the Notion integration is live.

Run: .venv\Scripts\python.exe tests/test_notion.py

Prerequisites:
  - NOTION_TOKEN set in .env
  - Node.js + npx installed
  - Notion integration shared with at least one page
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
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters as StdioServerParams
from google.genai import types

from agent_skills.utils import display_event

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")

TEST_MESSAGE = (
    "Please create a new Notion page titled 'Agent Skills - Smoke Test' "
    "with the content: 'Day 2 smoke test passed. Notion MCP is connected and working.'"
)


async def run_notion_smoke_test():
    print("=" * 60)
    print("Notion MCP Smoke Test")
    print("=" * 60)

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env")

    if not NOTION_TOKEN:
        raise ValueError("NOTION_TOKEN not found in .env")

    print("\nCreating Notion MCP toolset...")
    print("(npx will start when the agent first uses a Notion tool)\n")

    # McpToolset is instantiated directly and passed to the agent.
    # The agent framework manages the MCP server lifecycle automatically.
    notion_toolset = McpToolset(
        connection_params=StdioConnectionParams(
            server_params=StdioServerParams(
                command="npx",
                args=["-y", "@notionhq/notion-mcp-server"],
                env={
                    "OPENAPI_MCP_HEADERS": (
                        f'{{"Authorization": "Bearer {NOTION_TOKEN}", '
                        f'"Notion-Version": "2022-06-28"}}'
                    )
                },
            ),
            timeout=60.0,  # Allow 60s for npx to download and start the server
        )
    )

    print(f"Test prompt:\n  {TEST_MESSAGE}\n")

    # Load main agent prompt
    main_prompt_path = os.path.join(PROMPTS_DIR, "main_agent.md")
    with open(main_prompt_path, "r", encoding="utf-8") as f:
        main_agent_prompt = f.read().strip()

    # Orchestrator with Notion toolset — no subagents needed for this test
    orchestrator = LlmAgent(
        name="orchestrator",
        model="gemini-2.5-flash",
        description="Orchestrator with Notion MCP tools.",
        instruction=main_agent_prompt,
        sub_agents=[],
        tools=[notion_toolset],
    )

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())

    runner = Runner(
        agent=orchestrator,
        app_name="notion_mcp_test",
        session_service=session_service,
    )

    # InMemorySessionService requires explicit session creation before run_async
    await session_service.create_session(
        app_name="notion_mcp_test",
        user_id="test_user",
        session_id=session_id,
    )

    print("Streaming agent events:\n")
    print("-" * 60)

    content = types.Content(
        role="user",
        parts=[types.Part(text=TEST_MESSAGE)],
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
        print("\n[PASS] Notion MCP smoke test complete.")
        print("       Check your Notion workspace for the new page.\n")
    else:
        print("\n[FAIL] No final response received.")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(run_notion_smoke_test())
