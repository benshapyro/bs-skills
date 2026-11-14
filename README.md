# bs-skills

Claude skills by Ben Shapiro, grouped into four plugins. They work in Claude (the app, Cowork and Claude Code) and in Codex. Plain Markdown, plus a few small scripts.

| Plugin | Skills | For |
|---|---|---|
| `learning-loop` | `handover`, `filing`, plus two reminders | AI work sessions that pick up where the last one stopped, and project documents kept in order |
| `product` | `prd`, `build-spec`, `codebase-audit`, `changelog`, `ai-pr-review-setup` | Deciding what to build, speccing it for a coding agent, auditing a codebase, keeping change history, and automatic pull request reviews |
| `writing` | `say-less-but-more`, `walk-me-through`, `learn-anything`, `build-log` | Tightening drafts, interactive explainers, learning a subject properly, and logging lessons worth writing about |
| `music` | `suno-assistant` | Songwriting prompts for Suno |

## Install

**Claude app, Cowork or Claude Code:** open Customize > Plugins > Add > Add marketplace, enter `benshapyro/bs-skills`, then install the plugins you want. Plugins added there sync to Claude Code.

**Claude Code only, from the terminal:**

```bash
claude plugin marketplace add benshapyro/bs-skills
claude plugin install product@bs-skills
```

**Codex:**

```bash
codex plugin marketplace add benshapyro/bs-skills
codex plugin add product@bs-skills
```

## About the learning-loop plugin

- **`handover`** reads the newest note in a project's `docs/handovers/` at the start of a session, and writes one at the end: where things stand (each claim marked verified, stated, inferred or unknown), why, and what went wrong, with lessons a weekly review can turn into fixes.
- **`filing`** says where a project's documents go (`docs/current/`, `docs/work/<topic>/`, `docs/decisions/`, `docs/handovers/`) and how they're named, with templates.
- **Two reminders (Claude Code hooks):** when you say you're stopping, real work happened and no note was written, Claude is asked once to write one; when a long conversation is shortened, Claude is told what to keep. Neither writes a note itself.

## Checking a change

```bash
claude plugin validate .
claude plugin validate plugins/product      # or any plugin folder
./tests/test_hooks.sh                         # the reminders, no AI calls
cd plugins/learning-loop && claude plugin eval . --scaffold --allow-tools Bash Write Edit   # handover behaviour, about $1 a run
```

`scripts/privacy-check.sh` blocks a commit that names a client (read from a clients folder; see the script) or includes a home-folder path. Turn it on for a repository with `scripts/install-privacy-check.sh <repo>`.

Each skill keeps its own `CHANGELOG.md` and a `version` in its header; raise the plugin's `version` too when a skill changes.

## License

MIT. See `LICENSE`.
