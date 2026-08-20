<!-- kit: base/OPERATING@2026-08-21.1 — canonical: /workspace/kestrel/library/agentdocs/base/OPERATING.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# OPERATING.md — the shared contract for mhinbrief

**This file is the same in every repo the engine tends.** It answers the
questions that are not specific to what this repo is *for*: what you own,
what you must not touch, how to add something only this repo should have,
and how to close a session. Your kind-specific disciplines live in
`AGENTS.md` beside this file; what this repo is *about* lives in
`README.md`.

Read this one first. It is short on purpose.

---

## 0. Running engine tools

The engine is an installed package with one command. From anywhere:

```sh
kestrel <verb> --instance /workspace/mhinbrief-corpus
```

`kestrel --help` lists the verbs. Fleet-wide operations live under
`kestrel fleet <verb>` and are the engine's own business, not yours.

⚠️ **Always name the instance.** Without it the tools have no idea which
repo they are for; they fail loudly rather than guessing, which is the
intended behaviour. The older form —
`KESTREL_INSTANCE=/workspace/mhinbrief-corpus python3 /workspace/kestrel/tools/<tool>.py`
— still works and warns, because a great deal of installed documentation
still says it. Prefer the flag; do not be alarmed by the warning.

---

## 1. What you own, and what you don't

Two repos are in play whenever this one runs: **this repo**
(`/workspace/mhinbrief-corpus`) and **the engine** (`/workspace/kestrel`). The split
is *not* "code vs. data" — that reading is what causes the mistake this
section exists to prevent.

| lives in | what | may you edit it |
| --- | --- | --- |
| **the engine** | the engine's own package, and **every template under `library/`** — including the template this file was rendered from | ⛔ **never directly** — file a brief (§3) |
| **this repo, engine-rendered** | **exactly the files listed in §1.1** — no more, and never assume a file is on that list because its name looks like one | ⚠️ hot-fix locally when you must; it will report `dirty`, and **that is the correct outcome, not a fault to clear**. Back-port by brief, never by adopting from here |
| **this repo, yours outright** | everything else — your own code, your data, your `INBOX/`, your logs, your scripts, and any skill not listed in §1.1 | ✅ **edit freely** — no permission needed beyond this repo |

### 1.1 The files the engine currently owns here

- `.agents/run.sh`
- `.claude/skills/curate/SKILL.md`
- `.claude/skills/health/SKILL.md`
- `.claude/skills/publish/SKILL.md`
- `.claude/skills/start/SKILL.md`
- `.claude/skills/tend/SKILL.md`
- `.claude/skills/verify/SKILL.md`
- `AGENTS.md`
- `CLAUDE.md`
- `INBOX.md`
- `INBOX/.gitkeep`
- `OPERATING.md`
- `STATUS.md`

⚠️ **That list is a snapshot taken when this file was rendered. The
authority is `.agents/kit.yaml`** — read it if the two ever disagree,
because the stamp is what the drift check actually compares against.

**One case the list above deliberately does not cover: orphans.** If
`.agents/kit.yaml` tracks a file that the list above does not mention,
it is an **orphan** — the engine placed it once, but its template has
since left the library. It is frozen: no future install will update it,
and it may describe machinery that no longer exists. `kestrel fleet
status` names any that exist here, and `install --remove-orphan` clears
them. They are not listed above because this file is rendered *before*
an install writes the stamp, so any orphan list it carried would be
describing a world the install is about to change.

> ### The mechanical test, so you never have to guess
>
> Look the path up in `.agents/kit.yaml`'s `files:` map:
>
> - **not there at all**, and not under `/workspace/kestrel` → **yours.**
> - **there with a hash** → engine-owned. Hot-fix if you must; back-port
>   by brief.
> - **there with `null`** → ⚠️ **yours**, permanently and on purpose.
>   Someone recorded that decision. A null is a *recorded divergence*,
>   not an engine claim — reading "present in `files:`" as "engine-owned"
>   gets this exact case backwards.

### 1.2 "It belongs somewhere else" is not a reason to stop

**Discovering that a fix seems to live elsewhere is a reason to apply the
test in §1.1, not to hand the work off.** Most of the time the answer
comes back: it is yours.

A session once told the operator that a feature required an engine change
and offered to file a brief — when the entire change was a method in a
file inside its own repo. It only found out by accident. The reflex to
route a fix upward is right when the thing really is the engine's, and
expensive every other time.

### 1.3 Sibling repos are not yours to read either

