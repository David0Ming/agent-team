import json
from pathlib import Path
from projects.cereblink.scripts.learn_loop import process_learning_answer


def test_process_learning_answer_updates_full_learning_loop(tmp_path):
    root = tmp_path / "cereblink"
    (root / "progress").mkdir(parents=True)
    (root / "reviews").mkdir(parents=True)
    (root / "plans").mkdir(parents=True)
    (root / "sessions").mkdir(parents=True)
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")
    (root / "plans" / "today.md").write_text('', encoding="utf-8")

    result = process_learning_answer(
        root=root,
        slug="reranker",
        topic="rag/retrieval",
        title="Reranker 学习",
        learning_goal="理解为什么 RAG 需要 reranker",
        answer="retrieval 负责大范围粗召回候选内容，reranker 负责在小候选集上做精细排序。",
    )

    mastery = json.loads((root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    queue = json.loads((root / "reviews" / "review-queue.json").read_text(encoding="utf-8"))
    today = (root / "plans" / "today.md").read_text(encoding="utf-8")

    assert result["status"] == "mastered"
    assert mastery["concepts"]["reranker"]["status"] == "mastered"
    assert queue["items"][0]["slug"] == "reranker"
    assert "# Today Plan" in today
    assert "`reranker` · mastered" in today
    assert "原因：" in today
    assert Path(result["session_record"]).exists()


def test_process_learning_answer_generates_learning_summary(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "plans").mkdir()
    (root / "sessions").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    process_learning_answer(root, "reranker", "rag/retrieval", "Reranker 学习", "理解 reranker", "reranker 负责对小候选集精排")

    summary = root / "state" / "learning-summary.json"
    assert summary.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert "topicStates" in data
