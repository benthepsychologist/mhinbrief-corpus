<!-- kit: base/health@2026-08-21.1 — canonical: /workspace/kestrel/library/skills/base/health/SKILL.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

---
name: health
description: Read-only health check of this repo — kit drift, whether STATUS.md still describes reality, git state (uncommitted/unpushed), and inbox depth. Run it when picking up a session, before closing one, or any time you want to know whether this repo is actually in the state its docs claim.
---

# /health — is this repo in the state it says it is?

One command, four signals, **read-only**:

```sh
kestrel fleet status --target /workspace/mhinbrief-corpus --verbose
```

| signal | what it answers |
| --- | --- |
| **kit** | are the engine-rendered files current, deliberately diverged, drifted, or orphaned |
| **docs** | does `STATUS.md`'s own "as of" date still match what git has done since |
| **git** | uncommitted work · **unpushed commits** · missing upstream · detached HEAD |
| **inbox** | how many briefs are open, and how old is the oldest |

## Reading the result

**`ok` and `note` are not problems.** A `note` is information — being
`behind` the library is the *designed* state between engine releases, and
"no `INBOX/`" simply means this repo has not been set up to take handoffs.
Only `warn` and `alert` want a human.

⚠️ **`diverged by design` is reported as `ok`, on purpose.** It means a
human recorded that a file is permanently this repo's own. It is not
drift and it never becomes drift. If it ever starts reading as a problem,
that is a bug in the checker, not a task for you — the whole reason this
distinction exists is that a row which is always red trains its reader to
skim past red rows.

**The one to act on first is almost always `git`.** Unpushed commits are
invisible to `git status` and accumulate silently across sessions — this
was found once at 17 commits deep, inherited across two sessions that had
each closed without checking.

## What this does NOT do

**It never fixes anything.** Not kit drift, not a stale `STATUS.md`, not
an unpushed commit. Deciding what to do about a finding is a judgment
call, and several of them are not even this repo's to make — kit drift is
the engine's machinery, and a "another repo has a pattern this one lacks"
finding is an allocation question for the operator. See `OPERATING.md` §1
for what is yours.

**It is not a substitute for reading.** A green card means four mechanical
checks passed, not that the work is right.
