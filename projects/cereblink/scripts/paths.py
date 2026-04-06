from pathlib import Path


def resolve_user_root(root: Path, user_id: str | None = None) -> Path:
    if not user_id:
        return root
    return root / "users" / user_id
