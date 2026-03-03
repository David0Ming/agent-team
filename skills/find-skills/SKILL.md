---
name: find-skills
skill_version: 1.0.0
description: Discover and install skills from the open agent skills ecosystem using npx skills CLI. Helps find skills for React, testing, deployment, documentation, and more.
---

# find-skills

Discover and install skills from the open agent skills ecosystem.

## When to Use

- User asks "how do I do X" where X might have an existing skill
- User says "find a skill for X" or "is there a skill for X"
- User asks "can you do X" where X is specialized
- User wants to extend agent capabilities
- User wants tools, templates, or workflows

## CLI Commands

```bash
# Search for skills
npx skills find [query]

# Install a skill
npx skills add <owner/repo@skill> -g -y

# Check for updates
npx skills check

# Update all skills
npx skills update
```

## Common Categories

| Category | Example Queries |
|----------|-----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

## Usage Examples

```bash
# Find React performance skills
npx skills find react performance

# Install a specific skill
npx skills add vercel-labs/agent-skills@vercel-react-best-practices -g -y

# Browse all skills
open https://skills.sh/
```

## Tips

- Use specific keywords: "react testing" > "testing"
- Try alternatives: "deploy", "deployment", "ci-cd"
- Popular sources: vercel-labs/agent-skills, ComposioHQ/awesome-claude-skills
