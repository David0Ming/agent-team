import json
from pathlib import Path

from projects.cereblink.scripts.review_queue import normalize_queue_items


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


def generate_today_plan(queue_path: Path, out_path: Path, tracker_path: Path | None = None) -> None:
    data = json.loads(queue_path.read_text(encoding="utf-8"))
    legacy_items = _dedupe_items(data.get("items", []))
    legacy_status_by_slug = {item["slug"]: item.get("status") for item in legacy_items}
    queue_items = normalize_queue_items(data.get("items", []))
    tracker_concepts = {}
    if tracker_path and tracker_path.exists():
        tracker = json.loads(tracker_path.read_text(encoding="utf-8"))
        tracker_concepts = tracker.get("concepts", {})

    rendered_items = []
    for item in queue_items:
        slug = item["slug"]
        tracker_status = tracker_concepts.get(slug, {}).get("status")
        status = tracker_status or legacy_status_by_slug.get(slug) or "learning"
        rendered_items.append({"slug": slug, "status": status, "due_at": item.get("due_at")})

    unique_items = _dedupe_items(rendered_items)
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
