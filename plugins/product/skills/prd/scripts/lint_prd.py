#!/usr/bin/env python3
"""Mechanical checks for a PRD in the prd skill's format.

Checks what must be exact every time: no blanks, unique IDs, required fields
on situations (S), handover conditions (H), risks (R) and open questions (Q),
links between them, and length against a "Size:" line. Quality is for review.

Usage: python3 lint_prd.py PRD.md
Exit codes: 0 no problems, 1 problems listed, 2 file could not be read.
"""
import re
import sys

ITEM = re.compile(r"^- \*\*([SHRQ])(\d+)\*\*")
SOURCE = re.compile(r"\((users|doc|owner|guess)\b([^)]*)\)", re.I)
GUESS = re.compile(r"\(guess\b([^)]*)\)", re.I)
BLANK = re.compile(
    r"\bTBD\b|\bTODO\b|\?\?\?|\bXXX*\b|\[\s*\.{3}\s*\]|lorem ipsum"
    r"|\bto be (?:decided|determined|confirmed)\b"
    r"|\[(?:fill|insert|add|placeholder)[^\]]*\]",
    re.I,
)
YEAR = re.compile(r"\b(?:19|20)\d{2}\b")
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
TYPES = {"value", "usability", "feasibility", "viability", "harm"}
DECISIONS = ("test", "reduce", "accept", "cut", "stop")
SIZE = re.compile(r"\bSize:\s*(short|standard)\b", re.I)
LIMITS = {"short": 700, "standard": 1500}
UNCOUNTED = re.compile(r"#+\s*(decision log|change history|appendix)", re.I)


def field(text, label):
    """Value after 'Label:' up to the next '·' or line end, or None."""
    m = re.search(rf"\b{label}:\s*([^·\n]*)", text, re.I)
    return m.group(1).strip() if m else None


def parse(lines):
    """Return items as dicts: kind, id, line number, joined text."""
    items, current = [], None
    for n, line in enumerate(lines, 1):
        m = ITEM.match(line)
        if m:
            current = {"kind": m.group(1), "id": m.group(1) + m.group(2),
                       "line": n, "text": line}
            items.append(current)
        elif current and line.strip() and line[:1] in (" ", "\t"):
            current["text"] += "\n" + line
        else:
            current = None
    return items


def body_words(lines):
    """Words outside code blocks, headings, logs and appendices."""
    count, skipping, in_code = 0, False, False
    for line in lines:
        if line.strip().startswith("```"):
            in_code = not in_code
        elif line.startswith("#"):
            skipping = bool(UNCOUNTED.match(line))
        elif not (in_code or skipping):
            count += len(line.split())
    return count


def lint(text):
    lines = text.splitlines()
    problems = []
    in_code = False
    for n, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code and BLANK.search(line):
            problems.append((n, f"unfilled blank: {BLANK.search(line).group(0)!r}"))
        for m in SOURCE.finditer(line):
            if m.group(1).lower() == "users" and not YEAR.search(m.group(2)):
                problems.append((n, "users tag needs when they were heard from"))
        for m in GUESS.finditer(line):
            qs = re.findall(r"Q\d+", m.group(1))
            if not qs:
                problems.append((n, "guess must point to the Q item that settles it, e.g. (guess → Q2)"))

    items = parse(lines)
    seen = {}
    for it in items:
        if it["id"] in seen:
            problems.append((it["line"], f"{it['id']} already defined on line {seen[it['id']]}"))
        else:
            seen[it["id"]] = it["line"]
    defined = set(seen)

    for n, line in enumerate(lines, 1):
        for m in GUESS.finditer(line):
            for q in re.findall(r"Q\d+", m.group(1)):
                if q not in defined:
                    problems.append((n, f"guess points to {q}, which is not defined"))

    for it in items:
        t, n, i = it["text"], it["line"], it["id"]
        k = it["kind"]
        if k in "SHR" and not SOURCE.search(t):
            problems.append((n, f"{i} has no source tag"))
        if k == "H":
            if not field(t, "Checked by") and not (field(t, "No checker yet") is not None and field(t, "Stand-in")):
                problems.append((n, f"{i} needs Checked by, or No checker yet plus a Stand-in"))
        if k == "R":
            kind = field(t, "Type")
            if not kind:
                problems.append((n, f"{i} has no Type"))
            else:
                bad = [x for x in re.split(r"\s*(?:,|/|\band\b)\s*", kind.lower()) if x and x not in TYPES]
                if bad:
                    problems.append((n, f"{i} has unknown type {', '.join(bad)}"))
            links = re.findall(r"\b[SH]\d+\b", field(t, "Endangers") or "")
            if not links:
                problems.append((n, f"{i} must list the S or H items it endangers"))
            for link in links:
                if link not in defined:
                    problems.append((n, f"{i} endangers {link}, which is not defined"))
            decision = (field(t, "Decision") or "").lower()
            if not decision.startswith(DECISIONS):
                problems.append((n, f"{i} needs a Decision starting with one of: {', '.join(DECISIONS)}"))
            elif decision.startswith("test") and not (field(t, "This week") and field(t, "Without users")):
                problems.append((n, f"{i} is a test but lacks This week and Without users"))
        if k == "Q":
            if not field(t, "Answered by"):
                problems.append((n, f"{i} has no Answered by"))
            if not DATE.search(field(t, "Due") or ""):
                problems.append((n, f"{i} needs a Due date as YYYY-MM-DD"))

    for kind, name in (("S", "situations"), ("H", "handover conditions"), ("R", "risks")):
        if not any(it["kind"] == kind for it in items):
            problems.append((0, f"no {name} ({kind}1, {kind}2, ...) found"))

    size = SIZE.search(text)
    words = body_words(lines)
    if size and words > LIMITS[size.group(1).lower()]:
        limit = LIMITS[size.group(1).lower()]
        problems.append((0, f"main body is {words} words; a {size.group(1).lower()} PRD should be under about {limit}"))
    return sorted(problems), items


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    try:
        with open(argv[1], encoding="utf-8") as f:
            text = f.read()
    except OSError as e:
        print(f"could not read {argv[1]}: {e}")
        return 2
    problems, items = lint(text)
    for n, msg in problems:
        print(f"line {n}: {msg}" if n else msg)
    counts = {k: sum(1 for it in items if it["kind"] == k) for k in "SHRQ"}
    summary = ", ".join(f"{v} {k}" for k, v in counts.items())
    words = body_words(text.splitlines())
    print(f"{'PROBLEMS' if problems else 'OK'}: {len(problems)} problem(s); items {summary}; {words} main-body words")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
