#!/usr/bin/env bash
# kit: base/run@2026-08-21.3 — canonical: kestrel/library/runners/run.sh.tmpl — provenance only. A local edit is fine; kit.py sync will flag drift. Route a wanted template change to the engine's issue tracker (dev) or its ops inbox (anything naming a live repo), never a direct edit.
#
# Unattended runner for mhinbrief. A cron line calls:
#
#     <this repo>/.agents/run.sh <skill>
#
# The path is the caller's to supply and is NOT baked in here: this file
# derives its own repo from its own location, so the fleet can be dropped on
# a fresh machine at any root and every runner still works unchanged.
#
# THIS FILE IS YOURS. It is rendered from the engine's canonical template so
# every repo starts identical, but it lives here, it is stamped here, and you
# may change it — the same relationship your publish adapter has with the
# engine's publish core. If your repo needs a different invocation, edit it
# and let it report as diverged; that is the system working, not a fault.
#
# ⚠️ The cron line deliberately carries NOTHING but a time and a skill name.
# Everything about HOW this repo runs lives in here, so evolving the
# invocation never means regenerating anyone's crontab.

set -euo pipefail

SKILL="${1:?usage: run.sh <skill-name>   e.g. run.sh daily}"

# ── cron's PATH is not your PATH ────────────────────────────────────────────
# The single most common way a runner that works by hand fails on a schedule.
# cron gives a job `PATH=/usr/bin:/bin` and nothing else, so an agent CLI
# installed under a user prefix — npm's ~/.npm-global/bin, ~/.local/bin, a
# version manager's shim — is simply not found, and the job dies at 3am with
# "command not found" into a log nobody is reading.
#
# Resolve it here rather than baking an absolute path into the cron line: the
# binary can move (a reinstall, a version bump) without anyone having to
# regenerate a crontab, which is the same reasoning that keeps the cron line
# down to a time and a skill name.
# Written as an `if` for readability rather than out of necessity: a bare
# `[ -d x ] && ...` is ALSO safe here, because `set -e` exempts a command
# that is part of an `&&` list, and that exemption covers the enclosing
# loop. (Checked by running it, 2026-08-15, after asserting the opposite.)
for candidate in "$HOME/.npm-global/bin" "$HOME/.local/bin" /usr/local/bin; do
    if [ -d "$candidate" ]; then
        case ":$PATH:" in
            *":$candidate:"*) ;;
            *) PATH="$candidate:$PATH" ;;
        esac
    fi
done
export PATH

if ! command -v claude >/dev/null 2>&1; then
    echo "run.sh: FATAL — 'claude' is not on PATH ($PATH)." >&2
    echo "  This repo's cadence cannot run. Either install it somewhere on the" >&2
    echo "  PATH above, or edit this file (it is yours) to name its location." >&2
    exit 127
fi

