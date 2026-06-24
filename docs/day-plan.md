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

## ⬜ Day 2 — Notion MCP + Smoke Testing

### 2.1 Environment Setup
- [ ] `python -m venv .venv` + activate
- [ ] `pip install -r requirements.txt`
- [ ] Paste `GEMINI_API_KEY` into `.env`
- [ ] Create Notion integration → paste `NOTION_TOKEN`
- [ ] Share Notion pages with the integration

### 2.2 Validation
- [ ] `python src/agent_skills/agent.py` starts without errors
- [ ] Notion MCP connects (✅ message in terminal)
- [ ] Ask "What is FastAPI?" → 3 subagents spawn and respond
- [ ] Test Notion write: "Save this to Notion" → page created

### 2.3 Git Push
- [ ] `git commit -m "feat: notion mcp and subagent smoke tests"`
- [ ] `git push`

---

## ⬜ Day 3 — End-to-End Flow + Final Polish

### 3.1 Skill Loading
- [ ] Test `"Learn FastAPI"` → triggers `learning-a-tool` skill workflow
- [ ] All 3 subagents run in parallel and return structured results
- [ ] Output written to Notion page via MCP

### 3.2 Code Polish
- [ ] Error handling for missing `.env` keys (already done in agent.py)
- [ ] Review and tighten all prompts for ADK

### 3.3 Documentation (Final)
- [ ] Update `README.md` with actual run output / demo flow
- [ ] Add `CONTRIBUTING.md` (how to add new skills)
- [ ] Add `examples/` folder with sample queries

### 3.4 Final Git Push
- [ ] `git commit -m "feat: end-to-end learning skill with notion output"`
- [ ] `git tag v0.1.0`
- [ ] `git push && git push --tags`

---

## 📝 Decisions Log

| Date | Decision |
|------|----------|
| Day 1 | Replaced `claude-agent-sdk` with `google-adk` (Gemini ADK) |
| Day 1 | Switched from `uv` to `python venv + pip` |
| Day 1 | Skills moved from `.claude/skills/` → `skills/` |
| Day 1 | Repo name: `agent-skills` on github.com/Sushmender |
