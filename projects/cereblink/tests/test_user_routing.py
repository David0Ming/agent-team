import json
from pathlib import Path

from projects.cereblink.scripts.user_routing import resolve_active_user_id


def test_resolve_active_user_id_prefers_exact_open_id(tmp_path: Path):
    config = tmp_path / "user-routing.json"
    config.write_text(json.dumps({
        "profiles": {
            "main": {"defaultUserId": "zegang"},
            "feishu2": {"defaultUserId": "dengjingjing"}
        },
        "feishuUsers": {
            "ou_exact_djj": "dengjingjing"
        }
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    assert resolve_active_user_id(config, profile="main", feishu_open_id="ou_exact_djj") == "dengjingjing"


def test_resolve_active_user_id_falls_back_to_profile_default(tmp_path: Path):
    config = tmp_path / "user-routing.json"
    config.write_text(json.dumps({
        "profiles": {
            "main": {"defaultUserId": "zegang"},
            "feishu2": {"defaultUserId": "dengjingjing"}
        },
        "feishuUsers": {}
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    assert resolve_active_user_id(config, profile="main") == "zegang"
    assert resolve_active_user_id(config, profile="feishu2") == "dengjingjing"


def test_resolve_active_user_id_returns_none_when_unmapped(tmp_path: Path):
    config = tmp_path / "user-routing.json"
    config.write_text(json.dumps({
        "profiles": {},
        "feishuUsers": {}
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    assert resolve_active_user_id(config, profile="unknown") is None
