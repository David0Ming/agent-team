import json
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.generate_planning_summary import generate_planning_summary


def test_generate_planning_summary_reads_projects_and_learning_summary(tmp_path: Path):
    root = tmp_path / "growth-os"
    root.mkdir()
    (root / "state").mkdir()
    user_path = tmp_path / "USER.md"
    projects_path = tmp_path / "projects.md"
    learning_summary_path = tmp_path / "learning-summary.json"

    user_path.write_text("# USER\n\n- 当前阶段：求职+毕设\n", encoding="utf-8")
    projects_path.write_text("- [ ] 完善招银简历\n- [x] 复盘数字华夏面试\n", encoding="utf-8")
    learning_summary_path.write_text(json.dumps({
        "currentTrack": "mixed",
        "recommendedTopics": ["reranker"],
        "recommendedDuration": 30,
        "doNotRepeatToday": []
    }), encoding="utf-8")

    out = generate_planning_summary(root, user_path, projects_path, learning_summary_path)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["learningBudget"] == 30
    assert data["learningBias"] == "balanced"
    assert "完善招银简历" in data["topPriorities"][0]
