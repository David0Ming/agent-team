import json
from datetime import date, datetime
from pathlib import Path


MASTERED_HINTS = [
    "粗召回",
    "召回",
    "小候选",
    "候选集",
    "精排",
    "精细排序",
    "排序",
    "reranker",
    "retrieval",
]

CONFUSED_PHRASES = [
    "retrieval是精排",
    "retrieval  是精排",
    "retrieval负责精排",
    "retrieval 负责精排",
    "retrieval负责精细排序",
    "retrieval 负责精细排序",
    "reranker负责大范围召回",
    "reranker 负责大范围召回",
    "reranker负责粗召回",
    "reranker 负责粗召回",
]


def assess_mastery(answer: str) -> str:
    raw = answer.strip()
    if not raw:
        return "unlearned"

    normalized = raw.lower().replace("，", "").replace("。", "").replace("：", "").replace(" ", "")
    for phrase in CONFUSED_PHRASES:
        if phrase.replace(" ", "") in normalized:
            return "fragile"

    text = raw.lower()
    matched = 0
    for hint in MASTERED_HINTS:
        if hint.lower() in text:
            matched += 1
    if matched >= 4:
        return "mastered"
    return "learning"


def assessment_reason(answer: str, status: str) -> str:
    if status == "mastered":
        return "回答已明确覆盖 retrieval 的粗召回职责，以及 reranker 在小候选集上的精排职责。"
    if status == "fragile":
        return "回答出现了 retrieval 与 reranker 分工混淆，说明已有印象但当前理解不稳定。"
    if status == "unlearned":
        return "当前没有形成有效回答，系统无法确认对该知识点已有理解。"
    return "回答体现出方向正确，但对关键分工或精度/召回区别的表达还不够完整。"


def suggested_next_step(status: str) -> str:
    if status == "mastered":
        return "下一步补强 recall 与 precision 的区别，并理解为什么 reranker 不直接跑全库。"
    if status == "fragile":
        return "下一步先重新说清 retrieval 和 reranker 的分工，再用一个具体例子验证自己没有答反。"
    if status == "unlearned":
        return "下一步先看一遍 retrieval 与 reranker 的定义，再尝试用自己的话复述它们各自负责什么。"
    return "下一步请用自己的话复述 retrieval 和 reranker 的分工，再补上 recall 与 precision 的区别。"


def update_mastery(tracker_path: Path, slug: str, topic: str, status: str) -> None:
    data = json.loads(tracker_path.read_text(encoding="utf-8"))
    concepts = data.setdefault("concepts", {})
    existing = concepts.get(slug, {})
    concepts[slug] = {
        "topic": topic,
        "status": status,
        "last_studied_at": str(date.today()),
        "session_count": int(existing.get("session_count", 0)) + 1,
        "manually_dropped": bool(existing.get("manually_dropped", False)),
        "manually_dormant": bool(existing.get("manually_dormant", False)),
    }
    tracker_path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def write_session_record(
    sessions_dir: Path,
    title: str,
    learning_goal: str,
    summary: str,
    answer_excerpt: str = "",
    assessment_reason: str = "",
    next_step: str = "",
) -> Path:
    sessions_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    path = sessions_dir / f"{stamp}.md"
    path.write_text(
        f"# {title}\n\n"
        f"## 学习目标\n{learning_goal}\n\n"
        f"## 总结\n{summary}\n\n"
        f"## 回答内容\n{answer_excerpt}\n\n"
        f"## 判断理由\n{assessment_reason}\n\n"
        f"## 下一步建议\n{next_step}\n",
        encoding="utf-8",
    )
    return path
