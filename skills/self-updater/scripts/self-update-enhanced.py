#!/usr/bin/env python3
"""
OpenClaw Self-Updater (Enhanced)
- Pre/post health checks
- Automatic post-update fixes
- Codex integration for complex repairs
"""

import subprocess
import json
import sys
import time
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
CONFIG_FILE = BASE_DIR / "config" / "post-update-fixes.json"

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
    code, out, err = run_cmd("openclaw status 2>&1", timeout=15)
    running = "running" in out.lower() or "online" in out.lower()
    
    version = "unknown"
    for line in out.split('\n'):
        if "OpenClaw" in line and "202" in line:
            parts = line.split()
            for p in parts:
                if "202" in p:
                    version = p
                    break
    
    return {"running": running, "version": version, "raw": out[:200]}

def get_session_count():
    """Count active sessions"""
    code, out, err = run_cmd("openclaw status 2>&1 | grep -c 'agent:'")
    try:
        return int(out.strip()) if out.strip().isdigit() else 0
    except:
        return 0

def check_npm_update():
    """Check if update available"""
    code, out, err = run_cmd("npm info openclaw version 2>/dev/null")
    latest = out.strip() if out.strip() else None
    
    code, current, err = run_cmd("openclaw --version 2>/dev/null")
    current = current.strip() if current.strip() else "unknown"
    
    return {
        "current": current,
        "latest": latest,
        "update_available": latest and latest != current
    }

def load_fixes_config():
    """Load post-update fixes configuration"""
    if not CONFIG_FILE.exists():
        return {"fixes": [], "codex_tasks": []}
    
    with open(CONFIG_FILE) as f:
        return json.load(f)

def run_fix(fix):
    """Execute a single fix"""
    print(f"\n🔧 {fix['name']}: {fix['description']}")
    
    if fix['type'] == 'script':
        script_path = BASE_DIR / "scripts" / fix['script']
        code, out, err = run_cmd(f"bash {script_path}", timeout=60)
    elif fix['type'] == 'command':
        code, out, err = run_cmd(fix['command'], timeout=60)
    else:
        print(f"  ⚠️  Unknown fix type: {fix['type']}")
        return False
    
    # Verify
    if 'verify' in fix:
        vcode, vout, verr = run_cmd(fix['verify'], timeout=10)
        if vcode == 0 and vout.strip():
            print(f"  ✅ 验证通过")
            return True
        else:
            print(f"  ❌ 验证失败")
            return False
    
    return code == 0

def run_codex_task(task):
    """Run Codex for complex fixes"""
    print(f"\n🤖 Codex任务: {task['name']}")
    print(f"  描述: {task['description']}")
    
    # Call Codex via openclaw
    prompt = f"OpenClaw更新后修复任务：{task['prompt']}"
    cmd = f'echo "{prompt}" | openclaw chat --agent codex --timeout 300'
    
    code, out, err = run_cmd(cmd, timeout=360)
    
    if code == 0:
        print(f"  ✅ Codex任务完成")
        print(f"  输出: {out[:200]}...")
        return True
    else:
        print(f"  ❌ Codex任务失败: {err}")
        return False

def restart_gateway():
    """Restart OpenClaw gateway"""
    print("\n🔄 重启Gateway...")
    code, out, err = run_cmd("openclaw gateway restart", timeout=30)
    time.sleep(5)
    return code == 0

def main():
    parser = argparse.ArgumentParser(description="OpenClaw Self-Updater (Enhanced)")
    parser.add_argument("--check-only", action="store_true", help="Only check, don't update")
    parser.add_argument("--force", action="store_true", help="Force update")
    parser.add_argument("--skip-fixes", action="store_true", help="Skip post-update fixes")
    args = parser.parse_args()

    print("=== OpenClaw Self-Updater (Enhanced) ===\n")

    # === PRE-UPDATE ===
    print("📋 Pre-update checks...")
    status = get_gateway_status()
    sessions = get_session_count()
    
    print(f"  Gateway: {'ONLINE' if status['running'] else 'OFFLINE'} (v{status['version']})")
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
    code, out, err = run_cmd("npm update openclaw -g", timeout=180)
    
    if code != 0:
        print(f"❌ Update failed: {err}")
        return 1
    
    print(f"  ✅ Update completed")

    # === POST-UPDATE FIXES ===
    if not args.skip_fixes:
        print("\n🔧 Running post-update fixes...")
        config = load_fixes_config()
        
        # Sort by priority
        fixes = sorted(
            [f for f in config.get('fixes', []) if f.get('enabled', True)],
            key=lambda x: x.get('priority', 99)
        )
        
        fix_results = []
        for fix in fixes:
            result = run_fix(fix)
            fix_results.append((fix['name'], result))
        
        # Codex tasks
        codex_tasks = [t for t in config.get('codex_tasks', []) if t.get('enabled', False)]
        for task in codex_tasks:
            if task.get('trigger') == 'auto':
                run_codex_task(task)
        
        # Summary
        print("\n📊 修复结果:")
        for name, result in fix_results:
            print(f"  {'✅' if result else '❌'} {name}")

    # === RESTART & VERIFY ===
    restart_gateway()
    
    time.sleep(3)
    
    status2 = get_gateway_status()
    sessions2 = get_session_count()
    
    print(f"\n📋 Post-update verification...")
    print(f"  Gateway: {'ONLINE ✅' if status2['running'] else 'OFFLINE ❌'}")
    print(f"  Sessions: {sessions2} (was {sessions})")
    
    success = status2['running'] and sessions2 >= sessions
    
    if success:
        print("\n✅ All checks passed!")
        return 0
    else:
        print("\n⚠️  Some checks failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
