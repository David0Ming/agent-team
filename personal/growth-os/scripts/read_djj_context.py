import json
from pathlib import Path


def _extract_phase(user_text: str) -> str:
    for line in user_text.splitlines():
        stripped = line.strip()
        if "当前阶段：" in stripped:
            return stripped.split("当前阶段：", 1)[1].strip()
    return "unknown"


def _open_tasks(projects_text: str) -> list[str]:
    return [line.replace("- [ ] ", "").strip() for line in projects_text.splitlines() if line.startswith("- [ ] ")]


def read_djj_context(planning_summary_path: Path, learning_summary_path: Path, user_path: Path, projects_path: Path) -> dict:
    user_text = user_path.read_text(encoding="utf-8")
    projects_text = projects_path.read_text(encoding="utf-8")
    if planning_summary_path.exists() and learning_summary_path.exists():
        return {
            "sourceMode": "summary-first",
            "planning": json.loads(planning_summary_path.read_text(encoding="utf-8")),
            "learning": json.loads(learning_summary_path.read_text(encoding="utf-8")),
        }
    return {
        "sourceMode": "fallback",
        "planning": {
            "phase": _extract_phase(user_text),
            "topPriorities": _open_tasks(projects_text)[:3],
            "learningBudget": 0,
            "learningBias": "balanced",
        },
        "learning": {
            "currentTrack": "mixed",
            "recommendedTopics": [],
            "recommendedDuration": 0,
            "reviewPressure": "low",
        },
    }
