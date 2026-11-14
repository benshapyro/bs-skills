"""Tests for lint_prd.py. Run: python3 scripts/test_lint_prd.py"""
import os
import re
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lint_prd import lint  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))

GOOD = """\
# Online booking
Status: Draft · Size: short · Updated: 2026-11-11

- **S1** A client rebooks from her phone. (users, 2026-10, 3 of 4)
  - Expected: she gets a text confirmation.
- **H1** Bookings reach the calendar within a minute. (owner)
  - Checked by: the owner
- **R1** Clients keep phoning. (owner)
  - Type: value · Endangers: S1, H1
  - Decision: test. This week: a link for a week. Without users: read reviews.
- **R2** Deposits put clients off. (guess → Q1)
  - Type: value, viability · Endangers: H1
  - Decision: reduce. Launch without deposits.
- **Q1** Would clients accept a deposit?
  - Answered by: the owner · Due: 2026-11-20
"""


def messages(text):
    return [msg for _, msg in lint(text)[0]]


class LintTests(unittest.TestCase):
    def test_good_document_passes(self):
        self.assertEqual(messages(GOOD), [])

    def test_reference_example_passes(self):
        path = os.path.join(HERE, "..", "references", "document.md")
        with open(path, encoding="utf-8") as f:
            example = re.search(r"```markdown\n(.*?)```", f.read(), re.S).group(1)
        self.assertEqual(messages(example), [])

    def test_blank_is_flagged(self):
        self.assertTrue(any("blank" in m for m in messages(GOOD + "Pricing: TBD\n")))

    def test_guess_without_question(self):
        text = GOOD.replace("(guess → Q1)", "(guess)")
        self.assertTrue(any("guess must point" in m for m in messages(text)))

    def test_guess_points_to_missing_question(self):
        text = GOOD.replace("(guess → Q1)", "(guess → Q9)")
        self.assertTrue(any("Q9, which is not defined" in m for m in messages(text)))

    def test_users_tag_needs_date(self):
        text = GOOD.replace("(users, 2026-10, 3 of 4)", "(users, 3 of 4)")
        self.assertTrue(any("users tag" in m for m in messages(text)))

    def test_handover_needs_checker_or_stand_in(self):
        text = GOOD.replace("  - Checked by: the owner\n", "")
        self.assertTrue(any("H1 needs Checked by" in m for m in messages(text)))
        unassigned = GOOD.replace("Checked by: the owner", "No checker yet: owner away. Stand-in: builder checks")
        self.assertEqual(messages(unassigned), [])
        no_stand_in = GOOD.replace("Checked by: the owner", "No checker yet: owner away.")
        self.assertTrue(any("H1 needs Checked by" in m for m in messages(no_stand_in)))

    def test_risk_status_is_not_a_decision(self):
        text = GOOD.replace("Decision: reduce.", "Decision: monitoring.")
        self.assertTrue(any("R2 needs a Decision" in m for m in messages(text)))

    def test_test_needs_this_week_and_without_users(self):
        text = GOOD.replace(" Without users: read reviews.", "")
        self.assertTrue(any("lacks This week and Without users" in m for m in messages(text)))
        text = GOOD.replace("This week: a link for a week.", "")
        self.assertTrue(any("lacks This week and Without users" in m for m in messages(text)))

    def test_risk_must_link_to_defined_items(self):
        text = GOOD.replace("Endangers: S1, H1", "Endangers: S7")
        self.assertTrue(any("S7, which is not defined" in m for m in messages(text)))
        text = GOOD.replace("Endangers: S1, H1", "Endangers: nothing")
        self.assertTrue(any("must list the S or H" in m for m in messages(text)))

    def test_unknown_risk_type(self):
        text = GOOD.replace("Type: value ·", "Type: technical ·")
        self.assertTrue(any("unknown type technical" in m for m in messages(text)))
        text = GOOD.replace("Type: value ·", "")
        self.assertTrue(any("R1 has no Type" in m for m in messages(text)))

    def test_question_needs_answerer_and_date(self):
        text = GOOD.replace("Answered by: the owner · Due: 2026-11-20", "Due: soon")
        msgs = messages(text)
        self.assertTrue(any("Q1 has no Answered by" in m for m in msgs))
        self.assertTrue(any("Q1 needs a Due date" in m for m in msgs))

    def test_duplicate_id(self):
        text = GOOD + "- **S1** Another case. (owner)\n"
        self.assertTrue(any("S1 already defined" in m for m in messages(text)))

    def test_missing_source_tag(self):
        text = GOOD.replace("Bookings reach the calendar within a minute. (owner)",
                            "Bookings reach the calendar within a minute.")
        self.assertTrue(any("H1 has no source tag" in m for m in messages(text)))

    def test_length_over_size_is_flagged(self):
        padding = "The salon front desk answers calls. " * 120 + "\n"
        self.assertTrue(any("short PRD should be under" in m for m in messages(GOOD + padding)))
        standard = GOOD.replace("Size: short", "Size: standard")
        self.assertEqual(messages(standard + padding), [])

    def test_logs_and_appendix_do_not_count_toward_length(self):
        padding = "2026-11-11: moved deposits out of scope. " * 120 + "\n"
        self.assertEqual(messages(GOOD + "## Change history\n" + padding), [])
        self.assertEqual(messages(GOOD + "## Appendix: interview notes\n" + padding), [])

    def test_empty_document_reports_missing_sections(self):
        msgs = messages("# Idea\n")
        self.assertEqual(len(msgs), 3)


if __name__ == "__main__":
    unittest.main()
