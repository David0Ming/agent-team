from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root


def slug_to_title(slug: str) -> str:
    return slug.replace("-", " ").replace("_", " ").strip().title()


def write_concept_card(
    root: Path,
    *,
    slug: str,
    topic: str,
    title: str,
    summary: str,
    next_step: str,
    user_id: str | None = None,
) -> Path:
    target_root = resolve_user_root(root, user_id)
    knowledge_dir = target_root / "knowledge" / Path(topic)
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    card_path = knowledge_dir / f"{slug}.md"

    content = (
        "---\n"
        "type: concept\n"
        "status: seed\n"
        "---\n\n"
        f"# {title or slug_to_title(slug)}\n\n"
        "## Real Problem\n\n"
        f"- 本轮围绕 `{slug}` 形成了稳定学习结果，需要从会话转为可复用知识资产。\n\n"
        "## Why It Matters\n\n"
        f"- 若不收口为卡片，后续复习与迁移成本会升高。\n\n"
        "## Industry-Validated Method\n\n"
        "- 先提炼稳定概念，再用强结构卡片保存，而不是保留原始对话。\n\n"
        "## Transferable Capability\n\n"
        f"- 可迁移到 `{topic}` 相关学习、复习和系统设计。\n\n"
        "## Summary\n\n"
        f"{summary.strip()}\n\n"
        "## Links\n\n"
        f"- Next Step: {next_step.strip()}\n"
    )
    card_path.write_text(content, encoding="utf-8")
    return card_path
