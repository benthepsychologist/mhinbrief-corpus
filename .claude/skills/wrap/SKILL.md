---
name: wrap
description: Checkpoint the session's work on a standing corpus — sanity-gate the corpus invariants, refresh STATUS.md without rot, commit both zone repos with their provenance receipts, push, verify the push landed, and distinguish pushed from actually deployed. Safe to run several times a day; never reads as "session over."
disable-model-invocation: true
---

# /wrap — persist the session, verified

> ⚠️ **LOCAL EXTENSION, not a kit artifact.** The engine's library has
> `attention/wrap` but **no `standing/wrap`** (checked 2026-08-18). This file
> is written under `OPERATING.md` §2 — it lives in a file this repo owns
> outright, so it is sanctioned and needs no permission. But by §2's own test
> — *"would another repo want this unchanged"* — a standing wrap is
> **library-shaped**, so a brief has been filed asking the engine to render
> one. **When `standing/wrap` lands in the kit, delete this file and take the
> rendered one.** Do not grow this into a private fork that drifts.

**This is a CHECKPOINT, not a closer.** Ben runs `/wrap` as the save button,
possibly several times a day, mid-flow. Never append end-of-day framing to its
report, and never treat a wrap as permission to stop.

**Scope — what this writes, and what it does not.** It writes `STATUS.md`, git
commits and pushes in the two zone repos (this repo + `/workspace/mhinbrief-site`),
and at most one brief into `/workspace/kestrel-ops/INBOX/`. It does **NOT**
curate records (that is `/curate`, and AGENTS.md #2 gives accept/reject to the
operator), does not run `/tend`, does not verify claims (`/verify`), and does not
publish or deploy (`/publish`). A wrap that finds those needing work **names the
need in its report; it does not do the work.**

**No `log.md`.** That is an attention-kind convention. This repo's dated
top-note stack in `STATUS.md` *is* its log — see step 1. Do not create one.

## Steps

### 0 — sanity gate (read-only)

Run before writing anything. A wrap that snapshots state on top of a broken tree
writes a confident summary over a lie.

- **YAML guardrail** — `yaml.safe_load` every file this session touched under
  `records/`, `candidates/`, `changelog/`, `coverage/`, plus `kestrel.yaml`.
  This is the standing LLM-edit rule enforced at the exit.
- **The corpus invariants**, computed now, never recalled:
  - every `covered` cell in `coverage/matrix.yaml` has a `record_id` that
    exists in `records/`;
  - every file in `records/` has a cell pointing at it;
  - every record has at least one `changelog/` entry;
  - `governance.record_change_requires` holds — `source_url` and
    `last_verified` non-blank at top level on every record.
- **Stranded receipts** — `git status --short -- provenance/`. Publish and
  verify manifests are written *after* the work they describe, so untracked
  `provenance/*.yaml` at wrap time is the norm, not an anomaly. They go in
  step 2's commit. An untracked manifest *and nothing else* means a run
  happened after the last commit — commit the receipt anyway.
- If anything here fails in a way the session cannot explain, **stop and
  report.** Do not wrap over it.

### 1 — STATUS.md refresh (anti-rot)

Only if repo state actually moved this session; a read-only session skips this
and says so.

- **Rewrite the top note from scratch.** Read `git log` since STATUS.md's own
  "As of" date, then write the new note fresh. **Never patch a line inside an
  existing note.** Dated notes below it are history and stay untouched — that
  stack is this repo's log rotation.
- **Assert nothing a command computes.** Record/changelog/candidate counts,
  coverage tallies and confidence spread come from a script run *now*, not from
  memory and not from the previous note.
- **Do not "correct" numbers inside older dated entries.** A figure that was
  true on its date is history; rewriting it falsifies the record.
- Update the `*As of YYYY-MM-DD*` line to today.

### 2 — commit this repo, receipts included

One commit, or a few scoped ones if the session had distinct arcs. Repo-style
message, `Co-Authored-By` line. Scoped adds — never `-a` blind.

