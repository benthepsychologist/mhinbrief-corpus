# mhinbrief-corpus

> **Mission.** We're your practical guide to what's happening in the
> field — keeping you legal, current, and out of trouble. (Adopted
> 2026-07-31.)

The **MH in Brief** registry: the compliance-obligation records,
changelog, and instance manifest behind mhinbrief.com. Originally
branded "Therapy Bulletin" (locked 2026-07-31); renamed to MH in Brief
2026-08-12 (decision reconfirmed 2026-08-11 over an "mhinpractice"
alternative — "in brief" fits a regulatory-digest corpus better than
anything implying clinical practice guidance). **This repo stays
private** — it holds the working corpus and is not linked from any live
site.

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
Nova Scotia**. Site content ships only through the `mhinbrief` adapter at
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
