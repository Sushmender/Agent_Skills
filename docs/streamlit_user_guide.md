# Streamlit Web UI User Guide — Agent Skills

This guide walks you through all the interactive controls, input options, status panels, and output views available in the **Agent Skills Orchestrator** web interface.

---

## 🎨 Layout Overview

The user interface is divided into two primary zones:
1. **Left Sidebar**: Handles system status indicators and clickable profile buttons for Subagents and Skills.
2. **Main Application Board**: Divided into three tabs:
   - **🔬 Research Console**: The primary workspace for queries, execution triggers, live orchestration logs, and the final synthesized output.
   - **🏗️ Architecture**: Displays the system's technical design and data flow.
   - **📖 About & Skills**: Provides detailed descriptions of how the Agent Skills framework operates.

---

## ⚙️ Interactive Controls (Sidebar)

### 1. System Indicators
*   **API Key Status**: Displays a green `Loaded` banner if your Gemini key is configured in your `.env` file, or a yellow `Missing` warning if you need to provide one.
*   **Notion Integration**: Displays a blue `Connected` banner if a Notion Token is configured in `.env`, or a dark `Offline` banner indicating research will be terminal-only.

### 2. Active Subagents (Clickable Profiles)
*   **What it is**: A list of the active subagents (`docs_researcher`, `repo_analyzer`, `web_researcher`) rendered as interactive buttons.
*   **How to use**: Click any of the subagent buttons. A popup modal dialog will instantly appear over your workspace, displaying the agent's exact System Prompt and designated role.

### 3. Skills Loaded
*   **What it is**: A button indicating how many skill workflows were auto-discovered at startup.
*   **How to use**: Click the button to open a popup modal showing the raw Markdown workflow of every loaded skill (e.g., `learning-a-tool`). 

---

## 🚀 Main Board Actions (Research Console Tab)

### 1. Input Prompt Text Area
*   *What to look for*: The text area labeled *"Research Query"*.
*   *What it does*: Accepts any natural language query. It starts empty by default with shadow placeholders suggesting examples.
*   *Best Queries to Try*:
    - `"Learn FastAPI"` (Triggers the 5-level learning skill)
    - `"Get started with Redis"` (Triggers the learning skill)

### 2. Notion Output Configuration
*   **Save to Notion Checkbox**: Check this box if you want the final synthesized output saved directly to your Notion workspace.
*   **Notion Parent Page ID**: If the checkbox is enabled, a text input appears. Enter the 32-character ID of a parent page in Notion (e.g. `38bfcf1c204e80229d95ec10f8d10391`) that you have shared with your integration. 

### 3. Action Button: 🚀 Start Orchestrator
*   *What it does*: Triggers the asynchronous agent execution run:
    1. Validates your API keys and Notion parameters.
    2. Spawns the main orchestrator agent.
    3. Runs the multi-agent routing loop.

---

## 📊 Outputs & Monitoring

During execution, the Research Console tab displays new widgets dynamically:

### 1. 🚦 Phase Progress Bar
*   Visually tracks the system's progression through **Phase 1: Research**, **Phase 2: Structure**, and **Phase 3: Output**.

### 2. 🕵️ Orchestration Status & Traces
*   **Live Log Console**: A dark terminal-like box that updates in real-time as the orchestrator communicates with the subagents:
    - `[docs_researcher] Running search...`
    - `✨ Phase 3: Synthesizing final output...`

### 3. 📝 Synthesized Output
*   Renders the final synthesized response in a formatted markdown page directly below the console.
*   If the query matched the `learning-a-tool` skill, it outlines the progressive five levels with code examples and resource reference links.
