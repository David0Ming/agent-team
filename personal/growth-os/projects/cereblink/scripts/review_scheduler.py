import json
from datetime import date, timedelta
from pathlib import Path


def enqueue_review(queue_path: Path, slug: str, status: str, days: int) -> None:
    data = json.loads(queue_path.read_text(encoding="utf-8"))
    items = data.setdefault("items", [])

    new_due = str(date.today() + timedelta(days=days))
    existing = next((item for item in items if item.get("slug") == slug), None)
    stamp = str(date.today())

    if existing is None:
        items.append({
            "slug": slug,
            "status": status,
            "due_at": new_due,
            "last_enqueued_at": stamp,
        })
    else:
        existing["status"] = status
        existing["due_at"] = min(existing.get("due_at", new_due), new_due)
        existing["last_enqueued_at"] = stamp

    queue_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def next_review_days(status: str) -> list[int]:
    if status == "learning":
        return [1, 3]
    if status == "mastered":
        return [7, 14]
    if status == "fragile":
        return [1, 3]
    return []
