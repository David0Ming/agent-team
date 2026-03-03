---
name: token-estimator
description: "Estimate task token cost before execution and recommend optimal model selection. Use when: (1) starting coding tasks on large codebases, (2) need to decide between cost-effective vs high-performance models, (3) processing large files or batch operations. Analyzes file sizes, character counts, and task complexity to recommend model tier (lightweight/standard/premium)."
---

# Token Estimator

## Overview

Estimate token costs and select optimal models based on task scale. Prevents over-spending on small tasks while ensuring large tasks get sufficient capacity.

**Core principle**: Characters ÷ 4 ≈ Tokens (conservative estimate)

## Quick Start

```bash
# Estimate current directory
python {baseDir}/scripts/estimate.py --path ./src

# Estimate with specific file types
python {baseDir}/scripts/estimate.py --path ./src --ext .ts,.js,.json

# Estimate and get model recommendation
python {baseDir}/scripts/estimate.py --path ./src --recommend
```

## Decision Rules

| Total Characters | Estimated Tokens | Recommended Model |
|-----------------|------------------|-------------------|
| < 3M chars | < 750K tokens | Lightweight (Opus 4.6 / GPT-Mini) |
| 3M - 12M chars | 750K - 3M tokens | Standard (GPT-5.1 / Kimi) |
| > 12M chars | > 3M tokens | Premium (GPT-5.2 / Claude Opus) |

## When to Use This Skill

**Always use before:**
- Large refactoring tasks
- Codebase-wide searches or replacements
- Batch processing multiple files
- Starting coding agent sessions on unknown projects

**Skip for:**
- Single-file edits
- Quick queries (< 100 lines of context)
- Tasks with obvious small scope

## Workflow

1. **Scan** → Run estimate.py on target path
2. **Decide** → Check recommendation against rules above
3. **Configure** → Set model override if needed:
   ```bash
   # For premium tasks
   openclaw config set agent.model.primary "fox/gpt-5.2"
   
   # For lightweight tasks
   openclaw config set agent.model.primary "anthropic/claude-opus-4-6"
   ```

## Model Mapping

| Your Term | OpenClaw Model |
|-----------|---------------|
| Opus 4.6 | `anthropic/claude-opus-4-6` |
| GPT-Mini | `fox/gpt-5.1-codex-mini` |
| GPT-5.1 | `fox/gpt-5.1` |
| GPT-5.2 | `fox/gpt-5.2` |
| Kimi | `kimi-coding/k2p5` |
| Claude Opus | `anthropic/claude-opus-4-6` |

## Integration with Coding Agent

When spawning coding agents, estimate first:

```bash
# 1. Estimate the target
python {baseDir}/scripts/estimate.py --path ./src --recommend

# 2. Spawn with appropriate model
# Small project → lightweight model
bash pty:true workdir:./src command:"codex exec --model gpt-5.1-codex-mini 'Your task'"

# Large project → premium model  
bash pty:true workdir:./src command:"codex exec --model gpt-5.2 'Your task'"
```

## Script Reference

See `scripts/estimate.py` for:
- File filtering (gitignore-aware)
- Character counting
- Token estimation
- Model recommendation output
