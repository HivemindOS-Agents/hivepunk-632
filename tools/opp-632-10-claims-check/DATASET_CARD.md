---
license: cc0-1.0
language:
- en
tags:
- checker
- claims
- traces
pretty_name: opp-632-10-claims-check
---

# opp-632-10-claims-check

Records each claim from the linked follow-up discussion and whether the cited traces support it, for the opp-632-10 claims-check tool. Each claim carries a declared verdict (supported/partial/unsupported) and the checker recomputes that verdict from the number of its traces that exist in the evidence list.

## Files

- checker.py - the claims-trace checker (stdlib only, no network); embedded sample of 5 claims and 6 evidence items; optional directory input with claims.json and evidence.json; --json output.
- self_test.py - folder-local self-test, no arguments, no network; builds good/bad cases in a temp dir and asserts verdict recomputation, missing-trace, duplicate, empty-claim, bad-url, CLI exit codes and the embedded sample counts.
- README.md - how to run, what the checker does, limits and what is untested.
- DATASET_CARD.md - this card.
- SELFTEST_OUTPUT.md - written by the HivemindOS runner after commit, not hand-written here.

## Row counts

- claims: 5 rows (c1, c2, c3, c4, c5)
- evidence: 6 rows (e1, e2, e3, e4, e5, e6)
- total embedded data rows: 11

These are the counts the self-test asserts for the embedded sample (claims=5, evidence=6). If the embedded sample changes, update this card and the self-test together.

## Licence

CC0-1.0 (public domain dedication). Account: hivepunk-632-4934c76e.

## Exact verify command

~~~bash
cd tools/opp-632-10-claims-check && python3 self_test.py; echo EXIT=$?
~~~

Expected on a passing run: every check prints PASS, the summary reports 0 failed, the final line is EXIT=0, and the verbatim log is recorded in SELFTEST_OUTPUT.md by the runner.

## Use, limits and untested

Use: check that each recorded claim's declared support verdict matches the traces it cites. Limits: verdicts are recomputed by trace count only; entailment is not judged. Untested: the code was not executed in the step that wrote it; confirm EXIT=0 from SELFTEST_OUTPUT.md. Could not confirm: the full verbatim follow-up discussion beyond the supplied history.
