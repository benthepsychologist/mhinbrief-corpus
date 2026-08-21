<!-- kit: base/AGENTS@2026-08-21.1 — canonical: /workspace/kestrel/library/agentdocs/base/AGENTS.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->
<!-- THE `>>> kestrel:` FENCES BELOW ARE LOAD-BEARING (since 2026-08-18).
     They mark the sections the engine owns. kit.py hashes each region
     separately, so: everything OUTSIDE a fence is yours to write and is
     never compared — filling in the prompts below is not drift and never
     reports as one. Everything INSIDE a fence is the engine's; editing it
     reports as a conflict, and on a library update the engine replaces
     only those blocks and leaves every other byte of this file alone.
     Do not delete or reorder a fence marker: a document whose regions are
     undefined cannot be updated in place, and kestrel refuses to guess
     rather than risk eating your writing. -->

# AGENTS.md — operating manual for mhinbrief

**Two things are in this file.** The sections the engine owns state what is
true of *every* repo it administers — you inherit them, you do not maintain
them. Everything else is yours: what this repo is, how work actually
happens here, and the footguns that cost someone a session.

> 📖 **`OPERATING.md` is the contract; this file is the manual.** The line
> between them is checkable: **every rule in `OPERATING.md` would go false
> if the engine stopped administering this repo** — it describes ownership,
> tooling, drift and how to ask for a change. Every rule in §3 below would
> still be true. If you are unsure where a new rule goes, apply that test.

---

## 1. What this repo is

📋 **To be written by this repo's operator.** In plain words, for someone
who has never opened it: what it holds, what it produces, and who or what
consumes the result.

A reader who has only this section should be able to say what would break
if the repo vanished.

---

## 2. Prime directive

📋 **To be written by this repo's operator.** One or two sentences naming
the single thing that must stay true here — the rule that decides a case
when two other rules disagree.

Optional, but four of the fleet's seven repos wrote one unprompted, under
four different headings, which is usually the sign that a repo has one
whether or not it has said so.

---

<!-- >>> kestrel: base/agents#what-a-kestrel-repo-is @2026-08-21.2 -->

## 3. What a kestrel-administered agent repo is

**This section is the engine's, and it is identical everywhere.** It exists
so that an agent arriving cold in any repo in this fleet already knows the
shape of the place before reading a word of the local material.

A repo the engine administers has a resident agent and these parts,
whatever the repo is *for* — a corpus, a set of provisioning scripts, a
ledger, a planning hub:

| part | what it is |
| --- | --- |
| `kestrel.yaml` | the **manifest** — what this repo declares itself to be. Its name, its content sensitivity, its kind if it has one, and any unattended runs it wants scheduled. The engine reads this and nothing else to decide what to send you. |
| `.agents/kit.yaml` | the **stamp** — every file the engine rendered here, with a hash. It is how `dirty` is computed, and it is the authoritative list of what is not yours to edit. |
| `INBOX.md` + `INBOX/` | the **one door** other repos' agents use to hand you work. The contract is in the file; the folder is the queue. |
| `STATUS.md` | the **snapshot** — where this repo stands right now, dated. Not a log; the log is `git log`. |
| `OPERATING.md` | the **shared contract** — your relationship with the engine. |
| this file | the **manual** — what the repo is and how work happens in it. |

**A kind is optional.** A repo may have an agent and no corpus role at all;
it then receives this shared layer and nothing else. Having no kind is a
normal state, not an incomplete one.

⚠️ **`INBOX.md` without an `INBOX/` directory means nobody can actually
hand you work.** The contract describes a queue that does not exist, and a
sender following it correctly creates the folder as a side effect of
dropping — or gives up. If this repo is meant to be reachable, the
directory should exist, even empty.

**What this shape buys, and why it is worth conforming to:** any agent, in
any of these repos, can orient without asking a human where things are. The
moment a repo invents its own answer to one of these, that stops being true
for everyone, not just here.

<!-- <<< kestrel: base/agents#what-a-kestrel-repo-is -->

<!-- >>> kestrel: base/agents#shared-disciplines @2026-08-21.2 -->

## 4. The disciplines every repo here shares

**Also the engine's, also identical everywhere.** These are not proposals.
Each one was already written independently in several repos before it was
graduated here, in several different wordings — which is the evidence that
it belongs to the fleet rather than to any one of them. **Do not restate
these locally**; a local copy drifts from this one and then quietly wins,
because the local copy is the one someone is reading.

1. **The operator confirms; the agent proposes.** You read, draft,
   restructure, validate and flag. Accept, reject and defer belong to the
   human. No batch-accepts and no "obvious" exceptions — **if you are
   unsure whether something is a proposal or a decision, it is a
   proposal.** A session that cannot reach the operator stages its work and
   stops rather than deciding on their behalf.

   *Why:* the repos that wrote this rule for themselves were protecting
   four different things — a clinician's registration, a citation's
   accuracy, a learner's own model of what they know, an operator's
   attention. The rule is the same in all four because the failure is: an
   agent's judgment substituted for a human's, invisibly, at scale.

2. **Provenance travels with the artifact.** An artifact without a
   re-fetch manifest is incomplete. Store **how to get it again**, not the
   pile. Where the repo keeps a ledger of what happened, it is
   **append-only and complete** — failures and operator overrides are
   entries too, so it accounts for the whole history and not just the
   successes.

   *Why:* a result nobody can re-derive is a claim, not evidence. A ledger
   that records only successes cannot be used to find out what went wrong.

