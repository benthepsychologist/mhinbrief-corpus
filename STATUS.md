# STATUS — mhinbrief-corpus (registry instance)

*Hand-maintained. **As of 2026-08-18** (newest note first.)*

**Where things actually stand right now:**

| | |
| --- | --- |
| **Sources** | 50, all `wired`, across all 13 provinces/territories + federal. 3 carry `verified: false` (see below). |
| **Records** | **45 committed** — 15 Ontario, 15 Nova Scotia, 10 Quebec, 5 federal. NS and QC were built 2026-08-17, Ontario licensure and federal privacy (PIPEDA) closed immediately after. Every in-play cell now has a record. |
| **Changelog** | 47 entries — 45 `record-added` plus 2 `record-corrected` (the 2026-08-17 Quebec telepractice correction, rendered as an old→new delta rather than absorbed silently). |
| **Candidates** | **86 staged, 0 curated** — still the oldest open item, and note that none of the 45 records came from this queue: coverage was built by directed research against the rubric, which is the point the rubric exists to make. ⚠️ Two sources (`mb-mcsw`, `ns-oipc-phia`) stage a candidate on **every** daily sweep with a 1–2 line diff, so the queue grows ~2/day from what looks like page churn rather than news. Worth triaging or demoting before the count stops meaning anything. |
| **Coverage** | `coverage/matrix.yaml` + `coverage/rubric.md` — the real definition of "done." **45 cells tracked (ON/QC/NS/federal only), all 45 covered, 0 `not_started`, 0 `not_applicable`.** The count moved 43→45 when NS's privacy cell was split into three subtopics to match Ontario's shape. **Coverage is a floor, not an end state** — 5 cells are covered at `confidence: medium`, each naming its own open question in the record's notes. `/tend` still cannot close a cell; directed research does. |
| **Claims** | **1 cell verified statement-by-statement** — `verification/ca-on-retention-psychology.stamp.jsonl`, 3 statements, 6 gaps. Method is pm's `claim-verification-method-spec` v0.2 (STAMP). ⚠️ **3 of 3 statements are unsigned** — signoff is a person's act and nothing here is signed until Ben signs it. |
| **Schema** | `record.yaml` **v1, finalized** 2026-07-31. Not a draft, not gated. |
| **Cadence** | **Running unattended.** A cron line calls `.agents/run.sh tend` daily at 09:00 America/Toronto (`cadence.runs` in `kestrel.yaml`); logs and receipts in `.agents/runs/`, gitignored and pruned to 60. Declared *product* cadence stays weekly — the daily machine schedule is deliberate. ⚠️ The crontab was generated against the EDT offset and **America/Toronto changes offset 2026-11-01** — regenerate then or the runs fire an hour off. |
| **Verify** | `/verify` has now run **once** (2026-08-17, telepractice records, operator-requested after a correction). Receipt: `provenance/verify-20260817T221000Z-telepractice.yaml`. Declared cadence is quarterly. |
| **Publish** | **Operational.** `publish/adapter.py`, this repo. Single content writer into the site; also emits `data/review.yaml` for the review queue. Its engine import broke 2026-08-17 when kestrel moved its publish core out of `tools/publish/core.py` into a package — fixed here, API unchanged, only the path moved. |
| **Site render scope** | `publish/adapter.py`'s `RENDER_JURISDICTIONS` guardrail (added 2026-08-12): every wired jurisdiction is curated, but only **ON, QC, NS, and federal** records actually render to the site — "we are not ready to be responsible outside of those lanes" (Ben). All 45 current records are in-lane, so 0 are excluded today; the filter matters the moment any other jurisdiction's candidates get curated. |
| **Site** | **mhinbrief.com** (renamed from therapybulletin.org, 2026-08-12) live: jurisdiction map (unfiltered, all 14 jurisdictions — a directory of regulators, not a compliance claim, so the render-scope guardrail above doesn't apply to it), changelog (47 entries + per-entry pages), **6 topic matrices** — a `/topics/licensure/` page was added 2026-08-17 because 8 verified licensure records were reaching the site data and rendering nowhere — and an unlisted **`/review/`** page (Cloudflare Access-gated — `ben@mensiomentalhealth.com` **plus** `@evidencefirstsolutions.com`, feedback becomes a GitHub issue attributed to the verified login — see 2026-08-12 note below and the 2026-08-18 access note above). Deploys via `hugo && wrangler deploy` from `mhinbrief-site`, NOT a deploy hook — see that same note. |

**The 3 `verified: false` sources, and why** — `mhcc-workplace-standard`
(scope call for Ben: workplace standard, not clinical-practice
regulation) · `nb-association-social-workers` and `yt-psychologists`
(both behind a full Cloudflare interstitial that `tools/fetch-blocked.sh`
deliberately does not defeat — an operator must look by hand).

> **2026-08-18 — the operator was locked out of his own review page, and the
> login only offers one route.** Ben tried `/review/` and could not get in: the
> Access policy allowed `@evidencefirstsolutions.com` and nothing else, so
> `ben@mensiomentalhealth.com` was never on the list. That is an error from the
> 2026-08-12 build — the design was "EFS colleagues review the queue" and nobody
> added the operator. **Fixed:** the policy now allows his address explicitly
> alongside the EFS domain. Access matches on the email an identity carries, not
> on how it was proved, so either login route satisfies it.
>
> ⛔ **Still open, and it affects colleagues rather than Ben.** The app has
> `auto_redirect_to_identity: true` with **zero identity providers configured**,
> which forces every visitor down a single login path — the Cloudflare-account
> prompt. Ben has said that route is his preference *for himself*. His
> colleagues almost certainly have no Cloudflare account on this org, so as
> configured they may have no way in at all. Setting the flag to `false` shows
> the login picker instead, which serves both: Ben picks the account route,
> colleagues get the email one-time PIN. **The change was attempted and blocked
> by the permission classifier** (an account-settings write) and is waiting on
> Ben to approve it or flip it in the dashboard.
>
> Also corrected: the token's documented scope was wrong in project memory — it
> **can** now read Access identity providers, which is how the empty list was
> found. One-time PIN is a Cloudflare built-in and does not appear in that list,
> so its availability is probable but unconfirmed. **Nobody has ever
> successfully logged in to this page**, so no part of the colleague path has
> been exercised end to end. Treat it as unproven until a colleague gets in.

> **2026-08-18 — the verification pivot: claims get checked one statement at a
> time, and the review page finally has something a clinician can answer.** Ben
> put two things to the session. First, that the `/tend` candidate queue is
> answering a question nobody is asking — *"we aren't a news feed at this time...
> we've got this growing list, for what?"* Second, what he actually needs:
> *"have we nailed file retention for social workers in Ontario? here are our
> claims and sources. verify each, verify overall."* He pointed at pm's existing
> method rather than letting one be invented here.
>
> **Adopted: STAMP** (`pm/streams/research-and-writing/projects/`
> `claim-verified-authorship/deliverables/claim-verification-method-spec`, v0.2).
> Its core move is that the **statement**, not the record, is the unit of
> verification, and that two checks run and are reported **separately and never
> merged**: a mechanical check (does the quote appear verbatim — deterministic,
> no model) and a semantic check (does that quote support the statement as made
> — a judgment, actor named). Then a **signoff by a named person**.
>
> That separation is not academic here. **The Quebec telepractice error the day
> before was exactly a mechanical pass with a semantic failure** — every
> fragment verbatim, and the quote still did not support the claim. This repo's
> `confidence: high|medium|low` is precisely the single combined badge STAMP
> §6.3 prohibits, and it cannot express that state at all. Whether `confidence`
> should be retired from the schema is an open question for the engine, since
> `record.yaml` is engine-shaped.
>
> **Worked example on `ca-on-retention-psychology`** — Ben's own college, and a
> cell that has read `confidence: high` since 2026-07-31 without re-examination.
> All three quotes passed the mechanical check. One did not survive the semantic
> check: our record drops the Standard's opening qualifier *"Unless otherwise
> required by law"* and omits the rest of the same bullet, which lets content
> older than ten years be destroyed for a long-running organizational client
> where it is not relevant to current services. **As written the record is
> stricter than the Standard.** A second statement is fully supported but
> mis-cited — the record's `statute_citation` says s. 9.4 and the obligation is
> at s. 9.6. Six further **gaps** were found: things the Standard says that the
> record asserts nothing about, including the non-HIC counterpart duty at
> 9.5(h), which covers most employed registrants.
>
> **The review page was rebuilt around this.** It had been showing only the raw
> candidate queue — 86 machine-surfaced page diffs and gazette issue numbers,
> every `note` field empty, and **zero feedback ever submitted**, which is what
> an unusable page looks like rather than an adoption problem. Records were
> structurally invisible to it, so Kathryn could not see one of the 15 Nova
> Scotia records she was brought in to fact-check. `publish/adapter.py` now
> emits `data/claims.yaml` and `/review/` renders each statement with its quote,
> its exact location, both check verdicts as separate rows, and its signoff
> state shown as an absence when absent. The feedback path needed no worker
> change — claim refs reuse the existing `candidate_id` field.
>
> **Also landed: a local `/wrap`.** Ben asked for one like theprojection's;
> theirs is kit-rendered `attention/wrap` and the engine library has **no
> `standing/wrap`**. Written as a local extension under OPERATING.md §2, and a
> brief filed at `kestrel-ops/INBOX/` asking the engine to render one, because
> §2's own test — *"would another repo want this unchanged"* — says a standing
> wrap is library-shaped. The local file is banner-marked for deletion when a
> rendered one lands.

> **2026-08-17/18 — full coverage of the four in-play lanes: 16 records → 45,
> and the matrix goes 45/45.** Nova Scotia (15 cells) and Quebec (10) were
> researched against primary sources and built in one pass, then Ontario
> licensure (3) and federal privacy (1) closed the rest. NS's privacy cell was
> split into three subtopics (breach-notification / custodian-status /
> data-residency) to match Ontario's shape, which is why the tracked total moved
> 43 → 45.
>
> The content finding that shapes every page built on this: **naming a
> jurisdiction without naming the profession is usually wrong.** Nova Scotia's
> three professions sit under three different statutes with retention at 10/7/7
> years on three differently-worded clock triggers, and insurance ranging from
> $1M (psychology) to $2M-per-claim/$5M-aggregate with employer cover expressly
> refused (counselling therapy) to "adequate", no figure, private practice only
> (social work). Quebec is the opposite — uniform at 5 years for both
> professions, because its rules are government regulations under one framework
> statute rather than college-authored standards. And the same master's-level
> clinician is a *psychological associate* in Ontario, a *psychologist* in Nova
> Scotia, and *not eligible* in Quebec.
>
> Quebec doesn't fit the profession-by-topic grid and isn't forced to:
> psychotherapy there is a **reserved act** under Loi 21, held automatically by
> physicians and psychologists and available by permit to members of seven other
> ordres — a permit issued and policed by the psychologists' ordre, not their
> own. Read directly, that statutory list includes *criminologues* and
> *sexologues*, which earlier project notes had omitted.
>
> **A correction, kept visible rather than absorbed.** The first Quebec
> telepractice record claimed the OPQ applies a "location-of-the-professional
> jurisdictional test" and built a three-province comparison on it. Ben
> challenged it as implausible — it would have left anyone anywhere free to
> treat Quebec clients — and he was right about the framing. The source is a
> scenario FAQ about *registration*, not a doctrine, and the quote had been
> truncated by an ellipsis that dropped two material clauses. Root cause: that
> record was built on a summarising fetch rather than on text actually read.
> Corrected the same day, with two `record-corrected` changelog entries showing
> the delta, and the reserved-act limit (Code des professions a. 187.1) now
> stated — which is what actually closes the apparent gap.
>
> That prompted a full **`/verify` pass over all 8 telepractice records**, the
> first verify run this instance has ever done. Method was built around the
> failure: locate every quote fragment in source *and read the elided material
> between fragments*. Seven held. Two Ontario quotes join a heading to its body
> or three bullets with semicolons — wording exact, a strict matcher fails, a
> reader is not misled. Receipt in `provenance/`.
>
> Also landed: a `/topics/licensure/` page (8 verified records were reaching
> the site and rendering nowhere), a fix to `publish/adapter.py` after the
> engine moved its publish core into a package, and the first three unattended
> `/tend` runs under the new cron cadence.

> **2026-08-12 — coverage/matrix.yaml + coverage/rubric.md: "acceptable
> coverage" stops being a vague build-order line and becomes a real
> tracked scoreboard.** Ben, questioning the candidates-queue work
> directly: "isn't it still news feed thinking?" — correctly. `/tend`'s
> weekly sweep surfaces whatever changed on a watched page with zero
> judgment about relevance; it can maintain a cell that's already
> `covered` but cannot discover one that isn't. Building QC/NS coverage
> needs a deliberate research pass, not a feed. That distinction is now
> a real artifact: `coverage/rubric.md` defines what "covered" requires
> (primary source, verbatim quote, dated, confidence level honestly
> assigned) and the per-topic granularity rules (most topics are
> profession-specific — confirmed by real cases: OCSWSSW doesn't require
> liability insurance where CPBAO/CRPO do, the three ON colleges'
> retention clocks start on three differently-worded triggers — but
> `privacy` is jurisdiction-wide, one law covering every profession).
> `coverage/matrix.yaml` is the scoreboard: 43 cells across the four
> in-play lanes, 16 covered (exactly the 16 live records, verified by
> script), 27 `not_started`, honestly.
>
> Two real gaps surfaced while building this, not resolved here:
> Quebec's `qc-occoq`/`qc-oppq` sources (conseillers d'orientation,
> psychoéducateurs) don't map onto the record schema's `profession_scope`
> enum — flagged, not enumerated as cells yet. And this session's NS
> `/tend` finds (new duty-to-report standards, a new Code of Ethics) are
> professional-conduct/discipline material that doesn't fit any of the
> five core topics (licensure/telepractice/privacy/retention/insurance)
> — a topic-taxonomy gap, not a research gap, noted on the relevant cell
> rather than force-fit.

