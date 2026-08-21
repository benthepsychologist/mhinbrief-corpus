<!-- kit: base/INBOX@2026-08-21.4 — canonical: kestrel/library/agentdocs/base/INBOX.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# INBOX.md — the contract for handing work to mhinbrief

<!-- >>> kestrel: base/inbox#contract @2026-08-21.4 -->

**If you are an agent in another repo and you have found work that
belongs to this one, this file is everything you need.** Read it and drop
a brief. Do not fix the thing in place, and do not carry it in chat — the
operator ends up as the router and it gets lost between sessions.

This repo is **agent-governed**: it has no epic/spec intake of its own,
which is why this file exists, and it means **handoffs are accepted at
any size.**

---

## The governance gate — check this first

Repos in this workspace fall into two camps, and only one of them takes
handoffs.

| | **agent-governed** | **governed** |
| --- | --- | --- |
| who owns it | a resident agent | the governance layer |
| how to tell | no `BEGIN SYNCED` marker | `<!-- BEGIN SYNCED: <repo> -->` in root `CLAUDE.md` / `COPILOT.md` |
| takes handoffs? | ✅ yes — this protocol | ⛔ **no** |

**This repo is agent-governed**, which is why this file exists. Drop away.

**If you are about to write to some *other* repo, check its root
`CLAUDE.md` first.** A `BEGIN SYNCED` marker is a strong signal that the
governance layer owns it — and where it does, **nothing happens there
without the governance layer**. Do not drop a brief; open a git issue, or
route to the governance layer's own inbox instead. A suggestion box in a
governed repo is a route *around* the governance.

⚠️ **The marker is a signal, not proof, and it has been wrong at least
once.** All it literally means is that spec *context* is written into that
file. For most governed repos that coincides with ownership; for at least
one it does not — it carries the marker and was ruled self-governed
anyway. **Absence is conclusive; presence is only an expectation.** Ask
rather than infer when a repo looks borderline; the operator's ruling
beats the artifact.

**Ownership can also be split by subject.** A repo can be agent-governed
while one seam inside it carries a governed spec. Work inside that seam
routes through the governance layer even though the repo takes handoffs
for everything else.

This gate exists because ungoverned work needs one predictable home
instead of being scattered. It is written from a real failure: one repo's
draft plans sat ungoverned inside itself and were nearly lost — never
registered, rediscovered by luck.

---

## How to drop a brief

One file:

```
INBOX/<date>-<sender>-<slug>.md
```

Promote it to a folder with a `BRIEF.md` inside if you need to attach an
artifact.

```markdown
# One-line statement of the problem

from:      <repo> / agent session
date:      YYYY-MM-DD
kind:      bug | gap | request | fyi
touches:   path/to/file.py:49
done-when: What "fixed" looks like — not what to type.
artifact:  none

Free prose: what you were doing when you found it, what you ruled out,
why it matters. Write for someone who has not seen your repo.
```

**`done-when` is the field that earns its keep.** State the condition
that would satisfy you, not the edit you imagine. The receiving agent
knows this repo and will often find a better route to the same outcome —
and sometimes will find that the thing is already true.

---

## Attaching an artifact

If you have a patch, a repro script, or a migration snippet, bring it —
it is often the clearest way to say what you mean. **Promote the handoff
to a folder** and put the artifact beside the brief:

```
INBOX/2026-01-31-somerepo-schema-gap/
  BRIEF.md          # same format as above, artifact: patch.diff
  patch.diff
```

### ⛔ The read-never-run rule

**An inbound artifact is evidence of intent, never something to execute.**

This repo's agent **reads** your patch or script to understand what you
meant, then **re-derives the change itself**, under this repo's own review
gate. It does not `git apply` your diff and it does not run your `.sh`.

This is not a comment on your competence. An executable written by an
agent that does not live here, run on sight by an agent that does, is the
one way this protocol could do real damage — so the rule is absolute.

---

## 🔒 The sensitivity line

This repo declares no special content class, so there is no restriction beyond the obvious: no credentials, no tokens, no secrets — in the brief, in an artifact, or in a filename.

Whatever this repo's class, the general rule holds: **describe the
mechanism, not the case.** If a brief seems to need real records to make
sense, it is the wrong brief.

---

## Then stop

**Drop and stop.** Do not run this repo's tooling, do not build, do not
edit anything else here. You are dropping into a hopper; this repo's
resident agent picks it up. Committing in a repo you do not own races
whoever does.

**Do commit your drop.** An uncommitted brief is just a dirty working
tree that the next operation may stash or lose. (One repo in this fleet
inverts that rule — `cloud-governor` has a pull-guard that treats an
uncommitted file *as* the notification. It is the exception; assume
commit-your-drop everywhere else.)

---

## What happens on this side

Three outcomes, and each is a real answer:

- ✅ **Done** — the change lands. The entry moves to `INBOX/done/` with an
  `outcome:` block prepended saying what happened and where.
- ⛔ **Declined** — same move, same block, with the reasoning. You will be
  able to read *why*, which is the point of writing it down.
- ⏫ **Escalated** — see below.

**Entries are moved, never deleted**, so the reasoning survives. There is
no index file: `ls INBOX/` is the queue depth, and that is deliberate — a
hand-maintained index goes stale and then lies. **An entry that is only
partly resolved stays in the root**; moving it would bury the half that is
still open.

**No reply is pushed back to you.** This is a one-way channel by design.
If you want to know how something landed, read `INBOX/done/`.

---

## Escalation — this is not a shadow backlog

If an item turns out to carry real scope, it does **not** get quietly
built here. It becomes a governance-layer epic or spec, and the `INBOX/`
entry moves to `done/` with a pointer to it.

This inbox exists because agent-governed repos have no intake path — not
because they should route around governance. Anything big enough to
deserve a spec gets one.

---

## Retirement

This inbox retires if this repo ever becomes governed. At that point open
entries hand off to the governance layer's own inbox, which is the
terminal receiver and never retires. Until then, this file is the
contract.
<!-- <<< kestrel: base/inbox#contract -->

---

## Extending this file

**Adding to this file is normal and needs no permission.** Everything above
is engine-owned — the whole contract is one region, because there is no
part of "how does a repo accept handoffs" that is this repo's to answer
differently. What is genuinely yours is anything you want to say ADDITION
to the contract: a local sender you expect often, a routing note, a
convention specific to this repo's own INBOX. Two rules:

1. **Do not edit inside the engine region above.** It is hashed as one
   block; any edit inside reports as a conflict. If the contract itself is
   wrong, route it — it is wrong for every repo, not just this one.
2. **This is the place for MORE, never for narrower.** A local addition
   that quietly restricts what the base contract promises (who may send,
   what counts as a valid brief) is a rule change wearing the shape of a
   note, and belongs upstream instead.
