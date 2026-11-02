#!/bin/sh
# capture_selftest.sh - run this package's own self-test offline, write the real
# capture into self_test/SELFTEST_OUTPUT.md, and compare the printed FAIL lines
# with the printed problem count.
#
# UNTESTED: written and never executed (the step that wrote it had no shell).
# Run from the package folder, with no arguments and no network:
#
#     sh capture_selftest.sh
#
# It writes only inside this package (self_test/SELFTEST_OUTPUT.md) and a
# temporary file. It does not touch data/run_lines.csv, README_DATASET_CARD.md
# or self_test.py, and it uploads nothing. It exits with the self-test's own
# status, so a failing self-test makes this script fail too.

set -u

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
mkdir -p "$here/self_test"
out="$here/self_test/SELFTEST_OUTPUT.md"
raw="${TMPDIR:-/tmp}/selftest-output.$$"

python3 "$here/self_test.py" >"$raw" 2>&1
rc=$?

echo "--- self_test.py output (also written to self_test/SELFTEST_OUTPUT.md) ---"
cat "$raw"
echo "--- exit status: $rc ---"

fails=$(grep -c '^FAIL' "$raw" 2>/dev/null)
case "${fails:-}" in ''|*[!0-9]*) fails=0 ;; esac

summary=$(grep '^self_test:' "$raw" | tail -n 1)
[ -n "${summary:-}" ] || summary="(no line starting 'self_test:' was printed)"

counted=$(printf '%s\n' "$summary" | sed -n \
  -e 's/^self_test: \([0-9][0-9]*\) problem(s)$/\1/p' \
  -e 's/^self_test: [0-9][0-9]*\/[0-9][0-9]*, \([0-9][0-9]*\) problems$/\1/p' \
  | tail -n 1)
case "${counted:-}" in ''|*[!0-9]*) counted="" ;; esac

if [ -n "$counted" ] && [ "$fails" = "$counted" ]; then
  verdict="Match: the number of FAIL lines printed equals the counted figure ($fails)."
else
  verdict="**Mismatch: $fails FAIL line(s) printed against a counted figure of ${counted:-unknown}.** Reported verbatim; neither side was adjusted, and the unnamed problems are not guessed."
fi

{
  printf '# SELFTEST_OUTPUT.md - publish-attribution-run-lines-package\n\n'
  printf 'Provenance: **CAPTURED: YES - written by capture_selftest.sh**, a real run\n'
  printf 'of `self_test.py` from this package folder, no arguments, no network. The\n'
  printf 'block below is stdout+stderr exactly as printed; nothing in it was retyped,\n'
  printf 'reordered or adjusted.\n\n'
  printf 'Ran at (UTC): %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  printf 'Exit status: %s\n\n' "$rc"
  printf '~~~\n'
  cat "$raw"
  printf '~~~\n\n'
  printf '## Count check\n\n'
  printf -- '- FAIL lines printed: %s\n' "$fails"
  printf -- '- Summary line printed: %s\n' "$summary"
  printf -- '- Problems counted by the summary line: %s\n\n' "${counted:-unknown}"
  printf '%s\n\n' "$verdict"
  printf 'Rules unchanged: this script writes neither data/run_lines.csv,\n'
  printf 'README_DATASET_CARD.md nor self_test.py, and uploads nothing.\n\n'
  printf '## Publication gate\n\n'
  if [ "$rc" = "0" ] && [ "$fails" = "0" ]; then
    printf 'A run showing 0 problems and exit 0 permits the next step: publishing\n'
    printf 'README_DATASET_CARD.md plus both data files unchanged under\n'
    printf 'hivepunk-632-4934c76e/ with title attribution-docs-check-fixtures-run-lines.\n'
  else
    printf 'This run does not show 0 problems with exit 0, so nothing is published.\n'
    printf 'Send the output above back as printed rather than publishing.\n'
  fi
  printf '\n---\nBee #632. Card: https://hivemindos.app/bee/632. A person decides; a bee\n'
  printf 'never merges anything. CC0-1.0 for this note.\n'
} >"$out"

rm -f "$raw"

if [ -n "$counted" ] && [ "$fails" = "$counted" ]; then
  echo "FAIL lines: $fails, counted: $counted - match"
else
  echo "FAIL lines: $fails, counted: ${counted:-unknown} - MISMATCH (reported verbatim)"
fi
echo "capture written: self_test/SELFTEST_OUTPUT.md"
exit "$rc"
