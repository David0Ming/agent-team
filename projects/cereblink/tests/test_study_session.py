import json
from pathlib import Path
from projects.cereblink.scripts.study_session import assess_mastery, update_mastery, write_session_record


def test_update_mastery_creates_new_learning_concept(tmp_path):
    tracker = tmp_path / "mastery-tracker.json"
    tracker.write_text('{"concepts": {}}', encoding="utf-8")
    update_mastery(tracker, slug="reranker", topic="rag/retrieval", status="learning")
    text = tracker.read_text(encoding="utf-8")
    assert '"reranker"' in text
    assert '"status": "learning"' in text


def test_write_session_record_creates_markdown_file(tmp_path):
    path = write_session_record(
        sessions_dir=tmp_path,
        title="Reranker 学习",
        learning_goal="理解 reranker 的作用",
        summary="已完成讲解和追问",
        answer_excerpt="retrieval 负责粗召回，reranker 负责精排。",
        assessment_reason="已经说明两者分工，达到基础掌握。",
        next_step="下一步补清 recall 和 precision 的区别。",
    )
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "理解 reranker 的作用" in text
    assert "已完成讲解和追问" in text
    assert "retrieval 负责粗召回，reranker 负责精排。" in text
    assert "已经说明两者分工，达到基础掌握。" in text
    assert "下一步补清 recall 和 precision 的区别。" in text


def test_assess_mastery_marks_mastered_when_recall_and_rerank_are_clear():
    answer = "retrieval 负责大范围粗召回候选内容，reranker 负责在小候选集上做精细排序。"
    assert assess_mastery(answer) == "mastered"


def test_assess_mastery_marks_unlearned_for_empty_answer():
    answer = ""
    assert assess_mastery(answer) == "unlearned"


def test_assess_mastery_marks_fragile_for_confused_answer():
    answer = "retrieval 是精排，reranker 负责大范围召回。"
    assert assess_mastery(answer) == "fragile"


def test_assess_mastery_keeps_learning_for_vague_answer():
    answer = "reranker 会让结果更好，更准确。"
    assert assess_mastery(answer) == "learning"


def test_update_mastery_creates_session_count_for_new_concept(tmp_path: Path):
    tracker = tmp_path / "mastery-tracker.json"
    tracker.write_text('{"concepts": {}}', encoding="utf-8")
    update_mastery(tracker, slug="reranker", topic="rag/retrieval", status="learning")
    data = json.loads(tracker.read_text(encoding="utf-8"))
    concept = data["concepts"]["reranker"]
    assert concept["session_count"] == 1
    assert concept["manually_dropped"] is False
    assert concept["manually_dormant"] is False


def test_update_mastery_increments_session_count(tmp_path: Path):
    tracker = tmp_path / "mastery-tracker.json"
    tracker.write_text(
        '{"concepts": {"reranker": {"topic": "rag/retrieval", "status": "learning", "last_studied_at": "2026-03-28", "session_count": 1, "manually_dropped": false, "manually_dormant": false}}}',
        encoding="utf-8",
    )
    update_mastery(tracker, slug="reranker", topic="rag/retrieval", status="fragile")
    data = json.loads(tracker.read_text(encoding="utf-8"))
    assert data["concepts"]["reranker"]["session_count"] == 2
    assert data["concepts"]["reranker"]["status"] == "fragile"
