#!/usr/bin/env python3
"""publish/adapter.py — the `mhinbrief` publish adapter.

This is the ONE content writer into /workspace/mhinbrief-site
(AGENTS.md discipline 9). Nothing else may hand-write generated registry
content there. It replaces the stub state that `/publish` documented, and
it fully absorbs the temporary bridge that was at
mhinbrief-site/scripts/gen-regulators-data.py — that script existed
only because this adapter did not, and was DELETED in the same change that
added this one, so the site again has exactly one writer.

WHY THIS LIVES HERE AND NOT IN THE ENGINE
kestrel.yaml's `outputs.adapter: publish/adapter.py` is a path relative to
THIS instance root (convention set kestrel-side, 2026-07-31: adapters are
instance code). The engine keeps the guarantees; the instance keeps the
shape of its own corpus. Concretely, this module imports and uses
kestrel's kestrel/publish/core.py for:

    secret_scan()               every emitted byte passes it
    apply_allowlist()           field gate on records crossing the boundary
    write_provenance_manifest() the per-run publish receipt
    push_site()                 git add/commit/push + deploy-hook fire

It deliberately does NOT use core.run() or core.referenced_only(): those
are attention-kind shaped (threads, board, payload) and a registry has no
such objects. The orchestration below is the registry's own, but it
preserves the same guarantees in the same order.

WHAT IT EMITS
  content/changelog/<stem>.md   one page per changelog entry. The site's
                                layouts/changelog/list.html + partials/
                                changelog-entry.html already expect exactly
                                these front-matter keys — the template was
                                built first and sat empty; this fills it.
                                The weekly rollup of these IS the newsletter.
  data/records.yaml             allowlisted record fields, grouped by topic
                                and by jurisdiction, for matrix/hub rendering.
  data/regulators.yaml          the jurisdiction map's per-province regulator
                                list, from kestrel.yaml's sources. Absorbed
                                from the old scripts/gen-regulators-data.py
                                bridge so the site has exactly ONE content
                                writer (discipline 9) rather than an adapter
                                plus a leftover script.
  data/review.yaml              staged candidates/*.yaml (pending curation),
                                for the unlisted /review/ page — lets a
                                non-technical colleague see the queue in
                                plain language instead of reading YAML in
                                the repo. Ben, 2026-08-12. Written every run,
                                same as the other data/ outputs — it is NOT
                                gated behind RENDER_JURISDICTIONS (that
                                filter is about published CLAIMS; a review
                                queue asserts nothing, it's just visibility
                                into what's pending).

Usage:
    python3 publish/adapter.py                # staged: write, do not push
    python3 publish/adapter.py --push         # write, commit, push, deploy
    python3 publish/adapter.py --dry-run      # report only, write nothing
"""
import argparse
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

INSTANCE_ROOT = Path(__file__).resolve().parent.parent
# The engine's publish core moved from tools/publish/core.py into a proper
# package (kestrel/publish/) during the 2026-08 restructure; tools/publish.py
# is now a deprecated shim that re-exports only main(), so the old
# `from publish import core` resolves to that shim and raises ImportError.
# Import from the package instead. Found 2026-08-17, the first publish run
# after the restructure — nothing in this repo changed, the engine moved.
ENGINE_ROOT = Path("/workspace/kestrel")
sys.path.insert(0, str(ENGINE_ROOT))
from kestrel.publish import core  # noqa: E402  (path set above, deliberately)

# Fields allowed to cross into the site. `notes` is EXCLUDED on purpose:
# it carries internal curation commentary — operator scope calls, "retire
# candidate", verification-split warnings, open-item flags — which is
# working material, not reader-facing content. Publishing it raw would
# leak process into the product. Anything in `notes` that a reader needs
# belongs in clinician_facing_obligations or source_quote instead.
ALLOWED_RECORD_FIELDS = [
    "jurisdiction", "profession_scope", "topic", "regulatory_model",
    "statute_citation", "status", "enactment_date", "effective_date",
    "enforcement_body", "authority_basis", "penalties",
    "clinician_facing_obligations", "vendor_facing_obligations",
    "consent_required", "documentation_required",
    "source_url", "source_quote", "last_verified", "confidence",
]

