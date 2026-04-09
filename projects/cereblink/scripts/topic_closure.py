from datetime import date
from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root


def topic_title_from_path(topic: str) -> str:
    return " ".join(part.replace("-", " ").replace("_", " ").title() for part in topic.split("/"))


def topic_slug(topic: str) -> str:
    return topic.split("/")[-1]


def update_topic_page(
    root: Path,
    *,
    slug: str,
    topic: str,
    title: str,
    concept_card_path: str | None = None,
    question_card_path: str | None = None,
    user_id: str | None = None,
) -> Path:
    target_root = resolve_user_root(root, user_id)
    topics_dir = target_root / "topics"
    topics_dir.mkdir(parents=True, exist_ok=True)
    page_path = topics_dir / f"{topic_slug(topic)}.md"

    concept_link = f"[[{slug}]]"
    question_link = f"[[{slug}]]"
    page_title = topic_title_from_path(topic)
    today = str(date.today())

    if page_path.exists():
        text = page_path.read_text(encoding="utf-8")
        if concept_link not in text:
            text = text.replace("## Concepts\n", f"## Concepts\n- {concept_link}\n")
        if "## Questions\n" not in text:
            text += "\n## Questions\n"
        if question_link not in text:
            text = text.replace("## Questions\n", f"## Questions\n- {question_link}\n")
        if f"updated: {today}" not in text:
            text = text.replace("type: topic\n", f"type: topic\nupdated: {today}\n")
        page_path.write_text(text, encoding="utf-8")
        return page_path

    content = (
        "---\n"
        f"title: {page_title}\n"
        "type: topic\n"
        "status: active\n"
        f"created: {today}\n"
        f"updated: {today}\n"
        "---\n\n"
        f"# {page_title}\n\n"
        "## Scope\n\n"
        f"- 本专题当前围绕 `{topic}` 相关学习资产进行组织。\n\n"
        "## Concepts\n"
        f"- {concept_link}\n\n"
        "## Questions\n"
        f"- {question_link}\n"
    )
    page_path.write_text(content, encoding="utf-8")
    return page_path