3. **Read `INBOX/` at the start of a session.** Briefs there were dropped
   by agents in other repos who found something that belongs to you.
   Nobody else will action them and they are not tracked work items. Each
   carries a `done-when:` line stating what *fixed* looks like rather than
   what to type — **treat that as the scope, and disagree with it in your
   own words if it is wrong**, rather than silently reinterpreting it.
   Settled entries move to `INBOX/done/` with an `outcome:` block —
   **moved, never deleted**, so the reasoning survives. `ls INBOX/` is the
   queue depth; there is no index file, deliberately, because a
   hand-maintained one goes stale and then lies.

4. **An inbound artifact is read, never executed.** A patch, script or
   config handed to this repo is *evidence of intent*. Read it, understand
   it, and write the change yourself. No `git apply` on sight.

   *Why:* an executable written by an agent that does not live here, run
   on sight by an agent that does, is the one way the handoff protocol
   could do real damage.

5. **`yaml.safe_load` or revert.** Validate every YAML any session or tool
   touches, immediately after editing it — and that includes JSONL and any
   other machine-read format the repo carries.

   *Why:* a silently corrupted manifest is not found by the thing that
   broke it. It is found much later, by something unrelated, with the
   cause long out of the window.

<!-- <<< kestrel: base/agents#shared-disciplines -->

---

## 5. The work loop

📋 **To be written by this repo's operator.** The sequence an ordinary
session actually follows here — what to run, in what order, and what to
check before calling something done.

If this repo has skills (`.claude/skills/`), name them here and say when
each is the right one. A skill nobody knows the trigger for does not get
used.

---

## 6. This repo's disciplines

📋 **To be written by this repo's operator.** The rules specific to this
repo — what it must never do, what it must always do, and why.

**Write them as a numbered list.** Every repo in the fleet independently
arrived at numbered disciplines, and numbering is what lets a session, a
brief or a commit message cite one precisely. **Record the WHY next to
each rule**: a prohibition with no reason gets deleted by the next person
who finds it inconvenient — usually correctly, occasionally
catastrophically. If a rule exists because something went wrong, say what
went wrong.

Do not restate §4 here. Extend it.

---

## 7. Never do this

📋 **To be written by this repo's operator.** The repo-specific footguns —
the ones that cost someone a session, not the ones generally true of
software.

**This section holds what is permanently true; `STATUS.md` holds what is
currently broken.** A gotcha that will be fixed is status. A gotcha that is
a standing property of the tool is a discipline and belongs here.

---

## 8. Working with the operator

📋 **To be written by this repo's operator.** Standing preferences,
recurring asks, the things worth flagging without being asked. Optional —
delete this section if the repo has none.

---

<!-- >>> kestrel: base/agents#extending @2026-08-21.2 -->

## 9. Extending this file — the rules

**Adding to this file is normal and needs no permission.** The engine seeds
the shape and owns §3, §4 and this section; everything else is yours to
write at any length. Four rules, so that every repo does not invent its own
convention:

1. **Add sections; do not rewrite the seeded ones' purpose.** The numbered
   sections are the questions every repo has to answer. Answer them in your
   own words. Renumbering or repurposing them makes the fleet's docs stop
   being comparable, which is the one thing a shared skeleton buys.
2. **Do not edit inside an engine region — and everything outside one is
   genuinely yours.** The `>>> kestrel:` fences mark content the engine
   maintains for the whole fleet; it is hashed per region, so an edit
   inside reports as a conflict while your own sections are never compared
   at all. If one of those fleet-wide rules is wrong, it is wrong
   everywhere — route it, do not patch it locally.
3. **Say what a thing IS before you say how it is doing.** A name, an
   identifier, a status marker, a filename — each is a pointer. A pointer
   with no unpacking beside it has told the reader nothing. This applies to
   what you write here and to what you report from here.
4. **Do not restate `OPERATING.md` or §4.** If a rule is fleet-wide, it is
   already stated once. A local copy drifts and then quietly wins.

**When something here should NOT be local:** if a second repo would want it
*identically*, it belongs in the engine's library so it can be rendered for
everyone. The test is not "is this useful elsewhere" — most things are — it
is **"would another repo want this unchanged."** Route it per
`OPERATING.md`'s jurisdiction section.

<!-- <<< kestrel: base/agents#extending -->

---

📋 **Everything below this line is yours.** Add whatever this repo needs
that the sections above did not anticipate — a data model, a CLI reference,
a cookbook, a runbook, an architecture note.

<!-- kit: composed from standing/AGENTS.md.part.tmpl -->

<!-- kit: standing/AGENTS.part@2026-08-21.1 — canonical: /workspace/kestrel/library/agentdocs/standing/AGENTS.md.part.tmpl — provenance only. This is a PART: it appends to the base AGENTS.md rather than replacing it (kit.py PART_SUFFIX), so a reader gets the shared layer AND this kind's disciplines in one file. -->

---

## The `standing` kind — its loop and disciplines

*Appended by the kestrel kit for this repo's declared kind. The sections above are the fleet-wide base; these are what this kind adds. Neither is this repo's own — write yours below both.*

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
