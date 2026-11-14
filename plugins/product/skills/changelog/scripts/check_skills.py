#!/usr/bin/env python3
"""Check skill histories. Reads only; changes nothing.

  python3 check_skills.py <skill folder, or a folder of skills>

Prints one line per problem and exits 1, or prints "No problems." and exits 0.
"""
import re
import sys
from pathlib import Path

# Every edition of the standard maintenance text, oldest first; the last is the
# standard. To revise it, append a new edition and never edit an old one.
SECTION = "## Keeping this skill up to date"
EDITIONS = [
    ("1", "Each change gets a new entry at the top of CHANGELOG.md saying what changed, "
          "why, when and on whose say-so, and the `version` in the header moves to match. "
          "The first number goes up only when someone who already knows the skill would "
          "see it behave differently; every other change raises the second. Normal use "
          "never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it "
          "only with permission."),
]

ENTRY = re.compile(r"^## v?(\d+)\.(\d+) +[—–-]+ +(\d{4}-\d{2}-\d{2})(?: +(\d{1,2}:\d{2}))?")
SET_APART = "## Earlier history"  # reconstructed or merged history; not checked


def flat(text):
    return " ".join(text.split())


def header_version(skill_text):
    """Return (metadata version or None, True if a version is stored anywhere else)."""
    m = re.match(r"---\n(.*?)\n---\n", skill_text, re.S)
    head = m.group(1) if m else ""
    meta = re.search(r"^metadata:[ \t]*\n((?:[ \t]+.*(?:\n|$))*)", head, re.M)
    found = re.search(r"^\s+version:\s*[\"']?([^\"'\s]+)", meta.group(1), re.M) if meta else None
    elsewhere = bool(re.search(r"^version:", head, re.M))
    return (found.group(1) if found else None), elsewhere


def edition(skill_text):
    """Return the edition label of the maintenance section, None if absent, '?' if unrecognised."""
    parts = re.split(r"^" + re.escape(SECTION) + r"[ \t]*$", skill_text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return None
    body = re.split(r"^#{1,2} ", parts[1], maxsplit=1, flags=re.M)[0]
    return next((label for label, text in EDITIONS if flat(body) == flat(text)), "?")


def read_entries(log_text):
    """Return (entries, problems). Each entry is [major, minor, date, time, body]."""
    entries, problems = [], []
    for n, line in enumerate(log_text.splitlines(), start=1):
        if line.startswith(SET_APART):
            break
        if line.startswith("## "):
            m = ENTRY.match(line)
            if m:
                entries.append([int(m[1]), int(m[2]), m[3], m[4] or "", ""])
            else:
                problems.append(f"line {n}: entry heading not understood: {line.strip()}")
        elif entries:
            entries[-1][4] += line.lower() + "\n"
    return entries, problems


def check_order(entries):
    problems = [f"entry {e[0]}.{e[1]} has no time" for e in entries
                if not e[3] and "time not recorded" not in e[4]]
    for new, old in zip(entries, entries[1:]):
        nv, ov = (new[0], new[1]), (old[0], old[1])
        if new[2] + new[3].zfill(5) < old[2] + old[3].zfill(5):
            problems.append(f"entry {nv[0]}.{nv[1]} is dated earlier than the entry below it")
        if nv == ov:
            if "version unchanged" not in new[4]:
                problems.append(f"version {nv[0]}.{nv[1]} appears twice")
        elif nv < ov:
            problems.append(f"version {nv[0]}.{nv[1]} sits above {ov[0]}.{ov[1]}")
        elif nv not in ((ov[0], ov[1] + 1), (ov[0] + 1, 0)):
            problems.append(f"{ov[0]}.{ov[1]} is followed by {nv[0]}.{nv[1]}: an entry may be missing")
    return problems


def check_skill(folder):
    skill_text = (folder / "SKILL.md").read_text(encoding="utf-8")
    version, elsewhere = header_version(skill_text)
    problems = []
    if version is None:
        problems.append("no version under metadata: in the header")
    elif not re.fullmatch(r"\d+\.\d+", version):
        problems.append(f"header version {version} is not major.minor")
    if elsewhere or (folder / "VERSION").exists():
        problems.append("a version is also stored outside metadata:")
    log = folder / "CHANGELOG.md"
    if not log.exists():
        problems.append("no CHANGELOG.md")
    else:
        entries, found = read_entries(log.read_text(encoding="utf-8"))
        problems += found + check_order(entries)
        if not entries:
            problems.append("CHANGELOG.md has no entries")
        elif version and f"{entries[0][0]}.{entries[0][1]}" != version:
            problems.append(f"header says {version} but the top entry says {entries[0][0]}.{entries[0][1]}: "
                            "possibly an unrecorded change, so ask before fixing")
    label, standard = edition(skill_text), EDITIONS[-1][0]
    if label is None:
        problems.append("maintenance section missing")
    elif label == "?":
        problems.append("maintenance section matches no edition of the standard text")
    elif label != standard:
        problems.append(f"maintenance section is edition {label}; the standard is edition {standard}")
    return problems


def skill_folders(root):
    if (root / "SKILL.md").exists():
        return [root]
    return sorted(p.parent for p in root.rglob("SKILL.md") if not any(s.startswith(".") for s in p.parts))


def main(argv):
    if len(argv) != 1 or not Path(argv[0]).is_dir():
        print(__doc__.strip(), file=sys.stderr)
        return 2
    lines = [f"{f.name}: {p}" for f in skill_folders(Path(argv[0]).resolve()) for p in check_skill(f)]
    print("\n".join(lines) or "No problems.")
    return 1 if lines else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
