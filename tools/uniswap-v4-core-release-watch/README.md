# uniswap-v4-core-release-watch

A labelled watch record for the latest Uniswap/v4-core GitHub release, ready to
publish on Hugging Face. Source endpoint:
https://api.github.com/repos/Uniswap/v4-core/releases/latest
Source repo: https://github.com/Uniswap/v4-core
Dataset target: https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch
Account: hivepunk-632-4934c76e. Licence: CC0-1.0.

## Labels

FACT = carried by the live response. DERIVED = computed from a FACT value (today
only `days_since`). UNKNOWN = not proven, stored as null, never 0 and never
"safe" (never zero/safe). The four `prerelease_or_draft_newer`,
`newer_tag_without_release`, `later_deletion_or_yank` and `maintenance_verdict`
fields stay UNKNOWN always.

## Files

- `publish_model.py` - the publish shape, row and card checks, and the verbatim
  manifest with SHA-256 hashes. No network, no upload.
- `verify.py` - label check for the rows; `--fetch` is the owner's network step.
- `dataset_rows.jsonl` - the labelled rows, published verbatim as
  `data/dataset_rows.jsonl`.
- `dataset_card.md` - the card, published verbatim as `README.md`.
- `self_test.py` - folder-local self-test, no arguments, no network.
- `export_dataset.py`, `status_check.py`, `render_status.py`, `publish_check.py`,
  `STATUS.md`, `release_watch.jsonl`, `GOAL.md` - earlier helpers and data.

## Commands

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 self_test.py; echo EXIT=$?
python3 verify.py; echo EXIT=$?
python3 publish_model.py; echo EXIT=$?
~~~

`publish_model.py` checks `dataset_rows.jsonl` and `dataset_card.md`, then prints
the verbatim mapping (`dataset_card.md` -> `README.md`,
`dataset_rows.jsonl` -> `data/dataset_rows.jsonl`), both SHA-256 hashes, the
target URL and `live_values_claimed=false`.

## Publish status

NOT PUBLISHED. Live URL: none. Publish date: none. Uploading is the owner's
Publish a small open dataset step under hivepunk-632-4934c76e, using
`dataset_card.md` as `README.md` and `dataset_rows.jsonl` as
`data/dataset_rows.jsonl`, unchanged. There is no upload script, token step or
CLI command in this folder.

## Could not confirm

The live tag, name, published date, days_since, release URL, asset count, asset
downloads or maintenance status: the endpoint was not fetched, so those fields
stay UNKNOWN/null. The Hugging Face page's existence and publish date: not
fetched here.

## Untested

`python3 verify.py --fetch` (network) and the dataset as downloaded from Hugging
Face after the owner publishes it. No self-test run result is written here by
hand; HivemindOS writes each run into SELFTEST_OUTPUT.md.

Not advice and not financial information.
