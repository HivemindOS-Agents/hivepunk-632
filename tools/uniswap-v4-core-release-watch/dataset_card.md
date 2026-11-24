---
license: cc0-1.0
task_categories:
  - other
language:
  - en
tags:
  - uniswap
  - v4-core
  - github-releases
  - release-watch
---

# uniswap-v4-core-release-watch

Dataset: hivepunk-632-4934c76e/uniswap-v4-core-release-watch
Licence: CC0-1.0. Account: hivepunk-632-4934c76e.

## Source repo and endpoint

Source repo: https://github.com/Uniswap/v4-core
Source endpoint: https://api.github.com/repos/Uniswap/v4-core/releases/latest
Release page: https://github.com/Uniswap/v4-core/releases/latest

## What this is

One labelled row per export of the latest Uniswap/v4-core GitHub release.
Fields: tag, name, published_at, days_since, html_url, plus headline numbers
in data/status.json. Labels are preserved exactly as in release_watch.jsonl:
FACT = carried by the live response, DERIVED = computed from a FACT value,
UNKNOWN = not proven. UNKNOWN is never zero/safe: UNKNOWN fields are null
in the exported JSONL, never 0.

Fields that always stay UNKNOWN: prerelease_or_draft_newer,
newer_tag_without_release, later_deletion_or_yank, maintenance_verdict.

## How to reproduce / verify

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 verify.py; echo EXIT=$?
python3 self_test.py; echo EXIT=$?
python3 export_dataset.py --output dataset_rows.jsonl
python3 render_status.py --output STATUS.md
~~~

Verify command: python3 verify.py

## Could not confirm

Could not confirm the live tag, published date, asset count or downloads:
the endpoint was not fetched when the committed row was written, so those
fields are null/UNKNOWN and no live value is claimed. Could not confirm
maintenance status. Untested: live fetch path, and the published dataset
URL itself (publishing is the owner's publish step, not this folder).

This dataset is not advice and not financial information.
