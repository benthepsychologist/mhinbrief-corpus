<!-- kit: standing/CLAUDE@2026-08-21.1 — canonical: /workspace/kestrel/library/agentdocs/standing/CLAUDE.md.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit. -->

# CLAUDE.md — mhinbrief

**This file is a router, not a manual.** Everything durable lives in
harness-neutral files beside it, so that this repo reads the same to any
agent runtime. Nothing is stated only here.

> ## ⚠️ Read these, in this order, before doing anything
>
> 1. **`OPERATING.md`** — the shared contract: how to run engine tools,
>    **what you own vs. what the engine owns**, the local-extension
>    protocol, jurisdiction, and how to close a session. Identical in
>    every repo the engine tends.
> 2. **`AGENTS.md`** — the disciplines specific to this **standing** kind.
> 3. **`README.md`** — what this particular repo is and how it is laid
>    out.

**What this repo is:** a standing corpus — sourced, operator-confirmed records with an append-only changelog. It is an instance of the kestrel engine
(`/workspace/kestrel`); the engine holds the code, this repo holds the
data and its own local extensions.

**Fastest orientation:** run the repo's `/start` skill. It reads the docs
above plus live state and tells you where the work actually is.

⚠️ **If you take one thing from this file:** before concluding that some
fix belongs in the engine, apply the ownership test in `OPERATING.md` §1.
The answer is usually that the file is yours — a session once reported
otherwise to the operator and was wrong.