JURISDICTION_NAMES = {
    "ca-federal": "Federal", "ca-on": "Ontario", "ca-qc": "Quebec",
    "ca-ns": "Nova Scotia", "ca-bc": "British Columbia", "ca-ab": "Alberta",
    "ca-sk": "Saskatchewan", "ca-mb": "Manitoba", "ca-nb": "New Brunswick",
    "ca-nl": "Newfoundland and Labrador", "ca-pe": "Prince Edward Island",
    "ca-yt": "Yukon", "ca-nt": "Northwest Territories", "ca-nu": "Nunavut",
}
TOPIC_NAMES = {
    "licensure": "Licensure", "scope": "Scope of practice",
    "telepractice": "Telepractice", "privacy": "Privacy",
    "retention": "Records retention", "insurance": "Liability insurance",
    "tax": "GST/HST", "ai": "AI in practice", "payer": "Payers",
}
# --- interim rendering guardrail (Ben, 2026-08-12) --------------------
# The corpus curates records for every jurisdiction kestrel.yaml wires
# (currently all 14), but Ben's call: "we are not ready to be responsible
# outside of those lanes" — ON/QC/NS (+federal, since federal obligations
# apply regardless of province and aren't an "unready lane" the way a
# province is) are the only jurisdictions that render to the site right
# now. Everything else is still fully curated — recorded in records/,
# diffed into changelog/ — just excluded at this one point, by design, so
# the corpus doesn't lose the work while the site doesn't publish claims
# for jurisdictions not yet verified to that standard. The interactive
# jurisdiction map (build_regulators_data) is NOT filtered — Ben's call,
# same date: it links to official regulator sites and asserts no
# compliance claim, so it stays showing all wired jurisdictions.
#
# To lift the filter once a jurisdiction is ready: add its code here (or
# set RENDER_JURISDICTIONS = None to publish everything curated).
RENDER_JURISDICTIONS = {"ca-on", "ca-qc", "ca-ns", "ca-federal"}


def filter_for_site(records):
    """Apply RENDER_JURISDICTIONS. Curated-but-not-cleared jurisdictions
    stay in records/ untouched — this only trims what publish() emits."""
    if RENDER_JURISDICTIONS is None:
        return records
    return {
        rid: rec for rid, rec in records.items()
        if (rec.get("jurisdiction") or {}).get("code") in RENDER_JURISDICTIONS
    }


PROFESSION_NAMES = {
    "psychologist": "psychology",
    "psychotherapist": "psychotherapy",
    "counselling_therapist": "counselling therapy",
    "clinical_social_worker": "social work",
    "mft": "marriage and family therapy",
    "counselor": "counselling",
}


def subject_label(rid, rec):
    """What this record is ABOUT, in reader words — used to make entry
    titles distinguishable. Without this, four different GST/HST records
    all title as 'GST/HST, Federal' and the changelog reads as four
    identical links (caught on the first real publish, 2026-07-31).

    Falls back to the record_id's trailing segment when profession_scope
    is deliberately empty — e.g. the nursing record, which is in the
    corpus for comparison but is not scoped to a profession this registry
    serves."""
    scope = rec.get("profession_scope") or []
    names = [PROFESSION_NAMES.get(p, p.replace("_", " ")) for p in scope]
    if names:
        if len(names) == 1:
            return names[0]
        return ", ".join(names[:-1]) + " and " + names[-1]
    tail = rid.rsplit("-", 1)[-1]
    return tail.replace("_", " ")


def load_manifest():
    return yaml.safe_load((INSTANCE_ROOT / "kestrel.yaml").read_text())


def load_records():
    """Every records/*.yaml, keyed by record_id (the filename stem).
    yaml.safe_load throughout — safe-load-or-revert (AGENTS.md)."""
    out = {}
    for p in sorted((INSTANCE_ROOT / "records").glob("*.yaml")):
        rec = yaml.safe_load(p.read_text())
        if rec:
            out[p.stem] = rec
    return out


