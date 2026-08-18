# You now have an `INBOX/` that actually exists — and a standing-kind gap worth knowing

from:      kestrel / engine session
date:      2026-08-18
kind:      fyi
touches:   `AGENTS.md` (90 -> 315 lines), `INBOX/`, `.agents/run.sh`, 12 kit files
done-when: You have read this, and decided about `STATUS.md` and the publish cadence.
artifact:  none

---

## Your `INBOX/` did not exist until today

You had `INBOX.md` — the contract telling other repos' agents how to hand
you work — and **no `INBOX/` directory**. Anyone following that contract
correctly either created the folder as a side effect or gave up. `kestrel
fleet status` had been reporting *"no INBOX/ — this repo cannot be handed
work"* and that was literally true.

It now ships with a keepfile, so it survives a fresh clone. This note is
the first thing in it.

## Your `AGENTS.md` more than tripled, and none of it is new prose

90 -> 315 lines. The growth is the shared layer arriving, not new rules
about you: your nine numbered `standing` disciplines are unchanged and
still there, below the base. What is gone is the duplicated preamble your
kind template used to carry (its own H1 and its own "read `OPERATING.md`
first" block) — the base says both once now.

## ⚠️ A gap that is the kit's fault, not yours

Your scheduled run collects and then stops. **`/publish` is not scheduled
at all** — your `kestrel.yaml` declares one `cadence.runs` entry, `tend` at
09:00. The `standing` pipeline is `tend -> curate -> publish`, `/tend` is
contractually forbidden from doing the other two, and `/curate` needs a
human on every candidate and can never be automated.

The `attention` kind escapes this only because its `/daily` is one
monolithic turn. **This is a gap in the standing kit, not a
misconfiguration by you**, and it is recorded in kestrel's design doc.
Ben has ruled the deploy step will use `MHINBRIEF_DEPLOY_HOOK` from your
site repo's `.env` rather than a `wrangler` install.

Adding a second `cadence.runs` entry for `publish` is yours to decide.

## What is held back

**`STATUS.md` — untouched**, and reports as drift. Same reason as
everywhere: overwriting a real snapshot with a seeded skeleton is what the
unbuilt `migrate` verb is for. Worth fixing by hand: your `As of` line
needs to sit alone on its own line for the freshness check to read it.

## What happened, from scratch

**kestrel** is the engine that renders a versioned set of operating
documents and skills into each repo it administers, hashes what it wrote,
and reports drift. This repo is one of its six targets.

On 2026-08-18 Ben ruled that the **base layer is a schema, not a seed**:
the documents every agent repo has — `AGENTS.md`, `OPERATING.md`,
`INBOX.md`, `STATUS.md` — get an ordered list of sections with an owner
each, and the engine now lints them. Four things landed here as a result.

1. **`AGENTS.md` gained a shared layer.** The base was previously a
   near-empty skeleton; it now carries two engine-owned sections — what a
   kestrel-administered agent repo *is*, and five disciplines the fleet had
   been re-deriving separately in seven different wordings (the operator
   confirms / the agent proposes · provenance travels with the artifact ·
   read `INBOX/` at session start · read-never-run · `yaml.safe_load` or
   revert). Those five were mined from the fleet's own real files, not
   invented. **The operator-confirms rule alone was independently restated
   in four of seven repos**, which is what justified promoting it.

2. **A kind no longer replaces the base.** A kind template is now a
   `.part.tmpl` that *appends*, so a kinded repo gets the shared layer
   **and** its kind's disciplines in one file.

3. **`INBOX/` ships with `INBOX.md`.** Three repos had the contract and no
   queue directory — the file described a hopper that was not there.

4. **`kestrel fleet status` now lints the core docs.** A missing core doc
   is an `alert` with no grace period. Non-conformance is a `warn`, because
   every repo predates the schema — that is migration backlog, not
   breakage. Diverged files report `exempt` and are never flagged.

## Two things about this commit specifically

⚠️ **kestrel committed in your repo, which it normally must not do.**
Discipline 6 says instance repos are tended, not owned, and the commit is
the resident agent's. Ben instructed this one directly — *"do all the
commits and leave notes for each agent so they know what happened."* It is
a one-off on his word, not a new default. Nothing here was authored on your
behalf: every file in the commit is either a rendered kit artifact or this
note.

⚠️ **A bug was found and fixed mid-install, and it touched your stamp.**
`--skip` (meaning "not now") and `--diverge` (meaning "permanently mine")
share one encoding — a null stamp entry *is* diverge. For a file that had
never been stamped, `--skip` wrote that null, silently marking it
permanently yours. Eight files across five repos were affected, and
`kestrel fleet sync` reported all of them as **clean**. Fixed; the entries
were repaired by diffing each stamp against its committed state, which
preserved deliberate divergences. Your held-back files below now correctly
report as drift, which is what "not now" is supposed to look like.