**Zero coupling to sibling corpora.** Other instances the engine tends are
not inputs to this one — do not read their data to answer a question here.
Everything this repo needs is either in this repo or arrives through a
declared source. If you find yourself reaching into a sibling, the honest
move is a brief (§3) asking for the thing you actually need, not a
cross-read that silently couples two corpora together.

(Reading another repo to *understand* it — its docs, its code, while
debugging — is fine and always was. This is about data dependencies.)

---

## 2. Adding something only this repo should have

Sanctioned, and it needs no permission beyond this repo. Four rules, so
that every repo does not re-derive its own:

1. **It lives in a file you own outright** — never in an engine-rendered
   file. A local feature written into a rendered skill is a *hot-fix*,
   not an extension: it reports `dirty` forever and competes with the
   template on every sync.
2. **It declares its runtime dependencies inline, at the point of use,
   with the reason.** If it needs an interpreter or package this repo
   does not otherwise have, say which and why in a comment beside the
   call — not in a README nobody reads at the moment it fails.
3. **It degrades; it never fails its host.** If its dependency is missing
   or its step errors, it logs and skips, and the run it hangs off
   completes. An extension that can break the main loop is not an
   extension — it is a change to the main loop, and *that* one is an
   engine brief.
4. **It is idempotent within its own natural period.** Re-running the
   host flow must not redo expensive work that is already current.

**When it should NOT be local:** if a second repo would want the same
thing *identically*, it is a library change — file it (§3) and let it be
rendered for everyone, rather than growing a second private copy that
drifts. The test is not "is this useful elsewhere" (most things are); it
is **"would another repo want this unchanged."**

---

## 3. Jurisdiction, and how to ask for an engine change

**Your write zone is this repo** (and its site sibling, if one is
declared). Commit and push either without asking first, on request or on
reasonable judgment.

**`/workspace/kestrel` is outside that zone.** Being right about what a
template should say is not authority to write it there yourself. Any
change the engine needs goes in as a brief — **and where it goes depends
on what kind it is:**

| your brief | goes to |
| --- | --- |
| **dev** — a template bug, a missing feature, a design question. About the engine's *code* | a **GitHub issue** on the engine repo |
| **ops** — an incident, a drift report, anything naming a live repo, a path, or a run | `/workspace/kestrel-ops/INBOX/<date>-mhinbrief-<slug>.md` |

⚠️ **If you are unsure which, file it as OPS.** Over-filing to the private
side costs someone a redirect; under-filing to a public issue tracker
cannot be taken back.

Write the file, **commit it, and stop.** Do not run the engine's tooling,
do not build, do not edit anything else there. See `INBOX.md` beside this
file for the brief format — the same one that governs briefs arriving
*here*.

⚠️ **Never run an "adopt" from here to push a local fix back into the
canonical template.** That writes into the engine, which is exactly the
out-of-zone write this section prohibits. The brief is the channel; the
engine's own resident agent or the operator decides.

---

## 4. Kit artifacts, and why `dirty` is not an error

The files in §1.1 are **rendered artifacts**. Each carries a provenance
header naming the template it came from.

- Editing one locally is legitimate — that is how a real correction gets
  made and read immediately.
- The next drift check will report this repo **`dirty`**. That means
  "this target has diverged; its owner should look." It is information,
  not damage: the kit never auto-applies to a dirty target, so nothing is
  at risk while it sits.
- Resolution is always explicit and per-file — adopt the local version
  upstream, discard it for the template, defer, or mark it **permanently
  yours**. A file marked permanently yours stops being reported as drift
  at all, because a recorded decision is not drift.

---

## 5. Two rules that have each been learned the hard way

**`yaml.safe_load` or revert.** Every YAML this session or the engine
touches. No exceptions, no "it's just a small edit".

**A clean `git status` is not evidence your work is safe.** Nothing in
the normal flow pushes this repo on your behalf, so unpushed commits
accumulate *silently across sessions* and look fine locally. Check
`git log @{u}..` — on this repo and its site sibling if it has one —
before calling a session done. This was found once with **17 commits
unpushed**, ten of them inherited from a previous session that had also
closed without checking.

---

## 6. Closing a session

1. **Append to your log** — what ran, what surfaced, what changed, where
   to pick up.
2. **Commit, including provenance receipts.** An artifact without its
   re-fetch manifest is incomplete; receipts are evidence, not scratch,
   and they are easy to leave untracked because they are written after
   the work they describe.
3. **Push, and verify the push** — `git log @{u}..`, per §5.
4. **If you edited an engine-rendered file, do not back-port it
   yourself.** File the brief (§3) and stop. This repo showing `dirty`
   afterwards is the expected state until the engine's side acts.
