<!-- kit: standing/AGENTS@2026-08-15.3 — canonical: /workspace/kestrel/library/agentdocs/standing/AGENTS.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# AGENTS.md — mhinbrief operating disciplines

This instance's shared disciplines, numbered so they can be cited. They
inherit kestrel's engine invariants (see `/workspace/kestrel/README.md`) and
add the ones every **standing**-kind instance shares. This file is
deliberately silent on this instance's own subject, voice, or safety
rules — those belong in this repo's own hand-authored contract content,
layered alongside this file, never generated here.

**⚠️ Read `OPERATING.md` beside this file FIRST — it is the shared
contract.** What you own vs. what the engine owns (with the mechanical
test), the local-extension protocol, jurisdiction and how to file an
engine brief, why `dirty` is not an error, YAML safety, and the
session-close and push discipline all live there, identical in every repo
the engine tends. **What follows is only what is specific to this kind**
— it deliberately does not repeat any of it.

**The loop, in order:** `/tend` (sweep declared sources, stage candidates)
→ `/curate` (operator confirms; a candidate becomes a record) → `/verify`
(re-check what is already recorded) → `/publish`. `/start` orients before
any of it. The ordering is the contract — a record that reaches `/publish`
without having passed `/curate` has skipped the human gate this kind
exists to enforce.

1. **Citation or nothing.** Every record field change carries a source
   and a verified-as-of date. `record_diff.governance_check` enforces
   presence mechanically; the curate loop enforces that the source
   actually says what the record claims — that part is judgment, and it
   is the operator's.
2. **The operator confirms every record change.** The agent reads,
   drafts, and proposes; accept/reject/defer belongs to the human. No
   batch-accepts, no "obvious" exceptions. A session that can't reach the
   operator stages and stops.
3. **The changelog is append-only and complete.** One YAML file per
   entry, never edited after writing; record creation and retirement are
   entries too, so the log accounts for the whole corpus, not just
   mutations of survivors.
4. **A verified non-change is information.** `/verify` bumps the
   verified-as-of date on unchanged records and tallies the sweep in a
   run note; those bumps do NOT emit changelog entries — the changelog
   records the tracked thing moving, not us looking.
5. **Candidates are an audit trail.** Pending-item files are resolved in
   place (`accepted`/`rejected`/`deferred` + why), never deleted; `/tend`
   (if this instance runs it) stages them, only `/curate` resolves them.
6. **The manifest is curated, not automated.** Source additions, feed-
   health demotions, cadence changes — proposed by runs, confirmed by
   the operator, committed like any other curated change.
7. **Buffer is cache; everything else is record.** `buffer/` is
   gitignored, 30-day semantics (if this instance uses it). Candidates,
   records, changelog, snapshots, provenance: committed, always.
8. **One content writer per outward channel.** Generated content into
   any declared channel comes only from this instance's own adapter,
   which calls the engine's publish core for the guarantees. Site/channel
   code (templates, hand-authored editorial pages) is that channel's own;
   this corpus's data never gets hand-transcribed into it.
9. **Provenance discipline.** Every sweep, verify pass, and publish
   leaves a dated manifest in `provenance/`. An artifact without a
   re-fetch manifest is incomplete.

## Your publish surface

**Your publish adapter is yours, not the engine's.** (**Operational** — `publish/adapter.py` exists in this repo.)

The engine's publish core is generic orchestration — the run loop, the
secret scan, the git push, the guarantees. **What pages exist, what data
ships, and any step you add to the publish flow live in this repo's own
adapter file.** This is the specific thing a session once got wrong,
telling the operator a feature needed an engine change when the whole
change was a method here.

**Your site, if you have one, is YOURS — including its docs.** If this
instance declares a site (`/workspace/mhinbrief-site`), that repo is your publish surface, and you are its only
content writer. Two things follow, pulling opposite ways:

- ✅ **You own it.** The engine manages nothing there — no rendered docs,
  no hashes, no drift reporting. Its `AGENTS.md`, `README.md`, layouts,
  CSS and deploy config belong to whoever works in it, usually you.
- ⛔ **Its generated content is not hand-editable, by you or anyone.**
  Whatever your adapter writes is overwritten wholesale on the next
  publish. A fix belongs **here** — in the records, or in the adapter that
  renders them — never in the site.

**Why the engine stopped managing sites** (2026-08-14): a site has no
agent of its own. Pushing a doc into one from the engine produced a single
file that either duplicated what the site already said or froze and went
stale — one carried a wrong path for ten days while the site's own README
stayed accurate. This contract is the replacement, and it lives on this
side because you are the one who writes there.
