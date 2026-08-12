# STATUS — mhinbrief-corpus (registry instance)

*Hand-maintained. **As of 2026-08-01** (newest note first.)*

**Where things actually stand right now:**

| | |
| --- | --- |
| **Sources** | 50, all `wired`, across all 13 provinces/territories + federal. 3 carry `verified: false` (see below). |
| **Records** | **16 committed** — 4 federal (GST/HST exemption routes) + 12 Ontario (retention, privacy, telepractice, insurance; three each, one per college). |
| **Changelog** | 16 entries, all `record-added`. |
| **Schema** | `record.yaml` **v1, finalized** 2026-07-31. Not a draft, not gated. |
| **Publish** | **Operational.** `publish/adapter.py`, this repo. Single content writer into the site. |
| **Site** | mhinbrief.com live: jurisdiction map, changelog (16 entries + per-entry pages), and 5 topic matrices — tax, retention, privacy, telepractice, insurance. |

**The 3 `verified: false` sources, and why** — `mhcc-workplace-standard`
(scope call for Ben: workplace standard, not clinical-practice
regulation) · `nb-association-social-workers` and `yt-psychologists`
(both behind a full Cloudflare interstitial that `tools/fetch-blocked.sh`
deliberately does not defeat — an operator must look by hand).

> **2026-08-01 — Ontario landed, and the site's own agentdoc was describing
> a different site.** 12 Ontario records committed and published (retention,
> privacy, telepractice, insurance — three each, one per college), taking the
> corpus to 16 records / 16 changelog entries. Four new topic matrices came
> nearly free because `layouts/topics/single.html` was built topic-generic
> rather than tax-specific; 16 rows now render across 5 topic pages.
>
> The sources corrected several starting assumptions, and those corrections
> are the substance: **OCSWSSW does not require liability insurance** (checked
> against O. Reg. 383/00 itself, not the College's summary — a broker FAQ in
> circulation claims the opposite); **PHIPA sets no retention period at all**,
> only secure handling, though s.13(2) can extend retention past the college
> clock during a live access request — which none of the three colleges'
> pages mention; **OCSWSSW's "client's location governs" rule is guidance-tier,
> not a numbered Standard**, unlike CPBAO 16 and CRPO 3.4.5; and the three
> colleges' retention clocks start on *different events* ("last professional
> contact" / "last interaction" / "last entry").
>
> Also: **mhinbrief-site's `CLAUDE.md` named seven paths that don't
> exist in it** — `content/threads|entities|map|claim`, `content/about.md`,
> `content/metric/*`, `assets/css/`. Those are theprojection-site's content
> model; the `site` agentdoc template appears not to vary by instance kind.
> It mattered operationally: `content/changelog/*` IS generated and was not
> on its list, so a session would reasonably have hand-edited it. Rewritten
> locally; canonical fix filed in `kestrel/INBOX/`.

> **2026-08-01 — doc-honesty sweep.** Corrected three stale claims that
> all said the same false thing: `/publish` is a stub whose adapter is
> "not built". It was built and committed 2026-07-31 (`356f6a0`) and has
> published the live corpus. The worst of the three was
> `.claude/skills/publish/SKILL.md` itself — a future session invoking
> `/publish` would have read "this skill is not operational yet" and
> declined to publish. That is an operational falsehood, not a cosmetic
> one. All three live in kit-rendered files, so each carries a local
> override note and a correction is filed in `kestrel/INBOX/` for the
> canonical templates (discipline 11: kestrel is not this repo's
> jurisdiction). Also added `tools/fetch-blocked.sh` to the README, which
> had gone undocumented.

> **2026-07-31 (later) — the schema block was never real; `record.yaml` is
> finalized v1, and the corpus is unblocked.** `schema/record.yaml` had
> carried a `DO NOT FINALIZE` banner since scaffolding, on the stated
> grounds that the worked schema existed only in chat history pending
> "three §14.1 research artifacts." Four independent sweeps (kestrel's 286
> transcripts; pm + cloud-governor's 244; nine other transcript trees; and
> full git history — all refs, deleted files, stashes, reflog, dangling
> objects — across six repos) established that the schema has been
> committed in `pm` since 2026-07-29, at
> `bh-compliance-initiation.md` §7, **with the types and enums the DRAFT
> claimed did not exist**, and byte-identical to Ben's original paste of
> it (2026-07-29T19:22Z). The block came from a three-step degradation:
> pm §7 (full) → kestrel `DESIGN.md` §7 (flattened to bare field names) →
> this repo's `record.yaml` (inherited the flattened list, then documented
> "§7 doesn't specify them" — true of kestrel's copy, false of pm's).
> v1 now restores every enum, splits `enactment_date`/`effective_date`
> back out of the collapsed `status` field, and Canadianizes the
> status vocabulary (`royal_assent`, `in_force`, `not_proclaimed`,
> `died` — Canada has no veto, and "assented but never proclaimed" is a
> real, publishable state: Alberta's CCTA, BC's 2027 counselling-therapy
> date). A correction for kestrel's DESIGN.md is filed in `kestrel/INBOX/`.
> **And the §14.1 question is now CLOSED, not merely narrowed** — Ben,
> same day, after seeing the search: those three reports were run on
> claude.ai's web interface, not in any CLI session, and **did not contain
> schemas we care about**. Nothing schema-shaped is outstanding; no future
> session should re-run this hunt or treat §14.1 as a gate. The initiation
> doc's §5/§13 already carry the Canadian spine and the 11-item
> verification-debt list, which is what actually informs content work.
>
> Also this session: full jurisdiction coverage reached (50 sources across
> all 13 provinces/territories + federal, 26 wired then all flipped live),
> the interactive jurisdiction map shipped to mhinbrief.com with a
> logo/palette pass, and one real bug caught and fixed — the map's click
> panel had never rendered live data, because Hugo's contextual escaper
> was turning the injected JSON into a string (caught by a jsdom harness
> firing real click events; grep/curl checks had all passed it).

> **2026-07-31 — first `/start` run surfaced a kit mismatch; fixed at the
> engine, and this repo's operator now runs it as lead agent for that
> fix.** The rendered `/start` skill this repo had (kit stamp
> `common/start@2026-07-31.1`) was written against an attention-kind
> instance's pipeline (digest status, expectations due, flash rail,
> thread freshness) — none of which exists here. mhinbrief is
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
