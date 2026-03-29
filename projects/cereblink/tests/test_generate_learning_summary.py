import json
from pathlib import Path
from projects.cereblink.scripts.generate_learning_summary import generate_learning_summary


def test_generate_learning_summary_writes_expected_keys(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text(json.dumps({
        "concepts": {
            "reranker": {
                "topic": "rag/retrieval",
                "status": "learning",
                "last_studied_at": "2026-03-29",
                "session_count": 1,
                "manually_dropped": False,
                "manually_dormant": False
            }
        }
    }), encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text(json.dumps({
        "items": [{"slug": "reranker", "status": "learning", "due_at": "2026-03-29"}]
    }), encoding="utf-8")

    out = generate_learning_summary(root)
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["currentTrack"] == "mixed"
    assert "recommendedTopics" in data
    assert "topicStates" in data
    assert "reviewPressure" in data
    assert data["topicStates"]["reranker"] in {"introduced", "practicing", "reviewing"}
