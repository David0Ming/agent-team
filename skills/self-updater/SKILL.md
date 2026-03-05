---
name: self-updater
description: "Self-update OpenClaw safely with pre/post verification. Use when: (1) scheduled self-update (2) manual update trigger (3) keeping OpenClaw current. Ensures gateway stays alive and agents remain functional before and after update."
---

# Self Updater

Automatically update OpenClaw with pre/post health checks to ensure uninterrupted service.

## When to Use This Skill

- **Scheduled updates**: Run via heartbeat/cron (e.g., every 6h or daily)
- **Manual updates**: When you notice `openclaw update` is available
- **After system reboot**: Verify OpenClaw is running correctly

## Quick Start

```bash
# Run full update with health check
python {baseDir}/scripts/self-update.py

# Check only (no update)
python {baseDir}/scripts/self-update.py --check-only

# Force update even if already current
python {baseDir}/scripts/self-update.py --force
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
