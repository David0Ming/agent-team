from pathlib import Path


def test_seed_cards_exist_for_default_user():
    base = Path("projects/cereblink/users/zegang")
    assert (base / "knowledge/rag/retrieval.md").exists()
    assert (base / "questions/rag/why-rag-needs-reranker.md").exists()
    assert (base / "topics/rag-foundations.md").exists()
