# CerebLink State Normalization Design

## Summary
Normalize CerebLink state ownership so a concept cannot simultaneously appear as `learning` and `mastered` in different layers. `mastery-tracker.json` becomes the only source of concept mastery state. `review-queue.json` remains in place for low-frequency review scheduling, but it no longer owns or duplicates concept mastery status.

## Problem
The current CerebLink state model allows the same concept to exist in multiple inconsistent states at the same time.

Observed `reranker` example:
- `progress/mastery-tracker.json` says `mastered`
- `reviews/review-queue.json` contains two entries for the same slug with `mastered` and `learning`
- `plans/today.md` renders `learning`
- `state/learning-summary.json` renders `reviewing`

This is happening because:
- the queue stores a duplicate copy of concept status
- queue writes only update the first matching slug and do not clean preexisting duplicates
- derived files tolerate dirty queue data but still surface conflicting interpretations

## Goals
- Make `mastery-tracker.json` the only authority for concept mastery state
- Keep `mastered` concepts eligible for low-frequency review scheduling
- Guarantee one queue item per slug
- Ensure `today.md` and `learning-summary.json` never expose conflicting mastery states for the same concept
- Add regression coverage for queue normalization and derived-state consistency

## Non-Goals
- Do not remove low-frequency review for `mastered` concepts
- Do not redesign the mastery assessment heuristics
- Do not redesign the user-facing copy in the generated plan beyond what is required for consistent state
- Do not introduce a database or a larger persistence layer

## Current Failure Analysis

### Source of truth confusion
Today, concept mastery is effectively stored twice:
- once in `progress/mastery-tracker.json`
- once again in each queue item under `reviews/review-queue.json`

That duplication is unnecessary because the queue only needs to answer:
- should this concept be reviewed
- when is it due
- what scheduling metadata applies

It does not need to answer:
- is the concept mastered, fragile, or learning

### Queue duplication path
`enqueue_review()` currently updates only the first matching slug entry. If dirty data already exists with multiple entries for the same slug, the function does not normalize the list back to one item. The queue can therefore remain permanently inconsistent.

### Derived-state leakage
`today.md` and `learning-summary.json` are not the primary problem, but they currently reflect queue dirt in ways that look like state disagreement:
- `today.md` chooses the highest-priority queue status for a duplicated slug
- `learning-summary.json` maps `mastered + still in queue` to `reviewing`

The second behavior is acceptable when the queue is clean and only expresses review scheduling. The first behavior is not acceptable because it lets a stale queue status override the true mastery state in generated output.

## State ownership

### `progress/mastery-tracker.json`
This is the only source of concept mastery state.

Fields remain concept-oriented:
- `topic`
- `status`
- `last_studied_at`
- `session_count`
- `manually_dropped`
- `manually_dormant`

### `reviews/review-queue.json`
This becomes a scheduling structure only.

Each queue item is reduced to scheduling metadata:
- `slug`
- `due_at`
- `last_enqueued_at`

Queue items no longer need a concept `status` field for steady-state operation.

### Derived files
- `plans/today.md` derives display text from tracker mastery state plus queue membership/due-ness
- `state/learning-summary.json` derives planning state from tracker mastery state plus queue membership/due-ness

No derived file may present a concept mastery state that contradicts `mastery-tracker.json`.

## Normalization strategy

### Read normalization
Whenever queue data is read, the queue loader should normalize duplicate slugs into one record before the data is used.

Normalization rules:
- group by `slug`
- keep one final queue item per slug
- preserve the earliest `due_at`
- preserve the latest `last_enqueued_at` when available
- ignore stale per-item `status` as an authority

This provides self-healing behavior for existing dirty queue files.

### Write normalization
Whenever queue data is written:
- the writer must rewrite the queue in normalized form
- one slug must produce one queue item
- the queue writer must not emit a new per-item mastery status field

This prevents reintroduction of duplicate mixed-state rows.

## Backward compatibility
Existing queue files may still contain `status` fields. During migration:
- old queue items with `status` remain readable
- normalization discards `status` as a state authority
- new writes stop depending on `status`

This allows the system to clean up existing data without a separate manual migration step.

## Generation rules

### `today.md`
The today-plan generator should:
- normalize the queue first
- iterate over normalized queue items only
- derive display state from `mastery-tracker.json`
- continue to prioritize urgent review states, but never infer `learning` from stale queue rows

Expected result:
- a mastered concept that is due for review can appear as a review item
- it cannot appear as `learning` unless the tracker says it is `learning`

### `learning-summary.json`
The summary generator should:
- normalize the queue first
- derive `in_review_queue`, `is_due`, and `is_overdue` from normalized queue data
- derive planning state from the tracker mastery state

Expected result:
- `mastered + queued review` may still legitimately map to `reviewing`
- but the summary cannot disagree with the tracker about whether the concept is mastered

## Implementation plan

### 1. Add shared queue normalization helper
Create a small helper in the CerebLink scripts layer that:
- reads queue items
- normalizes duplicate slugs
- returns deterministic scheduling rows

This helper should be used by:
- queue writes
- today-plan generation
- learning-summary generation

### 2. Update queue writer
Refactor `enqueue_review()` to:
- normalize existing items first
- update the single normalized row for the slug
- write back normalized scheduling-only data

### 3. Update today-plan generation
Refactor `generate_today_plan()` to:
- read normalized queue items
- join them with tracker mastery state
- generate display copy from the tracker state instead of queue status

### 4. Update learning-summary generation
Refactor `generate_learning_summary()` to:
- read normalized queue items
- compute queue presence and due-ness from normalized rows
- keep the existing planning-state semantics where `mastered` concepts can still be in `reviewing`

### 5. Migrate existing state opportunistically
When the next normal write occurs, dirty queue data should be rewritten into normalized form automatically.

No standalone migration command is required for v1 if the normalizers are applied consistently.

## Required regression tests
- a queue with duplicate rows for one slug is normalized to one row
- a duplicated queue with stale `learning` plus current `mastered` does not make `today.md` render `learning`
- a mastered concept can still appear in today-plan review flow when due
- `learning-summary.json` can report `reviewing` for a mastered concept in queue without contradicting tracker state
- queue rewrites strip duplicate rows and stop relying on per-item status

## Existing test updates
Current tests that explicitly assert queue-driven `mastered` rendering should be updated to match the new source-of-truth rule:
- queue presence still matters for review scheduling
- displayed mastery state must come from the tracker

## Risks
- Leaving any generator on the old queue interpretation would preserve partial inconsistency
- Silent retention of legacy `status` fields could confuse future maintenance if not normalized out on write
- If normalization rules are inconsistent across readers and writers, dirty state could reappear

## Decision
Proceed with a tracker-authoritative state model:
- `mastery-tracker.json` owns mastery state
- `review-queue.json` owns review scheduling only
- all reads and writes normalize queue data
- low-frequency review for mastered concepts is preserved
