# GOAL - uniswap-v4-core-release-watch

opportunity: opp-632-313
Parent-tracking issue: https://github.com/for-toolathlon/uniswap-v4-watch/issues/17 (issue #17)
Source endpoint: https://api.github.com/repos/Uniswap/v4-core/releases/latest
Source repo: https://github.com/Uniswap/v4-core
Release page: https://github.com/Uniswap/v4-core/releases/latest
Dataset: https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch
Licence: CC0-1.0. Account: hivepunk-632-4934c76e.

## Goal

Track the latest Uniswap/v4-core GitHub release for opp-632-313 and
issue #17 with every claim labelled FACT/DERIVED/UNKNOWN. UNKNOWN
fields are null, never 0/safe.

## Steps in order

1. Update this GOAL.md before work (done in this step).
2. Build STATUS.md citing the source endpoint above, with Upgrade
   summary, Headline numbers, Could not confirm, and a parent-tracking
   draft for issue #17 marked DRAFT ONLY.
3. Label claims FACT (carried by live response), DERIVED (computed
   from a FACT value), UNKNOWN (not proven, null never 0).
4. Extend standalone self_test.py to verify STATUS.md labels/nulls.
5. Commit code and README; README notes untested live fetch.

## Status this step

STATUS.md written with all fields UNKNOWN/null because the live
endpoint was not fetched in this step. No live tag/date claimed.

## Could not confirm

Could not confirm live tag, published date, asset count, downloads,
or maintenance status. Untested: live fetch (verify.py --fetch).

## Owner left

Run python3 self_test.py; with network run python3 verify.py --fetch
then python3 verify.py; then publish via the owner publish step.
A person decides; an agent never merges or posts automatically.
