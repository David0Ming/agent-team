import json
from pathlib import Path
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
