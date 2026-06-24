import os
from google.adk.agents import LlmAgent
from google.adk.tools import google_search


def load_prompt(prompts_dir: str, filename: str) -> str:
    """Load a prompt from the given directory."""
    prompt_path = os.path.join(prompts_dir, filename)
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read().strip()


def create_subagents(prompts_dir: str) -> list[LlmAgent]:
    """
    Create and return all specialized subagents.

    Each subagent is an LlmAgent with:
    - A focused description the orchestrator uses for routing
    - A system prompt loaded from the prompts/ directory
    - Appropriate tools for its role
    """

    # --- Docs Researcher ---
    # Finds and extracts information from official documentation sources.
    docs_researcher = LlmAgent(
        name="docs_researcher",
        model="gemini-2.0-flash",
        description=(
            "Finds and extracts information from official documentation sources. "
            "Use for questions about official APIs, guides, or reference material."
        ),
        instruction=load_prompt(prompts_dir, "docs_researcher.md"),
        tools=[google_search],
    )

    # --- Repo Analyzer ---
    # Analyzes GitHub repositories for structure, examples, and implementation details.
    repo_analyzer = LlmAgent(
        name="repo_analyzer",
        model="gemini-2.0-flash",
        description=(
            "Analyzes code repositories for structure, examples, and implementation "
            "details. Use when the user wants to understand how a project is built."
        ),
        instruction=load_prompt(prompts_dir, "repo_analyzer.md"),
        tools=[google_search],
    )

    # --- Web Researcher ---
    # Finds community articles, videos, tutorials, and discussions.
    web_researcher = LlmAgent(
        name="web_researcher",
        model="gemini-2.0-flash",
        description=(
            "Finds articles, videos, tutorials, and community discussions. "
            "Use for community content, comparisons, and real-world use cases."
        ),
        instruction=load_prompt(prompts_dir, "web_researcher.md"),
        tools=[google_search],
    )

    return [docs_researcher, repo_analyzer, web_researcher]
