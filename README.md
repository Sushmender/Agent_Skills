# Agent Skills

A multi-agent research system built with **Google ADK** (Agent Development Kit) and **Gemini**, demonstrating agent orchestration, subagent delegation, and MCP (Model Context Protocol) integration with Notion.

## What It Does

The system has a **main orchestrator** that receives user queries and delegates work to three specialized subagents running in parallel:

| Subagent | Role |
|---|---|
| `docs_researcher` | Searches official documentation |
| `repo_analyzer` | Analyzes GitHub repositories |
| `web_researcher` | Finds community articles, tutorials, and videos |

Results are synthesized by the orchestrator and can optionally be saved to a **Notion page** via MCP.

## Project Structure

```
agent-skills/
├── src/
│   └── agent_skills/
│       ├── __init__.py
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
├── docs/
│   └── day-plan.md           # Day-by-day project tracker
├── .env                      # Your API keys (gitignored)
├── .env.example              # Key template
├── .gitignore
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
5. Share your Notion pages with the integration:
   - Open the page in Notion → **...** menu → **Connections** → add your integration

> **Note:** Node.js must be installed for the Notion MCP server. Download from [nodejs.org](https://nodejs.org/).

## Running the Agent

```bash
python src/agent_skills/agent.py
```

Then type your query and press Enter. The orchestrator will delegate to subagents and synthesize a response.

```
🤖  Agent Skills — Powered by Gemini ADK
    Type 'exit' to quit

You: Learn FastAPI
[Main] 🔧 transfer_to_agent → docs_researcher
[docs_researcher] 🔧 google_search ...
[web_researcher] 🔧 google_search ...
Agent: Here is your FastAPI learning path...
```

Type `exit` to quit.

## Skills

Skills define structured workflows for specific tasks. The agent automatically uses a skill when your query matches.

### Available Skills

| Skill | Trigger | Description |
|---|---|---|
| `learning-a-tool` | "learn X", "get started with X" | Creates a 5-level learning path for any programming tool |

The `learning-a-tool` skill:
1. Spawns all 3 subagents in parallel to research official docs, the repo, and community content
2. Structures findings into 5 progressive levels (Overview → Next Steps)
3. Outputs a learning path (optionally saved to Notion)

## Architecture

```
User Input
    │
    ▼
Orchestrator (gemini-2.0-flash)
    │── reads skill from skills/
    │── delegates to subagents
    │
    ├── docs_researcher  (gemini-2.0-flash + google_search)
    ├── repo_analyzer    (gemini-2.0-flash + google_search)
    └── web_researcher   (gemini-2.0-flash + google_search)
    │
    ▼
Synthesis + Optional Notion MCP output
```

## Tech Stack

| Component | Technology |
|---|---|
| Agent Framework | [Google ADK](https://google.github.io/adk-docs/) |
| LLM | Gemini 2.0 Flash |
| MCP Server | [@notionhq/notion-mcp-server](https://github.com/makenotion/notion-mcp-server) |
| Runtime | Python 3.11+ · venv · pip |
