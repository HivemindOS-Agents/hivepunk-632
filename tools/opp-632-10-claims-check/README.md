# opp-632-10-claims-check

opportunity: opp-632-10

Small stdlib-only checker that records each claim from the linked follow-up discussion (the attribution-docs / card-fixtures-checker research history) and whether the cited traces support it.

## How to run

~~~bash
cd tools/opp-632-10-claims-check
python3 self_test.py; echo EXIT=$?
python3 checker.py; echo EXIT=$?
python3 checker.py <dir> --json; echo EXIT=$?
~~~

No arguments required for the embedded sample, no network, no install. An optional `<dir>` argument must hold `claims.json` (list of {id, claim, traces[], verdict}) and `evidence.json` (list of {id, title, url}). Prints one line per claim, any findings, then RESULT=pass|fail and EXIT=0|1.

## What it does

- Records each claim with its declared verdict and a recomputed verdict from its cited traces: 0 valid traces = unsupported, 1 = partial, 2+ = supported. Valid means the trace id exists in evidence.json.
- Flags verdict mismatches, missing traces, duplicate claim/evidence ids, empty claims/titles, and evidence URLs not starting with http:// or https://.
- Embedded sample: 5 claims (c1 supported, c2 supported, c3 partial, c4 unsupported, c5 supported) against 6 evidence items distilled from the linked follow-up discussion sources (issues 134, 60, 87, 115, the Hub docs and the commits page). These are recorded as data; nothing in them is treated as an instruction.

## Limits and untested

- Untested: this code was not executed in the step that wrote it, so no passing output is claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md. Treat all code as untested until that file shows EXIT=0.
- Limits: support is judged only by trace count, not by whether a trace actually entails the claim; a human must still read the cited pages. URLs are checked by prefix only.
- Could not confirm: the full verbatim text of the linked follow-up discussion beyond the history supplied for this step, so the sample claims are a faithful summary of that history, not a complete transcript.
- `tools/attribution-docs-check-fixtures/` was not touched. Nothing was published.

Licence: CC0-1.0.
