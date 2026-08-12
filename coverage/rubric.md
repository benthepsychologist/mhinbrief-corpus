# Coverage rubric — the shadow matrix

This file defines what a "cell" in `coverage/matrix.yaml` actually means,
what has to be true for it to count as `covered`, and which sources are
authoritative for it. **This is the criteria; `matrix.yaml` is the
scoreboard.** Ben, 2026-08-12: "a shadow matrix with our coverage
criteria, sources, and guidelines" — this is that file.

## The distinction this exists to enforce

**Matrix admission is not a gate. Completeness is a gate.** Every topic
below is legitimately trackable in principle — nothing is excluded on
subject-matter grounds. What gates a cell from `not_started` to `covered`
is not "does a record exist" but **"have we polled the source material
well enough that if someone asks, we can say we've handled the
research."** A thin record sourced to a secondary summary is not covered;
it's `researching`, flagged honestly.

**`/tend`'s crawl sits on the back of this matrix, not the other way
around.** The weekly sweep is a maintenance signal for cells that are
already `covered` — "did the thing we've already established change."
It cannot discover an uncovered cell; it can only tell you a watched page
posted something. Building coverage for a `not_started` cell is a
deliberate, directed research pass — go find the statute, the
regulation, the college standard, read it, decide you're confident —
not something to wait for a feed to surface piecemeal. See
[[project-render-jurisdiction-filter]] and the corpus README's build
order for the related but separate publish-scope gate (a cell can be
`covered` and still not render publicly if its jurisdiction isn't
cleared).

## Cell statuses

- **`not_started`** — no research done, no record exists. The honest
  default for anything not yet worked.
- **`researching`** — a candidate or a lead exists (e.g. something
  `/tend` surfaced, or a partial read) but it hasn't been verified
  against a primary source to the confidence bar below. Not published,
  not counted as coverage — a `researching` cell is explicitly NOT
  ready and should not be mistaken for done.
- **`covered`** — a record exists, sourced primary (or the best
  available primary-adjacent source with the gap noted), quoted, dated,
  and the operator is confident it reflects current reality. Maps to a
  `record_id` in `records/`.
- **`not_applicable`** — the cell genuinely doesn't exist for this
  jurisdiction/profession (e.g. a profession isn't regulated there at
  all). Requires a one-line reason, same discipline as a real finding —
  "no regulator" is itself a publishable fact, not an empty cell.

## What "covered" requires, concretely

A cell is NOT `covered` on the strength of a news item, a college blog
post, or a secondary summary alone. It requires:

1. **A primary source** — the actual statute, regulation, or college
   Standard of Practice, not a summary of it. `source_url` in the
   record points here.
2. **A verbatim quote** (`source_quote`) supporting the specific claim,
   not a paraphrase.
3. **A `last_verified` date** — mechanically enforced already by
   `kestrel.yaml`'s `governance.record_change_requires`.
4. **`confidence: high`** requires the primary source was read directly.
   `confidence: medium` is acceptable when only a corroborating
   secondary source is available (flag why in `notes`); `confidence: low`
   ships only if genuinely necessary, visibly flagged, never silently.
5. **The instrument type stated plainly** — is this a statute, a
   regulation made under a statute, or a college-enforceable Standard of
   Practice? These carry different binding force and a record must not
   blur them (see `records/ca-on-retention-psychology.yaml`'s `notes`
   for the worked example: the retention *number* comes from a College
   Standard, not PHIPA, which is silent on duration).

## Granularity varies by topic — this is not a uniform grid

Some topics differ by profession within a jurisdiction (each college sets
its own rule); some don't (one law governs everyone). Forcing every topic
into "one cell per profession" would either duplicate identical rows or
miss that a law is jurisdiction-wide. Per current evidence:

