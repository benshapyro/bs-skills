#!/usr/bin/env python3
"""Check a repo's Claude GitHub Action workflows against the tuning checklist.

Usage:
    python audit_workflows.py <repo-root-or-workflow-file> [--json]

Reads every workflow under .github/workflows/ that uses anthropics/claude-code-action
and reports what Step 3 and Step 4 of the skill would change. It only reads files.

It checks structure, not behaviour. A clean result means the files look tuned, not
that the reviewer works: only the planted-fault test (Step 6) shows that.

Exit code: 2 if anything is marked "critical", otherwise 0.
Needs PyYAML (pip install pyyaml).
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    sys.exit("PyYAML is needed: pip install pyyaml")

ACTION = "anthropics/claude-code-action"
SHA = re.compile(r"@[0-9a-f]{40}$")
KEY_LITERAL = re.compile(r"sk-ant-[A-Za-z0-9_-]{10,}")
MENTION_EVENTS = {"issue_comment", "pull_request_review_comment", "pull_request_review", "issues"}


def finding(sev: str, file: str, where: str, msg: str) -> dict:
    return {"severity": sev, "file": file, "where": where, "message": msg}


def triggers(doc: dict) -> dict:
    # PyYAML reads the bare key `on` as True.
    on = doc.get("on", doc.get(True, {}))
    if isinstance(on, str):
        return {on: {}}
    if isinstance(on, list):
        return {e: {} for e in on}
    return on or {}


def steps_using_action(job: dict) -> list[dict]:
    return [s for s in job.get("steps", []) or [] if ACTION in str(s.get("uses", ""))]


def audit_file(path: Path) -> list[dict]:
    text = path.read_text()
    name = path.name
    out: list[dict] = []
    if ACTION not in text:
        return out
    try:
        doc = yaml.safe_load(text) or {}
    except yaml.YAMLError as e:
        return [finding("critical", name, "file", f"YAML does not parse: {e}")]

    if KEY_LITERAL.search(text):
        out.append(finding("critical", name, "file", "Looks like an Anthropic key written into the workflow. Move it to a repository secret and rotate it."))

    on = triggers(doc)
    events = set(on)
    pr_types = set((on.get("pull_request") or {}).get("types", []) or [])
    is_review = "pull_request" in events or "pull_request_target" in events
    is_mention = bool(events & MENTION_EVENTS)

    if "permissions" not in doc:
        out.append(finding("warn", name, "top level", "No top-level permissions. Set `permissions: {}` and let each job ask for what it needs."))
    elif doc.get("permissions") not in ({}, None) and doc.get("permissions") != "read-all":
        out.append(finding("info", name, "top level", "Top-level permissions grant something. Prefer `permissions: {}` with per-job grants."))

    has_wf_concurrency = "concurrency" in doc
    jobs = doc.get("jobs", {}) or {}
    any_sync_split = any("synchronize" in str(j.get("if", "")) for j in jobs.values())

    for jname, job in jobs.items():
        where = f"job {jname}"
        cond = str(job.get("if", ""))
        claude_steps = steps_using_action(job)

        for step in job.get("steps", []) or []:
            uses = str(step.get("uses", ""))
            if uses and re.search(r"@<[^>]+>", uses):
                out.append(finding("info", name, where, f"`{uses}` has a placeholder. Fill in the exact commit SHA before merging."))
            elif uses and not uses.startswith("./") and not SHA.search(uses):
                out.append(finding("warn", name, where, f"`{uses}` follows a moving tag. Pin it to an exact commit SHA with the version in a comment."))
            if "actions/checkout" in uses:
                w = step.get("with", {}) or {}
                ref = str(w.get("ref", ""))
                if "pull_request_target" in events and ("head" in ref or "pull_request.head" in ref):
                    if w.get("path"):
                        out.append(finding("warn", name, where, "pull_request_target checks out the PR's code into a subfolder. Safe only if nothing there is run, built or installed, and the job follows the docs' current pattern exactly. Check it by hand."))
                    else:
                        out.append(finding("critical", name, where, "pull_request_target checks out the PR's own code as the workspace. That hands secrets to untrusted code. Use pull_request and skip forks, or the docs' read-only subfolder pattern."))
                perms = job.get("permissions", {}) or {}
                if claude_steps and perms.get("contents") in ("read", None) and w.get("persist-credentials") is not False:
                    out.append(finding("info", name, where, "Checkout keeps credentials in the workspace. A read-only job can set `persist-credentials: false`."))

        if not claude_steps:
            continue

        if "timeout-minutes" not in job:
            out.append(finding("warn", name, where, "No `timeout-minutes`. Set a generous one (e.g. 30) to stop a stuck run."))
        if not has_wf_concurrency and "concurrency" not in job:
            out.append(finding("warn", name, where, "No concurrency group. Add one per PR so overlapping runs don't pile up."))

        perms = job.get("permissions", {}) or {}
        if perms.get("contents") == "write":
            out.append(finding("warn", name, where, "`contents: write` lets Claude push. A reviewer should be read-only."))

        for step in claude_steps:
            w = step.get("with", {}) or {}
            args = str(w.get("claude_args", ""))
            prompt = str(w.get("prompt", ""))
            if "--model" not in args and "model" not in w:
                out.append(finding("warn", name, where, "No model named. The default can change and may be the most expensive. Name it explicitly."))
            if "--max-turns" not in args and "max_turns" not in w:
                out.append(finding("warn", name, where, "No turn cap. Set a generous one (e.g. 100) as a runaway guard."))

            if is_review:
                runs_on_sync = "synchronize" in pr_types and "synchronize" not in cond
                excludes_sync = "!= 'synchronize'" in cond or '!= "synchronize"' in cond
                if "draft" not in cond:
                    out.append(finding("warn", name, where, "No draft skip. Add a job condition on `pull_request.draft == false`."))
                if "head.repo" not in cond and "fork" not in cond:
                    out.append(finding("warn", name, where, "No fork skip. Fork PRs get no secrets, so the run only fails. Skip when the head repo isn't this repo."))
                if runs_on_sync and not excludes_sync:
                    if "/code-review" in prompt:
                        out.append(finding("warn", name, where, "The built-in review runs on every push, but it skips PRs it has already commented on. Split pushes into their own diff-only job (Step 4)."))
                    elif not any_sync_split:
                        out.append(finding("warn", name, where, "The same full review runs on every push without being told what changed. Split pushes into a diff-only job (Step 4)."))
                if "synchronize" in cond and "== 'synchronize'" in cond.replace('"', "'"):
                    if "before" not in prompt or "after" not in prompt:
                        out.append(finding("warn", name, where, "Push review doesn't use the push's before and after commits, so it may re-review the whole PR."))
                    fetch = None
                    for s in job.get("steps", []) or []:
                        if "actions/checkout" in str(s.get("uses", "")):
                            fetch = (s.get("with", {}) or {}).get("fetch-depth")
                    if fetch not in (0, "0"):
                        out.append(finding("warn", name, where, "Push review checks out shallow history, so the `before` commit may be missing. Use `fetch-depth: 0`."))

            if is_mention:
                if "repository_owner" not in cond and "author_association" not in cond and "github.actor" not in cond:
                    out.append(finding("warn", name, where, "Anyone who can comment can start a run. Limit it to the owner or to OWNER/MEMBER/COLLABORATOR."))
                if "Bot" not in cond:
                    out.append(finding("info", name, where, "Bots aren't excluded. Excluding them also stops a comment Claude wrote from starting another run."))

    return out


def audit(target: Path) -> list[dict]:
    if target.is_file():
        files = [target]
    else:
        # A repo root, or a folder that holds workflow files directly.
        wf = target / ".github" / "workflows"
        folder = wf if wf.is_dir() else target
        files = sorted(list(folder.glob("*.yml")) + list(folder.glob("*.yaml")))
    results: list[dict] = []
    for f in files:
        results.extend(audit_file(f))
    return results


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 1
    results = audit(Path(argv[1]))
    if "--json" in argv:
        print(json.dumps(results, indent=2))
    elif not results:
        print("No findings. The files look tuned. Run the planted-fault test before trusting the reviewer.")
    else:
        order = {"critical": 0, "warn": 1, "info": 2}
        for r in sorted(results, key=lambda r: order[r["severity"]]):
            print(f"[{r['severity']}] {r['file']} ({r['where']}): {r['message']}")
    return 2 if any(r["severity"] == "critical" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
