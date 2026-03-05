#!/usr/bin/env python3
"""
OpenClaw Self-Updater
Checks for updates, performs update, verifies health before/after
"""

import subprocess
import json
import sys
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent / "workspace" / "skills" / "self-updater"

def run_cmd(cmd, timeout=30):
    """Run shell command and return output"""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)

def get_gateway_status():
    """Check gateway health"""
    code, out, err = run_cmd("openclaw status --json 2>/dev/null || openclaw status 2>&1", timeout=15)
    
    # Parse token usage if available
    tokens = "unknown"
    if "Tokens" in out:
        for line in out.split('\n'):
            if 'Tokens' in line:
                parts = line.split('Tokens')
                if len(parts) > 1:
                    tokens = parts[1].split('·')[0].strip() if '·' in parts[1] else parts[1].strip()
    
    # Check if running
    running = "running" in out.lower() or "online" in out.lower()
    
    # Extract version
    version = "unknown"
    for line in out.split('\n'):
        if "app" in line.lower() and "202" in line:
            version = line.strip().split()[-1] if line.strip() else "unknown"
    
    return {
        "running": running,
        "version": version,
        "tokens": tokens,
        "raw": out[:200]
    }

def get_session_count():
    """Count active sessions"""
    code, out, err = run_cmd("openclaw status 2>&1 | grep -c 'agent:'")
    try:
        return int(out.strip()) if out.strip().isdigit() else 0
    except:
        return 0

def check_npm_update():
    """Check if update available"""
    code, out, err = run_cmd("cd ~ && npm info openclaw version 2>/dev/null")
    latest = out.strip() if out.strip() else None
    
    code, current, err = run_cmd("openclaw --version 2>/dev/null || echo 'unknown'")
    current = current.strip() if current.strip() else "unknown"
    
    return {
        "current": current,
        "latest": latest,
        "update_available": latest and latest != current
    }

def restart_gateway():
    """Restart OpenClaw gateway"""
    print("🔄 Restarting gateway...")
    code, out, err = run_cmd("openclaw gateway restart", timeout=30)
    time.sleep(5)  # Wait for startup
    return code == 0

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Self-Updater")
    parser.add_argument("--check-only", action="store_true", help="Only check, don't update")
    parser.add_argument("--force", action="store_true", help="Force update even if current")
    args = parser.parse_args()

    print("=== OpenClaw Self-Updater ===\n")

    # === PRE-UPDATE ===
    print("📋 Pre-update checks...")
    status = get_gateway_status()
    sessions = get_session_count()
    
    print(f"  Gateway: {'ONLINE' if status['running'] else 'OFFLINE'} (version: {status['version']})")
    print(f"  Sessions: {sessions} active")

    # === CHECK UPDATE ===
    print("\n🔍 Checking for updates...")
    update_info = check_npm_update()
    print(f"  Current: {update_info['current']}")
    print(f"  Latest:  {update_info['latest']}")
    
    if not update_info['update_available'] and not args.force:
        print("\n✅ Already up to date!")
        return 0
    
    if args.check_only:
        print("\n⚠️  Update available (--check-only mode)")
        return 0

    # === EXECUTE UPDATE ===
    print("\n⬆️  Running update...")
    code, out, err = run_cmd("cd ~ && npm update openclaw -g", timeout=120)
    
    if code != 0:
        print(f"❌ Update failed: {err}")
        return 1
    
    print(f"  Update output: {out[:100]}...")

    # === POST-UPDATE ===
    print("\n📋 Post-update verification...")
    
    # Restart if needed
    restart_gateway()
    
    time.sleep(3)
    
    # Verify
    status2 = get_gateway_status()
    sessions2 = get_session_count()
    
    print(f"  Gateway: {'ONLINE ✅' if status2['running'] else 'OFFLINE ❌'}")
    print(f"  Sessions: {sessions2} (was {sessions})")
    
    # Check success
    success = status2['running'] and sessions2 >= sessions
    
    if success:
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n⚠️  Some checks failed, attempting recovery...")
        restart_gateway()
        time.sleep(3)
        status3 = get_gateway_status()
        
        if status3['running']:
            print("✅ Recovery successful!")
            return 0
        else:
            print("❌ Recovery failed - manual intervention needed")
            return 1

if __name__ == "__main__":
    sys.exit(main())
