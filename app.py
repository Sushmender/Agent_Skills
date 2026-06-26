import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import asyncio
import os
import sys
import uuid
import streamlit as st
from dotenv import load_dotenv

# Add src/ to path so agent_skills package is importable
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from google.adk.agents import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset, StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_session_manager import StdioServerParameters
from google.genai import types

from agent_skills.agent import load_prompt, load_skills
from agent_skills.subagents import create_subagents

# Load local environment variables
load_dotenv()

# Streamlit Page Configuration
st.set_page_config(
    page_title="Agent Skills Orchestrator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Sleek UI Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif;
    }
    
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #FF4B4B, #4776E6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        font-size: 1.1rem;
        color: #888888;
        margin-bottom: 2rem;
    }
    
    .status-log {
        background-color: #1e1e1e;
        border-radius: 8px;
        padding: 10px;
        font-family: 'Courier New', Courier, monospace;
        font-size: 0.9rem;
        color: #d4d4d4;
        max-height: 300px;
        overflow-y: auto;
        border-left: 4px solid #4776E6;
        margin-bottom: 15px;
    }
    
    .metric-card {
        background-color: #262730;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #444;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.markdown('<div class="main-title">🤖 Agent Skills Orchestrator</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">A multi-agent research framework powered by Google ADK & Gemini 2.5 Flash</div>', unsafe_allow_html=True)

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("## ⚙️ Configuration")

# Get credentials from .env
env_gemini_key = os.environ.get("GEMINI_API_KEY", "")
env_notion_token = os.environ.get("NOTION_TOKEN", "")

# Allow dynamic overrides in the UI
gemini_key = st.sidebar.text_input(
    "Google Gemini API Key",
    value=env_gemini_key,
    type="password",
    help="Google AI Studio API Key. If left empty, the app will fail to run."
)

notion_token = st.sidebar.text_input(
    "Notion Integration Secret (Token)",
    value=env_notion_token,
    type="password",
    help="Notion Integration Token to write results back to Notion."
)

notion_page_id = st.sidebar.text_input(
    "Notion Parent Page ID (Optional)",
    value="",
    placeholder="e.g. 1a2b3c4d5e...",
    help="Optional parent page ID to guide Notion page creation."
)

st.sidebar.divider()
st.sidebar.markdown("### 🚦 Integration Status")

if gemini_key:
    st.sidebar.success("Gemini API Key: Loaded")
else:
    st.sidebar.warning("Gemini API Key: Missing")

if notion_token:
    st.sidebar.info("Notion Integration: Connected")
else:
    st.sidebar.warning("Notion Integration: Offline (Local Only)")

st.sidebar.divider()
st.sidebar.markdown("### 👥 Active Subagents")
st.sidebar.markdown("- 🌐 **docs_researcher** (Documentation)")
st.sidebar.markdown("- 💻 **repo_analyzer** (Code / Repository)")
st.sidebar.markdown("- 💬 **web_researcher** (Community / Web)")

# ----------------- MAIN VIEW -----------------

# Display active skills loaded from directories
skills_context = load_skills()
with st.expander("🎓 Active Skills Extracted at Startup"):
    if skills_context:
        st.markdown(skills_context)
    else:
        st.info("No custom skills discovered in skills/ folder.")

# Query input
user_query = st.text_area(
    "What programming tool, framework, or library would you like to learn or research?",
    value="Learn FastAPI",
    height=70,
    help="Try queries like 'Learn FastAPI' or 'Get started with Streamlit' to trigger specific skills."
)

execute_btn = st.button("🚀 Start Orchestrator", use_container_width=True)

# Event logging display list
if "log_messages" not in st.session_state:
    st.session_state.log_messages = []
if "final_report" not in st.session_state:
    st.session_state.final_report = ""

async def execute_orchestrator(query, g_key, n_token, n_page_id, status_container, status_box, report_box):
    st.session_state.log_messages = []
    st.session_state.final_report = ""
    
    # Temporarily set environment key for Google ADK client
    os.environ["GEMINI_API_KEY"] = g_key
    
    # 1. Base instructions and loaded skills compilation
    base_prompt = load_prompt("main_agent.md")
    skills_context = load_skills()
    main_agent_prompt = base_prompt
    if skills_context:
        main_agent_prompt += "\n\n" + skills_context
        
    prompts_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "prompts")
    subagents = create_subagents(prompts_dir)
    
    # 2. Notion MCP Server lifecycle management
    notion_toolset = None
    if n_token:
        status_box.write("🔌 Booting Notion MCP Server...")
        try:
            notion_toolset = McpToolset(
                connection_params=StdioConnectionParams(
                    server_params=StdioServerParameters(
                        command="npx",
                        args=["-y", "@notionhq/notion-mcp-server"],
                        env={
                            "OPENAPI_MCP_HEADERS": (
                                f'{{"Authorization": "Bearer {n_token}", '
                                f'"Notion-Version": "2022-06-28"}}'
                            )
                        },
                    ),
                    timeout=60.0,
                )
            )
            status_box.write("✅ Notion MCP Server connected successfully.")
        except Exception as e:
            status_box.write(f"⚠️ Warning: Notion MCP initialization failed: {e}")
            
    # Assemble orchestrator agent
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
        app_name="streamlit_skills",
        session_service=session_service,
    )
    
    await session_service.create_session(
        app_name="streamlit_skills",
        user_id="streamlit_user",
        session_id=session_id,
    )
    
    # Adjust query with Notion page if provided
    modified_query = query
    if n_page_id and n_token:
        modified_query += f" and save the learning path to Notion page '{n_page_id}'"
        
    content = types.Content(
        role="user",
        parts=[types.Part(text=modified_query)]
    )
    
    status_box.write("🚀 Running Orchestration...")
    
    # Listen to asynchronous streaming events
    try:
        async for event in runner.run_async(
            user_id="streamlit_user",
            session_id=session_id,
            new_message=content,
        ):
            author = getattr(event, "author", "unknown")
            label = "[Main]" if author == "orchestrator" else f"[{author}]"
            
            # Show tool calls
            if hasattr(event, "get_function_calls"):
                for fc in event.get_function_calls():
                    msg = f"🔧 {label} tool call: {fc.name}({fc.args})"
                    st.session_state.log_messages.append(msg)
                    status_container.markdown(
                        f'<div class="status-log">{"<br>".join(st.session_state.log_messages)}</div>', 
                        unsafe_allow_html=True
                    )
            
            # Show final report
            if event.is_final_response():
                if event.content and event.content.parts:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            st.session_state.final_report += part.text
                            report_box.markdown(st.session_state.final_report)
                            
            # Show intermediate updates
            elif event.content and event.content.parts:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text and part.text.strip():
                        # Truncate long lines for log preview
                        preview = part.text.strip()[:100] + "..." if len(part.text.strip()) > 100 else part.text.strip()
                        msg = f"💭 {label}: {preview}"
                        st.session_state.log_messages.append(msg)
                        status_container.markdown(
                            f'<div class="status-log">{"<br>".join(st.session_state.log_messages)}</div>', 
                            unsafe_allow_html=True
                        )
    except Exception as e:
        st.error(f"Execution Error: {e}")
        status_box.write(f"❌ Execution failed: {e}")
    finally:
        if notion_toolset:
            status_box.write("🔌 Terminating Notion MCP Server Connection...")
            await notion_toolset.close()
            status_box.write("✅ Terminated Notion connection.")

# Button click handler
if execute_btn:
    if not gemini_key:
        st.error("Please provide a valid Google Gemini API Key in the sidebar config panel.")
    else:
        # Containers for streaming updates
        st.subheader("🕵️ Orchestration Status & Traces")
        status_box = st.empty()
        status_container = st.empty()
        
        st.subheader("📝 Synthesized Output")
        report_box = st.empty()
        
        # Streamlit runner entry-point for async function
        asyncio.run(execute_orchestrator(
            user_query,
            gemini_key,
            notion_token,
            notion_page_id,
            status_container,
            status_box,
            report_box
        ))
        
        # Mark as complete
        status_box.write("✨ **Orchestration Complete!** View the synthesized output below.")

# If query was already run and stored in state, show it
elif st.session_state.final_report:
    st.subheader("📝 Synthesized Output")
    st.markdown(st.session_state.final_report)
    
    with st.expander("📜 View Raw Agent Traces from Last Run"):
        st.markdown(
            f'<div class="status-log">{"<br>".join(st.session_state.log_messages)}</div>', 
            unsafe_allow_html=True
        )
