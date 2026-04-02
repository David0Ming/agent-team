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
2. System selects New Learning or Review mode
3. In New Learning, the system performs standard search when needed and synthesizes a short structured explanation
4. In Review, the system asks first and diagnoses the learner answer before correcting
5. Session record persisted to `sessions/`
6. Mastery tracker updated in `progress/mastery-tracker.json`
7. Review queue updated in `reviews/review-queue.json`
8. Today plan regenerated in `plans/today.md`

## File Layout
- `knowledge/` — concept cards (Obsidian-compatible Markdown)
- `questions/` — high-value question cards
- `topics/` — topic/MOC pages
- `sessions/` — per-session learning records
- `reviews/` — review queue and history
- `progress/` — mastery tracking state
- `plans/` — generated study plans
- `templates/` — card and record templates
- `scripts/` — automation scripts
- `tests/` — pytest test suite
