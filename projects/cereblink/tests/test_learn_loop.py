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
    assert "status" not in queue["items"][0]
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


def test_process_learning_answer_uses_profile_default_user_routing(tmp_path: Path):
    root = tmp_path / "cereblink"
    user_root = root / "users" / "dengjingjing"
    for rel in ["progress", "reviews", "plans", "sessions", "state"]:
        (user_root / rel).mkdir(parents=True, exist_ok=True)
    (user_root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (user_root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    routing = root / "state" / "user-routing.json"
    routing.parent.mkdir(parents=True, exist_ok=True)
    routing.write_text(json.dumps({
        "profiles": {"feishu2": {"defaultUserId": "dengjingjing"}},
        "feishuUsers": {}
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    process_learning_answer(
        root,
        "clinical-pharmacology",
        "clinical/pharma",
        "临床药理学",
        "理解药代动力学基础",
        "这是一个方向正确但不完整的回答",
        profile="feishu2",
        routing_config_path=routing,
    )

    summary = user_root / "state" / "learning-summary.json"
    assert summary.exists()
    mastery = json.loads((user_root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    assert "clinical-pharmacology" in mastery["concepts"]
