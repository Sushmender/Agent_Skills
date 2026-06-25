import asyncio
import os
import uuid
from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters
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


def load_skills() -> str:
    """
    Scan skills/ directory and return all SKILL.md contents concatenated
    into a section that is injected into the orchestrator's system prompt.
    """
    skills_section = ""
    if not os.path.isdir(SKILLS_DIR):
        return skills_section

    for skill_dir in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, skill_dir, "SKILL.md")
        if os.path.isfile(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            skills_section += f"\n\n---\n## Skill: {skill_dir}\n\n{content}"

    if skills_section:
        skills_section = "## Available Skills" + skills_section

    return skills_section


async def main():
    if not GEMINI_API_KEY:
        print("GEMINI_API_KEY not found. Please add it to your .env file.")
        return

    # Build orchestrator prompt: base prompt + all skills injected
    base_prompt = load_prompt("main_agent.md")
    skills_context = load_skills()
    main_agent_prompt = base_prompt
    if skills_context:
        main_agent_prompt += "\n\n" + skills_context

    subagents = create_subagents(PROMPTS_DIR)

    # Connect to Notion MCP server (requires Node.js + npx installed)
    notion_toolset = None

    if NOTION_TOKEN:
        try:
            notion_toolset = McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="npx",
                        args=["-y", "@notionhq/notion-mcp-server"],
                        env={
                            "OPENAPI_MCP_HEADERS": (
                                f'{{"Authorization": "Bearer {NOTION_TOKEN}", '
                                f'"Notion-Version": "2022-06-28"}}'
                            )
                        },
                    ),
                    timeout=60.0,
                )
            )
            print("Notion MCP toolset created.\n")
        except Exception as e:
            print(f"Warning: Notion MCP setup failed: {e}")
            print("    Continuing without Notion tools.\n")
    else:
        print("Warning: NOTION_TOKEN not set. Skipping Notion MCP.\n")

    try:
        # Main orchestrator agent
        orchestrator = LlmAgent(
            name="orchestrator",
            model="gemini-2.5-flash",
            description="Research orchestrator that delegates tasks to specialized subagents.",
            instruction=main_agent_prompt,
            sub_agents=subagents,
            tools=[notion_toolset] if notion_toolset else [],
        )

        session_service = InMemorySessionService()
        session_id = str(uuid.uuid4())

        runner = Runner(
            agent=orchestrator,
            app_name="agent_skills",
            session_service=session_service,
        )

        # InMemorySessionService requires explicit session creation
        await session_service.create_session(
            app_name="agent_skills",
            user_id="user",
            session_id=session_id,
        )

        print("Agent Skills -- Powered by Gemini ADK")
        print("Type 'exit' to quit\n")

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

    except Exception as e:
        print(f"\nError: {e}")
    finally:
        # Clean up MCP toolset (terminates the npx process)
        if notion_toolset:
            await notion_toolset.close()


if __name__ == "__main__":
    asyncio.run(main())
