from pathlib import Path

from projects.cereblink.scripts.generate_learning_summary import generate_learning_summary
from projects.cereblink.scripts.generate_today import generate_today_plan
from projects.cereblink.scripts.review_scheduler import enqueue_review, next_review_days
from projects.cereblink.scripts.study_session import (
    assess_mastery,
    assessment_reason,
    suggested_next_step,
    update_mastery,
    write_session_record,
)


def process_learning_answer(
    root: Path,
    slug: str,
    topic: str,
    title: str,
    learning_goal: str,
    answer: str,
) -> dict:
    status = assess_mastery(answer)
    reason = assessment_reason(answer, status)
    next_step = suggested_next_step(status)
    tracker_path = root / "progress" / "mastery-tracker.json"
    queue_path = root / "reviews" / "review-queue.json"
    today_path = root / "plans" / "today.md"
    sessions_dir = root / "sessions"

    update_mastery(tracker_path, slug=slug, topic=topic, status=status)
    session_record = write_session_record(
        sessions_dir=sessions_dir,
        title=title,
        learning_goal=learning_goal,
        summary=answer,
        answer_excerpt=answer,
        assessment_reason=reason,
        next_step=next_step,
    )

    days_list = next_review_days(status)
    if days_list:
        enqueue_review(queue_path, slug=slug, status=status, days=days_list[0])

    generate_today_plan(queue_path, today_path)
    generate_learning_summary(root)

    return {
        "status": status,
        "assessment_reason": reason,
        "next_step": next_step,
        "session_record": str(session_record),
        "today_plan": str(today_path),
    }
