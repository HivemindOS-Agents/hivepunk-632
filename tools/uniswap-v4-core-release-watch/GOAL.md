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

1. Keep STATUS.md citing the source endpoint above, with Upgrade
   summary, Headline numbers, Could not confirm, and a parent-tracking
   draft for issue #17 marked DRAFT ONLY.
2. Label claims FACT (carried by live response), DERIVED (computed
   from a FACT value), UNKNOWN (not proven, null never 0).
3. Enforce that contract with status_check.py, run from self_test.py.
4. Commit code and README; README notes untested live fetch.
5. Prove the verbatim publish package with publish_package.py:
   dataset_card.md as README.md and dataset_rows.jsonl as data,
   labels preserved, UNKNOWN=null, citing the source repo and
   python3 verify.py, for the owner publish step under
   hivepunk-632-4934c76e. This step uploads nothing.

## Status this step

publish_package.py added and covered by self_test.py: it checks the
committed rows/card, prints the verbatim manifest with SHA-256 hashes
and the exact Hugging Face target, and rejects MAYBE labels,
UNKNOWN-as-0, UNKNOWN non-null, DERIVED on raw fields, and cards
missing the source repo or python3 verify.py. No live fetch was made;
tag, date, asset count and downloads remain UNKNOWN/null, and no live
Hugging Face URL is claimed as fetched.

## Could not confirm

Could not confirm live tag, published date, asset count, downloads,
or maintenance status, or that the Hugging Face dataset exists live.
Untested: live fetch (verify.py --fetch) and the owner publish step.

## Owner left

Run python3 self_test.py; with network run python3 verify.py --fetch
then python3 verify.py; then publish via the owner publish step under
hivepunk-632-4934c76e using dataset_card.md as README.md and
dataset_rows.jsonl as data verbatim. A person decides; an agent never
merges or posts automatically.
