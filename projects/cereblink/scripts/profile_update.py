import json
from datetime import date
from pathlib import Path

from projects.cereblink.scripts.paths import resolve_user_root


TRIGGERS = [
    ("个人助手", "practiceMainline", "以改造 OpenClaw 成为真正服务自己的个人助手为核心工程对象，在真实高频使用中验证改造价值。"),
    ("openclaw", "practiceMainline", "以改造 OpenClaw 成为真正服务自己的个人助手为核心工程对象，在真实高频使用中验证改造价值。"),
    ("超级个体", "longTermGoal", "成为超级个体 / 产品技术人，具备发现问题、构建产品、编排系统、创造价值的综合能力。"),
    ("多 agent", "shortTermGoal", "提升求职竞争力，重点补齐企业私域问答系统与多 Agent 编排系统相关能力。"),
]


def update_learning_profile_from_text(root: Path, user_input: str, user_id: str | None = None) -> Path:
    target_root = resolve_user_root(root, user_id)
    profile_path = target_root / "state" / "learning-profile.json"
    profile = {}
    if profile_path.exists():
        profile = json.loads(profile_path.read_text(encoding="utf-8"))

    text = user_input.strip().lower()
    for keyword, field, value in TRIGGERS:
        if keyword.lower() in text:
            profile[field] = value

    profile["updatedAt"] = str(date.today())
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return profile_path
