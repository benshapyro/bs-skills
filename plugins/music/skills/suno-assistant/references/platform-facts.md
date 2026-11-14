# Suno Platform Facts

**Last verified: July 2026. These facts change often — re-confirm against Suno's own site (suno.com, help.suno.com) before quoting money, rights, or exact limits to a user.** Everything below is the volatile layer of this skill, deliberately quarantined here so refreshing it is a single-file edit.

Tags: `[verified]` = confirmed from Suno's own docs/blog this session · `[sourced]` = from reputable third-party 2026 writeups, not first-party · `[verify]` = flagged as needing a first-party check before you rely on it.

---

## Current model

- **v5.5**, released **March 26, 2026** — Suno's most expressive model to date, built around personalization. `[verified]`
- Suno has signaled a **next-generation model built with the music industry** coming later in 2026; treat "v5.5" as current-but-not-final. `[verified]`
- Practical takeaway: this skill's craft (Style/Lyrics model, structures, translation, patterns) is model-independent and stays true across versions. Only the feature/tier facts below churn.

## The three v5.5 personalization features

- **Voices** — voice cloning. Record or upload yourself singing/rapping, pass a verification step (speak a random prompted phrase), then generate songs in your own voice. Private to you by default; sharing planned but not live. **Pro/Premier.** It's the evolution of Personas. `[verified]`
- **Custom Models** — upload tracks from your own catalog (made outside Suno) to fine-tune v5.5 toward your style. **Pro/Premier, up to three.** `[verified]`
- **My Taste** — learns your favorite genres and moods over time to bias suggestions. **All users, including free.** `[verified]`

## Personas vs. Voices (people confuse these)

- **Personas** capture the *essence of a song's style* so you can recall that sonic identity on new tracks. Still available. Good for "make more songs that sound like this one."
- **Voices** capture *your actual singing voice*. Good for "make this song sound like me singing it."
- For vocal consistency across a project, a Persona locks the style; a Voice locks the singer. `[verified]`

## Suno Studio (the in-browser editor / "AI DAW")

- Opens on a generated track and lets you edit at the **stem** level rather than re-rolling the whole song. **Pro/Premier.** `[sourced]`
- Separates a track into individual stems (drums, bass, vocals, instruments, and more). Per-stem volume/pan/EQ; you can **swap a single instrument by prompting** ("change this to a string section") without regenerating the rest. `[sourced]`
- Exports **time-aligned WAV stems** that drop straight into Ableton, Logic, FL Studio, etc. `[sourced]`
- Use it in the iteration loop: when someone loves a take *except* one instrument or the mix, send them to Studio instead of re-rolling.

## Stems & tiers

| Tier | Stems | Notes |
|---|---|---|
| **Free** | None | No stem separation. MP3 of the full mix. `[sourced]` |
| **Pro** | Up to **12** time-aligned stems | Full stem export + Studio access. `[sourced]` |
| **Premier** | 12 stems **+ Advanced Split / Split-from-Mix** | Premier-only advanced separation (per Suno's June 2026 stem update). `[sourced]` |

> Note: this corrects a common stale claim that "Pro only gets 2 stems." As of 2026, Pro gets the full stem export. `[sourced]` — but confirm on Suno's live pricing page before advising a purchase. `[verify]`

## Excluding sounds — the reliable way

- The dedicated **Exclude Styles field** (advanced options, **Pro/Premier**) is Suno's official mechanism for removing elements, and it's parsed more reliably than negation inside the Style field. Put unwanted things there: `autotune, electronic drums, heavy distortion`. `[verified]` (Suno help center) + `[sourced]`
- Keep it to **~5 exclusions**. Beyond that Suno gets confused and produces thin, over-sparse output. `[sourced]`
- Writing `no drums` inside the **Style field** does now work in current Suno (it was unreliable in legacy v4, fixed by v4.5+), but it remains the weaker lever. Prefer Exclude Styles when the user has it. `[sourced]`

## Song length

- v5 / v5.5 generate up to roughly **4 minutes** of coherent music in a single generation — no longer the old ~2-minute cap. `[verified]` (v5 release notes) / `[sourced]` (testing writeups)
- Practical effect: you usually don't need a multi-generation "stitch it together" pipeline for a normal-length song anymore. Reserve that for genuinely long pieces or multi-part suites. Use **Extend** to add sections to an existing generation.

## Bracketed-tag behavior (why we keep tags short)

- Bracketed tags longer than ~3–4 words, or tags placed inside a sung lyric line, are prone to being **sung aloud** instead of interpreted as production cues. Keep them short and on their own line; use a parenthetical stage direction on the next line for nuance. `[sourced]`

## Commercial rights & ownership `[verify — re-check current terms]`

Rights language shifts and a user will act on this, so confirm on Suno's terms page before stating it as fact.

- **Free tier** — generally personal / non-commercial use. `[verify]`
- **Pro / Premier** — commercial rights to what you create while subscribed. `[verify]`
- **General cautions (stable):** only upload audio you own the rights to; AI-generated music has limited/uncertain copyright protection that varies by jurisdiction; lyrics you write yourself are yours; describing a sound with sonic descriptors (not artist names) avoids style-attribution problems and, for instrumentals, don't impersonate a real artist in a commercial release.

---

## Refresh checklist (for the next update of this file)

When Suno ships a new model or changes plans, re-verify, in order: current model name + date; the feature set (what's new, what's renamed); tier/stem table; Exclude field availability; song-length cap; commercial-rights language. Update the "Last verified" date at the top.
