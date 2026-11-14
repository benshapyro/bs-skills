#!/usr/bin/env python3
"""Ready check for a spec from references/spec-template.md. Standard library only.

Usage: python3 ready_check.py [--light] SPEC.md   (--light: a brief; Done when + Start command)
Exit: 0 READY, 1 GAPS (listed), 2 ON HOLD (complete; an open question or unproven blocker waits).
"""
import os
import re
import shlex
import sys

FULL = ["Why this run", "Done when", "Pieces", "Real-world checks", "Baseline", "Facts to use",
        "Agent rules", "Not in this run", "Launch blockers", "Settings to apply", "Still open",
        "Start command"]
TABLES = ["Real-world checks", "Agent rules", "Launch blockers"]
UNFINISHED = [(r"\[\[.*?\]\]", "template slot"), (r"\b(TODO|TBD|FIXME|XXX)\b|\?\?\?", "to-do marker")]
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
EMPTY = {"none", "none.", "n/a", "-", "nothing"}


def sections_of(text):
    """'## Heading' -> body, skipping headings inside code fences."""
    found, current, fenced = {}, None, False
    for line in text.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("## "):
            current = line[3:].strip()
            found[current] = []
        elif current is not None:
            found[current].append(line)
    return {k: "\n".join(v) for k, v in found.items()}


def field(body, name):
    m = re.search(r"(?im)^[ \t>-]*" + re.escape(name) + r":[ \t]*(\S.*)$", body.replace("*", ""))
    return m.group(1).strip() if m else ""


def items(body):
    lines = [l.strip().lstrip("-*0123456789. ") for l in body.splitlines() if l.strip()]
    return [l for l in lines if l.lower() not in EMPTY]


def table(body):
    rows = [l.strip().strip("|") for l in body.splitlines() if l.strip().startswith("|")]
    split = lambda r: [c.strip() for c in re.split(r"(?<!\\)\|", r)]
    head = [h.lower() for h in split(rows[0])] if rows else []
    return [dict(zip(head, split(r) + [""] * len(head))) for r in rows[2:]]


def fences(body):
    return re.findall(r"```[^\n]*\n(.*?)```", body, re.S)


def timed(value):
    return value.lower() == "now" or bool(DATE.search(value))


def seen_failing(body, where):
    value = field(body, "Seen failing").lower().rstrip(".")
    if not value:
        return [f"{where}: add 'Seen failing:' (the break and its output)"]
    if value in {"no", "never", "not yet", "none"}:
        return [f"{where}: never seen failing; break working code on purpose and record the output"]
    return []


def flag(words, name):
    for i, w in enumerate(words):
        if w == name and i + 1 < len(words):
            return words[i + 1]
        if w.startswith(name + "="):
            return w.split("=", 1)[1]
    return ""


def check_command(body, spec_name):
    """Parse the start command as a shell line; check what a headless run needs."""
    code = fences(body)
    try:
        words = shlex.split(code[0].replace("\\\n", " ")) if code else []
    except ValueError as e:
        return [f"Start command: won't paste cleanly into a shell ({e})"]
    mode, need = flag(words, "--permission-mode"), []
    if not words or os.path.basename(words[0]) != "claude" or not {"-p", "--print"} & set(words):
        need.append("a headless 'claude -p' command in a ``` block")
    if not any(re.fullmatch(r"\d+(\.\d+)?", flag(words, f)) for f in ("--max-turns", "--max-budget-usd")):
        need.append("a cap the tool enforces (--max-budget-usd N or --max-turns N)")
    if "--dangerously-skip-permissions" in words or mode == "bypassPermissions":
        need.append("no permission bypass; it switches off every block")
    elif not mode:
        need.append("--permission-mode; a headless run can't answer approval prompts")
    if flag(words, "--output-format") != "stream-json" or "--verbose" not in words:
        need.append("--output-format stream-json --verbose for a full log")
    if not (any(w in (">", ">>", "tee") for w in words[:-1]) or any(re.match(r">>?\w", w) for w in words)):
        need.append("the output saved to a file (> run-log.jsonl) for the review")
    if spec_name and words and spec_name not in max(words, key=len):
        need.append(f"a prompt that points at this spec ({spec_name})")
    return [f"Start command needs {n}" for n in need]


