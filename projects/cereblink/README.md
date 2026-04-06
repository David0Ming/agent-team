# CerebLink（脑机接口）

## Goal
A personal AI learning tutor for RAG, Agent, and workflow automation.

## Knowledge Card Storage
The live knowledge-card system is stored in `/home/mzg/文档/Obsidian Vault/cereblink`.
The `projects/cereblink/` directory in this workspace is used as a project copy and should be treated as a synchronized mirror unless a task explicitly targets the workspace version.

## Multi-user Isolation
CerebLink now uses per-user roots under `users/<userId>/` for live data and the workspace mirror.
Current users:
- `users/zegang/` — 泽钢
- `users/dengjingjing/` — 邓菁菁

User-isolated data includes:
- `knowledge/`
- `questions/`
- `topics/`
- `sessions/`
- `reviews/`
- `progress/`
- `plans/`
- `state/`

Shared project metadata stays at repository root, such as `README.md`, `docs/`, `templates/`, and scripts.

## Default Closed Loop
For CerebLink learning tasks, the default workflow is:
1. Finish one explicit learning goal
2. Extract stable takeaways instead of saving raw dialogue
3. Convert them into concept cards and/or question cards
4. Save cards into the active user root under `/home/mzg/文档/Obsidian Vault/cereblink/users/<userId>/`
5. Keep `projects/cereblink/users/<userId>/` synchronized when needed
6. Commit and push the Obsidian `cereblink` vault to GitHub

This is the default persistence loop even when a future session starts without conversational memory.

## Current Milestones
- Milestone A: usable study loop
- Milestone B: Obsidian-native knowledge cards
- Milestone C: dashboards and polish

## Quick Start
```bash
python3 projects/cereblink/scripts/init_cereblink.py
pytest projects/cereblink/tests -v
```