> **2026-08-12 — renamed therapybulletin → mhinbrief, and the "deploy
> hook" the old docs described turns out to have likely never been real.**
> Corpus and site renamed end to end: local dirs (`therapybulletin-data`
> → `mhinbrief-corpus`, `therapybulletin-site` → `mhinbrief-site`), GitHub
> repos (Ben, via the web UI — an API rename attempt 403'd, the token
> lacked the `Administration: write` scope a rename specifically needs),
> every in-repo reference, and the live domain (`mhinbrief.com`, which
> turned out to already be an active zone on the Cloudflare account —
> registration was never actually the blocker it looked like). Decision
> itself (mhinbrief over a considered "mhinpractice") was confirmed
> 2026-08-08, reconfirmed 2026-08-11 — closed, not open again. Commits
> `918a97a` (corpus), `ea30565` (site).
>
> Separately, while reconciling the deploy docs: checked Cloudflare's
> deployments API directly rather than trust the old README/CLAUDE.md
> claim of a "push → deploy hook → Cloudflare build" pipeline. **Every
> deployment ever recorded for this site, back to 2026-07-31 when it
> first went live, shows `source: wrangler`, none show a connected
> build** — so that pipeline, "Cloudflare Pages" framing included, was
> likely never the actual mechanism, not something the rename broke. The
> real, always-true mechanism: `hugo` (build) + `wrangler deploy` (ship),
> authenticated via a Cloudflare API token, run manually. Docs in both
> repos corrected to say this; `MHINBRIEF_DEPLOY_HOOK` stays in `.env` as
> documented legacy, not deleted. Commits `b06e1ba` (corpus), `0914ff3`
> (site).

