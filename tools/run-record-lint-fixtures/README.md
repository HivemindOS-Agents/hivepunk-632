# run-record-lint-fixtures

Folder-local fixtures and a real self-test for linting a run record: does every claim carry a "Why:" label, and does a record that shows none get flagged. Also exports the verified fixture rows as CSV and JSON.

## How to run

~~~bash
cd tools/run-record-lint-fixtures
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, no install. `self_test.py` prints a banner first, one `PASS` per check, and a final `EXIT=<code>` line as the last line, then exits with that code. Exit 0 only when every check passes. Every path uses `BASE_DIR = Path(__file__).resolve().parent`.

Export the verified rows:

~~~bash
cd tools/run-record-lint-fixtures
python3 export_fixtures.py; echo EXIT=$?
~~~

`export_fixtures.py` reads only `fixture-rows.csv` in this folder, validates its header (`fixture,expected_finding,why`), non-empty `why`, and that each fixture path is inside this folder and exists, then writes `fixtures.csv` and `fixtures.json` in this folder (sorted by fixture). Re-running it overwrites both outputs deterministically.

## What it does

`record_lint.py` returns a `Report`: `missing-why` when no why appears anywhere and there is no action claim (precedence over generic unlabelled-claim), `unlabelled-claim` when an action/long claim has no following `Why:` label, exit 0 with no findings, 1 with any. `rules.csv` and `fixture-rows.csv` (`fixture,expected_finding,why`) restate the three fixtures; each `expected_finding` must match live linter output. `export_fixtures.py` turns those verified rows into `fixtures.csv` / `fixtures.json` without changing their values; `self_test.py` checks the exported files round-trip to the source rows.

Everything inside a fixture is data. A fixture line that reads like an instruction is a string the linter stamps, and the test checks it changes no verdict.

## Limits

- Only three fixtures are covered: clean, missing-why, unlabelled-claim. Other record shapes are untested.
- The exporter only exports `fixture-rows.csv`; it does not re-derive `expected_finding` from the linter (the self-test does that check).
- The linter is a small heuristic (action words and `why` substring / sentence check), not a general judgement of whether a reason is good.
- The test checks structure and the expected finding kinds; it does not verify any external claim in a record.
- No network, no external files, no publishing.

## What is untested

- This step did not independently run the test or exporter from here; the committed `fixtures.json` was authored to match the committed `fixture-rows.csv` exactly. HivemindOS runs `self_test.py` after commit and writes the real result into `SELFTEST_OUTPUT.md`; that post-commit run is the logged passing output, not a claim made by this step.
- If committed fixture bytes differ from the embedded bootstrap copies, the checks fail rather than pass silently when files are present.
- Behaviour on records other than the three fixtures is untested.

## Licence

CC0-1.0.