| Topic | Granularity | Why |
|---|---|---|
| `licensure` | profession-specific | Registration requirements are set per college |
| `telepractice` | profession-specific | Confirmed different requirements across ON's three colleges already |
| `retention` | profession-specific | Confirmed: ON's three colleges word the trigger differently ("last professional contact" / "last interaction" / "last entry") and PHIPA itself sets no duration |
| `insurance` | profession-specific | Confirmed: OCSWSSW does NOT require liability insurance while CPBAO/CRPO do — a jurisdiction-wide cell would have hidden this |
| `privacy` | **jurisdiction-wide** | Provincial privacy statutes (PHIPA, PHIA, Quebec's Law 25) apply across professions; sub-questions (breach notification, custodian status, data residency) are the right split, not profession |
| `tax` | profession-specific | Confirmed: GST/HST exemption is four separate Excise Tax Act provisions with different tests per profession |
| `scope` | profession-specific | Scope of practice is inherently profession-defined |
| `ai` | not yet determined | Opportunistic so far (the OCCOQ finding) — decide granularity when deliberately researched, don't force it now |
| `payer` | not yet determined | Same — opportunistic only so far |

**Quebec does not fit this grid cleanly, and the rubric does not force
it to.** Psychotherapy in Quebec is a **reserved act under Loi 21**, not
a profession — psychologists hold it automatically, and members of
several *other* ordres (OTSTCFQ, OPPQ, OCCOQ, some OTs and nurses) may be
authorized to perform it by permit. Tracking this as one profession's
"scope" cell would misrepresent it. It gets its own sui-generis row:
`qc / (cross-cutting) / psychotherapy-permit`.

## Jurisdiction rosters — who's actually regulated, and who watches them

Scoped to the four lanes actually in play (matches
[[project-render-jurisdiction-filter]] — ON/QC/NS/federal). The other 10
wired jurisdictions are NOT matrix-tracked yet; their sources still run
in `/tend`'s sweep as opportunistic scouting only, per the mission's
pilot order.

**Federal** — no registration body (professions are provincially
regulated); federal authority is cross-cutting (tax, privacy where
provincial law doesn't apply). Sources: `canada-gazette-p1/p2`
(legislative instrument), `opc-pipeda` (privacy regulator),
`cra-gst-hst-counselling` (tax), `cpa-national`/`ccpa-national`/
`casw-national` (associations, corroboration only — not authoritative).

**Ontario** — `psychologist` (CPBAO, tier 1), `psychotherapist` (CRPO,
tier 1), `clinical_social_worker` (OCSWSSW, tier 1). Base statute:
`on-rhpa-elaws` (RHPA). Associations (OPA, OASW) are corroboration only.

**Nova Scotia** — `psychologist` (NSRP, tier 1), `counselling_therapist`
(NSCCT, tier 1), `clinical_social_worker` (NSCSW, tier 1). Base
instrument: `ns-royal-gazette-part-ii`. Privacy regulator:
`ns-oipc-phia`. Association (APNS) is corroboration only.

**Quebec** — `psychologist` (Ordre des psychologues, tier 1),
`clinical_social_worker` (OTSTCFQ, tier 1). Base authority:
`qc-office-professions` + `qc-gazette-officielle`. Privacy regulator:
`qc-cai`. Association (APQ) is corroboration only.

⚠️ **Open question, not resolved here:** `qc-occoq` (conseillers
d'orientation) and `qc-oppq` (psychoéducateurs) are wired sources and
real regulated professions relevant to Quebec's psychotherapy-permit web,
but neither maps cleanly onto the record schema's `profession_scope`
enum (`psychologist | psychotherapist | counselling_therapist |
clinical_social_worker | mft | counselor`). Not enumerated as full matrix
rows until Ben decides whether/how to extend the enum — flagged here so
it isn't silently dropped, same discipline as any other open item.

## How to use this when actually researching a cell

1. Check `matrix.yaml` for the cell's current status and its
   `authoritative_sources` list.
2. Read the primary source(s) directly — not the college's own summary
   of it if the underlying statute/regulation/Standard is reachable.
3. Draft the record per `schema/record.yaml`, through `/curate`'s normal
   operator-confirms discipline (AGENTS.md #1–#2) — this rubric doesn't
   change that, it only changes *what informs the decision to start
   researching a cell in the first place*.
4. Update `matrix.yaml`'s status, `record_id`, `confidence`, and
   `last_reviewed` together with the record itself, same commit.