# The runtime below is claude because this repo declares
# content.sensitivity: normal in its own kestrel.yaml. A repo
# holding restricted content names the harness cleared to read it, and the
# engine renders THAT here — an unattended run must not be able to reach
# an uncleared runtime just because nobody thought about it.
# ⚠️ Derived, never rendered. An absolute path baked in at render time is
# correct on exactly one machine and silently wrong everywhere else — the run
# still starts, then reads and writes the wrong tree. `cd`+`pwd` gives the
# physical path, which is what --add-dir needs.
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# The site sibling, as this repo's own manifest declares it. A relative
# declaration resolves against THIS repo, so it travels; an absolute one is
# honoured as given, for a target that genuinely lives elsewhere.
SITE_DECL="../mhinbrief-site"
SITE=""
if [ -n "$SITE_DECL" ]; then
  case "$SITE_DECL" in
    /*) SITE="$SITE_DECL" ;;
    *)  SITE="$(cd "$REPO/$SITE_DECL" 2>/dev/null && pwd)" || SITE="" ;;
  esac
  if [ -z "$SITE" ]; then
    echo "[run.sh] WARNING: declared site '$SITE_DECL' does not resolve from $REPO — continuing without it" >&2
  fi
fi

# An ARRAY, not a string. `--add-dir "$SITE"` with an unresolved SITE passes
# an empty argument, and the scope guard is the thing least able to afford a
# silently malformed flag — an empty --add-dir is not a smaller scope, it is
# an unpredictable one. A site that did not resolve contributes nothing here.
ADD_DIRS=(--add-dir "$REPO")
if [ -n "$SITE" ]; then
    ADD_DIRS+=(--add-dir "$SITE")
fi
RUN_ID="$(date -u +%Y-%m-%dT%H%M%SZ)"
LOG_DIR="$REPO/.agents/runs"
LOG="$LOG_DIR/${RUN_ID}-${SKILL}.log"
RECEIPT="$LOG_DIR/${RUN_ID}-${SKILL}.receipt"

mkdir -p "$LOG_DIR"

# ── Keep run output out of git ──────────────────────────────────────────────
# Logs and receipts are produced by every scheduled run, so without this the
# repo has an unclean working tree permanently, from the day cron is wired up.
# Two things break when that happens, and both are worse than they sound:
# `kestrel fleet status`'s git signal goes red for every cadence repo and stops
# meaning anything, and a `/wrap` doing a scoped add can sweep a day of logs
# into a commit.
#
# A directory-local .gitignore rather than a line in the repo's root one: the
# root .gitignore belongs to the repo, is not a kit artifact, and editing it
# from the engine would be writing to a file kestrel does not own. This file
# ignores its own directory, needs no cooperation from anybody, and heals
# itself if deleted.
if [ ! -f "$LOG_DIR/.gitignore" ]; then
    printf '# Run logs and receipts — written by run.sh, never committed.\n*\n' \
        > "$LOG_DIR/.gitignore"
fi

# ── Prune old runs ──────────────────────────────────────────────────────────
# A twice-daily cadence leaves ~730 logs a year. Keep the last 60 of each kind;
# the receipt for a run three months ago has already told anyone who was going
# to look. Failures are preserved by the same rule that preserves successes —
# if that ever proves wrong, it is this line that changes.
# The trailing `|| true` is load-bearing, not defensive habit: `ls` exits 2
# when its glob matches nothing, which is precisely a repo's FIRST scheduled
# run, and `set -o pipefail` promotes that to a fatal error before the run
# starts. Found by running this file under a stripped cron-like environment
# on 2026-08-15 — it exits 2 with no output, so it would have failed silently
# at 09:00 and looked like cron never fired.
ls -1t "$LOG_DIR"/*.log 2>/dev/null | tail -n +61 | xargs -r rm -f || true
ls -1t "$LOG_DIR"/*.receipt 2>/dev/null | tail -n +61 | xargs -r rm -f || true

# ── Never lap a run ─────────────────────────────────────────────────────────
# A sweep that takes longer than the gap between two scheduled runs must not
# have a second copy start on top of it. `flock -n` fails immediately rather
# than queueing, because a run that starts an hour late is worse than one that
# is skipped and reported.
exec 9>"/tmp/kestrel-run-mhinbrief-${SKILL}.lock"
if ! flock -n 9; then
    echo "SKIPPED: a previous '${SKILL}' run is still going" | tee -a "$LOG"
    printf 'skill=%s\nstarted=%s\noutcome=skipped-locked\n' "$SKILL" "$RUN_ID" > "$RECEIPT"
    exit 0
fi

# ── Run it ─────────────────────────────────────────────────────────────────
# Headless, non-interactive, from the repo root.
#
# ⚠️ `--permission-mode auto` is REQUIRED, not a convenience (Ben,
# 2026-08-14): anything stricter stalls partway through /start and /daily,
# and a run that cannot finish is worse than no run — it leaves the repo
# half-swept with no published output. The same reasoning covers the
# publish: a /daily that stops short of publishing means the site never
# goes live, which is the entire point of running it on a schedule.
#
# So permissions are NOT the safety surface here. Two other things are, and
# both hold regardless of permission mode:
#
#   * SCOPE — `--add-dir` names this repo and its site sibling, and nothing
#     else. An unattended run can do this instance's own work; it cannot
#     wander into the engine or a sibling corpus.
#   * THE PUBLISH CORE'S OWN GUARANTEES — secret scan, field allowlist, and
#     the no-empty-wipe guard, which is precisely the unattended failure
#     worth fearing: a run that collects nothing must never wipe the live
#     site back to empty. Those are mechanical and cannot be skipped by an
#     adapter or a permission flag.
#
# And the receipt below is the third leg: a failed 3am run is detectable
# the next morning rather than invisible.
start_epoch=$(date -u +%s)
set +e
(
  cd "$REPO"
  claude -p "/${SKILL}" \
      --permission-mode auto \
      "${ADD_DIRS[@]}"
) >>"$LOG" 2>&1
status=$?
set -e
end_epoch=$(date -u +%s)

# ── Leave a receipt ────────────────────────────────────────────────────────
# The point of the receipt is that `kestrel fleet status` can read it and say
# "this repo's 14:00 daily has failed two days running". Without it, an
# unattended failure is invisible until someone notices the output missing.
#
# `dirty` is the second thing it has to record, and it exists because exit
# status alone LIED. A real unattended run announced it would wait for a
# backgrounded sweep, ended the turn on that sentence, never reached its
# commit step — and exited 0, because the CLI did shut down cleanly after
# printing it. `exit=0 dirty=46` is distinguishable from success; `exit=0`
# on its own is not. This runner's own logs and receipts do not inflate the
# count: they live under a directory it .gitignores itself.
# ⚠️ Guarded, not inlined, and this script has paid for the lesson once
# already. `set -o pipefail` is on, so ANY failing command in a `$(...)`
# assignment aborts the whole run — and it aborts it HERE, after the work
# is done and before the receipt is written, which is the worst possible
# place. The 2026-08-15 fix hit exactly this shape with the log-prune `ls`
# on an empty glob; writing it inline reintroduced it for a target that is
# not a git repo. `?` is a real answer: "not recorded" is not "clean".
dirty="?"
if git -C "$REPO" rev-parse --git-dir >/dev/null 2>&1; then
    dirty=$(git -C "$REPO" status --porcelain 2>/dev/null | wc -l | tr -d ' ') \
        || dirty="?"
fi
printf 'skill=%s\nstarted=%s\nseconds=%s\nexit=%s\noutcome=%s\ndirty=%s\nlog=%s\n' \
    "$SKILL" "$RUN_ID" "$((end_epoch - start_epoch))" "$status" \
    "$([ "$status" -eq 0 ] && echo ok || echo FAILED)" "$dirty" "$LOG" > "$RECEIPT"

if [ "$status" -ne 0 ]; then
    echo "run.sh: '${SKILL}' FAILED (exit ${status}) — see $LOG" >&2
fi
exit "$status"
