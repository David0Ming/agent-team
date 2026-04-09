import json
from pathlib import Path
from projects.cereblink.scripts.learn_loop import process_learning_answer


def test_process_learning_answer_updates_full_learning_loop(tmp_path):
    root = tmp_path / "cereblink"
    (root / "progress").mkdir(parents=True)
    (root / "reviews").mkdir(parents=True)
    (root / "plans").mkdir(parents=True)
    (root / "sessions").mkdir(parents=True)
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")
    (root / "plans" / "today.md").write_text('', encoding="utf-8")

    result = process_learning_answer(
        root=root,
        slug="reranker",
        topic="rag/retrieval",
        title="Reranker 学习",
        learning_goal="理解为什么 RAG 需要 reranker",
        answer="retrieval 负责大范围粗召回候选内容，reranker 负责在小候选集上做精细排序。",
    )

    mastery = json.loads((root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    queue = json.loads((root / "reviews" / "review-queue.json").read_text(encoding="utf-8"))
    today = (root / "plans" / "today.md").read_text(encoding="utf-8")

    assert result["status"] == "mastered"
    assert result["route"]["actionType"] == "new_learning"
    assert result["concept_card"] is None
    assert result["question_card"] is None
    assert result["topic_page"] is None
    assert mastery["concepts"]["reranker"]["status"] == "mastered"
    assert queue["items"][0]["slug"] == "reranker"
    assert "status" not in queue["items"][0]
    assert "# Today Plan" in today
    assert "`reranker` · mastered" in today
    assert "原因：" in today
    assert Path(result["session_record"]).exists()


def test_process_learning_answer_generates_learning_summary(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "plans").mkdir()
    (root / "sessions").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    process_learning_answer(root, "reranker", "rag/retrieval", "Reranker 学习", "理解 reranker", "reranker 负责对小候选集精排")

    summary = root / "state" / "learning-summary.json"
    assert summary.exists()
    data = json.loads(summary.read_text(encoding="utf-8"))
    assert "topicStates" in data


def test_process_learning_answer_uses_profile_default_user_routing(tmp_path: Path):
    root = tmp_path / "cereblink"
    user_root = root / "users" / "dengjingjing"
    for rel in ["progress", "reviews", "plans", "sessions", "state"]:
        (user_root / rel).mkdir(parents=True, exist_ok=True)
    (user_root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (user_root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    routing = root / "state" / "user-routing.json"
    routing.parent.mkdir(parents=True, exist_ok=True)
    routing.write_text(json.dumps({
        "profiles": {"feishu2": {"defaultUserId": "dengjingjing"}},
        "feishuUsers": {}
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    process_learning_answer(
        root,
        "clinical-pharmacology",
        "clinical/pharma",
        "临床药理学",
        "理解药代动力学基础",
        "这是一个方向正确但不完整的回答",
        profile="feishu2",
        routing_config_path=routing,
    )

    summary = user_root / "state" / "learning-summary.json"
    assert summary.exists()
    mastery = json.loads((user_root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    assert "clinical-pharmacology" in mastery["concepts"]


def test_process_learning_answer_writes_concept_card_when_route_requests_cardify(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "plans").mkdir()
    (root / "sessions").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    result = process_learning_answer(
        root,
        "learning-router",
        "workflow",
        "学习动作路由器",
        "把这一轮整理成卡片",
        "路由器负责把已有状态输入统一收束成当前学习动作决策。",
    )

    assert result["route"]["actionType"] == "cardify"
    assert result["concept_card"] is not None
    assert result["question_card"] is not None
    assert result["topic_page"] is not None
    card = Path(result["concept_card"])
    assert card.exists()
    text = card.read_text(encoding="utf-8")
    assert "## Real Problem" in text
    assert "## Industry-Validated Method" in text
    qcard = Path(result["question_card"])
    assert qcard.exists()
    qtext = qcard.read_text(encoding="utf-8")
    assert "## Question" in qtext
    assert "## Answer" in qtext
    tpage = Path(result["topic_page"])
    assert tpage.exists()
    ttext = tpage.read_text(encoding="utf-8")
    assert "## Concepts" in ttext
    assert "## Questions" in ttext


def test_process_learning_answer_planning_update_skips_session_and_mastery_write(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "plans").mkdir()
    (root / "sessions").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")

    result = process_learning_answer(
        root,
        "plan-anchor",
        "workflow",
        "学习计划调整",
        "帮我安排一下今天学什么",
        "今天优先继续 OpenClaw 与 CerebLink 主线。",
    )

    mastery = json.loads((root / "progress" / "mastery-tracker.json").read_text(encoding="utf-8"))
    assert result["route"]["actionType"] == "planning_update"
    assert result["status"] == "planning"
    assert result["session_record"] is None
    assert result["concept_card"] is None
    assert result["question_card"] is None
    assert result["topic_page"] is None
    assert "plan-anchor" not in mastery["concepts"]


def test_process_learning_answer_updates_profile_when_route_requests_profile_update(tmp_path: Path):
    root = tmp_path
    (root / "progress").mkdir()
    (root / "reviews").mkdir()
    (root / "plans").mkdir()
    (root / "sessions").mkdir()
    (root / "state").mkdir()
    (root / "progress" / "mastery-tracker.json").write_text('{"concepts": {}}', encoding="utf-8")
    (root / "reviews" / "review-queue.json").write_text('{"items": []}', encoding="utf-8")
    (root / "state" / "learning-profile.json").write_text('{"userId":"zegang"}', encoding="utf-8")

    result = process_learning_answer(
        root,
        "career-mainline",
        "workflow",
        "主线调整",
        "以后按这个来，默认学超级个体和个人助手主线",
        "后续学习应围绕超级个体与个人助手改造展开。",
    )

    assert result["route"]["actionType"] == "profile_update"
    assert result["profile_path"] is not None
    profile = json.loads(Path(result["profile_path"]).read_text(encoding="utf-8"))
    assert "超级个体" in profile["longTermGoal"]
    assert "个人助手" in profile["practiceMainline"]
