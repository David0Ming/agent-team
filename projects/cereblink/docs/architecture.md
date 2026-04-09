# Architecture

## Overview
CerebLink is a repository-first learning system.
OpenClaw webchat acts as the interaction layer, teaching-policy orchestrator, and persistence coordinator, while Markdown/JSON files act as the state and knowledge layer.

## Teaching Policy Layer
The teaching layer distinguishes between:
- New Learning: search-grounded, shallow-to-deep guided teaching
- Review: answer-first, correction-oriented mastery checking

For new topics, external search is part of lesson preparation when the topic benefits from current or authoritative information.

## Knowledge Capture Principles
CerebLink should persist stable learning value rather than raw conversation dump.
When a round is worth saving, the preferred abstraction is:
- real problem encountered
- why the problem matters
- industry-validated method
- transferable capability

This keeps cards reusable across future learning, product work, and system design, instead of storing one-off narrative notes.

## Data Flow
1. User starts a study session via webchat
2. System resolves the active `userId`
3. System reads `users/<userId>/state/learning-profile.json` first when present, then reads current working state such as `learning-summary.json`, `today.md`, and `review-queue.json`
4. System selects New Learning or Review mode
5. In New Learning, the system performs standard search when needed and synthesizes a short structured explanation
6. In Review, the system asks first and diagnoses the learner answer before correcting
7. Session record persisted to `users/<userId>/sessions/`
8. Mastery tracker updated in `users/<userId>/progress/mastery-tracker.json`
9. Review queue updated in `users/<userId>/reviews/review-queue.json`
10. Today plan regenerated in `users/<userId>/plans/today.md`
11. Learning summary regenerated in `users/<userId>/state/learning-summary.json`
12. When a completed round produces stable new user-level learning direction, the system should also attempt to update `users/<userId>/state/learning-profile.json`

## File Layout
### Shared repository-level files
- `README.md`
- `docs/`
- `templates/`
- `scripts/`
- `tests/`

### User-isolated data
- `users/<userId>/knowledge/` — concept cards (Obsidian-compatible Markdown, strongly structured)
- `users/<userId>/questions/` — high-value question cards
- `users/<userId>/topics/` — topic/MOC pages
- `users/<userId>/sessions/` — per-session learning records
- `users/<userId>/reviews/` — review queue and history
- `users/<userId>/progress/` — mastery tracking state
- `users/<userId>/plans/` — generated study plans
- `users/<userId>/state/` — generated summaries and planning state
  - `learning-profile.json` = stable user learning profile / default domain / long-term mainline
  - `learning-summary.json` = current stage summary / short-horizon working state

### Entry routing
- `state/user-routing.json` defines how entry context maps to a CerebLink user
- Priority: `feishu_open_id` exact match > profile default
- Current defaults:
  - `main` -> `zegang`
  - `feishu2` -> `dengjingjing`
