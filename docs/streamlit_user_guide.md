# Streamlit Web UI User Guide — Agent Skills

This guide walks you through all the interactive controls, input options, status panels, and output views available in the **Agent Skills Orchestrator** web interface.

---

## 🎨 Layout Overview

The user interface is divided into two primary zones:
1. **Left Sidebar**: Handles API keys, credentials, target integration IDs, and system status indicators.
2. **Main Application Board**: Contains active skill views, the search prompt area, execution triggers, live orchestration logs, and the final synthesized output.

---

## ⚙️ Interactive Controls (Sidebar)

### 1. Credentials Input Overrides
*   **Google Gemini API Key**: 
    - *What it is*: A secure password field.
    - *Initial value*: Automatically loaded from the `GEMINI_API_KEY` parameter in your [.env](file:///c:/Users/susmi/OneDrive/Desktop/Agent_Skills/.env) file.
    - *How to use*: If you want to switch accounts or use a different key, simply paste your Google AI Studio API key here.
*   **Notion Integration Secret (Token)**:
    - *What it is*: A secure password field.
    - *Initial value*: Automatically loaded from the `NOTION_TOKEN` parameter in your [.env](file:///c:/Users/susmi/OneDrive/Desktop/Agent_Skills/.env) file.
    - *How to use*: Enter your Notion Integration Token. If left empty, the application will default to running locally only without exporting to Notion.

### 2. target Configuration
*   **Notion Parent Page ID (Optional)**:
    - *What it is*: A text box for a Notion block or page identifier.
    - *How to use*: Enter the 32-character ID of a parent page in Notion (e.g. `1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d`) that you have shared with your integration. The orchestrator will automatically create a new subpage containing your synthesized guide under this parent page.

### 3. System Indicators
*   **API Key Status**: Displays a green `Loaded` banner if your Gemini key is input, or a yellow `Missing` warning if you need to provide one.
*   **Notion Integration**: Displays a blue `Connected` banner indicating Notion operations are enabled, or a yellow `Offline` banner indicating research will be terminal-only.
*   **Active Subagents Checklist**: Lists the active sub-agents (`docs_researcher`, `repo_analyzer`, `web_researcher`) so you know who is working on the research in the background.

---

## 🚀 Main Board Actions

### 1. Expander: 🎓 Active Skills Extracted at Startup
*   *What to look for*: Click the expander header.
*   *What it does*: Displays the exact parsed contents of all `SKILL.md` files (such as `learning-a-tool`). You can inspect the required research phases, progressive structure, and triggers to align your queries.

### 2. Input Prompt Text Area
*   *What to look for*: The text area labeled *"What programming tool, framework, or library would you like to learn or research?"*.
*   *What it does*: Accepts any natural language query.
*   *Best Queries to Try*:
    - `"Learn FastAPI"` (Triggers the 5-level learning skill)
    - `"Get started with TailwindCSS"` (Triggers the learning skill)
    - `"What is Streamlit? Give me an overview"` (Generates a general synthesized guide)

### 3. Action Button: 🚀 Start Orchestrator
*   *What it does*: Triggers the asynchronous agent execution run:
    1. Boots up the Notion MCP Server subprocess if a Notion Token is configured.
    2. Spawns the main orchestrator agent.
    3. Runs the multi-agent routing loop.

---

## 📊 Outputs & Monitoring

During execution, Streamlit displays new widgets dynamically:

### 1. 🕵️ Orchestration Status & Traces
*   **Status Indicator**: Shows a live progress log (e.g. `🔌 Booting Notion MCP Server...` ➔ `🚀 Running Orchestration...`).
*   **Terminal Event Log**: A dark terminal-like console box that updates in real-time as the orchestrator communicates with the subagents:
    - `🔧 [Main] tool call: transfer_to_agent(agent_name='docs_researcher')`: Shows which subagent is being invoked.
    - `💭 [web_researcher]: Searching for FastAPI...`: Shows active query grounding and subagent reasoning steps.

### 2. 📝 Synthesized Output
*   Renders the final synthesized response in a formatted markdown page.
*   If the query matched the `learning-a-tool` skill, it outlines the progressive five levels with code examples and resource reference links.

### 3. Expander: 📜 View Raw Agent Traces from Last Run
*   *Where it is*: Appears below the output report once execution completes.
*   *What it does*: Lets you scroll through the historical logs of the entire run for debugging or inspect details.
