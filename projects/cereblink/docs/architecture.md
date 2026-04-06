# Architecture

## Overview
CerebLink is a repository-first learning system.
OpenClaw webchat acts as the interaction layer, teaching-policy orchestrator, and persistence coordinator, while Markdown/JSON files act as the state and knowledge layer.

## Teaching Policy Layer
The teaching layer distinguishes between:
- New Learning: search-grounded, shallow-to-deep guided teaching
- Review: answer-first, correction-oriented mastery checking

For new topics, external search is part of lesson preparation when the topic benefits from current or authoritative information.

## Data Flow
1. User starts a study session via webchat
2. System resolves the active `userId`
3. System selects New Learning or Review mode
4. In New Learning, the system performs standard search when needed and synthesizes a short structured explanation
5. In Review, the system asks first and diagnoses the learner answer before correcting
6. Session record persisted to `users/<userId>/sessions/`
7. Mastery tracker updated in `users/<userId>/progress/mastery-tracker.json`
8. Review queue updated in `users/<userId>/reviews/review-queue.json`
9. Today plan regenerated in `users/<userId>/plans/today.md`
10. Learning summary regenerated in `users/<userId>/state/learning-summary.json`

## File Layout
### Shared repository-level files
- `README.md`
- `docs/`
- `templates/`
- `scripts/`
- `tests/`

### User-isolated data
- `users/<userId>/knowledge/` — concept cards (Obsidian-compatible Markdown)
- `users/<userId>/questions/` — high-value question cards
- `users/<userId>/topics/` — topic/MOC pages
- `users/<userId>/sessions/` — per-session learning records
- `users/<userId>/reviews/` — review queue and history
- `users/<userId>/progress/` — mastery tracking state
- `users/<userId>/plans/` — generated study plans
- `users/<userId>/state/` — generated summaries and planning state

### Entry routing
- `state/user-routing.json` defines how entry context maps to a CerebLink user
- Priority: `feishu_open_id` exact match > profile default
- Current defaults:
  - `main` -> `zegang`
  - `feishu2` -> `dengjingjing`
