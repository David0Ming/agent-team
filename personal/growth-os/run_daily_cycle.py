#!/usr/bin/env python3
import subprocess
from pathlib import Path

ROOT = Path('/home/mzg/.openclaw/workspace/personal/growth-os')
steps = [
    ROOT / 'analysis' / 'learning_analyzer.py',
    ROOT / 'analysis' / 'focus_builder.py',
    ROOT / 'planner' / 'monthly_planner.py',
    ROOT / 'planner' / 'weekly_planner.py',
    ROOT / 'planner' / 'daily_planner.py',
    ROOT / 'planner' / 'review_builder.py',
    ROOT / 'scripts' / 'run_generate_planning_summary.py',
]

for step in steps:
    subprocess.run(['python3', str(step)], check=True)

print('daily cycle complete')
