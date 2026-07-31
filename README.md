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

Records are not yet populated — population is gated on the §14.1 research
artifacts landing, and until then `schema/record.yaml` stays marked DRAFT
rather than finalized. Site content ships only through the kestrel publish
core's `therapybulletin` adapter (not yet written); the live site currently
carries editorial pages only.
