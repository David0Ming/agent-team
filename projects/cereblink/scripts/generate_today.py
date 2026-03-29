import json
from pathlib import Path


PRIORITY = {"fragile": 0, "learning": 1, "unlearned": 2, "mastered": 3}
REASON = {
    "fragile": "原因：这个知识点处于易遗忘状态，应优先回补。",
    "learning": "原因：这个知识点还在学习中，需要趁热巩固。",
    "unlearned": "原因：这个知识点还没真正学过，应先建立基础理解。",
    "mastered": "原因：这个知识点已掌握，做低频复习即可。",
}


def action_text(item: dict) -> str:
    slug = item["slug"]
    status = item["status"]
    if status == "unlearned":
        return f"- 先学 `{slug}`"
    return f"- `{slug}` · {status}"


def _dedupe_items(items: list[dict]) -> list[dict]:
    best = {}
    for item in items:
        slug = item["slug"]
        current = best.get(slug)
        if current is None or PRIORITY.get(item.get("status"), 9) < PRIORITY.get(current.get("status"), 9):
            best[slug] = item
    return list(best.values())


def generate_today_plan(queue_path: Path, out_path: Path) -> None:
    data = json.loads(queue_path.read_text(encoding="utf-8"))
    unique_items = _dedupe_items(data.get("items", []))
    items = sorted(unique_items, key=lambda x: PRIORITY.get(x.get("status"), 9))[:3]

    lines = [
        "# Today Plan",
        "",
        "## 今日重点",
        f"今天建议优先处理 {len(items)} 个学习项，先急后缓，避免贪多。",
        "",
    ]

    for item in items:
        lines.extend(
            [
                action_text(item),
                f"  {REASON.get(item['status'], '原因：这是今天应处理的学习项。')}",
            ]
        )

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
