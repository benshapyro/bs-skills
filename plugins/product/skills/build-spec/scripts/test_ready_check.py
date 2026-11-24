"""ready_check.py passes a good spec and catches each kind of bad one.
Run from this folder: python3 -m unittest test_ready_check"""
import contextlib
import io
import os
import unittest

import ready_check

HERE = os.path.dirname(os.path.abspath(__file__))

GOOD = """# Spec: invoice export
## Why this run
The October export took two hours by hand on 2026-10-31. [src: finance lead]
## Done when
```
./scripts/acceptance.sh
```
Passes if: exits 0.
Seen failing: swapped two columns on 2026-11-09; 1 failed.
## Pieces
<!-- a comment with a [[slot]] is ignored -->
### 1. One invoice
Check: `pytest -k single` passes on 5 varied fixtures.
Decided by: pytest
Seen failing: agent breaks it on purpose after it passes
### 2. Month export
Check: `pytest -k month` passes.
**Decided by:** pytest
Seen failing: dropped the last row; 1 failed.
## Real-world checks
| Check | Judged by | Judge on |
|---|---|---|
| Totals match the ledger | reconcile.py | now |
Person: Dana, finance lead
Task: exports October and sends it to the accountant
Judge on: 2026-12-05
## Baseline
`pytest` passed 212 on 2026-11-09.
## Rules that must still hold
| Rule today | Enforced where | New path it must cover | Test through the whole run |
|---|---|---|---|
| Voided invoices are never exported | export/filter.py | The new month export | `pytest -k month_skips_voided` |
## Facts to use
- Amounts are in cents. [src: models/invoice.py]
## Agent rules
| Rule | Enforced by |
|---|---|
| No production writes | deny rule |
## Not in this run
- PDF export
## Launch blockers
| Command | Could stall on | Cleared by | Proven |
|---|---|---|---|
| acceptance.sh | staging key | ops lead | 2026-11-10: op read printed it |
## Settings to apply
Deny Bash(psql *prod*).
## Still open
- None
## Start command
```
claude -p --permission-mode auto --max-turns 120 --output-format stream-json --verbose "/goal
Read specs/invoice-export.md in full." > run-log.jsonl
```
"""


# (find, replace with, expected exit code, expected message)
CASES = [(old, new, 1, msg) for old, new, msg in [
    ("PDF export", "TBD", "to-do marker"),
    ("ops lead", "[[person]]", "template slot"),
    ("## Not in this run\n- PDF export\n", "", "no '## Not in this run'"),
    ("## Not in this run\n- PDF export\n", "```\n## Not in this run\n```\n", "no '## Not in this run'"),
    ("- PDF export", "None", "'## Not in this run' is empty"),
    ("| No production writes | deny rule |\n", "", "'## Agent rules': fill in"),
    ("```\n./scripts/acceptance.sh\n```\n", "Run it.\n", "Done when: put the command"),
    ("Passes if:", "Result:", "'Passes if:'"),
    ("Seen failing: swapped two columns on 2026-11-09; 1 failed.", "Seen failing: no", "Done when: never seen failing"),
    ("Seen failing: dropped the last row; 1 failed.\n", "", "'2. Month export': add 'Seen failing:'"),
    ("**Decided by:** pytest", "", "'2. Month export': no 'Decided by:'"),
    ("### ", "#### ", "'### ' heading"),
    ("| reconcile.py |", "| |", "who or what judges it"),
    ("| now |", "| soon |", "now or a date"),
    ("Person: Dana, finance lead\n", "", "needs 'Person:'"),
    ("Judge on: 2026-12-05", "Judge on: later", "needs 'Person:'"),
    ("| deny rule |", "| |", "'Enforced by'"),
    ("| Voided invoices are never exported | export/filter.py | The new month export | `pytest -k month_skips_voided` |\n",
     "", "'## Rules that must still hold' is empty"),
    ("## Rules that must still hold\n", "## Other\n", "no '## Rules that must still hold'"),
    ("| `pytest -k month_skips_voided` |", "| |", "needs a test through the whole run"),
    ("| The new month export |", "| |", "needs a test through the whole run"),
    ("2026-11-10: op read", "op read", "'Proven' needs a date"),
    ("| ops lead |", "| |", "fill every column"),
    ("claude -p ", "claude ", "headless"),
    ("--max-turns 120 ", "", "cap the tool enforces"),
    ("--permission-mode auto", "--dangerously-skip-permissions", "switches off every block"),
    ("--permission-mode auto ", "", "approval prompts"),
    ("--output-format stream-json ", "", "full log"),
    (" > run-log.jsonl", "", "output saved to a file"),
    ("specs/invoice-export.md", "specs/other.md", "points at this spec"),
    ('in full."', "in full.", "won't paste cleanly"),
]] + [
    ("- None", "- Which tax field? Finance lead, by 2026-11-11", 2, "still open"),
    ("2026-11-10: op read printed it", "not yet, by 2026-11-12", 2, "not proven yet"),
    ("# Spec", "# Spec", 0, "READY"),
    ("| Rule today | Enforced where | New path it must cover | Test through the whole run |\n|---|---|---|---|\n"
     "| Voided invoices are never exported | export/filter.py | The new month export | `pytest -k month_skips_voided` |\n",
     "None found: searched export/ and tests/ for filters and guards on 2026-11-09.\n", 0, "READY"),
]


def run(text, light=False):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = ready_check.report(text, "invoice-export.md", light)
    return code, out.getvalue()


class ReadyCheck(unittest.TestCase):
    def test_cases(self):
        for old, new, code, msg in CASES:
            with self.subTest(msg):
                self.assertIn(old, GOOD)
                got, out = run(GOOD.replace(old, new))
                self.assertEqual(got, code, out)
                self.assertIn(msg, out)

    def test_brief_checks_only_done_when_and_command(self):
        brief = GOOD[GOOD.index("## Done when"):GOOD.index("## Pieces")] + GOOD[GOOD.index("## Start command"):]
        self.assertEqual(run(brief.replace(" > ", " | tee "), light=True)[0], 0)
        got, out = run(brief.replace("--max-turns 120 ", ""), light=True)
        self.assertEqual(got, 1)
        self.assertIn("cap the tool enforces", out)

    def test_blank_template_has_gaps(self):
        with open(os.path.join(HERE, "..", "references", "spec-template.md"), encoding="utf-8") as f:
            self.assertEqual(run(f.read())[0], 1)

    def test_gap_outranks_hold(self):
        self.assertEqual(run(GOOD.replace("- None", "- Tax field?").replace("| ops lead |", "| |"))[0], 1)


if __name__ == "__main__":
    unittest.main()
