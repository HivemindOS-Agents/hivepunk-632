# GOAL - uniswap-v4-core-release-watch

opportunity: opp-632-201

## Goal

Finish uniswap-v4-upgrade-watch in this folder only (never a new
tools/uniswap-v4-upgrade-watch/ folder): keep a FACT/DERIVED/UNKNOWN-labeled
STATUS.md summarizing the latest Uniswap v4-core release tag, published
date and headline numbers from
https://api.github.com/repos/Uniswap/v4-core/releases/latest
with source URLs, mirroring data/status.json, and verified by the
folder-alone self_test.py.

## Status this step

- GOAL.md updated first (this file).
- STATUS.md added: every summary line labeled FACT, DERIVED or UNKNOWN
  with a source URL. UNKNOWN is never presented as zero or safe.
- data/status.json added mirroring STATUS.md fields and labels.
- self_test.py extended to check STATUS.md labels/sources, the fields
  in data/status.json, GOAL.md, and README literal phrases.
- README.md and ARTIFACTS.md were not changed in this commit because
  this step commits at most 4 files; they already exist in this folder
  and the existing README phrases are checked by the extended test.
  Updating them with the verbatim runner output is owner-left below.

## Could not confirm

Could not confirm the live tag, published date or headline numbers from
https://api.github.com/repos/Uniswap/v4-core/releases/latest in this
step: no network fetch was run here. Those values stay null/UNKNOWN in
STATUS.md and data/status.json and no live value is claimed.

## Owner left

1. Run `python3 self_test.py` in this folder; read SELFTEST_OUTPUT.md
   written by the HivemindOS runner for the verbatim output.
2. Record that verbatim output in ARTIFACTS.md and update README.md
   to list STATUS.md, data/status.json and GOAL.md.
3. With network, run `python3 verify.py --fetch`, then
   `python3 verify.py`, and only then quote tag/date as FACT.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
