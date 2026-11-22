# GOAL — fastify-decorators-maintenance-status

Opportunity: opp-632-44

Goal: build a maintenance-status check for L2jLiga/fastify-decorators (https://github.com/L2jLiga/fastify-decorators/issues/1078): `check.py` reads the GitHub API for recent commits/releases and writes `summary.md` with FACT/UNKNOWN labels, without claiming a maintenance verdict the data cannot prove.

Status (2026-11-22): `check.py`, `README.md` and `self_test.py` written in this folder. Live API values were not fetched in this step, so no live `summary.md` is included and the maintenance verdict remains UNKNOWN. No issue or comment was posted to #1078 and nothing was published.

Next step: owner left — run `python3 check.py` with network in this folder to generate a live `summary.md`, then read SELFTEST_OUTPUT.md (written by the HivemindOS runner, not hand-written) and confirm it ends EXIT=0 before using any FACT rows in discussion of #1078.

---

# ARTIFACTS — fastify-decorators-maintenance-status

Committed together in this folder:

- `check.py` - GitHub API reader (commits, releases, repo) that writes `summary.md`; pure helpers tested offline; `--sample` runs offline on embedded demo data. Run: `python3 check.py; echo EXIT=$?`
- `summary.md` - generated output of `check.py`; not hand-written and absent until `check.py` is run (live run needs network).
- `README.md` - how to use, contents, use/limits/untested notes, and what could not be confirmed.
- `self_test.py` - folder-local self-test (no args, no network); imports `check.py`, feeds sample commits/releases JSON, and verifies FACT/UNKNOWN rendering, sections and links, plus README/ARTIFACTS coverage. Run: `python3 self_test.py; echo EXIT=$?`
- `ARTIFACTS.md` - this file, including the GOAL update above.
- `SELFTEST_OUTPUT.md` - **not hand-written here**: written by the HivemindOS runner after copying this folder alone to a temp dir and running `python3 self_test.py` there. Owner left: read that file and confirm it ends EXIT=0.

## Verify command

~~~bash
cd tools/fastify-decorators-maintenance-status && python3 self_test.py; echo EXIT=$?
~~~

Expected on a passing run: every check prints PASS, the summary reports 0 failed, and the final line is EXIT=0.

## Notes

- No sibling folder was created; `tools/attribution-docs-check-fixtures/` was not touched; nothing was published and no issue/comment was posted.
- Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
