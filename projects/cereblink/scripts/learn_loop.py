from pathlib import Path

from projects.cereblink.scripts.card_closure import write_concept_card
from projects.cereblink.scripts.generate_learning_summary import generate_learning_summary
from projects.cereblink.scripts.paths import resolve_user_root
from projects.cereblink.scripts.generate_today import generate_today_plan
from projects.cereblink.scripts.learning_router import route_learning_action
from projects.cereblink.scripts.profile_update import update_learning_profile_from_text
from projects.cereblink.scripts.question_closure import write_question_card
from projects.cereblink.scripts.review_scheduler import enqueue_review, next_review_days
from projects.cereblink.scripts.topic_closure import update_topic_page
from projects.cereblink.scripts.user_routing import resolve_active_user_id
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
    user_id: str | None = None,
    profile: str | None = None,
    feishu_open_id: str | None = None,
    routing_config_path: Path | None = None,
) -> dict:
    if user_id is None and routing_config_path is not None:
        user_id = resolve_active_user_id(
            routing_config_path,
            profile=profile,
            feishu_open_id=feishu_open_id,
        )

    target_root = resolve_user_root(root, user_id)
    route = route_learning_action(
        root,
        slug=slug,
        user_input=learning_goal,
        user_id=user_id,
    )
    tracker_path = target_root / "progress" / "mastery-tracker.json"
    queue_path = target_root / "reviews" / "review-queue.json"
    today_path = target_root / "plans" / "today.md"
    sessions_dir = target_root / "sessions"

    if route["actionType"] == "planning_update":
        status = "planning"
        reason = "当前轮次被判定为学习计划调整，而不是知识点学习或复习。"
        next_step = "下一步根据 today plan 执行对应学习项，并在完成后再进入知识收口。"
        session_record = None
        concept_card = None
        question_card = None
        topic_page = None
    else:
        status = assess_mastery(answer)
        reason = assessment_reason(answer, status)
        next_step = suggested_next_step(status)
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
        if "review_queue" in route["closureMode"] and days_list:
            enqueue_review(queue_path, slug=slug, status=status, days=days_list[0])

        concept_card = None
        if "concept_card" in route["closureMode"]:
            concept_card = write_concept_card(
                root,
                slug=slug,
                topic=topic,
                title=title,
                summary=answer,
                next_step=next_step,
                user_id=user_id,
            )

        question_card = None
        if "question_card" in route["closureMode"]:
            question_card = write_question_card(
                root,
                slug=slug,
                topic=topic,
                title=title,
                learning_goal=learning_goal,
                answer=answer,
                user_id=user_id,
            )

        topic_page = None
        if "topic_page" in route["closureMode"]:
            topic_page = update_topic_page(
                root,
                slug=slug,
                topic=topic,
                title=title,
                concept_card_path=str(concept_card) if concept_card else None,
                question_card_path=str(question_card) if question_card else None,
                user_id=user_id,
            )

    profile_path = None
    if route.get("profileUpdate"):
        profile_path = update_learning_profile_from_text(root, learning_goal, user_id=user_id)

    generate_today_plan(queue_path, today_path, tracker_path=tracker_path)
    generate_learning_summary(root, user_id=user_id)

    return {
        "status": status,
        "assessment_reason": reason,
        "next_step": next_step,
        "session_record": str(session_record) if session_record else None,
        "today_plan": str(today_path),
        "route": route,
        "concept_card": str(concept_card) if concept_card else None,
        "question_card": str(question_card) if question_card else None,
        "topic_page": str(topic_page) if topic_page else None,
        "profile_path": str(profile_path) if profile_path else None,
    }
