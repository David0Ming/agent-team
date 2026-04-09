import json
from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root
from projects.cereblink.scripts.review_queue import normalize_queue_items


DEFAULT_ROUTE = {
    "actionType": "new_learning",
    "closureMode": "session+mastery+summary+review_queue",
    "profileUpdate": False,
    "reason": ["default to new learning when no stronger routing signal exists"],
}


def _safe_read_json(path: Path, fallback: dict) -> dict:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def route_learning_action(
    root: Path,
    *,
    slug: str,
    user_input: str,
    user_id: str | None = None,
) -> dict:
    target_root = resolve_user_root(root, user_id)
    state_root = target_root / "state"
    progress_root = target_root / "progress"
    review_root = target_root / "reviews"
    sessions_root = target_root / "sessions"

    profile = _safe_read_json(state_root / "learning-profile.json", {})
    summary = _safe_read_json(state_root / "learning-summary.json", {})
    tracker = _safe_read_json(progress_root / "mastery-tracker.json", {"concepts": {}})
    queue = _safe_read_json(review_root / "review-queue.json", {"items": []})

    concepts = tracker.get("concepts", {})
    concept = concepts.get(slug, {})
    queue_items = normalize_queue_items(queue.get("items", []))
    queue_by_slug = {item["slug"]: item for item in queue_items}
    in_queue = slug in queue_by_slug
    has_concept = slug in concepts
    mastery_status = concept.get("status")
    recent_summary_topics = set(summary.get("recommendedTopics", []))
    recent_session_exists = any(sessions_root.glob("*.md"))

    text = user_input.strip().lower()
    reasons: list[str] = []

    if any(k in text for k in ["整理成卡片", "收成卡片", "写成卡片", "cardify", "收口"]):
        reasons.append("user explicitly asked to close the round into cards")
        return {
            "actionType": "cardify",
            "closureMode": "session+mastery+summary+concept_card+question_card+topic_page",
            "profileUpdate": False,
            "reason": reasons,
        }

    if any(k in text for k in ["考我", "复习", "回忆", "quiz", "review"]):
        reasons.append("user explicitly asked for review/recall mode")
        return {
            "actionType": "review",
            "closureMode": "session+mastery+summary+review_queue",
            "profileUpdate": False,
            "reason": reasons,
        }

    if any(k in text for k in ["没懂", "搞反", "纠正", "澄清", "clarify", "repair"]):
        reasons.append("user signaled confusion or repair instead of fresh learning")
        if has_concept:
            reasons.append("concept already exists in mastery tracker")
        return {
            "actionType": "clarification",
            "closureMode": "session+mastery+summary+concept_card",
            "profileUpdate": False,
            "reason": reasons,
        }

    if any(k in text for k in ["以后按这个来", "以后就按这个", "默认学", "长期目标改成", "主线改成"]):
        reasons.append("user explicitly changed stable learning direction")
        return {
            "actionType": "profile_update",
            "closureMode": "session+summary+profile",
            "profileUpdate": True,
            "reason": reasons,
        }

    if any(k in text for k in ["学习计划", "今日学习", "今天学什么", "安排一下", "plan"]):
        reasons.append("user asked to adjust planning rather than learn a concept directly")
        return {
            "actionType": "planning_update",
            "closureMode": "summary+today",
            "profileUpdate": False,
            "reason": reasons,
        }

    if in_queue:
        reasons.append("topic is already present in review queue")
        return {
            "actionType": "review",
            "closureMode": "session+mastery+summary+review_queue",
            "profileUpdate": False,
            "reason": reasons,
        }

    if mastery_status in {"fragile", "mastered", "learning"} and has_concept:
        reasons.append(f"concept already exists with mastery status={mastery_status}")
        if slug in recent_summary_topics or recent_session_exists:
            reasons.append("recent state suggests this is continuation rather than brand new learning")
            return {
                "actionType": "clarification",
                "closureMode": "session+mastery+summary+concept_card+question_card+topic_page",
                "profileUpdate": False,
                "reason": reasons,
            }

    if profile.get("defaultDomain"):
        reasons.append("learning-profile provides stable domain context")

    fallback = dict(DEFAULT_ROUTE)
    fallback["reason"] = reasons or DEFAULT_ROUTE["reason"]
    return fallback
