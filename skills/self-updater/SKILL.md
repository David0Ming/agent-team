---
name: self-updater
version: 1.0.0
author: DJJ
compatibility: openclaw >= 2026.2.0
description: "Self-update OpenClaw safely with pre/post verification and automatic fixes. Use when: (1) scheduled self-update (2) manual update trigger (3) keeping OpenClaw current. Ensures gateway stays alive, agents remain functional, and custom configurations are preserved after update."
tags: [maintenance, automation, system]
---

# Self Updater (Enhanced)

Automatically update OpenClaw with:
- Pre/post health checks
- **Automatic post-update fixes** (NEW)
- **Codex integration for complex repairs** (NEW)
- Configuration preservation

## When to Use This Skill

- **Scheduled updates**: Run via heartbeat/cron (e.g., every 6h or daily)
- **Manual updates**: When you notice `openclaw update` is available
- **After system reboot**: Verify OpenClaw is running correctly
- **After breaking changes**: Automatically fix known issues

## Quick Start

```bash
# Enhanced updater (recommended)
python {baseDir}/scripts/self-update-enhanced.py

# Legacy updater (basic)
python {baseDir}/scripts/self-update.py

# Check only (no update)
python {baseDir}/scripts/self-update-enhanced.py --check-only

# Force update + skip fixes
python {baseDir}/scripts/self-update-enhanced.py --force --skip-fixes
```

## Workflow

### 1. Pre-Update Check
- Save current version
- Check gateway status
- Record active sessions count

### 2. Execute Update
- Run `pnpm update` or `npm update`
- Verify new version installed

### 3. Post-Update Verification
- Restart gateway if needed
- Verify gateway responds
- Check agent health (sessions operational)
- Compare session count (should match pre-update)

### 4. Rollback (if failed)
- If health check fails, attempt restart
- Alert user if cannot recover

## Success Criteria

| Check | Expected |
|-------|----------|
| Gateway ping | < 100ms |
| Sessions | >= pre-update count |
| Agents | All online |
| Tools | Available |

## Integration

### Heartbeat Integration
Add to your HEARTBEAT.md:
```markdown
## Self-Update Check (every 6h)
python {baseDir}/../skills/self-updater/scripts/self-update.py
```

### Cron Style (optional)
```bash
# Run every 6 hours
0 */6 * * * cd ~/.openclaw/workspace && python skills/self-updater/scripts/self-update.py
```

## Output Example

```
=== OpenClaw Self-Updater ===
Pre-update: v2026.2.24 → Checking...
Gateway: ONLINE (23ms)
Sessions: 4 active

Running update...
Updated: v2026.3.2

Post-update: Verifying...
Gateway: ONLINE (18ms) ✅
Sessions: 4 active ✅
All checks passed! ✅
```

## New Features (Enhanced Version)

### 1. Automatic Post-Update Fixes

After updating OpenClaw, automatically fixes known issues:

**Current Fixes**:
- ✅ Microphone permission (Web Speech API)
- ✅ Voice-call plugin enablement
- ✅ Custom configurations preservation

**Configuration**: `config/post-update-fixes.json`

### 2. Codex Integration

For complex repairs that need code analysis:
- Automatic migration of config file formats
- Detection of breaking changes
- Smart conflict resolution

### 3. Priority-Based Execution

Fixes run in priority order:
1. Critical (microphone, plugins)
2. Important (configurations)
3. Optional (optimizations)

## Configuration

Edit `config/post-update-fixes.json` to add custom fixes:

```json
{
  "fixes": [
    {
      "name": "your-fix-name",
      "description": "What this fix does",
      "enabled": true,
      "priority": 1,
      "type": "script",
      "script": "your-script.sh",
      "verify": "command to verify success"
    }
  ]
}
```

## Adding New Fixes

### Method 1: Shell Script

1. Create script in `scripts/fix-yourname.sh`
2. Add to `config/post-update-fixes.json`
3. Test with `--check-only` first

### Method 2: Direct Command

```json
{
  "name": "enable-plugin",
  "type": "command",
  "command": "openclaw plugins enable your-plugin"
}
```

### Method 3: Codex Task (Complex)

```json
{
  "codex_tasks": [
    {
      "name": "migrate-config",
      "enabled": true,
      "trigger": "auto",
      "prompt": "Migrate old config format to new format"
    }
  ]
}
```

