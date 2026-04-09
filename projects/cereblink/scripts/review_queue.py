def normalize_queue_items(items: list[dict]) -> list[dict]:
    normalized: dict[str, dict] = {}

    for item in items:
        slug = item["slug"]
        current = normalized.get(slug)
        due_at = item.get("due_at")
        last_enqueued_at = item.get("last_enqueued_at")

        if current is None:
            current = {"slug": slug}
            if due_at:
                current["due_at"] = due_at
            if last_enqueued_at:
                current["last_enqueued_at"] = last_enqueued_at
            normalized[slug] = current
            continue

        if due_at and (not current.get("due_at") or due_at < current["due_at"]):
            current["due_at"] = due_at
        if last_enqueued_at and last_enqueued_at > current.get("last_enqueued_at", ""):
            current["last_enqueued_at"] = last_enqueued_at

    return [normalized[slug] for slug in sorted(normalized)]
