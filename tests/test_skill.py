r"""
Smoke test for the learning-a-tool skill workflow.

Sends "Learn FastAPI" to the orchestrator, which should:
1. Detect the learning-a-tool skill from its injected prompt
2. Delegate to docs_researcher, repo_analyzer, and web_researcher
3. Return a structured 5-level learning path response

Run: .venv\Scripts\python.exe tests/test_skill.py
"""
import asyncio
import os
import sys
import uuid

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent_skills.subagents import create_subagents
from agent_skills.utils import display_event

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "..", "prompts")
SKILLS_DIR = os.path.join(os.path.dirname(__file__), "..", "skills")

TEST_PROMPT = "Learn FastAPI"


def load_prompt(filename: str) -> str:
    path = os.path.join(PROMPTS_DIR, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read().strip()


def load_skills() -> str:
    """Load all SKILL.md files and inject into orchestrator prompt."""
    section = ""
    if not os.path.isdir(SKILLS_DIR):
        return section
    for skill_dir in sorted(os.listdir(SKILLS_DIR)):
        skill_path = os.path.join(SKILLS_DIR, skill_dir, "SKILL.md")
        if os.path.isfile(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            section += f"\n\n---\n## Skill: {skill_dir}\n\n{content}"
    if section:
        section = "## Available Skills" + section
    return section


async def run_skill_test():
    print("=" * 60)
    print("Skill Loading Test: learning-a-tool")
    print("=" * 60)

    if not GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY not found in .env")

    base_prompt = load_prompt("main_agent.md")
    skills_context = load_skills()
    main_agent_prompt = base_prompt
    if skills_context:
        main_agent_prompt += "\n\n" + skills_context
        print(f"\nSkills loaded: {[d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]}")
    else:
        print("\n[WARN] No skills found in skills/")

    print(f"\nTest prompt: {TEST_PROMPT!r}\n")

    subagents = create_subagents(PROMPTS_DIR)

    orchestrator = LlmAgent(
        name="orchestrator",
        model="gemini-2.5-flash",
        description="Research orchestrator that delegates tasks to specialized subagents.",
        instruction=main_agent_prompt,
        sub_agents=subagents,
        tools=[],
    )

    session_service = InMemorySessionService()
    session_id = str(uuid.uuid4())

    runner = Runner(
        agent=orchestrator,
        app_name="skill_test",
        session_service=session_service,
    )

    await session_service.create_session(
        app_name="skill_test",
        user_id="test_user",
        session_id=session_id,
    )

    print("Streaming agent events:\n")
    print("-" * 60)

    content = types.Content(
        role="user",
        parts=[types.Part(text=TEST_PROMPT)],
    )

    final_seen = False
    agents_used = set()
    async for event in runner.run_async(
        user_id="test_user",
        session_id=session_id,
        new_message=content,
    ):
        display_event(event)
        # Track which agents participated
        author = getattr(event, "author", None)
        if author:
            agents_used.add(author)
        if event.is_final_response():
            final_seen = True

    print("-" * 60)
    print(f"\nAgents involved: {sorted(agents_used)}")

    if final_seen:
        print("[PASS] Skill test complete — orchestrator produced final response.")
    else:
        print("[FAIL] No final response received.")
        sys.exit(1)

    # Check that at least one researcher subagent was used
    research_agents = {"docs_researcher", "repo_analyzer", "web_researcher"}
    used_researchers = agents_used & research_agents
    if used_researchers:
        print(f"[PASS] Research subagents used: {sorted(used_researchers)}")
    else:
        print("[WARN] No research subagents were invoked (orchestrator answered directly).")

    print()


if __name__ == "__main__":
    asyncio.run(run_skill_test())
