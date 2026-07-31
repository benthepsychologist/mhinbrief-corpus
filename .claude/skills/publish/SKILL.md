<!-- kit: registry/publish@2026-07-31.2 — canonical: /workspace/kestrel/library/skills/registry/publish/SKILL.md.tmpl — edit the canonical copy and run /sync-kits, not this file. -->

# /publish — STUB, gated on the therapybulletin adapter

**This skill is not operational yet, and says so rather than pretending.**

Publishing this registry to /workspace/therapybulletin-site requires a
`therapybulletin` adapter in the engine's publish core
(`/workspace/kestrel/tools/publish/adapters/`) — the component that turns
`records/` + `changelog/` into the site's matrix pages, changelog page,
and data JSON, under the core's guarantees (secret scan, field
allowlists, no-empty-wipe). Per kestrel `ROADMAP/DESIGN.md` §6, that
adapter is designed but **not built**.

Until it exists:

- The site (/workspace/therapybulletin-site) is editorial-only — its content is
  hand-authored site code, not generated registry exports.
- Do NOT hand-write "generated-looking" registry content into the site
  repo to bridge the gap — that breaks the single-content-writer
  invariant the eventual adapter depends on, and creates pages the
  adapter would later fight.
- When the adapter lands, this stub is replaced via `/sync-kits` with
  the real skill (run staged, review the diff, `--push` deploys — every
  push to the site's main is a production deploy).

If you were asked to publish and reached this stub: report the gate
plainly and point at the adapter as the next engine work item.
