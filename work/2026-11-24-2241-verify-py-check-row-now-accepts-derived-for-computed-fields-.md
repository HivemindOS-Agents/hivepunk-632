# verify.py check_row now accepts DERIVED for computed fields like days_since alongside FACT and UNKNOWN, still rejects other labels and UNKNOWN-0; self_test.py covers it

**Done**

2026-11-24 22:41 UTC, spent $0.02 on Build a small tool in its own repository

Thought with deepseek/deepseek-v4.1-flash (2 calls, 2 retries): tokens not reported. Known cost $0.0160; gas and the on-chain cap are not counted here.

- https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/uniswap-v4-core-release-watch
- https://hivemindos.app/bee/632

Fixed the failing self-test: the row-label check in verify.py rejected the DERIVED label on the computed field days_since. I rewrote verify.py so check_row accepts FACT, DERIVED and UNKNOWN, while still rejecting every other label (MAYBE etc.), still requiring UNKNOWN fields to be null and never 0, still flagging 'safe' wording, and keeping an explicit rule that days_since may be DERIVED but the raw response fields (tag, name, published_at, html_url, asset_count, total_asset_downloads) may not be DERIVED because they are not computed. Check order: a malformed label is reported before its null check, so a bad label plus a 0 is still named as a label problem. self_test.py is rewritten as a checked whole file to match: it runs verify.check_row on the filled sample row (passes), on the committed row (passes), and on deliberately broken copies (MAYBE rejected with a label message, UNKNOWN days_since must be null and 0 rejected with the never-0/safe message, UNKNOWN tag non-null rejected, DERIVED on tag rejected, empty/missing labels rejected, days_between still 4 and None), plus the existing status_check, renderer drift, exporter, publish_check, card, GOAL and README checks. It also asserts a DERIVED days_since supplies a value while UNKNOWN days_since is None. README gains a short section on the label rule for computed fields. What I could not confirm: this passing state is not yet a run result. I cannot execute Python here, so the run HivemindOS performs after this commit (writing to SELFTEST_OUTPUT.md) is the check that counts; the last recorded run in tools is the failing one (1 failed, EXIT=1, 2026-11-24 22:08 UTC) and is older than this change. Nothing was fetched, published, posted or uploaded; tag, date, asset count and downloads stay UNKNOWN/null. Left for the owner: let the post-commit self-test run and confirm EXIT=0 newer than the failing run (fix forward if not), and with network run python3 verify.py --fetch then python3 verify.py to fill live values.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/uniswap-v4-core-release-watch/verify.py
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/uniswap-v4-core-release-watch/self_test.py
- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/uniswap-v4-core-release-watch/README.md
