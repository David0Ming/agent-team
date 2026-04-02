# CerebLink Teaching Strategy Redesign

## Goal
Redesign CerebLink’s teaching behavior so that:
- it supports two explicit modes: new-learning and review
- new-learning uses standard search by default before teaching
- the teaching voice is a logic-first friend: concise, precise, structured, and low on analogy
- explanation proceeds from shallow to deep through short explanation + immediate check questions

## Why this change
Current CerebLink is good at recording study state, but its teaching behavior is under-specified.
The main issues are:
- it can rely too much on model prior knowledge instead of current authoritative sources
- explanation structure is not stable enough
- the difference between first-time learning and review is not explicit enough
- tone and pedagogy are not well constrained

## User Preference Summary
- Two modes are required: new-learning and review
- For new topics, default to standard search
- Preferred style: logic-strong friend
- Preferred rhythm for new topics: short explanation + interactive questioning
- Teaching progression: from shallow to deep
- Avoid unnecessary analogy and metaphor
- Prefer definitions, boundaries, distinctions, causes, and conditions

## Scope
This redesign covers CerebLink’s rule layer and workflow layer.
Primary target files:
- `projects/cereblink/AGENTS.md`
- `projects/cereblink/docs/workflows.md`
- `projects/cereblink/docs/architecture.md`

Out of scope for this phase:
- major script refactor
- retrieval automation inside Python scripts
- UI/product changes outside current file-based workflow

## Approaches Considered

### Approach A: Rules only
Update tutor rules and workflow descriptions, but keep everything else unchanged.

Pros:
- fastest
- lowest risk

Cons:
- weaker behavioral consistency
- structure may still drift in actual use

### Approach B: Rules + explicit teaching structure
Update rules and workflows, and define a fixed teaching structure for both modes.

Pros:
- strong enough to noticeably improve behavior
- still lightweight
- easy to extend later

Cons:
- not yet enforced by code

### Approach C: Rules + structure + script-level mode handling
Add explicit mode handling to Python scripts.

Pros:
- strongest consistency
- best long-term product foundation

Cons:
- higher cost now
- premature before the pedagogy is validated

## Chosen Approach
Approach B.

Reason:
The current problem is primarily pedagogical, not infrastructural. The highest-leverage move is to define how CerebLink should search, explain, question, and switch modes before modifying script internals.

## Design

### 1. Explicit Modes
CerebLink should support two explicit learning modes.

#### Mode 1: New Learning
Use when the user is learning a topic for the first time or only has weak prior understanding.

Default flow:
1. clarify the learning goal
2. perform standard search
3. prioritize authoritative/current sources
4. provide a short structured explanation
5. ask one immediate check question
6. continue to the next layer based on the answer
7. end with summary and persistence if appropriate

#### Mode 2: Review
Use when the topic has already been studied and the goal is retention, correction, or mastery checking.

Default flow:
1. ask a question first
2. diagnose weakness from the answer
3. provide minimal correction
4. ask one follow-up check
5. update review/persistence state if appropriate

### 2. Search Policy
For new-learning mode, standard search is the default.

Rules:
- do not default to stale model memory when a topic benefits from current or authoritative information
- especially for fast-moving domains such as AI, agents, RAG, workflow automation, and tools, external search should be assumed necessary unless clearly unnecessary
- source priority:
  1. official documentation
  2. academic or otherwise authoritative references
  3. high-quality open-source project documentation
  4. credible technical blogs
- when the final teaching material relies on external information, the response should briefly indicate source type and note time-sensitivity when relevant
- if search quality is poor or incomplete, say so explicitly instead of pretending certainty

### 3. Teaching Style
The default teaching voice should be a logic-first friend.

Operational meaning:
- concise rather than expansive
- precise rather than performatively friendly
- structured rather than free-form
- low-analogy by default
- define terms before elaborating
- emphasize distinctions, boundaries, causes, and conditions
- if one sentence is enough, do not use two

This is not a cold examiner voice.
It should still feel cooperative and companion-like, but not fluffy.

### 4. New Learning Teaching Structure
Each step in new-learning mode should follow this progression:
1. definition — what it is
2. problem — what problem it solves
3. mechanism — how it works
4. boundary — what it is not / what it differs from
5. check question — verify the user is keeping up

Execution rules:
- advance one layer at a time
- do not dump the whole lesson at once
- keep each explanation chunk short
- every chunk should be understandable, restatable, and testable

### 5. Review Structure
Each review step should follow this progression:
1. ask first
2. inspect the answer for misunderstanding or incompleteness
3. provide the smallest correction that restores correctness
4. ask one check question again
5. only expand if necessary

### 6. Architecture Impact
`projects/cereblink/docs/architecture.md` should reflect that:
- OpenClaw is not only the interaction layer but also the teaching-policy orchestrator
- the learning flow now branches by mode
- external search is part of new-learning preparation, not an optional afterthought

## Error Handling / Edge Cases
- If no reliable search result is available, state that the teaching answer is based on limited evidence
- If a topic is stable and well-established, search may be minimal, but the system should still prefer explicitness over assumption
- If the user asks for quick review, do not force a full new-learning flow
- If the user already demonstrates strong understanding, shorten explanation and increase testing density

## Testing / Validation
This phase is validated by behavioral checks, not script tests.

Success criteria:
- new-topic sessions clearly distinguish themselves from review sessions
- new-topic sessions mention or reflect external source grounding when appropriate
- explanations feel more structured and easier to retain
- tone is concise, clean, and logic-first
- the system no longer defaults to broad, blob-like explanations

## Implementation Plan for This Phase
1. update `projects/cereblink/AGENTS.md`
2. update `projects/cereblink/docs/workflows.md`
3. update `projects/cereblink/docs/architecture.md`
4. keep script changes out of scope for now

## Risks
- Rule-only enforcement can still drift during real conversations
- “standard search” may add latency in some sessions
- if source quality is weak, concise explanations may become too thin unless carefully synthesized

## Future Upgrade Path
If this redesign works in practice, the next phase can add:
- explicit mode flags in scripts
- reusable teaching templates
- stronger search-source recording
- automated behavior tests for mode switching and explanation shape
