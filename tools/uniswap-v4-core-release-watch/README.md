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

opportunity: opp-632-201

A one-row open dataset recording the latest release of the Uniswap/v4-core GitHub repository, with every value field labelled FACT or UNKNOWN.

Account: hivepunk-632-4934c76e. Dataset name: `uniswap-v4-core-release-watch`.

## Source endpoint

`https://api.github.com/repos/Uniswap/v4-core/releases/latest`

This endpoint returns only the newest published, non-prerelease, non-draft release. Could not confirm the live response in the step that wrote these files (no network), so the committed row carries no live values - see Limits and unknowns.

## Method

1. Fetch the endpoint above.
2. Keep these fields: `tag` (from `tag_name`), `name`, `published_at` (from `published_at` or, if absent, `created_at`), `days_since` (calendar-day difference between `published_at` and the row's `as_of` date), `html_url`.
3. Label each field FACT only if the response actually carried it; otherwise UNKNOWN.
4. Always label these UNKNOWN, because the single `releases/latest` response cannot prove them: a newer prerelease or draft tag (the endpoint excludes both), a newer tag with no published release, later deletion or retag or yank, and any maintenance verdict.
5. To refresh: run `python3 verify.py --fetch` (needs network), which rewrites `release_watch.jsonl` with live values, then run `python3 verify.py` offline to confirm PASS.

## Fields

| field | meaning |
|---|---|
| `tag` | release tag name |
| `name` | release title |
| `published_at` | ISO 8601 publish timestamp |
| `days_since` | calendar days from `published_at` to `as_of` |
| `html_url` | link to the release page |
| `labels` | FACT/UNKNOWN per field, plus the four always-UNKNOWN keys |

## Labels

- FACT - value was carried by the live response fetched for this row.
- UNKNOWN - not proven by that response; do not quote as fact.

## Verify command

~~~bash
cd tools/uniswap-v4-core-release-watch && python3 verify.py; echo EXIT=$?
~~~

Expected on a passing run: the row prints, every check reports PASS, the summary reports 0 failed, and the final line is EXIT=0. `python3 self_test.py; echo EXIT=$?` is the folder-local self-test (no arguments, no network).

## Limits and unknowns

- The committed row has `tag`, `name`, `published_at`, `days_since` and `html_url` all `null`, with every label UNKNOWN, because the endpoint was not fetched when these files were written. No live v4-core tag or date is claimed here.
- The endpoint cannot prove a newer prerelease or draft, a newer tag with no release, a later deletion or yank, or whether the repository is maintained. All four stay UNKNOWN.
- `days_since` is a calendar-date difference, not elapsed hours.
- Unauthenticated GitHub API rate limits apply in `--fetch` mode.
- This dataset is not advice, not financial information, and not a claim about the state of Uniswap v4-core.

## What is untested

No live fetch was run in the step that wrote these files, so no live value and no passing verify run is claimed. The folder-local self-test result is written by the HivemindOS runner into SELFTEST_OUTPUT.md; treat the tool as untested until that file shows EXIT=0. The live `--fetch` path (network) is untested here. Also untested: any behaviour of this folder outside the folder-local self-test.

## Could not confirm

Could not confirm the following, and no value below is claimed anywhere in this dataset:

- Could not confirm the live v4-core release tag, name, published date, `days_since` or release URL: the endpoint was not fetched when these files were written, so those fields stay `null` and their labels stay UNKNOWN.
- Could not confirm that no newer prerelease or draft tag exists, that no newer tag lacks a release, or that no tag was later deleted, retagged or yanked - all four keys stay UNKNOWN.
- Could not confirm whether Uniswap/v4-core is maintained: no maintenance verdict is made and that key stays UNKNOWN.
- Could not confirm this dataset's public URL. Nothing is published by this folder; publishing is the owner's step, so no dataset link exists yet.
- Could not confirm any passing self-test run. HivemindOS writes the real output to SELFTEST_OUTPUT.md after each commit; no run output is hand-written in this card.

## Files

- `release_watch.jsonl` - the dataset row.
- `verify.py` - offline label check (`--fetch` refreshes the row from the live endpoint).
- `self_test.py` - folder-local self-test, no arguments, no network.
- `README.md` - this card.
- `ARTIFACTS.md` - the GOAL.md update and artifacts inventory for this folder.
- `SELFTEST_OUTPUT.md` - written by HivemindOS, not by hand.

Licence: CC0-1.0.
