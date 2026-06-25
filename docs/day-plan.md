# 📅 Day-by-Day Task Tracker

**Project**: Agent Skills — Google ADK (Gemini) + Notion MCP  
**Repo**: https://github.com/Sushmender/agent-skills

---

## ✅ Day 1 — Project Structure, Migration & First Git Push

### 1.1 Folder Structure
- [x] Create `src/agent_skills/` package
- [x] Create `skills/learning-a-tool/` (migrated from `.claude/skills/`)
- [x] Create `docs/` directory with day plan

### 1.2 File Migration & Rewrites
- [x] Write `src/agent_skills/__init__.py`
- [x] Write `src/agent_skills/agent.py` — Gemini ADK orchestrator
- [x] Write `src/agent_skills/subagents.py` — 3 subagents with ADK `LlmAgent`
- [x] Write `src/agent_skills/utils.py` — ADK event display (no Claude SDK)
- [x] Move `SKILL.md` → `skills/learning-a-tool/SKILL.md`
- [x] Move `progressive-learning.md` → `skills/learning-a-tool/references/`
- [x] Rewrite `README.md` for Gemini ADK + venv setup

### 1.3 Config & Dependencies
- [x] Create `requirements.txt` (`google-adk`, `python-dotenv`)
- [x] Update `pyproject.toml` (removed `claude-agent-sdk`)
- [x] Create `.env` (empty — paste keys here)
- [x] Create `.env.example` (key template)
- [x] Create `.gitignore`

### 1.4 Cleanup
- [x] Delete old root `agent.py`
- [x] Delete old root `utils.py`
- [x] Delete old root `main.py`
- [x] Delete `.claude/` directory
- [x] Delete `uv.lock`

### 1.5 Git Push
- [ ] `git init`
- [ ] `git add .`
- [ ] `git commit -m "feat: initial structure with Gemini ADK migration"`
- [ ] Create GitHub repo: `agent-skills`
- [ ] `git remote add origin https://github.com/Sushmender/agent-skills.git`
- [ ] `git push -u origin main`

---

## [x] Day 2 — Notion MCP + Smoke Testing

### 2.1 Environment Setup
- [x] `python -m venv .venv` + activate
- [x] `pip install -r requirements.txt` (added `mcp>=1.0.0`)
- [x] `GEMINI_API_KEY` confirmed working in `.env`
- [x] `NOTION_TOKEN` confirmed working in `.env`
- [x] Notion integration connected via MCP

### 2.2 Validation
- [x] `test_gemini.py` passes — Gemini API (gemini-2.5-flash) works
- [x] `test_agent.py` passes — ADK orchestrator + 3 subagents spawn and respond
- [x] Asked "What is FastAPI?" — `web_researcher` delegated and returned full response
- [x] `test_notion.py` passes — Notion MCP connects, `API-post-page` tool called successfully

### 2.3 Git Push
- [ ] `git commit -m "feat: notion mcp and subagent smoke tests"`
- [ ] `git push`

---

## [x] Day 3 — End-to-End Flow + Final Polish

### 3.1 Skill Loading
- [x] `"Learn FastAPI"` triggers `learning-a-tool` skill workflow
- [x] All 3 subagents delegated to (docs_researcher, repo_analyzer, web_researcher)
- [x] Structured 5-level learning path returned in response

### 3.2 Code Polish
- [x] Error handling for missing `.env` keys (in agent.py)
- [x] All prompts reviewed and working correctly with gemini-2.5-flash
- [x] Fixed google_search + transfer_to_agent conflict (disallow_transfer flags)
- [x] Updated MCP toolset to new McpToolset + StdioConnectionParams API

### 3.3 Documentation (Final)
- [x] Updated `README.md` with demo output, structure, test commands
- [x] Added `CONTRIBUTING.md` (how to add new skills)
- [x] Added `examples/queries.md` with sample prompts

### 3.4 Final Git Push
- [x] `git commit -m "feat: end-to-end learning skill with notion output"`
- [x] `git tag v0.1.0`
- [x] `git push && git push --tags`

---

## 📝 Decisions Log

| Date | Decision |
|------|----------|
| Day 1 | Replaced `claude-agent-sdk` with `google-adk` (Gemini ADK) |
| Day 1 | Switched from `uv` to `python venv + pip` |
| Day 1 | Skills moved from `.claude/skills/` → `skills/` |
| Day 1 | Repo name: `agent-skills` on github.com/Sushmender |
| Day 2 | Switched gemini-2.0-flash → gemini-2.5-flash (free tier quota) |
| Day 2 | Added disallow_transfer_to_parent/peers=True on subagents (google_search conflict) |
| Day 2 | Updated MCPToolset.from_server() → McpToolset + StdioConnectionParams (new API) |
| Day 3 | Skill loading: SKILL.md files auto-discovered and injected into orchestrator prompt |
| Day 3 | tests/ un-gitignored — smoke tests are project artifacts, not throwaway scripts |
| Day 3 | Released v0.1.0 |
