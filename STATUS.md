# STATUS — therapybulletin-data (registry instance)

*Hand-maintained. **As of 2026-07-31** (first STATUS.md for this repo —
none existed before this note; top note below, no prior dated entries.)*

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
