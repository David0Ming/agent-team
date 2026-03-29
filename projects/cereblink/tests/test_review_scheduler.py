import json
from pathlib import Path
from projects.cereblink.scripts.review_scheduler import enqueue_review


def test_enqueue_review_adds_learning_review_item(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text('{"items": []}', encoding="utf-8")
    enqueue_review(queue, slug="reranker", status="learning", days=1)
    data = json.loads(queue.read_text(encoding="utf-8"))
    assert data["items"][0]["slug"] == "reranker"
    assert data["items"][0]["status"] == "learning"


def test_enqueue_review_deduplicates_same_slug_and_keeps_earliest_due_date(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text('{"items": []}', encoding="utf-8")
    enqueue_review(queue, slug="reranker", status="learning", days=3)
    enqueue_review(queue, slug="reranker", status="fragile", days=1)
    data = json.loads(queue.read_text(encoding="utf-8"))
    assert len(data["items"]) == 1
    assert data["items"][0]["slug"] == "reranker"
    assert data["items"][0]["status"] == "fragile"


def test_enqueue_review_keeps_single_item_per_slug_and_updates_status(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text('{"items": []}', encoding="utf-8")
    enqueue_review(queue, slug="reranker", status="learning", days=3)
    enqueue_review(queue, slug="reranker", status="fragile", days=1)
    data = json.loads(queue.read_text(encoding="utf-8"))
    assert len(data["items"]) == 1
    assert data["items"][0]["status"] == "fragile"


def test_enqueue_review_adds_last_enqueued_at_field(tmp_path):
    queue = tmp_path / "review-queue.json"
    queue.write_text('{"items": []}', encoding="utf-8")
    enqueue_review(queue, slug="retrieval", status="learning", days=1)
    data = json.loads(queue.read_text(encoding="utf-8"))
    assert "last_enqueued_at" in data["items"][0]
