# therapybulletin-data

> **Mission.** We're your practical guide to what's happening in the
> field — keeping you legal, current, and out of trouble. (Adopted
> 2026-07-31.)

The **Therapy Bulletin** registry: the compliance-obligation records,
changelog, and instance manifest behind therapybulletin.org. Brand locked
2026-07-31; the site is live; **this repo stays private** — it holds the
working corpus and is not linked from any live site.

It is tended by the kestrel engine via the manifest in `kestrel.yaml`,
which declares the record schema location, the sweep/verify cadence, and
the sources this instance watches. Runner invocation:

    KESTREL_INSTANCE=/workspace/therapybulletin-data \
      python3 /workspace/kestrel/tools/tend.py /workspace/therapybulletin-data

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
therapybulletin.org.

- **Federal (4)** — the GST/HST exemption routes, which are four separate
  provisions with different tests, not one rule: s. 7(j) psychology,
  s. 7(j.1)/(j.2) psychotherapy and counselling therapy, s. 7.2 social work
  (narrower — also requires a professional-client relationship and a clinical
  purpose), s. 6 nursing.
- **Ontario (12)** — records retention, privacy/PHIPA, telepractice, and
  liability insurance, three each: one per college (CPBAO, CRPO, OCSWSSW),
  because the colleges genuinely differ and the differences are the product.

Build order for jurisdiction work, set 2026-07-31: **Ontario → Quebec →
Nova Scotia**. Site content ships only through the `therapybulletin` adapter at
`publish/adapter.py` — **built 2026-07-31**, so `/publish` is no longer a
stub. It emits the changelog pages, `data/records.yaml`, and the
jurisdiction map's `data/regulators.yaml`, under the engine's guarantees
(secret scan, field allowlist, no-empty-wipe, provenance receipt). The
temporary bridge script that previously produced the map data was deleted
in the same change, so the site again has exactly one content writer.

    python3 publish/adapter.py            # staged — writes, does not push
    python3 publish/adapter.py --push     # commit, push, fire deploy hook

**Pushing the site is not the same as deploying it.** therapybulletin-site
builds only on its Cloudflare deploy hook, never on git push. `--push`
fires the hook; a manual push does not. Verify against served content
before reporting anything as live.

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
