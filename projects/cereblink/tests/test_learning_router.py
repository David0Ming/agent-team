import json
from pathlib import Path

from projects.cereblink.scripts.learning_router import route_learning_action


def test_route_learning_action_defaults_to_new_learning(tmp_path: Path):
    route = route_learning_action(tmp_path, slug="reranker", user_input="我想学习 reranker")
    assert route["actionType"] == "new_learning"
    assert route["profileUpdate"] is False


def test_route_learning_action_prefers_review_when_user_explicitly_requests_it(tmp_path: Path):
    route = route_learning_action(tmp_path, slug="reranker", user_input="来考我一下 reranker")
    assert route["actionType"] == "review"
    assert "review" in route["closureMode"]


def test_route_learning_action_prefers_cardify_on_explicit_closure_request(tmp_path: Path):
    route = route_learning_action(tmp_path, slug="reranker", user_input="把这一轮整理成卡片")
    assert route["actionType"] == "cardify"
    assert "concept_card" in route["closureMode"]


def test_route_learning_action_uses_review_queue_as_routing_signal(tmp_path: Path):
    (tmp_path / "reviews").mkdir(parents=True)
    (tmp_path / "reviews" / "review-queue.json").write_text(json.dumps({
        "items": [{"slug": "reranker", "due_at": "2026-04-09"}]
    }, ensure_ascii=False), encoding="utf-8")

    route = route_learning_action(tmp_path, slug="reranker", user_input="继续学习这个点")
    assert route["actionType"] == "review"


def test_route_learning_action_writes_profile_update_for_stable_direction_change(tmp_path: Path):
    route = route_learning_action(tmp_path, slug="career-mainline", user_input="以后按这个来，默认学这个主线")
    assert route["actionType"] == "profile_update"
    assert route["profileUpdate"] is True
