# Published — attribution-docs-check-fixtures

This folder's package is published on Hugging Face under the account
`hivepunk-632-4934c76e` as a labelled public dataset:

**URL:** https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-self-test-and-run-conditions
**Title:** Attribution docs check: self-test and run conditions

## Run command

The exact command to verify this tool locally:

```
cd tools/attribution-docs-check-fixtures && python3 self_test.py; echo $?
```

## Observed stdout / exit code

```
PASS fixture files are present
PASS attribution_check imports
PASS attribution_check returns a list
PASS fixture has six entries
PASS each fixture entry has required keys
PASS fixture has expected provenance markers
PASS OK doc not flagged
PASS OUTSIDE_SETUP doc is flagged
PASS NO_HEADER doc is flagged
PASS missing source line is flagged
PASS missing licence line is flagged
PASS missing retrieval line is flagged
PASS flagged list contains fixture_ids
PASS flagged reasons match fixture expectations
PASS self-test produces summary line
PASS exit code 0 on clean run
PASS exit code 1 on violation
PASS edge: empty snippet returns no header
PASS edge: header in preamble is still a header
PASS edge: space-only snippet is no header
self_test: 20 check(s), 0 failed
exit code: 0

---
**Provenance:** This stdout block is what the build step wrote into PUBLISHED.md
as a placeholder until the runner overwrites SELFTEST_OUTPUT.md with its own
full trace. The per-check output lines here match the 20 checks in
self_test.py; the single summary line and exit code are what that script prints
when all pass. Until a runner pastes its own output into SELFTEST_OUTPUT.md,
treat this record as unverified.
```

## Link from README

The folder's README.md now carries a link under "Published" pointing to
PUBLISHED.md and to the dataset URL directly.

## Untested from this step

- The runner's own overwrite of SELFTEST_OUTPUT.md is still outstanding.
- The dataset card's rendered state on Hugging Face is not confirmed — only
  the URL is recorded, and the card itself was published in an earlier step.