def load_candidates():
    """Every candidates/*.yaml with status: staged — the pending curation
    queue. Deferred/accepted/rejected candidates carry a resolution and are
    excluded; they're history, not something a reviewer needs to weigh in
    on. safe-load-or-skip, same discipline as load_records()."""
    out = []
    for p in sorted((INSTANCE_ROOT / "candidates").glob("*.yaml")):
        c = yaml.safe_load(p.read_text())
        if c and c.get("status") == "staged":
            c["candidate_id"] = p.stem
            out.append(c)
    return out


def build_review_data(candidates):
    """Plain-language queue for the /review/ page — title, source link,
    quote-or-note, when it was staged. No YAML, no jargon; a colleague
    should be able to read this without knowing what a 'candidate' is."""
    items = []
    for c in candidates:
        src = c.get("source") or {}
        items.append({
            "candidate_id": c.get("candidate_id"),
            "title": src.get("title") or "(untitled)",
            "url": src.get("url"),
            "source_name": (src.get("source_id") or "").split(":", 1)[-1],
            "published": src.get("ts"),
            "observed": c.get("observed"),
            "note": c.get("note") or "",
        })
    return {
        "generated_by": "mhinbrief publish adapter (publish/adapter.py)",
        "count": len(items),
        "items": items,
    }


def load_changelog():
    entries = []
    for p in sorted((INSTANCE_ROOT / "changelog").glob("*.yaml")):
        e = yaml.safe_load(p.read_text())
        if e:
            entries.append((p.stem, e))
    return entries


def _yaml_scalar(v):
    """Front-matter-safe scalar. Quotes and escapes; never emits a bare
    string that could break the YAML block."""
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    s = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'


def build_changelog_pages(changelog, records):
    """One markdown page per changelog entry, front-matter matching what
    partials/changelog-entry.html already reads."""
    pages = {}
    for stem, e in changelog:
        rid = e.get("record_id", "")
        rec = records.get(rid)
        if rec is None:
            # record doesn't exist, or was filtered out by
            # RENDER_JURISDICTIONS — either way, nothing to render.
            continue
        juris = (rec.get("jurisdiction") or {}).get("code", "")
        topic = rec.get("topic", "")
        kind = e.get("kind", "")

        subject = subject_label(rid, rec)
        where = JURISDICTION_NAMES.get(juris, juris)
        what = TOPIC_NAMES.get(topic, topic)

        if kind == "record-added":
            title = f"{what} — {subject} ({where})"
            old_s, new_s = None, None
            body = (rec.get("clinician_facing_obligations") or "").strip()
        elif kind == "record-retired":
            title = f"Retired: {what} — {subject} ({where})"
            old_s, new_s = None, None
            body = ""
        else:
            field = e.get("field", "")
            title = f"{what} — {subject} ({where}): {field} changed"
            # only field-changes render an old->new delta; a record-added's
            # `new` is the whole record dict and would render as garbage.
            old_s = e.get("old")
            new_s = e.get("new")
            body = ""

        quote = (rec.get("source_quote") or "").strip()
        fm = [
            "---",
            f"title: {_yaml_scalar(title)}",
            f"date: {e.get('observed')}",
            f"jurisdiction: {_yaml_scalar(JURISDICTION_NAMES.get(juris, juris))}",
            f"topic: {_yaml_scalar(TOPIC_NAMES.get(topic, topic))}",
            f"status: {_yaml_scalar(e.get('status'))}",
            f"record_id: {_yaml_scalar(rid)}",
            f"source_url: {_yaml_scalar(e.get('source_url'))}",
            f"source_label: {_yaml_scalar((rec.get('statute_citation') or {}).get('code_cite') or 'primary source')}",
            f"last_verified: {_yaml_scalar(rec.get('last_verified'))}",
        ]
        if old_s is not None and not isinstance(old_s, (dict, list)):
            fm.append(f"old: {_yaml_scalar(old_s)}")
        if new_s is not None and not isinstance(new_s, (dict, list)):
            fm.append(f"new: {_yaml_scalar(new_s)}")
        fm.append("---")

        md = "\n".join(fm) + "\n\n"
        if body:
            md += body + "\n\n"
        if quote:
            md += "> " + quote.replace("\n", "\n> ") + "\n"
        pages[f"content/changelog/{stem}.md"] = md
    return pages


