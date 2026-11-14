"""Stop hook: a one-time reminder to write the handover note when the person is leaving.

Claude Code runs this after every reply. It asks Claude to carry on and write the note
only when all of these hold:
  - the person's latest message sounds like they are stopping for now;
  - the session is in a git project where real work happened (uncommitted changes,
    or commits made since the session started);
  - no handover note in docs/handovers/ was written or changed during this session;
  - it hasn't already reminded once this session.
Otherwise it stays silent. It never writes a note itself.
"""
import json
import os
import re
import subprocess
import sys
import time

STOPPING = re.compile(
    r"\b(stopping|stop (for|here)|done for (the day|today|now|tonight)|that'?s (it|all|enough) for (today|now|tonight)"
    r"|wrap(ping)? (it )?up|call(ing)? it a day|signing off|logging off|heading off|i'?m off\b|good ?night"
    r"|see you tomorrow|end (of|the) (day|session)|write (the|a) handover|handover note)",
    re.IGNORECASE,
)


def latest_person_message(transcript_path):
    """Return the text of the last message the person typed, or ''."""
    last = ""
    try:
        with open(transcript_path, encoding="utf-8") as f:
            for line in f:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if entry.get("type") != "user" or entry.get("isMeta"):
                    continue  # skill text and other injected content are marked isMeta
                origin = (entry.get("origin") or {}).get("kind")
                if origin not in (None, "human"):
                    continue  # messages from other agents, task notices and so on
                content = (entry.get("message") or {}).get("content")
                if isinstance(content, list):
                    texts = [c.get("text", "") for c in content if isinstance(c, dict) and c.get("type") == "text"]
                    content = " ".join(texts) if texts else None
                if isinstance(content, str):
                    text = re.sub(r"<system-reminder>.*?</system-reminder>", "", content, flags=re.DOTALL).strip()
                    if text:
                        last = text
    except OSError:
        pass
    return last


def git(cwd, *args):
    result = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip()


def main():
    try:
        event = json.load(sys.stdin)
    except ValueError:
        return 0
    if event.get("stop_hook_active"):
        return 0
    transcript = event.get("transcript_path") or ""
    cwd = event.get("cwd") or os.getcwd()
    session = re.sub(r"[^A-Za-z0-9_-]", "", str(event.get("session_id") or "unknown"))

    state_dir = os.environ.get("CLAUDE_PLUGIN_DATA") or os.path.join(os.path.expanduser("~"), ".cache", "learning-loop")
    marker = os.path.join(state_dir, "nudged-" + session)
    if os.path.exists(marker):
        return 0

    if not STOPPING.search(latest_person_message(transcript)):
        return 0

    code, root = git(cwd, "rev-parse", "--show-toplevel")
    if code != 0 or not root:
        return 0

    try:
        stat = os.stat(transcript)
        started = getattr(stat, "st_birthtime", stat.st_mtime)
    except OSError:
        started = time.time() - 12 * 3600

    _, status = git(root, "status", "--porcelain")
    _, recent = git(root, "log", "--since=@%d" % int(started), "--format=%H")
    if not status and not recent:
        return 0

    notes = os.path.join(root, "docs", "handovers")
    if os.path.isdir(notes):
        for name in os.listdir(notes):
            if name.endswith(".md") and os.path.getmtime(os.path.join(notes, name)) >= started:
                return 0

    os.makedirs(state_dir, exist_ok=True)
    with open(marker, "w") as f:
        f.write(str(int(time.time())))
    print(json.dumps({
        "decision": "block",
        "reason": (
            "Reminder from the handover skill: the person sounds like they're stopping, real work happened in "
            "this project, and no handover note was written this session. Follow the handover skill now: write one "
            "note in docs/handovers/, then finish your reply. If they aren't actually stopping, ignore this and "
            "carry on. This reminder only appears once per session."
        ),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
