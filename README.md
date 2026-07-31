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

Records are not yet populated; population is now unblocked and begins
with Ontario/Quebec (build order set 2026-07-31: **Ontario → Quebec →
Nova Scotia**). Site content ships only through the `therapybulletin` adapter at
`publish/adapter.py` — **built 2026-07-31**, so `/publish` is no longer a
stub. It emits the changelog pages, `data/records.yaml`, and the
jurisdiction map's `data/regulators.yaml`, under the engine's guarantees
(secret scan, field allowlist, no-empty-wipe, provenance receipt). The
temporary bridge script that previously produced the map data was deleted
in the same change, so the site again has exactly one content writer.

    python3 publish/adapter.py            # staged — writes, does not push
    python3 publish/adapter.py --push     # commit, push, fire deploy hook