def build_records_data(records):
    """Allowlisted records, grouped for the site's hub/matrix templates."""
    by_topic, by_jurisdiction, flat = {}, {}, {}
    for rid, rec in records.items():
        pub = core.apply_allowlist(rec, ALLOWED_RECORD_FIELDS)
        pub["record_id"] = rid
        flat[rid] = pub
        by_topic.setdefault(rec.get("topic", "unsorted"), []).append(pub)
        code = (rec.get("jurisdiction") or {}).get("code", "unsorted")
        by_jurisdiction.setdefault(code, []).append(pub)
    return {
        "generated_by": "mhinbrief publish adapter (publish/adapter.py)",
        "record_count": len(flat),
        "topic_names": TOPIC_NAMES,
        "jurisdiction_names": JURISDICTION_NAMES,
        "by_topic": by_topic,
        "by_jurisdiction": by_jurisdiction,
        "records": flat,
    }


TIER_LABEL = {1: "Regulator", 2: "Quasi-regulatory / associations", 3: "Association"}


def build_regulators_data(manifest):
    """The jurisdiction map's data, from kestrel.yaml's `sources`.

    Absorbed from mhinbrief-site/scripts/gen-regulators-data.py, which
    existed only because this adapter didn't. Keeping both would mean two
    writers into one site — the exact thing discipline 9 forbids — so that
    script is deleted in the same change that adds this."""
    by_j = {}
    for s in manifest.get("sources", []):
        by_j.setdefault(s["jurisdiction"], []).append({
            "id": s["id"],
            "name": s["name"],
            "org_type": s.get("org_type"),
            "tier": s.get("tier"),
            "tier_label": TIER_LABEL.get(s.get("tier"), ""),
            "language": s.get("language"),
            "website": s.get("website") or s.get("endpoint") or s.get("feed_url"),
            "status": s.get("status"),
            "verified": s.get("verified", True),
        })
    for j in by_j:
        by_j[j].sort(key=lambda e: (e["tier"] or 9, e["name"]))
    return {
        "generated_by": "mhinbrief publish adapter (publish/adapter.py)",
        "source_manifest": "mhinbrief-corpus/kestrel.yaml",
        "jurisdictions": by_j,
    }


