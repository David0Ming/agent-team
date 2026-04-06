import json
from pathlib import Path


def load_user_routing(config_path: Path) -> dict:
    return json.loads(config_path.read_text(encoding="utf-8"))


def resolve_active_user_id(
    config_path: Path,
    profile: str | None = None,
    feishu_open_id: str | None = None,
) -> str | None:
    data = load_user_routing(config_path)

    if feishu_open_id:
        mapped = data.get("feishuUsers", {}).get(feishu_open_id)
        if mapped:
            return mapped

    if profile:
        return data.get("profiles", {}).get(profile, {}).get("defaultUserId")

    return None