def check(text, spec_name, light=False):
    """Return (gaps, holds)."""
    text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text, flags=re.S)
    gaps, holds, secs = [], [], sections_of(text)
    for n, line in enumerate(text.splitlines(), 1):
        gaps += [f"line {n}: unfinished ({what}): {line.strip()[:80]}"
                 for pat, what in UNFINISHED if re.search(pat, line)][:1]

    for name in ["Done when", "Start command"] if light else FULL:
        if name not in secs:
            gaps.append(f"no '## {name}' section")
        elif name != "Still open" and not items(secs[name]):
            gaps.append(f"'## {name}' is empty")
        elif name in TABLES and not table(secs[name]):
            gaps.append(f"'## {name}': fill in the table rows")

    done = secs.get("Done when")
    if done is not None:
        if not any(b.strip() for b in fences(done)):
            gaps.append("Done when: put the command in a ``` block")
        if not field(done, "Passes if"):
            gaps.append("Done when: add 'Passes if:' (the exact passing result)")
        gaps += [] if light else seen_failing(done, "Done when")
    if "Start command" in secs:
        gaps += check_command(secs["Start command"], None if light else spec_name)
    if light:
        return gaps, holds

    parts = re.split(r"(?m)^### +(.+)$", secs.get("Pieces", ""))
    if "Pieces" in secs and len(parts) < 3:
        gaps.append("Pieces: give each piece its own '### ' heading")
    for title, body in zip(parts[1::2], parts[2::2]):
        gaps += [f"Piece '{title}': no '{f}:'" for f in ("Check", "Decided by") if not field(body, f)]
        gaps += seen_failing(body, f"Piece '{title}'")

    real = secs.get("Real-world checks", "")
    for row in table(real):
        if not row.get("judged by") or not timed(row.get("judge on", "")):
            gaps.append(f"Real-world check '{row.get('check', '')[:60]}': say who or what judges it, now or a date")
    if "Real-world checks" in secs and not (field(real, "Person") and field(real, "Task")
                                            and timed(field(real, "Judge on"))):
        gaps.append("Hands-on test needs 'Person:', 'Task:' and 'Judge on:' (now or a date)")

    for row in table(secs.get("Agent rules", "")):
        if not row.get("enforced by"):
            gaps.append(f"Agent rule with nothing under 'Enforced by': {row.get('rule', '')[:60]}")

    for row in table(secs.get("Launch blockers", "")):
        cmd, proven = row.get("command", "")[:50], row.get("proven", "")
        if not (row.get("could stall on") and row.get("cleared by") and DATE.search(proven)):
            gaps.append(f"Launch blocker '{cmd}': fill every column; 'Proven' needs a date")
        elif "not yet" in proven.lower():
            holds.append(f"launch blocker not proven yet: {cmd} ({proven})")

    holds += [f"still open: {i[:70]}" for i in items(secs.get("Still open", ""))]
    return gaps, holds


def report(text, spec_name, light=False):
    gaps, holds = check(text, spec_name, light)
    for line in gaps or holds:
        print(f"- {line}")
    if gaps:
        print(f"GAPS: {len(gaps)} to fix, then run again.")
        return 1
    if holds:
        print(f"ON HOLD: complete, but {len(holds)} item(s) stop the launch.")
        return 2
    print("READY: nothing missing.")
    return 0


def main(argv):
    paths = [a for a in argv if a != "--light"]
    if len(paths) != 1:
        print(__doc__.strip())
        return 1
    try:
        with open(paths[0], encoding="utf-8") as f:
            return report(f.read(), os.path.basename(paths[0]), "--light" in argv)
    except OSError as e:
        print(f"GAPS: cannot read {paths[0]}: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
