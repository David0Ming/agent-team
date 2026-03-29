from projects.cereblink.scripts.planning_state import derive_planning_state


def test_unlearned_without_sessions_maps_to_not_started():
    assert derive_planning_state(
        mastery_status="unlearned",
        session_count=0,
        in_review_queue=False,
        is_due=False,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=False,
    ) == "not_started"


def test_learning_with_one_session_maps_to_introduced():
    assert derive_planning_state(
        mastery_status="learning",
        session_count=1,
        in_review_queue=False,
        is_due=False,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=False,
    ) == "introduced"


def test_learning_with_three_sessions_maps_to_practicing():
    assert derive_planning_state(
        mastery_status="learning",
        session_count=3,
        in_review_queue=False,
        is_due=False,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=False,
    ) == "practicing"


def test_fragile_due_review_maps_to_reviewing():
    assert derive_planning_state(
        mastery_status="fragile",
        session_count=2,
        in_review_queue=True,
        is_due=True,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=False,
    ) == "reviewing"


def test_mastered_without_pressure_maps_to_solid():
    assert derive_planning_state(
        mastery_status="mastered",
        session_count=4,
        in_review_queue=False,
        is_due=False,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=False,
    ) == "solid"


def test_manual_dormant_wins():
    assert derive_planning_state(
        mastery_status="learning",
        session_count=5,
        in_review_queue=False,
        is_due=False,
        is_overdue=False,
        manually_dropped=False,
        manually_dormant=True,
    ) == "dormant"


def test_manual_dropped_wins():
    assert derive_planning_state(
        mastery_status="mastered",
        session_count=9,
        in_review_queue=True,
        is_due=True,
        is_overdue=True,
        manually_dropped=True,
        manually_dormant=False,
    ) == "dropped"
