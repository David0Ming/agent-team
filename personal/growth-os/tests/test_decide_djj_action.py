import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))
from decide_djj_action import decide_djj_action


def test_decide_djj_action_returns_plan_for_today_work_request():
    result = decide_djj_action(
        user_request="今天做什么",
        planning={"topPriorities": ["完善招银简历"], "learningBudget": 30},
        learning={"recommendedTopics": ["reranker"], "recommendedDuration": 30},
    )
    assert result["mode"] == "plan"
    assert result["primaryItems"] == ["完善招银简历"]


def test_decide_djj_action_returns_study_for_explicit_learning_request():
    result = decide_djj_action(
        user_request="现在带我学 reranker",
        planning={"topPriorities": ["完善招银简历"], "learningBudget": 30},
        learning={"recommendedTopics": ["reranker"], "recommendedDuration": 30},
    )
    assert result["mode"] == "study"
    assert result["primaryItems"] == ["reranker"]


def test_decide_djj_action_returns_mixed_for_schedule_and_learning_conflict():
    result = decide_djj_action(
        user_request="今天怎么安排，顺便看看要不要学点东西",
        planning={"topPriorities": ["完善招银简历"], "learningBudget": 30},
        learning={"recommendedTopics": ["reranker"], "recommendedDuration": 30},
    )
    assert result["mode"] == "mixed"
