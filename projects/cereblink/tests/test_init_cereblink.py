from pathlib import Path
from projects.cereblink.scripts.init_cereblink import init_repo, required_paths


def test_required_paths_contains_core_project_structure():
    paths = required_paths(Path("projects/cereblink"))
    assert Path("projects/cereblink/knowledge") in paths
    assert Path("projects/cereblink/questions") in paths
    assert Path("projects/cereblink/progress/mastery-tracker.json") in paths
    assert Path("projects/cereblink/reviews/review-queue.json") in paths


def test_init_repo_creates_json_state_files(tmp_path):
    root = tmp_path / "cereblink"
    init_repo(root)
    assert (root / "progress" / "mastery-tracker.json").exists()
    assert (root / "reviews" / "review-queue.json").exists()
    assert (root / "plans" / "today.md").exists()
    assert (root / "state" / "learning-summary.json").exists()


def test_init_repo_creates_isolated_user_roots(tmp_path):
    root = tmp_path / "cereblink"
    init_repo(root, user_id="zegang")
    init_repo(root, user_id="dengjingjing")

    assert (root / "users" / "zegang" / "progress" / "mastery-tracker.json").exists()
    assert (root / "users" / "zegang" / "reviews" / "review-queue.json").exists()
    assert (root / "users" / "zegang" / "state" / "learning-summary.json").exists()
    assert (root / "users" / "dengjingjing" / "progress" / "mastery-tracker.json").exists()
    assert (root / "users" / "dengjingjing" / "reviews" / "review-queue.json").exists()
    assert (root / "users" / "dengjingjing" / "state" / "learning-summary.json").exists()
