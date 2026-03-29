def decide_djj_action(user_request: str, planning: dict, learning: dict) -> dict:
    text = user_request.strip()
    if "学" in text and ("带我" in text or "现在" in text):
        return {
            "mode": "study",
            "primaryItems": learning.get("recommendedTopics", [])[:1],
        }
    if "安排" in text and "学" in text:
        return {
            "mode": "mixed",
            "primaryItems": planning.get("topPriorities", [])[:2],
            "learningItems": learning.get("recommendedTopics", [])[:1],
        }
    return {
        "mode": "plan",
        "primaryItems": planning.get("topPriorities", [])[:3],
    }
