import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from read_djj_context import read_djj_context


def test_read_djj_context_prefers_existing_summaries(tmp_path: Path):
    root = tmp_path
    planning = root / "planning-summary.json"
    learning = root / "learning-summary.json"
    user = root / "USER.md"
    projects = root / "projects.md"

    planning.write_text(json.dumps({
        "generatedAt": "2026-03-29",
        "phase": "求职+毕设",
        "topPriorities": ["完善招银简历"],
        "learningBudget": 30,
        "learningBias": "balanced"
    }), encoding="utf-8")
    learning.write_text(json.dumps({
        "generatedAt": "2026-03-29",
        "currentTrack": "mixed",
        "recommendedTopics": ["reranker"],
        "recommendedDuration": 30,
        "reviewPressure": "medium"
    }), encoding="utf-8")
    user.write_text("# USER\n\n- 当前阶段：求职+毕设\n", encoding="utf-8")
    projects.write_text("- [ ] 完善招银简历\n", encoding="utf-8")

    data = read_djj_context(planning, learning, user, projects)
    assert data["sourceMode"] == "summary-first"
    assert data["planning"]["phase"] == "求职+毕设"
    assert data["learning"]["recommendedTopics"] == ["reranker"]


def test_read_djj_context_falls_back_when_summary_missing(tmp_path: Path):
    root = tmp_path
    planning = root / "missing-planning.json"
    learning = root / "missing-learning.json"
    user = root / "USER.md"
    projects = root / "projects.md"

    user.write_text("# USER\n\n- 当前阶段：求职+毕设\n", encoding="utf-8")
    projects.write_text("- [ ] 完善招银简历\n- [ ] 复盘聆海智能面试\n", encoding="utf-8")

    data = read_djj_context(planning, learning, user, projects)
    assert data["sourceMode"] == "fallback"
    assert data["planning"]["phase"] == "求职+毕设"
    assert "完善招银简历" in data["planning"]["topPriorities"][0]
