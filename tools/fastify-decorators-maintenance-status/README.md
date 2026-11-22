# fastify-decorators-maintenance-status

opportunity: opp-632-44

A maintenance-status check for L2jLiga/fastify-decorators and issue #1078 (https://github.com/L2jLiga/fastify-decorators/issues/1078): `check.py` reads the GitHub API (recent commits and releases) and writes `summary.md` with FACT/UNKNOWN labels, so API-returned dates are separated from any maintenance verdict, which stays UNKNOWN.

Issue: https://github.com/L2jLiga/fastify-decorators/issues/1078
Repo: https://github.com/L2jLiga/fastify-decorators

## How to use

1. Run live (needs network):

~~~bash
cd tools/fastify-decorators-maintenance-status
python3 check.py; echo EXIT=$?
~~~

This writes `summary.md` next to `check.py` from https://api.github.com/repos/L2jLiga/fastify-decorators/commits and /releases (the repo endpoint too, when reachable). If the fetch fails, `summary.md` is still written, with the failure labelled UNKNOWN.

2. Offline demo (no network, embedded sample data):

~~~bash
python3 check.py --sample
~~~

3. Run the folder-local self-test (no args, no network; it does not need `summary.md` to pre-exist):

~~~bash
python3 self_test.py; echo EXIT=$?
~~~

4. Read `summary.md` in this folder. Treat FACT rows as data from that run's API response and UNKNOWN rows as unproven; do not post anything to issue #1078 from this tool automatically.

## Contents

- `check.py` - GitHub API reader and `summary.md` writer; pure helpers (`summarise_commits`, `summarise_releases`, `render_summary`, `days_since`) are importable and tested offline. `days_since` uses a calendar-date difference (now.date() - dt.date()), so 2026-11-20 to 2026-11-22 counts as 2 days.
- `summary.md` - generated output of `check.py` (not hand-written; absent until `check.py` is run).
- `self_test.py` - folder-local self-test: feeds sample commits/releases JSON into `check.py` and verifies the rendered FACT/UNKNOWN summary, required sections, issue/repo links, plus README/ARTIFACTS coverage.
- `ARTIFACTS.md` - the GOAL.md update for this folder (goal, status, next step) and the artifacts inventory with the verify command.

## Use, limits and untested

- Use: a dated, labelled snapshot of commit/release recency for discussion of issue #1078.
- Limits: unauthenticated GitHub API rate limits apply; commit/release recency alone does not prove whether a repo is maintained, and `check.py` does not fetch issue comments, maintainer statements, or security data. Sample mode uses invented demo data, clearly labelled by the `--sample` run only.
- Untested: this artifact was not executed with a live API call in the step that wrote it, so no live summary is claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written). Treat as untested until that file shows EXIT=0.
- Could not confirm: live latest commit/release dates for L2jLiga/fastify-decorators, and any maintenance verdict. The self-test checks that the verdict is labelled UNKNOWN, not that it matches the live repo.
- Nothing was published, no issue or comment was posted, and `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
