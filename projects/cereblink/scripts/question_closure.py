from datetime import date
from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root


def infer_question_title(title: str, learning_goal: str) -> str:
    text = learning_goal.strip()
    if text:
        return text[0].upper() + text[1:]
    return f"{title} 的关键问题"


def infer_question_type(learning_goal: str) -> str:
    text = learning_goal.lower()
    if "为什么" in learning_goal or "why" in text:
        return "why"
    if "如何" in learning_goal or "how" in text:
        return "how"
    return "what"


def write_question_card(
    root: Path,
    *,
    slug: str,
    topic: str,
    title: str,
    learning_goal: str,
    answer: str,
    user_id: str | None = None,
) -> Path:
    target_root = resolve_user_root(root, user_id)
    questions_dir = target_root / "questions" / Path(topic)
    questions_dir.mkdir(parents=True, exist_ok=True)
    path = questions_dir / f"{slug}.md"

    question_title = infer_question_title(title, learning_goal)
    question_type = infer_question_type(learning_goal)
    today = str(date.today())
    content = (
        "---\n"
        f"title: {question_title}\n"
        "type: question\n"
        f"question_type: {question_type}\n"
        f"domain: {topic.split('/')[0] if '/' in topic else topic}\n"
        f"primary_concept: {slug}\n"
        "status: active\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "---\n\n"
        f"# {question_title}\n\n"
        "## Question\n\n"
        f"{learning_goal.strip()}\n\n"
        "## Answer\n\n"
        f"{answer.strip()}\n"
    )
    path.write_text(content, encoding="utf-8")
    return path
