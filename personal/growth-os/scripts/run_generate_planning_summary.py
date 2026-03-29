#!/usr/bin/env python3
from pathlib import Path
from scripts.generate_planning_summary import generate_planning_summary

ROOT = Path('/home/mzg/.openclaw/workspace')
GROWTH_OS = ROOT / 'personal' / 'growth-os'
USER_PATH = ROOT / 'USER.md'
PROJECTS_PATH = ROOT / 'memory' / 'projects.md'
LEARNING_SUMMARY_PATH = ROOT / 'projects' / 'cereblink' / 'state' / 'learning-summary.json'

if __name__ == '__main__':
    generate_planning_summary(GROWTH_OS, USER_PATH, PROJECTS_PATH, LEARNING_SUMMARY_PATH)
    print('planning summary generated')
