import json
from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root


TEMPLATES = {
    "concept-card.md": "---\ntype: concept\nstatus: seed\n---\n\n# {{title}}\n\n## Summary\n\n## Links\n",
    "question-card.md": "---\ntype: question\nstatus: seed\n---\n\n# {{title}}\n\n## Question\n\n## Answer\n",
    "topic-page.md": "---\ntype: topic\nstatus: seed\n---\n\n# {{title}}\n\n## Scope\n\n## Concepts\n",
    "session-record.md": "---\ntype: session\nstatus: seed\n---\n\n# {{title}}\n\n## Goal\n\n## Notes\n",
    "review-record.md": "---\ntype: review\nstatus: seed\n---\n\n# {{title}}\n\n## Concept\n\n## Outcome\n",
}


def required_paths(root: Path) -> list[Path]:
    return [
        root / "knowledge",
        root / "questions",
        root / "topics",
        root / "sessions",
        root / "reviews" / "history",
        root / "progress" / "mastery-tracker.json",
        root / "reviews" / "review-queue.json",
        root / "plans" / "today.md",
        root / "dashboards",
        root / "state" / "learning-summary.json",
        root / "templates",
        root / "docs",
    ]


def init_repo(root: Path, user_id: str | None = None) -> None:
    target_root = resolve_user_root(root, user_id)
    for path in required_paths(target_root):
        if path.suffix:
            path.parent.mkdir(parents=True, exist_ok=True)
            if not path.exists():
                if path.name.endswith('.json'):
                    path.write_text(json.dumps({}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
                else:
                    path.write_text("", encoding="utf-8")
        else:
            path.mkdir(parents=True, exist_ok=True)

    templates_dir = target_root / "templates"
    templates_dir.mkdir(parents=True, exist_ok=True)
    for name, content in TEMPLATES.items():
        template_path = templates_dir / name
        if not template_path.exists():
            template_path.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    init_repo(Path("projects/cereblink"))
