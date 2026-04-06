import json
from projects.cereblink.scripts.generate_today import generate_today_plan


def test_generate_today_plan_limits_items_to_three(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text(json.dumps({"items": [
        {"slug": "a", "status": "fragile", "due_at": "2026-03-28"},
        {"slug": "b", "status": "learning", "due_at": "2026-03-28"},
        {"slug": "c", "status": "mastered", "due_at": "2026-03-28"},
        {"slug": "d", "status": "learning", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    out = tmp_path / "today.md"
    generate_today_plan(queue, out)
    text = out.read_text(encoding="utf-8")
    assert text.count("- ") == 3


def test_generate_today_plan_adds_focus_and_reason_labels(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text(json.dumps({"items": [
        {"slug": "reranker", "status": "fragile", "due_at": "2026-03-28"},
        {"slug": "retrieval", "status": "learning", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    out = tmp_path / "today.md"
    generate_today_plan(queue, out)
    text = out.read_text(encoding="utf-8")
    assert "# Today Plan" in text
    assert "## 今日重点" in text
    assert "原因：" in text


def test_generate_today_plan_prioritizes_fragile_and_marks_unlearned_as_study(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text(json.dumps({"items": [
        {"slug": "new-concept", "status": "unlearned", "due_at": "2026-03-28"},
        {"slug": "reranker", "status": "fragile", "due_at": "2026-03-28"},
        {"slug": "retrieval", "status": "learning", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    out = tmp_path / "today.md"
    generate_today_plan(queue, out)
    text = out.read_text(encoding="utf-8")
    assert text.index("`reranker`") < text.index("`retrieval`")
    assert "先学 `new-concept`" in text


def test_generate_today_plan_deduplicates_same_slug(tmp_path):
    queue = tmp_path / "review-queue.json"
    out = tmp_path / "today.md"
    queue.write_text(json.dumps({"items": [
        {"slug": "reranker", "status": "fragile", "due_at": "2026-03-28"},
        {"slug": "reranker", "status": "learning", "due_at": "2026-03-29"},
        {"slug": "retrieval", "status": "learning", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    generate_today_plan(queue, out)
    text = out.read_text(encoding="utf-8")
    assert text.count("`reranker`") == 1


def test_generate_today_plan_uses_tracker_status_when_legacy_queue_is_dirty(tmp_path):
    root = tmp_path / "cereblink"
    (root / "reviews").mkdir(parents=True)
    (root / "progress").mkdir()
    out = root / "plans" / "today.md"
    out.parent.mkdir()
    queue = root / "reviews" / "review-queue.json"
    tracker = root / "progress" / "mastery-tracker.json"

    queue.write_text(json.dumps({"items": [
        {"slug": "reranker", "status": "mastered", "due_at": "2026-03-29", "last_enqueued_at": "2026-03-29"},
        {"slug": "reranker", "status": "learning", "due_at": "2026-03-29"},
    ]}), encoding="utf-8")
    tracker.write_text(json.dumps({
        "concepts": {
            "reranker": {
                "topic": "rag/retrieval",
                "status": "mastered",
                "last_studied_at": "2026-03-29",
                "session_count": 1,
                "manually_dropped": False,
                "manually_dormant": False,
            }
        }
    }), encoding="utf-8")

    generate_today_plan(queue, out, tracker_path=tracker)
    text = out.read_text(encoding="utf-8")

    assert "`reranker` · mastered" in text
    assert "`reranker` · learning" not in text


def test_generate_today_plan_limits_to_three_unique_items(tmp_path):
    queue = tmp_path / "review-queue.json"
    out = tmp_path / "today.md"
    queue.write_text(json.dumps({"items": [
        {"slug": "a", "status": "fragile", "due_at": "2026-03-28"},
        {"slug": "b", "status": "learning", "due_at": "2026-03-28"},
        {"slug": "c", "status": "unlearned", "due_at": "2026-03-28"},
        {"slug": "d", "status": "mastered", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    generate_today_plan(queue, out)
    text = out.read_text(encoding="utf-8")
    assert text.count("- ") <= 3


def test_generate_today_plan_isolated_per_user_root(tmp_path):
    root = tmp_path / "cereblink"
    zegang_queue = root / "users" / "zegang" / "reviews" / "review-queue.json"
    zegang_queue.parent.mkdir(parents=True)
    zegang_out = root / "users" / "zegang" / "plans" / "today.md"
    zegang_out.parent.mkdir(parents=True)

    deng_queue = root / "users" / "dengjingjing" / "reviews" / "review-queue.json"
    deng_queue.parent.mkdir(parents=True)
    deng_out = root / "users" / "dengjingjing" / "plans" / "today.md"
    deng_out.parent.mkdir(parents=True)

    zegang_queue.write_text(json.dumps({"items": [
        {"slug": "rag-retrieval", "status": "fragile", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")
    deng_queue.write_text(json.dumps({"items": [
        {"slug": "clinical-pharmacology", "status": "learning", "due_at": "2026-03-28"}
    ]}), encoding="utf-8")

    generate_today_plan(zegang_queue, zegang_out)
    generate_today_plan(deng_queue, deng_out)

    zegang_text = zegang_out.read_text(encoding="utf-8")
    deng_text = deng_out.read_text(encoding="utf-8")

    assert "rag-retrieval" in zegang_text
    assert "clinical-pharmacology" not in zegang_text
    assert "clinical-pharmacology" in deng_text
    assert "rag-retrieval" not in deng_text
