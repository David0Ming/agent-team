# Codex CerebLink Alignment Design

## Summary
Align the Codex `cereblink` skill with the OpenClaw CerebLink project so both surfaces use the same teaching policy and flow rules. Codex should keep only the adapter responsibilities that are specific to skill routing and persistence reporting, while delegating teaching behavior to the project-owned rules under `projects/cereblink/`.

## Problem
The current Codex `cereblink` skill and the OpenClaw CerebLink project are split across two rule sources:
- Codex skill files define trigger, closure, and persistence rules
- OpenClaw project files define teaching modes, search policy, and workflow structure

This creates drift risk:
- project rule updates do not automatically change Codex behavior
- Codex can continue using stale teaching behavior after the OpenClaw docs change
- the user has to maintain two similar but non-identical rule systems

## Goals
- Make `projects/cereblink/AGENTS.md` the shared teaching-policy source for both Codex and OpenClaw
- Make `projects/cereblink/docs/workflows.md` the shared flow-definition source
- Let Codex preserve its current trigger and closure adapter behavior
- Keep the current live-vault-primary persistence policy
- Reduce future maintenance to one main project rule layer instead of duplicated skill logic

## Non-Goals
- Do not replace the Codex skill entry point with raw project docs only
- Do not redesign CerebLink state scripts in this change
- Do not change mastery logic, queue scheduling, or today-plan generation
- Do not change primary persistence from the Obsidian live vault to the workspace mirror
- Do not implement automatic two-way synchronization between skill docs and project docs

## Design

### Rule Ownership
Split CerebLink behavior into two layers:

1. Project-owned shared rules
   - `projects/cereblink/AGENTS.md`
   - `projects/cereblink/docs/workflows.md`
   - `projects/cereblink/docs/architecture.md`

   These files define:
   - New Learning vs Review mode
   - search policy
   - teaching style
   - step order for each study mode
   - system boundaries

2. Codex-owned adapter rules
   - `~/.codex/skills/cereblink/SKILL.md`
   - `~/.codex/skills/cereblink/references/*.md`

   These files define:
   - when the skill triggers
   - how Mode A vs weak-auto closure is selected
   - how state files are located
   - how save intent and persistence results are reported
   - how live vault vs workspace mirror success is judged

### Runtime Order
When the user enters a CerebLink scenario, Codex should run in this order:

1. Trigger through the Codex `cereblink` skill
2. Determine whether the conversation is explicit entry or completed-pending-closure
3. If the round is not already complete, read project-owned rule files first
4. Use project rules to choose `New Learning` or `Review`
5. Execute the study exchange using project teaching policy
6. Return to Codex adapter rules for closure, save intent, and persistence reporting

This keeps one shared teaching brain while preserving Codex-specific orchestration boundaries.

### Conflict Resolution
When rules conflict:
- teaching behavior follows `projects/cereblink/AGENTS.md`
- flow sequencing follows `projects/cereblink/docs/workflows.md`
- system boundary interpretation may consult `projects/cereblink/docs/architecture.md`
- skill trigger and persistence reporting follow `~/.codex/skills/cereblink`

This priority prevents project docs from being treated as optional background.

### Persistence
Keep the current persistence model unchanged:
- primary truth: `/home/mzg/文档/Obsidian Vault/cereblink`
- secondary mirror: `/home/mzg/.openclaw/workspace/projects/cereblink`

Codex may align its teaching behavior to the project rules without changing where official save success is determined.

## File Changes

### `~/.codex/skills/cereblink/SKILL.md`
Update the skill so it explicitly instructs Codex to:
- read `projects/cereblink/AGENTS.md` on skill entry
- read `projects/cereblink/docs/workflows.md` before running a study exchange
- treat those files as the source of teaching behavior
- reserve Codex skill files for routing, state mapping, closure, and persistence

### `~/.codex/skills/cereblink/references/flow.md`
Update the flow reference so explicit entry uses the project teaching policy before the exchange starts.

### `~/.codex/skills/cereblink/references/state-map.md`
No major logic change expected beyond clarifying that project docs govern behavior while state files govern persistence and planning.

### `~/.codex/skills/cereblink/references/sync-policy.md`
No major logic change expected. Keep current primary-save vs mirror-sync honesty rules.

## Testing
- Manual verification that Codex `cereblink` now reads project rule files before teaching
- Manual verification that explicit `/cereblink` still routes through current state and plan checks
- Manual verification that weak-auto closure still produces the existing 3-line summary plus save intent pattern
- Manual verification that persistence reporting still distinguishes live vault from workspace mirror

## Risks
- Codex could still accidentally privilege older skill wording if the skill update is incomplete
- project docs may evolve and require future skill-reference wording updates if file paths change
- adding too much teaching detail back into the skill would recreate the same drift problem

## Decision
Proceed by making the OpenClaw CerebLink project docs the shared teaching-policy source and retaining the Codex `cereblink` skill only as the adapter layer for routing, closure, and persistence.
