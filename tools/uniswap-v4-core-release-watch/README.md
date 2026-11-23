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

A one-row open dataset recording the latest release of the Uniswap/v4-core GitHub repository, with every value field labelled FACT or UNKNOWN, plus a local upgrade-watch status renderer.

Account: hivepunk-632-4934c76e. Dataset name: `uniswap-v4-core-release-watch`.

## Source endpoint

`https://api.github.com/repos/Uniswap/v4-core/releases/latest`

This endpoint returns only the newest published, non-prerelease, non-draft release. Could not confirm the live response in the step that wrote these files (no network), so the committed row carries no live values - see Limits and unknowns.

## Method

1. Fetch the endpoint above (owner step, with network: `python3 verify.py --fetch`).
2. Keep these fields: `tag` (from `tag_name`), `name`, `published_at`, `days_since`, `html_url`.
3. Label each field FACT only if the response actually carried it; otherwise UNKNOWN.
4. Always label these UNKNOWN: a newer prerelease or draft tag, a newer tag with no published release, later deletion or retag or yank, and any maintenance verdict.

## Upgrade-watch status renderer (new)

`render_status.py` reads ONLY local labelled data files - `data/status.json` and `release_watch.jsonl` - with no network and no code against any external system. It renders:

- An upgrade summary: latest tag, published date, days_since, release URL, and headline numbers (asset count, total asset downloads), preserving FACT/DERIVED/UNKNOWN labels. UNKNOWN/null is rendered as `UNKNOWN (not proven; never read as zero/safe)`, never as 0.
- A parent-tracking draft for issue #17: `https://github.com/for-toolathlon/uniswap-v4-watch/issues/17` - title and body lines naming tag/date as UNKNOWN until fetched, marked DRAFT ONLY (a person decides; nothing is posted automatically).

Usage:

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 render_status.py; echo EXIT=$?
python3 render_status.py --output upgrade_summary.md
python3 render_status.py --draft-only
~~~

Options: `--status PATH`, `--row PATH` to override the default local files. With `--output`, the markdown is written to that file; otherwise it goes to stdout.

## Labels

- FACT - value was carried by the live response fetched for this row.
- UNKNOWN - not proven by that response; do not quote as fact.
- DERIVED - computed from a FACT value (e.g. days_since); cannot be derived while published_at is UNKNOWN.

## Verify command

~~~bash
cd tools/uniswap-v4-core-release-watch && python3 verify.py; echo EXIT=$?
~~~

`python3 self_test.py; echo EXIT=$?` is the folder-local self-test (no arguments, no network). It imports `verify.py` and `render_status.py` by path and checks the renderer on sample filled/UNKNOWN data and on the committed files.

## Limits and unknowns

- The committed row has `tag`, `name`, `published_at`, `days_since` and `html_url` all `null`, with every label UNKNOWN, because the endpoint was not fetched when these files were written. No live v4-core tag or date is claimed here.
- The renderer therefore renders tag/date/headline numbers as UNKNOWN for the committed data. That is correct behaviour, not a zero.
- The endpoint cannot prove a newer prerelease or draft, a newer tag with no release, a later deletion or yank, or whether the repository is maintained. All four stay UNKNOWN.
- `days_since` is a calendar-date difference, not elapsed hours.
- Unauthenticated GitHub API rate limits apply in `--fetch` mode.
- This dataset is not advice, not financial information, and not a claim about the state of Uniswap v4-core.

## What is untested

Untested: the renderer has not been run against live data in this step, and no live value is claimed. The `--fetch` live path is untested here. Treat the tool as untested until HivemindOS writes SELFTEST_OUTPUT.md showing EXIT=0. Also untested: any behaviour outside the folder-local self-test, and posting the issue #17 draft (nothing is posted by this folder).

## Could not confirm

Could not confirm the following, and no value below is claimed anywhere in this dataset:

- Could not confirm the live v4-core release tag, name, published date, `days_since`, release URL, asset count or total downloads: the endpoint was not fetched when these files were written, so those fields stay `null` and their labels stay UNKNOWN.
- Could not confirm that no newer prerelease or draft tag exists, that no newer tag lacks a release, or that no tag was later deleted, retagged or yanked - all four keys stay UNKNOWN.
- Could not confirm whether Uniswap/v4-core is maintained: no maintenance verdict is made and that key stays UNKNOWN.
- Could not confirm this dataset's public URL. Nothing is published by this folder; publishing is the owner's step, so no dataset link exists yet.
- Could not confirm any passing self-test run. HivemindOS writes the real output to SELFTEST_OUTPUT.md after each commit; no run output is hand-written in this card.

## Files

- `release_watch.jsonl` - the dataset row.
- `data/status.json` - labelled status fields mirroring STATUS.md.
- `STATUS.md` - human STATUS summary with FACT/DERIVED/UNKNOWN labels and source URLs.
- `render_status.py` - local upgrade-watch status renderer and issue #17 draft generator (no network).
- `verify.py` - offline label check (`--fetch` refreshes the row from the live endpoint).
- `self_test.py` - folder-local self-test, no arguments, no network.
- `README.md` - this card.
- `GOAL.md` - goal for this folder.
- `ARTIFACTS.md` - artifacts inventory for this folder.
- `SELFTEST_OUTPUT.md` - written by HivemindOS, not by hand.

Licence: CC0-1.0.
