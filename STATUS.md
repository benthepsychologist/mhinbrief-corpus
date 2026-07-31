# STATUS — therapybulletin-data (registry instance)

*Hand-maintained. **As of 2026-07-31** (first STATUS.md for this repo;
newest note first.)*

> **2026-07-31 (later) — the schema block was never real; `record.yaml` is
> finalized v1, and the corpus is unblocked.** `schema/record.yaml` had
> carried a `DO NOT FINALIZE` banner since scaffolding, on the stated
> grounds that the worked schema existed only in chat history pending
> "three §14.1 research artifacts." Four independent sweeps (kestrel's 286
> transcripts; pm + cloud-governor's 244; nine other transcript trees; and
> full git history — all refs, deleted files, stashes, reflog, dangling
> objects — across six repos) established that the schema has been
> committed in `pm` since 2026-07-29, at
> `bh-compliance-initiation.md` §7, **with the types and enums the DRAFT
> claimed did not exist**, and byte-identical to Ben's original paste of
> it (2026-07-29T19:22Z). The block came from a three-step degradation:
> pm §7 (full) → kestrel `DESIGN.md` §7 (flattened to bare field names) →
> this repo's `record.yaml` (inherited the flattened list, then documented
> "§7 doesn't specify them" — true of kestrel's copy, false of pm's).
> v1 now restores every enum, splits `enactment_date`/`effective_date`
> back out of the collapsed `status` field, and Canadianizes the
> status vocabulary (`royal_assent`, `in_force`, `not_proclaimed`,
> `died` — Canada has no veto, and "assented but never proclaimed" is a
> real, publishable state: Alberta's CCTA, BC's 2027 counselling-therapy
> date). A correction for kestrel's DESIGN.md is filed in `kestrel/INBOX/`.
> **Genuinely still missing:** the three raw research *reports*. They gate
> US-phase content depth, not the schema; the initiation doc's §5/§13
> already carry the Canadian spine and the 11-item verification-debt list.
>
> Also this session: full jurisdiction coverage reached (50 sources across
> all 13 provinces/territories + federal, 26 wired then all flipped live),
> the interactive jurisdiction map shipped to therapybulletin.org with a
> logo/palette pass, and one real bug caught and fixed — the map's click
> panel had never rendered live data, because Hugo's contextual escaper
> was turning the injected JSON into a string (caught by a jsdom harness
> firing real click events; grep/curl checks had all passed it).

> **2026-07-31 — first `/start` run surfaced a kit mismatch; fixed at the
> engine, and this repo's operator now runs it as lead agent for that
> fix.** The rendered `/start` skill this repo had (kit stamp
> `common/start@2026-07-31.1`) was written against an attention-kind
> instance's pipeline (digest status, expectations due, flash rail,
> thread freshness) — none of which exists here. therapybulletin is
> `kind: registry`: its live state is `candidates/` by status,
> `records/`/`changelog/` counts, per-source feed health, and
> provenance/snapshot freshness, a genuinely different shape. Fixed at
> `/workspace/kestrel` by splitting the skill into two kind-specific
> templates — `library/skills/attention/start/SKILL.md.tmpl` (relocated,
> content unchanged) and `library/skills/registry/start/SKILL.md.tmpl`
> (new) — so `kit.py`'s existing family-selection rule (`common` +
> `<kind>`) resolves the right one per instance with no template-level
> conditionals. Library bumped to `2026-07-31.2`, `kit.py sync --apply`
> run across all four kit-managed repos (kestrel itself needed no
> render — it's the library, not a target); this repo, theprojection-data,
> and both sites picked up the new stamp. All four commits are local
> only, **none pushed yet** — check `git log @{u}..` before assuming
> otherwise.
>
> Current pipeline state at the time of this note: 9 candidates staged
> from `canada-gazette-p2` (federal only), zero curated, `records/` and
> `changelog/` both empty (expected pre-population — see README.md).
> Manifest (`kestrel.yaml`) carries exactly 2 sources, both federal/
> Ontario (`canada-gazette-p2`, `crpo-news`) — nowhere near the 13
> provincial/territorial jurisdictions (10 provinces + 3 territories,
> not 14) this registry will eventually need to cite against. Building
> that jurisdiction/source master list is the next real milestone before
> this instance can claim broad coverage; curating the 9 staged
> candidates is a smaller, unblocked task that can happen either before
> or alongside it.
