"""Tests for check_skills.py. Run from scripts/: python3 -m unittest test_check_skills"""
import io
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_skills as cs  # noqa: E402

SECTION = cs.SECTION + "\n\n" + cs.EDITIONS[-1][1] + "\n"
LOG = """# Changelog

A record of every change to this skill, most recent first.

## 1.1 — 2026-11-11 09:00 PST

Second.

## 1.0 — 2026-11-10 08:00 PST

First.
"""


def skill(version='"1.1"', section=SECTION, extra=""):
    return f"---\nname: demo\n{extra}metadata:\n  version: {version}\n---\n\n# Demo\n\nBody.\n\n{section}"


class CheckSkills(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.root)

    def run_on(self, name, skill_text=None, log=LOG):
        d = self.root / name
        d.mkdir()
        (d / "SKILL.md").write_text(skill_text or skill())
        if log is not None:
            (d / "CHANGELOG.md").write_text(log)
        return " | ".join(cs.check_skill(d))

    def test_clean(self):
        self.assertEqual(self.run_on("a"), "")

    def test_this_skill_passes(self):
        here = Path(__file__).resolve().parent.parent
        self.assertEqual(cs.check_skill(here), [])
        self.assertEqual(cs.edition((here / "SKILL.md").read_text()), cs.EDITIONS[-1][0])

    def test_documented_layouts_parse(self):
        here = Path(__file__).resolve().parent.parent
        taught = [l for l in (here / "SKILL.md").read_text().splitlines() if l.startswith("## 1.")]
        self.assertTrue(taught)
        self.assertTrue(all(cs.ENTRY.match(l) for l in taught))

    def test_header_problems(self):
        self.assertIn("header says 1.2 but the top entry says 1.1", self.run_on("a", skill('"1.2"')))
        self.assertIn("not major.minor", self.run_on("b", skill('"1.1.0"')))
        self.assertIn("no version under metadata", self.run_on("c", "# no header\n" + SECTION))
        self.assertIn("also stored outside", self.run_on("d", skill(extra="version: 1.1\n")))
        self.assertIn("no CHANGELOG.md", self.run_on("e", log=None))

    def test_order_and_gaps(self):
        swapped = "# Changelog\n\n## 1.0 — 2026-11-10 08:00 PST\n\nx\n\n## 1.1 — 2026-11-11 09:00 PST\n\ny\n"
        self.assertIn("1.0 sits above 1.1", self.run_on("a", skill('"1.0"'), swapped))
        self.assertIn("may be missing", self.run_on("b", skill('"1.3"'), LOG.replace("## 1.1", "## 1.3")))
        self.assertIn("appears twice", self.run_on("c", log=LOG.replace("## 1.0", "## 1.1")))
        major = LOG.replace("## 1.1 — 2026-11-11 09:00", "## 2.0 — 2026-11-10 07:00")
        self.assertEqual(self.run_on("d", skill('"2.0"'), major), "entry 2.0 is dated earlier than the entry below it")
        self.assertIn("not understood", self.run_on("e", log=LOG + "\n## 0.9 sometime\n"))

    def test_same_version_allowed_for_section_update(self):
        log = LOG.replace("## 1.1 — 2026-11-11 09:00 PST", "## 1.1 — 2026-11-12 10:00 PST\n\n"
                          "Version unchanged: maintenance text moved to edition 1.\n\n## 1.1 — 2026-11-11 09:00 PST")
        self.assertEqual(self.run_on("a", log=log), "")

    def test_missing_time_unless_marked(self):
        self.assertIn("1.0 has no time", self.run_on("a", log=LOG.replace(" 08:00 PST", "")))
        marked = LOG.replace(" 08:00 PST", "").replace("First.", "(time not recorded) First.")
        self.assertEqual(self.run_on("b", log=marked), "")

    def test_earlier_history_is_not_checked(self):
        tail = "\n## Earlier history of other\n\n## 9.9 — 2020-01-01 00:00 PST\n\n## nonsense\n"
        self.assertEqual(self.run_on("a", log=LOG + tail), "")

    def test_maintenance_section(self):
        self.assertIn("section missing", self.run_on("a", skill(section="")))
        self.assertIn("matches no edition", self.run_on("b", skill(section=SECTION.replace("flag it", "say so"))))
        self.assertEqual(self.run_on("c", skill(section=SECTION.replace(" why, when", "\nwhy, when"))), "")
        cs.EDITIONS.append(("2", "A newer standard."))
        try:
            self.assertIn("is edition 1; the standard is edition 2", self.run_on("d"))
        finally:
            cs.EDITIONS.pop()

    def test_folder_of_skills(self):
        self.run_on("one")
        self.run_on("two", log=None)
        with redirect_stdout(io.StringIO()) as out:
            self.assertEqual(cs.main([str(self.root / "one")]), 0)
            self.assertEqual(cs.main([str(self.root)]), 1)
        self.assertEqual(out.getvalue(), "No problems.\ntwo: no CHANGELOG.md\n")


if __name__ == "__main__":
    unittest.main()
