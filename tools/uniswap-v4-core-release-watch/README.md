# uniswap-v4-core-release-watch

Tracks the latest Uniswap/v4-core GitHub release with FACT/DERIVED/UNKNOWN
labels. UNKNOWN is null, never 0/safe.

Source endpoint: https://api.github.com/repos/Uniswap/v4-core/releases/latest
Source repo: https://github.com/Uniswap/v4-core
Parent-tracking issue: https://github.com/for-toolathlon/uniswap-v4-watch/issues/17 (issue #17)
Opportunity: opp-632-313
Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
Dataset: https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch

## Files

- verify.py - label check (FACT/DERIVED/UNKNOWN), --fetch is an owner step
- render_status.py - renders STATUS.md from local labelled data (no network)
- STATUS.md - rendered summary for opp-632-313 / issue #17, drift-checked
- status_check.py - enforces the STATUS.md label/null contract
- data/status.json - labelled status data mirroring STATUS.md
- export_dataset.py - exports dataset_rows.jsonl preserving labels
- dataset_rows.jsonl - verified labelled rows for Hugging Face publication
- dataset_card.md - dataset card for publication
- publish_check.py - pre-upload publish check (no network)
- self_test.py - folder-local self-test, no args, no network
- GOAL.md - goal for this folder, updated before work

## Commands

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 verify.py
python3 status_check.py; echo EXIT=$?
python3 self_test.py; echo EXIT=$?
python3 render_status.py --output STATUS.md
python3 export_dataset.py --output dataset_rows.jsonl
python3 publish_check.py; echo EXIT=$?
~~~

Verify command: python3 verify.py
Renderer command: python3 render_status.py

## Labels

FACT = carried by the live response. DERIVED = computed from a FACT value:
today that is only `days_since`, worked out from published_at and as_of.
UNKNOWN = not proven; the value must be null, never 0, never "safe".

verify.py check_row accepts FACT, DERIVED and UNKNOWN. It rejects any other
label (MAYBE, GUESS, lower-case 'fact'), accepts DERIVED only on computed
fields such as days_since, requires raw response fields (tag, name,
published_at, html_url, asset_count, total_asset_downloads) to be FACT or
UNKNOWN, and fails if any UNKNOWN field holds a value instead of null.

## Status check

status_check.py reads STATUS.md only (no network) and fails if every claim
is not labelled FACT, DERIVED or UNKNOWN, if an unfetched field is not
`<field>: UNKNOWN` with a not-proven and a never-zero/safe note, if a field
line carries a fetched-looking value, if the Could-not-confirm fields stop
being null, if DRAFT ONLY is missing, if the source endpoint is dropped, or
if STATUS.md drifts from render_status.py output.

~~~bash
python3 status_check.py
python3 status_check.py --status STATUS.md
~~~

## Publish check

Run publish_check.py before any Hugging Face upload; it validates local
files only and never uploads:

~~~bash
python3 publish_check.py
python3 publish_check.py --rows dataset_rows.jsonl --card dataset_card.md
~~~

Checks: labels only FACT/DERIVED/UNKNOWN; UNKNOWN fields null, never
0/safe; always-UNKNOWN fields stay UNKNOWN; dataset name and CC0-1.0;
card cites source https://github.com/Uniswap/v4-core and the endpoint
https://api.github.com/repos/Uniswap/v4-core/releases/latest, contains
python3 verify.py, gives the Hugging Face URL and a load_dataset example,
and carries Could not confirm / Untested notes. Exit 0 means ready for the
owner publish step; exit 1 lists problems.

## Drift

STATUS.md must match render_status.py output exactly; dataset_rows.jsonl
must match export_dataset.py output exactly. Regenerate and rerun
python3 self_test.py after any change.

## Could not confirm

Could not confirm the live tag, published date, asset count or downloads:
the endpoint was not fetched when STATUS.md and the committed row were
written, so those fields are null/UNKNOWN and no live value is claimed.
Could not confirm maintenance status.

## Untested

Untested: live fetch path (verify.py --fetch), publish_check.py with live
data, STATUS.md live values, and the published dataset URL (publishing is
the owner publish step, not this folder). No self-test run result is
written here by hand; HivemindOS writes each run into SELFTEST_OUTPUT.md.

This dataset is not advice and not financial information.
