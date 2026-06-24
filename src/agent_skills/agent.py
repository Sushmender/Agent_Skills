import asyncio
import os
import uuid
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, StdioServerParameters
from google.genai import types

from agent_skills.subagents import create_subagents
from agent_skills.utils import display_event

load_dotenv()

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# Resolve paths relative to this file
_SRC_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROMPTS_DIR = os.path.join(_SRC_DIR, "prompts")
SKILLS_DIR = os.path.join(_SRC_DIR, "skills")


def load_prompt(filename: str) -> str:
    """Load a prompt from the prompts directory."""
    prompt_path = os.path.join(PROMPTS_DIR, filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


async def main():
    if not GEMINI_API_KEY:
        print("❌  GEMINI_API_KEY not found. Please add it to your .env file.")
        return

    main_agent_prompt = load_prompt("main_agent.md")
    subagents = create_subagents(PROMPTS_DIR)

    # Connect to Notion MCP server (requires Node.js + npx installed)
    notion_tools = []
    exit_stack = None

    if NOTION_TOKEN:
        try:
            notion_tools, exit_stack = await MCPToolset.from_server(
                connection_params=StdioServerParameters(
                    command="npx",
                    args=["-y", "@notionhq/notion-mcp-server"],
                    env={
                        "OPENAPI_MCP_HEADERS": (
                            f'{{"Authorization": "Bearer {NOTION_TOKEN}", '
                            f'"Notion-Version": "2022-06-28"}}'
                        )
                    },
                )
            )
            print("✅  Notion MCP server connected.\n")
        except Exception as e:
            print(f"⚠️   Notion MCP failed to connect: {e}")
            print("    Continuing without Notion tools.\n")
    else:
        print("⚠️   NOTION_TOKEN not set. Skipping Notion MCP.\n")

    try:
        # Main orchestrator agent
        orchestrator = LlmAgent(
            name="orchestrator",
            model="gemini-2.0-flash",
            description="Research orchestrator that delegates tasks to specialized subagents.",
            instruction=main_agent_prompt,
            sub_agents=subagents,
            tools=notion_tools,
        )

        session_service = InMemorySessionService()
        session_id = str(uuid.uuid4())

        runner = Runner(
            agent=orchestrator,
            app_name="agent_skills",
            session_service=session_service,
        )

        print("🤖  Agent Skills — Powered by Gemini ADK")
        print("    Type 'exit' to quit\n")

        while True:
            try:
                user_input = input("\033[1mYou\033[0m: ")
            except (KeyboardInterrupt, EOFError):
                print("\nExiting...")
                break

            print("")
            if user_input.strip().lower() == "exit":
                break
            if not user_input.strip():
                continue

            content = types.Content(
                role="user",
                parts=[types.Part(text=user_input)]
            )

            async for event in runner.run_async(
                user_id="user",
                session_id=session_id,
                new_message=content,
            ):
                display_event(event)

    finally:
        # Clean up MCP server connection
        if exit_stack:
            await exit_stack.aclose()


if __name__ == "__main__":
    asyncio.run(main())
