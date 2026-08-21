<!-- kit: standing/tend@2026-08-21.4 — canonical: kestrel/library/skills/standing/tend/SKILL.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

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

    cloud-researcher tend --corpus .

`--dry-run` first if you want the source-selection plan without fetches.
`--source <id>` scopes to one source.

⏱ **Give this an explicit long timeout (≥600s), and never background it
and stop.** A full sweep of a 50-source manifest takes ~195 seconds — well
past the Bash tool's 120s default — so the default is wrong for the normal
case here, not the exceptional one.

**The failure this prevents, from a real unattended run:** the sweep was
backgrounded, the session announced *"I'll wait for it to complete rather
than poll"* — and the turn ended on that message. It never reached its
report step **or its commit step**, and the run recorded `exit=0`, because
the CLI did exit cleanly after printing that line. Collected work sat
uncommitted and the site went stale for days while every signal said
success.

So: **a backgrounded sweep must be polled to completion inside the same
turn.** Announcing an intention to wait is not waiting. If the sweep
genuinely cannot finish in this turn, say so and commit what exists —
an honest partial beats a silent zero. This is the same defect the
attention kind's `/wrap` §5 documents for `hugo` and `publish`; the rule
is identical and it is here because this skill hit it independently.

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