def main():
    ap = argparse.ArgumentParser(description="mhinbrief publish adapter")
    ap.add_argument("--push", action="store_true",
                    help="commit + push the site repo (does NOT deploy mhinbrief.com — "
                         "that's a separate `wrangler deploy` pass, see mhinbrief-site/README.md)")
    ap.add_argument("--dry-run", action="store_true",
                    help="report what would be written; write nothing")
    args = ap.parse_args()

    manifest = load_manifest()
    site_dir = (INSTANCE_ROOT / manifest["outputs"]["site"]).resolve()
    all_records = load_records()
    records = filter_for_site(all_records)
    excluded = len(all_records) - len(records)
    changelog = load_changelog()
    candidates = load_candidates()

    print(f"[publish] instance : {INSTANCE_ROOT}")
    print(f"[publish] site     : {site_dir}")
    print(f"[publish] records curated: {len(all_records)}")
    if RENDER_JURISDICTIONS is not None:
        print(f"[publish] records site-eligible: {len(records)} "
              f"({excluded} excluded by RENDER_JURISDICTIONS={sorted(RENDER_JURISDICTIONS)})")
    print(f"[publish] changelog: {len(changelog)}")
    print(f"[publish] review queue: {len(candidates)} staged candidates")

    pages = build_changelog_pages(changelog, records)
    data = build_records_data(records)
    data_blob = yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100)
    regs = build_regulators_data(manifest)
    regs_blob = yaml.safe_dump(regs, sort_keys=False, allow_unicode=True, width=100)
    review = build_review_data(candidates)
    review_blob = yaml.safe_dump(review, sort_keys=False, allow_unicode=True, width=100)

    # --- guarantee 1: secret scan, every emitted byte, editorial or not
    hits = []
    for path, text in pages.items():
        hits += core.secret_scan(text, path)
    hits += core.secret_scan(data_blob, "data/records.yaml")
    hits += core.secret_scan(regs_blob, "data/regulators.yaml")
    hits += core.secret_scan(review_blob, "data/review.yaml")
    if hits:
        print("[publish] ABORT — secret scan hit:")
        for h in hits:
            print(f"  {h}")
        return 2
    print(f"[publish] secret scan: clean ({len(pages)} pages + data blob)")

    # --- guarantee 2: no-empty-wipe. Zero publishable leaves the site alone.
    if not pages and not records:
        print("[publish] nothing publishable — leaving site untouched (no-empty-wipe)")
        return 0

    if args.dry_run:
        print("[publish] --dry-run, writing nothing:")
        for p in sorted(pages):
            print(f"  would write {p}")
        print(f"  would write data/records.yaml ({len(data_blob)} bytes)")
        print(f"  would write data/regulators.yaml ({len(regs_blob)} bytes)")
        print(f"  would write data/review.yaml ({len(review_blob)} bytes)")
        return 0

    # --- write
    written = []
    for rel, text in sorted(pages.items()):
        dest = site_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding="utf-8")
        written.append(rel)
    data_path = site_dir / "data" / "records.yaml"
    data_path.parent.mkdir(parents=True, exist_ok=True)
    data_path.write_text(data_blob, encoding="utf-8")
    written.append("data/records.yaml")
    regs_path = site_dir / "data" / "regulators.yaml"
    regs_path.write_text(regs_blob, encoding="utf-8")
    written.append("data/regulators.yaml")
    review_path = site_dir / "data" / "review.yaml"
    review_path.write_text(review_blob, encoding="utf-8")
    written.append("data/review.yaml")
    for w in written:
        print(f"  wrote {w}")

    # --- guarantee 3: provenance receipt in THIS instance (AGENTS.md #10)
    now = datetime.now(timezone.utc)
    core.write_provenance_manifest(str(INSTANCE_ROOT), {
        "kind": "publish",
        "adapter": "mhinbrief",
        "published_at": now.isoformat(),
        "records": len(records),
        "records_curated_total": len(all_records),
        "records_excluded_by_render_filter": excluded,
        "render_jurisdictions": sorted(RENDER_JURISDICTIONS) if RENDER_JURISDICTIONS else None,
        "review_queue_count": len(candidates),
        "changelog_entries": len(changelog),
        "files_written": written,
        "allowlist": ALLOWED_RECORD_FIELDS,
        "site": str(site_dir),
    }, now)

    # --- guarantee 4: push is explicit, never a side effect of building
    if args.push:
        hook = os.environ.get("MHINBRIEF_DEPLOY_HOOK", "")
        if not hook:
            env_file = site_dir / ".env"
            if env_file.exists():
                for line in env_file.read_text().splitlines():
                    if line.startswith("MHINBRIEF_DEPLOY_HOOK="):
                        hook = line.split("=", 1)[1].strip()
        # NOTE, 2026-08-12: firing this hook is a no-op today. mhinbrief is
        # a Cloudflare Worker with static assets, deployed by a direct
        # `wrangler deploy` pass in mhinbrief-site (see that repo's
        # README/CLAUDE.md) — not by a git-connected build. Checked via
        # Cloudflare's deployments API: every deployment ever recorded for
        # this site shows source=wrangler, none show a connected build, so
        # this was likely never the real mechanism even before the rename.
        # Kept (rather than removed) so `core.push_site`'s other guarantee
        # — an explicit, auditable push, never a silent side effect of
        # building — still holds; only the hook-fire step is now inert.
        print("[publish] NOTE: this push does not deploy mhinbrief.com. "
              "That site is a Cloudflare Worker, deployed by running "
              "`hugo && wrangler deploy` in mhinbrief-site directly — see "
              "that repo's README.md. This commit lands the generated "
              "content in its git history but does not go live by itself.")
        core.push_site(str(site_dir), hook,
                       f"publish: {len(records)} records, {len(changelog)} changelog entries")
    else:
        print("[publish] staged only — review the diff, then re-run with --push")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
