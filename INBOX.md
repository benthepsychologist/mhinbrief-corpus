<!-- kit: base/INBOX@2026-08-14.13 — canonical: /workspace/kestrel/library/agentdocs/base/INBOX.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# INBOX.md — the contract for handing work to mhinbrief

**If you are an agent in another repo and you have found work that
belongs to this one, this file is everything you need.** Read it and drop
a brief. Do not fix the thing in place, and do not carry it in chat — the
operator ends up as the router and it gets lost between sessions.

This repo is **agent-governed**: it has no epic/spec intake of its own,
which is why this file exists, and it means **handoffs are accepted at
any size.**

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

- **Inbound artifacts are read and re-derived, never executed.** A patch
  or script you attach is evidence of intent — this repo's agent reads
  it, understands it, and writes the change itself. No applying a diff on
  sight, no running an attached script.
- **Settled entries move to `INBOX/done/` with an `outcome:` block
  prepended** — moved, never deleted, so the reasoning survives. There is
  no index file: `ls INBOX/` is the queue depth, and that is deliberate.
- **An entry that is only partly resolved stays in the root.** Moving it
  would bury the part that is still open.

---

## Retirement

This inbox retires if this repo ever becomes governed. At that point open
entries hand off to the governance layer's own inbox, which is the
terminal receiver and never retires. Until then, this file is the
contract.