The trap this step exists for: **provenance manifests are easy to strand**,
because tools write them after the real work was already committed.
`git status --short` must be empty after this step, except deliberate proposals
(a draft awaiting Ben's word) — **name those in the report.**

### 3 — site repo state, BEFORE any push decision

Check `/workspace/mhinbrief-site`'s working tree. Two situations, never
conflated:

- **Hand-authored edits** — layouts, CSS, `content/topics/*.md` editorial prose,
  worker code → **their own commit with a real message, now.** They must never
  ride an adapter-generated content commit, where they become unfindable.
- **Adapter-generated content** — `content/changelog/`, `data/*.yaml` → that is
  `/publish`'s output. If content is staged but no publish ran, say
  "staged, unpublished" in the report rather than pushing a half-state.

### 4 — push, verify, and separate PUSHED from DEPLOYED

- `git push` on this repo and on the site repo.
- **Verify, never assume:** `git log @{u}..` must print **nothing** on both.
  A clean `git status` is *not* evidence — only the upstream check is.
- **Engine repo (`/workspace/kestrel`): read-only check, flag-never-push.**
  `git -C /workspace/kestrel log @{u}..`. Unpushed commits there mean another
  session missed a push. That is a report flag addressed to Ben. Pushing it
  from here is a write-zone violation even though it would "help."

⚠️ **Pushing the site is not deploying it, and deploying is not being live.**
This site goes live by `hugo && npx wrangler deploy` from the site repo — never
by git push. Two failure modes seen in real runs, both of which produce a
confident false "it's up":

- `wrangler deploy` prints **"No targets deployed"** on a successful asset
  upload. That string is not an error; judge by the live site, not the output.
- **Propagation lags the deploy by tens of seconds.** A check run immediately
  after can return the *previous* build and look like a failed deploy.

So a wrap reports **four distinct states** — committed · pushed · deployed ·
verified live — and never collapses them. Verify live with a string that only
the new build can contain, and remember production is unminified `hugo`.

### 5 — hand-offs, then the report

- If a kit-rendered file was hot-fixed this session, or the engine needs
  anything, file **one brief** — `/workspace/kestrel-ops/INBOX/<date>-mhinbrief-<slug>.md`
  for ops-shaped items (an incident, drift, anything naming a live repo, path
  or run), or the engine's issue tracker for dev-shaped ones. **Commit the
  brief there and touch nothing else.** If unsure which, file OPS.
- **The report** — house style: one-line verdict; a table of lanes; what is
  waiting on Ben; the obvious next move; flags. Report only — fix nothing from
  inside the report.

Lanes worth a row on a standing corpus, each computed not recalled:

| lane | what to report |
| --- | --- |
| **Corpus** | records · changelog entries · deltas this session |
| **Coverage** | covered/total cells, confidence spread, anything `not_started` |
| **Claims** | statements in `verification/*.stamp.jsonl` **awaiting a human signoff** — this is the main standing "waiting on Ben" |
| **Candidates** | staged count and its growth rate; call out sources staging on every sweep, which is churn, not news |
| **Cadence** | last unattended run and its receipt; whether the crontab is still correct for the current UTC offset |
| **Push** | `@{u}..` on corpus · site · engine (read-only) |
| **Deploy** | committed / pushed / deployed / verified-live, as four states |

## Do not

- Do not curate, accept, reject or defer a candidate — that is `/curate`, and
  the operator holds accept/reject (AGENTS.md #2).
- Do not publish or deploy from inside a wrap. Name the need.
- Do not push, commit, build or lint in `/workspace/kestrel` — flag, never fix.
  The brief is the one sanctioned write, and it goes to `kestrel-ops`.
- Do not patch STATUS.md's top note in place, do not edit older dated notes,
  and do not let a count appear that a command did not just compute.
- Do not let hand-authored site edits ride an adapter-generated commit.
- Do not shortcut step 4's `@{u}` checks, and do not report "deployed" as
  "live" without checking served content.
- Do not create a `log.md`.
- Do not read a wrap as "session over," and never write one that says so.
