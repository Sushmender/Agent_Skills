# Contributing to Agent Skills

Thank you for your interest in contributing! This guide explains how to add new skills, fix bugs, or improve the codebase.

---

## Project Overview

Agent Skills is a multi-agent research system built on [Google ADK](https://google.github.io/adk-docs/). The orchestrator reads **Skills** at startup and uses them to structure research workflows. Each skill defines a specific task type (e.g. "learn a tool") and maps research phases to the three specialized subagents.

---

## How to Add a New Skill

Skills live in `skills/<skill-name>/SKILL.md`. The orchestrator auto-discovers and injects them at runtime — no code changes needed.

### Step 1: Create the skill directory

```
skills/
└── my-new-skill/
    ├── SKILL.md
    └── references/       # optional supporting docs
        └── my-reference.md
```

### Step 2: Write SKILL.md

The file must have YAML frontmatter followed by a markdown body:

```markdown
---
name: my-new-skill
description: Brief description of when this skill triggers. Write this clearly — the orchestrator uses it to decide whether to activate the skill.
---

# My New Skill Title

Brief description of what this skill does.

## Workflow

### Phase 1: Research

Describe what to research and from which sources. Map sources to subagents:

- Official Documentation → `docs_researcher`
- Repository / Code → `repo_analyzer`
- Community Content → `web_researcher`

### Phase 2: Structure

How to organize the collected information.

### Phase 3: Output

What the final output should look like (format, file structure, etc.)
```

### Step 3: Test the skill

```powershell
.venv\Scripts\python.exe tests/test_skill.py
```

Or run interactively and type a query that should trigger your skill:

```powershell
.venv\Scripts\python.exe src/agent_skills/agent.py
```

---

## How the Skill System Works

1. On startup, `agent.py` calls `load_skills()` which reads every `skills/*/SKILL.md`
2. The contents are appended to the orchestrator's system prompt under `## Available Skills`
3. The orchestrator uses the `description` in each skill's frontmatter to decide which skill (if any) to activate for a given user query
4. When a skill is activated, the orchestrator follows the skill's workflow precisely, delegating to the appropriate subagents

---

## Code Structure

```
src/agent_skills/
├── agent.py       — Entry point. Loads skills, builds orchestrator, runs REPL loop
├── subagents.py   — Creates the 3 research subagents (docs, repo, web)
└── utils.py       — Terminal display helpers for ADK events

prompts/
├── main_agent.md       — Orchestrator system prompt
├── docs_researcher.md  — Docs subagent prompt
├── repo_analyzer.md    — Repo subagent prompt
└── web_researcher.md   — Web subagent prompt

tests/
├── test_gemini.py  — Verify Gemini API key works
├── test_agent.py   — Full orchestrator + subagent smoke test
├── test_notion.py  — Notion MCP connectivity test
└── test_skill.py   — Skill loading end-to-end test
```

---

## Running Tests

```powershell
# Verify Gemini API
.venv\Scripts\python.exe tests/test_gemini.py

# Full orchestrator smoke test
.venv\Scripts\python.exe tests/test_agent.py

# Notion MCP test (requires NOTION_TOKEN)
.venv\Scripts\python.exe tests/test_notion.py

# Skill loading test
.venv\Scripts\python.exe tests/test_skill.py
```

---

## Modifying Subagents or Prompts

- **Prompts**: Edit the markdown files in `prompts/`. Changes take effect immediately on the next run.
- **Subagents**: Edit `src/agent_skills/subagents.py`. Note: do **not** add custom function tools alongside `google_search` — the Gemini API disallows mixing built-in grounding tools with function declarations in a single request. Keep `disallow_transfer_to_parent=True` and `disallow_transfer_to_peers=True` on all subagents.
- **Orchestrator model**: Change `model=` in `agent.py` and `subagents.py`. Currently `gemini-2.5-flash`.

---

## Conventions

- Python 3.11+, `venv + pip`, no `uv` or other package managers
- All async code uses `asyncio`; no threading
- Keep prompts in `prompts/`, skills in `skills/`, tests in `tests/`
- Do not commit `.env` (it is gitignored)
