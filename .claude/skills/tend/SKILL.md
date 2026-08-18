<!-- kit: standing/tend@2026-08-18.3 — canonical: /workspace/kestrel/library/skills/standing/tend/SKILL.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# /tend — sweep declared sources, stage the candidates

This kind's mechanical half. Runs the engine's manifest-driven runner
against this instance, then reports what it staged — **it never writes a
record** (the runner STOPs at candidates by design; the propose-then-
confirm discipline is structural, not a habit).

**If this instance's `kestrel.yaml` declares no `sources:`**, there's
nothing for this skill to sweep — say so plainly and stop. That's a real,
expected state, not an error: some instances get candidates from an
external sweep (this skill); others get them however their own upstream
process delivers them (an ingester, a manual drop into wherever
`layout.candidates` points) — either way, `/curate` is what turns a
candidate into a record, regardless of how it arrived.

## Run

    kestrel tend /workspace/mhinbrief-corpus

`--dry-run` first if you want the source-selection plan without fetches.
`--source <id>` scopes to one source.

## Then report, scannable

- **Per-source verdicts** — the runner prints them; relay the ones that
  matter: `changed` page-diffs, feeds that failed, anything `UNHANDLED`.
- **Candidates staged** — count + one line each (new files in
  `candidates/`). Zero staged on a quiet week is a normal, correct
  outcome — say so plainly rather than padding.
- **Feed health** — a source whose feed lied (200-but-empty, years-stale)
  is this instance's own data: flag it for a `method: page-diff` demotion
  in `kestrel.yaml`'s `sources:` (the governance rule is `feed_health:
  auto-demote`; the manifest edit itself is a curation act — propose it,
  don't silently rewrite the manifest mid-run).

## Close

Commit the run's artifacts in THIS repo (buffer is gitignored; candidates,
provenance, and snapshots are not): one commit, provenance manifests
included. If candidates were staged, say that `/curate` is the next move.
