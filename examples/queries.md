# Example Queries

A collection of example prompts that demonstrate what Agent Skills can do.

---

## Learning a Tool (Skill: `learning-a-tool`)

These queries trigger the **learning-a-tool** skill and produce a 5-level structured learning path.

```
Learn FastAPI
```

```
Get started with SQLModel
```

```
Help me understand LangChain
```

```
Learn Redis
```

```
I want to learn Kubernetes
```

---

## General Research (No Skill)

General research questions that the orchestrator handles without a specific skill.

```
What is the difference between FastAPI and Flask?
```

```
How does async/await work in Python?
```

```
What are the best practices for structuring a Python project?
```

```
Compare Pydantic v1 and v2
```

---

## Notion Output

Add "save this to Notion" or "write to Notion" to have the result saved as a Notion page (requires `NOTION_TOKEN` and a shared parent page).

```
Learn Docker and save the learning path to Notion
```

```
What is Terraform? Save a summary to my Notion page.
```

---

## Tips

- The agent streams its work in real time — you'll see `[Main]`, `[docs_researcher]`, etc. as subagents run
- Type `exit` to quit the REPL
- Each session remembers conversation history (within a single run)
