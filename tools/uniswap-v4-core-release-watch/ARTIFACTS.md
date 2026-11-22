# ARTIFACTS - uniswap-v4-core-release-watch

opportunity: opp-632-201

## GOAL.md update

- Goal: publish a one-row open dataset, `uniswap-v4-core-release-watch`, under hivepunk-632-4934c76e, recording the latest Uniswap/v4-core GitHub release with every value field labelled FACT or UNKNOWN.
- Status: files written and self-test fixed. The folder's check set previously failed one check, `README covers: Could not confirm`, because the card's old heading was `What could not be confirmed` and the check greps for the literal substring `could not confirm`. The card now carries a section headed `## Could not confirm` plus the phrase in prose. No other file's behaviour changed.
- Next step: owner runs `python3 self_test.py` in this folder (HivemindOS also does this after each commit), reads `SELFTEST_OUTPUT.md`, then with network runs `python3 verify.py --fetch` followed by `python3 verify.py` before publishing the dataset.

## Artifacts in this folder

- `README.md` - the dataset card: source endpoint, method, field table, FACT/UNKNOWN label rules, limits and unknowns, untested marking, the literal `## Could not confirm` section, files list, CC0-1.0.
- `release_watch.jsonl` - the one dataset row; values `null` and all labels UNKNOWN until a live fetch fills them.
- `verify.py` - offline label check over the row; `--fetch` refreshes it from the live GitHub endpoint.
- `self_test.py` - folder-local self-test, no arguments, no network, imports `verify.py` by path.
- `ARTIFACTS.md` - this file: the GOAL.md update and the artifact inventory.
- `SELFTEST_OUTPUT.md` - written by HivemindOS after each run; not hand-written, never edited here.

## Verify commands

~~~bash
cd tools/uniswap-v4-core-release-watch
python3 self_test.py; echo EXIT=$?
python3 verify.py; echo EXIT=$?
~~~

## Runner output

The verbatim self-test output for this folder is written by the HivemindOS runner into `SELFTEST_OUTPUT.md` in this folder, with the state, the last lines printed, the UTC time and a link to the run page. No run log, captured output or passing line is written by hand into any file in this folder. Read that file for the real result.

## Not done here

- No live fetch was run, so `tag`, `name`, `published_at`, `days_since` and `html_url` stay `null` with UNKNOWN labels, and no live v4-core value is claimed.
- Nothing was published. No Hugging Face upload, no forum post, no issue comment, no network call.
- No other tool folder was touched.
- No key, password or personal detail is in any file here.

## Owner left

1. Open `SELFTEST_OUTPUT.md` after the next run and, if it shows `EXIT=0`, paste that verbatim block under "Runner output" above.
2. With network: `python3 verify.py --fetch`, then `python3 verify.py` and confirm the summary reports 0 failed and `EXIT=0`.
3. Publish the folder contents as the dataset `uniswap-v4-core-release-watch` under hivepunk-632-4934c76e through the Publish-a-small-open-dataset play.
4. Post the forum announcement; only the owner's publish step can do that.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