> **2026-08-12 — Cloudflare Worker deployed, custom domain bound, and a
> password-gated `/review/` page shipped for non-technical colleague
> curation review.** This session obtained its first real Cloudflare API
> token (scoped: Workers Scripts/KV/Access on the account, Zone/DNS/
> Workers Routes/SSL on all zones — deliberately no Registrar/Billing/
> Member-management) and used it to deploy the `mhinbrief` Worker, bind
> `mhinbrief.com` via Workers Custom Domains (DNS + cert auto-managed by
> that binding), and stand up Cloudflare Access protecting `/review/` —
> the old `therapybulletin` Worker/domain were untouched throughout, this
> was purely additive.
>
> The `/review/` page (unlisted — `noindex`, `robots.txt` disallow, not in
> nav) renders the staged-candidates queue in plain language from a new
> `data/review.yaml` the adapter now emits, and lets a colleague leave a
> comment that becomes a GitHub issue in this repo. Identity comes from
> Cloudflare Access's login (`@evidencefirstsolutions.com`, email OTP),
> verified server-side in the Worker (`worker/access-jwt.js` checks the
> signed token against Cloudflare's public keys, the `aud` claim, and
> expiry) — not a typed name field. A real gap was caught and fixed while
> verifying this live: Access's path scope only covered `/review` at
> first, leaving `/api/feedback` reachable unauthenticated; widened to
> cover both. This EFS-colleague access is a backend/operational detail,
> not branding — explicitly cleared against this repo's no-EFS-branding
> rule by Ben, not a conflict. Commits `1d13cd1`…`b06e1ba` (corpus, this
> whole arc), `c5fc725`+`65a9328` (site).

> **2026-08-12 — the render-jurisdiction filter, and the 2026-08-12
> `/tend` sweep's 72-candidate queue is still fully uncurated.** Ben's
> call: this corpus curates every wired jurisdiction, but only ON/QC/NS +
> federal are cleared to actually render to the site right now — "we are
> not ready to be responsible outside of those lanes." Implemented as
> `RENDER_JURISDICTIONS` in `publish/adapter.py` (commit `92950a2`);
> doesn't touch the jurisdiction map, which stays showing all 14 (a
> directory of offices/frameworks, not a compliance claim — Ben's
> explicit distinction). Also this session: `/tend` ran, staged 63 new
> candidates on top of 9 pre-existing ones (72 total, commit `1d13cd1`),
> a shortlist of ~10 was read and triaged with a recommended 5-draft/
> 1-defer/4-reject split, Ben approved it — **and then the rename/
> Cloudflare work took over and none of those record changes were ever
> actually written.** This is the oldest real unfinished task in the
> corpus right now, not the infrastructure work above.

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
