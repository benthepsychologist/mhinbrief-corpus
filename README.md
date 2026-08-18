# mhinbrief-corpus

> **Mission.** We're your practical guide to what's happening in the
> field — keeping you legal, current, and out of trouble. (Adopted
> 2026-07-31.)

The **MH in Brief** registry: the compliance-obligation records,
changelog, and instance manifest behind mhinbrief.com. Originally
branded "Therapy Bulletin" (locked 2026-07-31); renamed to MH in Brief
2026-08-12 (decision reconfirmed 2026-08-11 over an "mhinpractice"
alternative — "in brief" fits a regulatory-digest corpus better than
anything implying clinical practice guidance).

**This repo is public** (Ben, 2026-08-12, confirming what was already
true on GitHub — no visibility change made). The corpus content is
sourced government/regulatory citations, not sensitive data, and the
working-corpus material (candidates, provenance, curation notes) carries
nothing that needs hiding either. This repo previously carried a "stays
private" claim inherited unchanged from its original pre-launch
scaffolding note ("private and dark... build dark until brand placement
resolves") — that was a launch-sequencing placeholder, never a
considered privacy decision, and GitHub itself was public the entire
time regardless of what this file said. Same pattern, same public-by-
default stance, as `theprojection-corpus`/`theprojection-site`.

It is tended by the kestrel engine via the manifest in `kestrel.yaml`,
which declares the record schema location, the sweep/verify cadence, and
the sources this instance watches. Runner invocation:

    kestrel tend --instance /workspace/mhinbrief-corpus

The engine restructured its tooling into a package in August 2026. The older
form still works —

    KESTREL_INSTANCE=/workspace/mhinbrief-corpus \
      python3 /workspace/kestrel/tools/tend.py /workspace/mhinbrief-corpus

— but `tools/tend.py` is now a **deprecated shim** kept alive only through the
engine's transition window, and it will be removed. The same restructure broke
this repo's `publish/adapter.py`, which imported the engine's publish core from
its old path; fixed 2026-08-17 (the core's API was unchanged — only its location
moved). If an engine import suddenly fails, check whether the module moved
before assuming anything here is at fault.

**The sweep also runs unattended.** `kestrel.yaml` declares a machine schedule
(`cadence.runs`) and a cron line calls `.agents/run.sh tend` daily at 09:00
America/Toronto. Run logs and receipts land in `.agents/runs/` (gitignored,
pruned to the last 60). Note the declared *product* cadence is weekly while the
machine schedule fires daily — that is deliberate, not drift.

`schema/record.yaml` was **finalized v1 on 2026-07-31**. It had been marked
DRAFT on the stated grounds that the worked schema was chat-history-only,
pending "§14.1 research artifacts" — that turned out to be false. The
schema, with full types and enums, has been committed in the `pm` repo
since 2026-07-29 (`bh-compliance-initiation.md` §7) and was verified
byte-identical to the original paste that created it. The §14.1 question is
now **closed**: Ben confirmed (2026-07-31) that those three reports were run
on claude.ai's web interface, not in any CLI session, and that they did not
contain schemas we care about — so nothing schema-shaped is outstanding and
this hunt should not be re-run. See the schema file's own header for the
full trace.

The corpus is live: **45 records** and 47 changelog entries, all rendering on
mhinbrief.com.

- **Federal (5)** — the four GST/HST exemption routes, which are separate
  provisions with different tests, not one rule: s. 7(j) psychology,
  s. 7(j.1)/(j.2) psychotherapy and counselling therapy, s. 7.2 social work
  (narrower — also requires a professional-client relationship and a clinical
  purpose), s. 6 nursing. Plus **PIPEDA**: a "substantially similar" provincial
  law exempts a clinician only for what occurs *within* the province, so
  cross-border work sits under both regimes.
- **Ontario (15)** — retention, privacy/PHIPA, telepractice, insurance and
  licensure, three each: one per college (CPBAO, CRPO, OCSWSSW), because the
  colleges genuinely differ and the differences are the product. Privacy splits
  by sub-question (breach / custodian status / data residency) rather than by
  profession, since one statute covers them all.
- **Nova Scotia (15)** — same five topics, one each for NSRP (psychology),
  NSCCT (counselling therapy) and NSCSW (social work). The three professions
  sit under three different statutes and disagree with each other on retention
  (10/7/7 years, three differently-worded triggers) and on insurance.
- **Quebec (10)** — psychology and social work across four topics, plus Law 25
  privacy and a sui-generis record for the **Loi 21 psychotherapy permit**:
  psychotherapy in Quebec is a reserved *act*, not a profession, so it does not
  fit the profession-by-topic grid and is not forced into it.

**What "done" means is tracked, not vague.** `coverage/matrix.yaml` is
the actual scoreboard — 45 cells across ON/QC/NS/federal (jurisdiction ×
profession × topic, with the granularity rules and per-cell criteria
defined in `coverage/rubric.md`), **all 45 covered as of 2026-08-18**.
Coverage is a floor, not an end state: five cells are `covered` at
`confidence: medium`, each naming its own open question in the record's
notes, and `/verify` re-checks what is already there.
`/tend`'s weekly sweep is a maintenance signal for cells already
`covered` — it cannot discover a `not_started` cell; closing one is a
deliberate research pass against the rubric, not something to wait for a
feed to surface. The build order set 2026-07-31 (**Ontario → Quebec →
Nova Scotia**) is **complete** — all four in-play lanes were closed
2026-08-17/18. Curation isn't limited to those lanes —
every wired jurisdiction can be curated into `records/` — but
`publish/adapter.py`'s `RENDER_JURISDICTIONS` guardrail means only
ON/QC/NS + federal records actually reach the site; see STATUS.md for
why. Site content ships only through the `mhinbrief` adapter at
`publish/adapter.py` — **built 2026-07-31**, so `/publish` is no longer a
stub. It emits the changelog pages, `data/records.yaml`, and the
jurisdiction map's `data/regulators.yaml`, under the engine's guarantees
(secret scan, field allowlist, no-empty-wipe, provenance receipt). The
temporary bridge script that previously produced the map data was deleted
in the same change, so the site again has exactly one content writer.

    python3 publish/adapter.py            # staged — writes, does not push
    python3 publish/adapter.py --push     # commit + push into mhinbrief-site's git history

**Pushing the site is not the same as deploying it.** `mhinbrief` is a
Cloudflare Worker with static assets, deployed by pushing straight to
Cloudflare (`hugo && wrangler deploy` in `mhinbrief-site`, see that repo's
CLAUDE.md/README.md), not by anything git-triggered. `--push` here still
does something real (lands the generated changelog/records/review data in
`mhinbrief-site`'s git history, under the engine's guarantees) — it just
doesn't put anything live by itself. **Checked directly (2026-08-12) via
Cloudflare's deployments API: every recorded deployment of this site,
back to 2026-07-31 when it first went live, shows `source: wrangler` —
none show a connected build.** The old docs described a "push → deploy
hook → Cloudflare build" pipeline; the evidence says that was likely
never the actual mechanism, and the site has always gone live via a
manual `wrangler deploy` pass, same as now. Verify against served content
(`curl -s https://mhinbrief.com/`) before reporting anything as live.

## Non-technical review of the pending queue

`mhinbrief.com/review/` (unlisted — not in site nav, `noindex`, not
meant to be discovered, just not treated as secret) renders every staged
`candidates/*.yaml` in plain language, so a colleague can review what
`/tend` found without reading YAML. It's gated by Cloudflare Access
(`@evidencefirstsolutions.com`, one-time-PIN login) covering both
`/review` and `/api/feedback`; a comment left there becomes a GitHub
issue in this repo, attributed to the verified login email — see
`mhinbrief-site/worker/access-jwt.js` and STATUS.md's 2026-08-12 entry
for the detail. `data/review.yaml` (site repo) is generated by
`publish/adapter.py`'s `build_review_data()` on every run, same as the
other `data/` outputs.

## Fetching sources that block agents

Several primary sources this registry must quote refuse ordinary HTTP —
canada.ca (CRA memoranda) returns nothing to `curl`, and Ontario e-Laws is
JavaScript-rendered. `tools/fetch-blocked.sh` runs headless Chromium and
returns readable page text:

    tools/fetch-blocked.sh <url>              # readable text
    tools/fetch-blocked.sh <url> --dom        # raw DOM
    tools/fetch-blocked.sh <url> -o out.txt   # to a file

**Use it rather than re-deriving a headless-browser invocation.** Confirmed
2026-08-18 against Ontario e-Laws regulation pages, which return an identical
~54KB JavaScript shell to any plain fetch (and whose own `/laws/docs/` path
returns S3 `AccessDenied`, while CanLII 403s). A session re-solved that from
scratch with raw `chromium --dump-dom` before noticing this script already
existed and worked.

It is **not** an evasion tool and has a documented, tested limit: a full
Cloudflare "Just a moment..." interstitial defeats it (verified against
both a long virtual-time budget and a driven Selenium session). Sources
behind that stay flagged `verified: false` pending an operator's own look
— do not reach for an evasion library to close the gap. See the script's
own header.
