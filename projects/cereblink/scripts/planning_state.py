def derive_planning_state(
    mastery_status: str,
    session_count: int,
    in_review_queue: bool,
    is_due: bool,
    is_overdue: bool,
    manually_dropped: bool,
    manually_dormant: bool,
) -> str:
    if manually_dropped:
        return "dropped"
    if manually_dormant:
        return "dormant"
    if mastery_status == "unlearned" and session_count == 0:
        return "not_started"
    if mastery_status == "mastered" and (in_review_queue or is_due or is_overdue):
        return "reviewing"
    if mastery_status == "mastered":
        return "solid"
    if mastery_status == "fragile" and (in_review_queue or is_due or is_overdue):
        return "reviewing"
    if mastery_status == "fragile":
        return "practicing"
    if mastery_status == "learning" and session_count <= 1:
        return "introduced"
    if mastery_status == "learning":
        return "practicing"
    return "introduced"
