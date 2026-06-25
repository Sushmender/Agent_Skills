# Agent Skills

A multi-agent research system built with **Google ADK** (Agent Development Kit) and **Gemini 2.5 Flash**, demonstrating agent orchestration, skill-driven workflows, and MCP (Model Context Protocol) integration with Notion.

## What It Does

The system has a **main orchestrator** that reads **Skills** at startup, then receives user queries and delegates work to three specialized research subagents:

| Subagent | Role |
|---|---|
| `docs_researcher` | Searches official documentation |
| `repo_analyzer` | Analyzes GitHub repositories and code |
| `web_researcher` | Finds community articles, tutorials, and videos |

Results are synthesized by the orchestrator and can optionally be saved to a **Notion page** via MCP.

## Demo

```
Agent Skills -- Powered by Gemini ADK
Type 'exit' to quit

You: Learn FastAPI

[Main] Skill detected: learning-a-tool
[Main] transfer_to_agent -> docs_researcher
[docs_researcher] google_search: FastAPI official documentation
[Main] transfer_to_agent -> repo_analyzer
[repo_analyzer] google_search: github.com/tiangolo/fastapi
[Main] transfer_to_agent -> web_researcher
[web_researcher] google_search: FastAPI tutorials community

Agent:
# FastAPI Learning Path

## Level 1: Overview & Motivation
FastAPI is a modern, high-performance Python web framework built on top of
Starlette and Pydantic. It was created to solve the gap between speed of
development and runtime performance...

## Level 2: Installation & Hello World
...
```

## Project Structure

```
agent-skills/
├── src/
│   └── agent_skills/
│       ├── agent.py          # Main orchestrator (entry point)
│       ├── subagents.py      # All 3 subagent definitions
│       └── utils.py          # Terminal display helpers
├── prompts/
│   ├── main_agent.md         # Orchestrator system prompt
│   ├── docs_researcher.md    # Docs subagent prompt
│   ├── repo_analyzer.md      # Repo subagent prompt
│   └── web_researcher.md     # Web subagent prompt
├── skills/
│   └── learning-a-tool/
│       ├── SKILL.md                          # Skill definition & workflow
│       └── references/
│           └── progressive-learning.md       # 5-level learning framework
├── examples/
│   └── queries.md            # Example prompts to try
├── tests/
│   ├── test_gemini.py        # Verify Gemini API key
│   ├── test_agent.py         # Orchestrator + subagent smoke test
│   ├── test_notion.py        # Notion MCP connectivity test
│   └── test_skill.py         # Skill loading end-to-end test
├── docs/
│   └── day-plan.md           # Day-by-day project tracker
├── .env                      # Your API keys (gitignored)
├── .env.example              # Key template
├── CONTRIBUTING.md           # How to add new skills
├── requirements.txt
└── pyproject.toml
```

## Setup

### Prerequisites

- Python 3.11+
- Node.js (required for Notion MCP server via `npx`)

### 1. Clone the Repo

```bash
git clone https://github.com/Sushmender/agent-skills.git
cd agent-skills
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv .venv
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

Edit `.env`:
```
GEMINI_API_KEY=your_gemini_api_key_here
NOTION_TOKEN=your_notion_token_here   # optional
```

#### Getting a Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click **Get API key** → **Create API key**
4. Copy the key into `.env`

#### Getting a Notion Token (Optional)

Required only if you want the agent to write output to Notion pages.

1. Create a free account at [notion.so](https://www.notion.so/signup)
2. Go to [Notion Integrations](https://www.notion.so/my-integrations)
3. Click **New integration**, give it a name, select your workspace
4. Copy the **Internal Integration Secret** into `.env` as `NOTION_TOKEN`
5. Share a Notion page with the integration:
   - Open a page in Notion → **...** menu → **Connections** → add your integration
6. When prompting the agent, include the parent page ID:
   > "Learn FastAPI and save the learning path to Notion page `<page-id>`"

> **Note:** Node.js must be installed for the Notion MCP server. Download from [nodejs.org](https://nodejs.org/).

## Running the Agent

```bash
python src/agent_skills/agent.py
```

Then type your query and press Enter. Try the examples in [`examples/queries.md`](examples/queries.md).

Type `exit` to quit.

## Running Tests

```powershell
# Verify Gemini API key
.venv\Scripts\python.exe tests/test_gemini.py

# Full orchestrator + subagent smoke test
.venv\Scripts\python.exe tests/test_agent.py

# Notion MCP connectivity test (requires NOTION_TOKEN)
.venv\Scripts\python.exe tests/test_notion.py

# Skill loading end-to-end test
.venv\Scripts\python.exe tests/test_skill.py
```

## Skills

Skills define structured, multi-phase workflows for specific task types. The orchestrator auto-discovers all skills in `skills/` at startup and activates the appropriate one when a query matches.

### Available Skills

| Skill | Trigger | Description |
|---|---|---|
| `learning-a-tool` | "learn X", "get started with X" | Creates a 5-level structured learning path for any programming tool |

### How It Works

1. At startup, `agent.py` reads every `skills/*/SKILL.md` and injects the contents into the orchestrator's system prompt
2. The orchestrator activates the matching skill when a user query fits its description
3. The skill's workflow is followed precisely — each research phase is delegated to the right subagent
4. Results are synthesized into the skill's output format

### Adding a New Skill

See [CONTRIBUTING.md](CONTRIBUTING.md) for step-by-step instructions.

## Architecture

```
User Input
    │
    ▼
Orchestrator (gemini-2.5-flash)
    │   reads skills/ at startup
    │   activates skill on matching query
    │   delegates phases to subagents
    │
    ├── docs_researcher  (gemini-2.5-flash + google_search)
    ├── repo_analyzer    (gemini-2.5-flash + google_search)
    └── web_researcher   (gemini-2.5-flash + google_search)
    │
    ▼
Synthesis + Optional Notion MCP output
```

## Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | [Google ADK](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.5 Flash |
| Search | Google Search (built-in ADK grounding tool) |
| MCP Server | [@notionhq/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) |
| Runtime | Python 3.11+ · venv · pip |
