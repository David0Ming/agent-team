import json
from pathlib import Path


def _open_tasks(projects_text: str) -> list[str]:
    return [line.replace("- [ ] ", "").strip() for line in projects_text.splitlines() if line.startswith("- [ ] ")]


def generate_planning_summary(root: Path, user_path: Path, projects_path: Path, learning_summary_path: Path) -> Path:
    projects_text = projects_path.read_text(encoding="utf-8")
    learning = json.loads(learning_summary_path.read_text(encoding="utf-8"))
    open_tasks = _open_tasks(projects_text)
    summary = {
        "generatedAt": "today",
        "phase": "graduation-and-job-hunt",
        "topPriorities": open_tasks[:3],
        "urgentItems": [],
        "learningBudget": int(learning.get("recommendedDuration", 0)),
        "learningBias": "balanced" if learning.get("currentTrack") == "mixed" else learning.get("currentTrack"),
        "blockedItems": [],
        "rationale": "优先基于真实未完成任务与学习摘要生成最小规划摘要。",
    }
    out = root / "state" / "planning-summary.json"
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out
