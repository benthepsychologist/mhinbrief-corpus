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

    KESTREL_INSTANCE=/workspace/mhinbrief-corpus \
      python3 /workspace/kestrel/tools/tend.py /workspace/mhinbrief-corpus

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

The corpus is live: **16 records** and 16 changelog entries, all rendering on
mhinbrief.com.

- **Federal (4)** — the GST/HST exemption routes, which are four separate
  provisions with different tests, not one rule: s. 7(j) psychology,
  s. 7(j.1)/(j.2) psychotherapy and counselling therapy, s. 7.2 social work
  (narrower — also requires a professional-client relationship and a clinical
  purpose), s. 6 nursing.
- **Ontario (12)** — records retention, privacy/PHIPA, telepractice, and
  liability insurance, three each: one per college (CPBAO, CRPO, OCSWSSW),
  because the colleges genuinely differ and the differences are the product.

Build order for jurisdiction work, set 2026-07-31: **Ontario → Quebec →
Nova Scotia**. As of 2026-08-12, curation isn't limited to those three —
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

It is **not** an evasion tool and has a documented, tested limit: a full
Cloudflare "Just a moment..." interstitial defeats it (verified against
both a long virtual-time budget and a driven Selenium session). Sources
behind that stay flagged `verified: false` pending an operator's own look
— do not reach for an evasion library to close the gap. See the script's
own header.
