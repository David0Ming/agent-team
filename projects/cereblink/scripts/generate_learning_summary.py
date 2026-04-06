import json
from datetime import date
from pathlib import Path
from projects.cereblink.scripts.paths import resolve_user_root
from projects.cereblink.scripts.planning_state import derive_planning_state
from projects.cereblink.scripts.review_queue import normalize_queue_items


def generate_learning_summary(root: Path, user_id: str | None = None) -> Path:
    target_root = resolve_user_root(root, user_id)
    tracker = json.loads((target_root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    queue = json.loads((target_root / "reviews" / "review-queue.json").read_text(encoding="utf-8"))
    normalized_items = normalize_queue_items(queue.get("items", []))
    queue_by_slug = {item["slug"]: item for item in normalized_items}
    topic_states = {}
    recommended = []
    for slug, concept in tracker.get("concepts", {}).items():
        item = queue_by_slug.get(slug, {})
        state = derive_planning_state(
            mastery_status=concept.get("status", "learning"),
            session_count=int(concept.get("session_count", 0)),
            in_review_queue=slug in queue_by_slug,
            is_due=item.get("due_at") == str(date.today()),
            is_overdue=bool(item.get("due_at") and item.get("due_at") < str(date.today())),
            manually_dropped=bool(concept.get("manually_dropped", False)),
            manually_dormant=bool(concept.get("manually_dormant", False)),
        )
        topic_states[slug] = state
        recommended.append(slug)
    summary = {
        "generatedAt": str(date.today()),
        "currentTrack": "mixed",
        "recommendedTopics": recommended[:3],
        "topicStates": topic_states,
        "reviewPressure": "high" if len(normalized_items) >= 3 else "medium" if normalized_items else "low",
        "recentProgress": "summary generated",
        "todayLearned": [],
        "doNotRepeatToday": [],
        "recommendedDuration": 30,
        "rationale": "优先根据当前学习状态与复习队列给出最小学习摘要。",
    }
    out = target_root / "state" / "learning-summary.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out
