# Workflows

## Mode Selection
- Use New Learning when the learner is new to the topic or only has weak prior understanding.
- Use Review when the topic has already been studied and the goal is retention, correction, or mastery checking.

## New Learning Flow
learning goal
-> read learning-profile first (if present)
-> read current working state
-> standard search
-> source selection
-> short structured explanation
-> immediate check question
-> shallow-to-deep continuation
-> mastery update
-> session record
-> review queue
-> today plan
-> learning summary
-> evaluate whether learning-profile should be updated

## Review Flow
review prompt
-> read learning-profile first (if present)
-> read current working state
-> learner answer
-> diagnose misunderstanding
-> minimal correction
-> follow-up check
-> mastery update
-> session record
-> review queue
-> today plan
-> learning summary
-> evaluate whether learning-profile should be updated

## Knowledge Capture Flow
session summary
-> extract stable problem and takeaway
-> map real problem to industry-validated method
-> concept card update using strong structure
-> question card renew/create decision
-> topic page update
-> daily session record append

## Flow Rules
- New Learning should not skip search when the topic benefits from current or authoritative information.
- New Learning should progress one layer at a time rather than dumping a full lecture.
- Review should ask first and explain second.
- Both modes should preserve concise, structured teaching.
- For stable completed rounds, concept card renew/create is mandatory.
- Concept cards should use a strong structure instead of loose freeform markdown.
- A concept card should capture: the real problem, why it matters, the industry-validated method, and the transferable capability.
- Session record is an auxiliary log and does not replace knowledge-card persistence.
- `learning-profile.json` should be treated as the first-read state file for user-level direction.
- `learning-profile.json` should only be updated when the round produces stable new direction, such as: clarified long/short-term goal relation, changed default domain, changed engineering focus, changed practice mainline, or explicit “以后按这个来” style user confirmation.
- Do not rewrite `learning-profile.json` on every round; use it for low-frequency stable state, while `learning-summary.json` remains the high-frequency working summary.
