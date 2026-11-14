"""Run: python -m pytest scripts/test_audit_workflows.py  (or python scripts/test_audit_workflows.py)"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent))
from audit_workflows import audit  # noqa: E402

DATA = Path(__file__).parent / "testdata"


def messages(name):
    return [r["message"] for r in audit(DATA / name)]


def test_installer_review_gets_the_main_warnings():
    m = " ".join(messages("installer-review.yml"))
    for phrase in ["moving tag", "timeout-minutes", "concurrency", "No model", "turn cap", "draft", "fork", "every push"]:
        assert phrase in m, phrase


def test_installer_mention_is_open_to_anyone():
    assert any("Anyone who can comment" in x for x in messages("installer-mention.yml"))


def test_tuned_review_is_clean():
    assert messages("tuned-review.yml") == []


def test_pull_request_target_with_head_checkout_is_critical():
    res = audit(DATA / "unsafe-target.yml")
    assert any(r["severity"] == "critical" and "pull_request_target" in r["message"] for r in res)


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
