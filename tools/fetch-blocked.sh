#!/usr/bin/env bash
# fetch-blocked.sh — retrieve a page that refuses ordinary agent fetches.
#
# WHY THIS EXISTS
# Several primary sources this registry must cite refuse plain HTTP fetches:
# canada.ca (CRA memoranda) returns nothing at all to curl; ccpa-accp.ca,
# nbasw-atsnb.ca, yukon.ca and cpbao.ca have all returned 403 / Cloudflare
# bot-challenges during source research. That left real gaps in the corpus
# and a standing "a human has to go look" answer, which does not scale for a
# registry whose entire product is verbatim quotes from primary sources.
#
# Headless Chromium executes JS and presents a real browser fingerprint, so
# it gets pages curl cannot. Verified 2026-07-31 against CRA GST/HST
# Memorandum 25-3: curl -> no response; this script -> 278KB of real DOM,
# from which every quote in ca-federal-tax-gst-hst-* was verified raw.
#
# WHAT THIS IS NOT
# Not an evasion tool. It does not solve CAPTCHAs, forge credentials, rotate
# identities, or bypass a login. It requests public pages the same way a
# person's browser would, one at a time, and is rate-limited by being a
# manual step. Respect robots.txt and terms of use; if a site genuinely does
# not want automated access, the answer is to ask the operator, not to
# escalate. Read AGENTS.md discipline 1 before citing anything it returns.
#
# TESTED LIMIT — WHERE THIS STOPS, AND WHY IT STOPS THERE
# Two classes of block, and only one of them is ours to solve:
#   WORKS  — servers that simply refuse non-browser clients (no JS, wrong
#            fingerprint). canada.ca returned nothing at all to curl and
#            returns full content here. ccpa-accp.ca 403'd every plain fetch
#            and returns full content here.
#   DOES NOT WORK — Cloudflare's full JS interstitial ("Just a moment...").
#            nbasw-atsnb.ca and yukon.ca sit behind it. Tested 2026-07-31 at
#            15s and 40s virtual-time budgets, and again with a properly
#            driven Selenium/chromedriver session polling for the redirect:
#            the challenge reports "Verification successful" and then never
#            hands over the page, because the automation itself is detected.
# Defeating that needs undetected-driver forks, fingerprint spoofing, or
# proxy rotation. That is deliberately NOT done here: it crosses from
# "fetch a public page the way a browser does" into "defeat a system that is
# actively refusing automated access", which is exactly what the paragraph
# above rules out. For those sources the honest answer really is an operator
# spot-check, and the affected records stay flagged `verified: false` until
# someone looks. Do not "fix" this by reaching for an evasion library.
#
# USAGE
#   tools/fetch-blocked.sh <url>                  # readable text to stdout
#   tools/fetch-blocked.sh <url> --dom            # raw DOM instead
#   tools/fetch-blocked.sh <url> -o out.txt       # write to a file
#   tools/fetch-blocked.sh <url> --wait 25000     # slower JS-heavy pages (ms)
#
# Text mode strips script/style/nav/header/footer and collapses whitespace —
# enough to grep for a quote. Use --dom when structure matters.

set -euo pipefail

URL="${1:-}"
if [[ -z "$URL" || "$URL" == "-h" || "$URL" == "--help" ]]; then
  sed -n '2,32p' "$0" | sed 's/^# \{0,1\}//'
  exit 0
fi
shift

MODE="text"; OUT=""; WAIT="15000"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --dom)  MODE="dom"; shift ;;
    -o)     OUT="${2:-}"; shift 2 ;;
    --wait) WAIT="${2:-15000}"; shift 2 ;;
    *) echo "fetch-blocked: unknown option '$1'" >&2; exit 2 ;;
  esac
done

BIN="$(command -v chromium || command -v chromium-browser || true)"
if [[ -z "$BIN" ]]; then
  echo "fetch-blocked: chromium not installed (apt-get install -y chromium)" >&2
  exit 3
fi

TMP="$(mktemp -d)"; trap 'rm -rf "$TMP"' EXIT

# --no-sandbox is required in this container (no user namespaces). Errors go
# to a file, not the terminal: Chromium is noisy on stderr (GPU/GCM warnings)
# even on a completely successful fetch, and that noise reads as failure.
if ! timeout 120 "$BIN" --headless --disable-gpu --no-sandbox \
      --virtual-time-budget="$WAIT" --dump-dom "$URL" \
      >"$TMP/page.html" 2>"$TMP/err.log"; then
  echo "fetch-blocked: chromium failed for $URL" >&2
  tail -5 "$TMP/err.log" >&2
  exit 4
fi

if [[ ! -s "$TMP/page.html" ]]; then
  echo "fetch-blocked: empty response for $URL (blocked even via browser?)" >&2
  exit 5
fi

if [[ "$MODE" == "dom" ]]; then
  cp "$TMP/page.html" "$TMP/final"
else
  python3 - "$TMP/page.html" "$TMP/final" <<'PY'
import html, re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8", errors="replace").read()
s = re.sub(r"(?is)<(script|style|nav|header|footer|noscript)[^>]*>.*?</\1>", " ", s)
t = html.unescape(re.sub(r"<[^>]+>", " ", s))
t = re.sub(r"[ \t\xa0]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
open(dst, "w", encoding="utf-8").write(t.strip())
PY
fi

if [[ -n "$OUT" ]]; then
  cp "$TMP/final" "$OUT"
  echo "fetch-blocked: wrote $(wc -c <"$OUT") bytes to $OUT" >&2
else
  cat "$TMP/final"
fi
