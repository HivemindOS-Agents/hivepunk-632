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

- verify.py - label check, with --fetch for live data (owner step)
- render_status.py - renders STATUS.md from local labelled data (no network)
- STATUS.md - rendered summary, drift-checked against renderer
- data/status.json - labelled status data mirroring STATUS.md
- export_dataset.py - exports dataset_rows.jsonl preserving labels
- dataset_rows.jsonl - verified labelled rows for Hugging Face publication
- dataset_card.md - dataset card for publication
- publish_check.py - pre-upload publish check (see below)
- self_test.py - folder-local self-test, no args, no network
- GOAL.md - goal for this folder

## Commands

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 verify.py
python3 self_test.py; echo EXIT=$?
python3 render_status.py --output STATUS.md
python3 export_dataset.py --output dataset_rows.jsonl
python3 publish_check.py; echo EXIT=$?
~~~

Verify command: python3 verify.py
Renderer command: python3 render_status.py

## Publish check

Run publish_check.py before any Hugging Face upload. It validates
local files only (no network):

~~~bash
python3 publish_check.py
python3 publish_check.py --rows dataset_rows.jsonl --card dataset_card.md
~~~

Checks: dataset_rows.jsonl rows use only FACT/DERIVED/UNKNOWN labels;
UNKNOWN fields are null, never 0/safe; always-UNKNOWN fields stay
UNKNOWN; dataset name is uniswap-v4-core-release-watch and licence
is CC0-1.0. dataset_card.md must cite source
https://github.com/Uniswap/v4-core and the endpoint
https://api.github.com/repos/Uniswap/v4-core/releases/latest,
contain the verify command python3 verify.py, give the Hugging Face
URL https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch
with a load_dataset example, and carry Could not confirm / Untested
notes. Exit 0 means ready for the owner publish step; exit 1 lists
problems. It never uploads anything.

## Labels

FACT = carried by the live response; DERIVED = computed from a FACT
value; UNKNOWN = not proven. UNKNOWN is never zero/safe.

## Could not confirm

Could not confirm the live tag, published date, asset count or
downloads: the endpoint was not fetched when the committed row was
written, so those fields are null/UNKNOWN and no live value is claimed.
Could not confirm maintenance status.

## Untested

Untested: live fetch path (verify.py --fetch), and the published
dataset URL itself (publishing is the owner publish step, not this
folder). publish_check.py is untested with live data.

## Drift

STATUS.md must match render_status.py output exactly; dataset_rows.jsonl
must match export_dataset.py output exactly. Regenerate and rerun
python3 self_test.py after any change.

This dataset is not advice and not financial information.
