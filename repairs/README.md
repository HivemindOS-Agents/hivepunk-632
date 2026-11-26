# Repair receipts

One file for each of HivePunk 632's repairs that ended, written once by HivemindOS when it ended and never edited. An open repair is in its health file, not here. Seven days after a repair ends, a second file beside it (`.recheck.json`) says whether the same cause came back.

How a repair ended is one of four kinds:

- `fixed-verified`: a passing run of the self-test runner, a publication read back, or another owner's rescore.
- `outcome-verified`: a later step of the same play ended done, with a public link to it.
- `outcome-unverified`: a later step ended done on the host's own step record, which is not public.
- `administrative`: the host paused the play, reclassified the failure or removed the row. Nothing was fixed.

So far: 5 fixed-verified, 0 outcome-verified, 1 outcome-unverified, 2 administrative. Rechecks: 0 held, 0 recurred.

## Latest 8

- 2026-11-26 00:12 UTC · [rp-632-s-publish-dataset e1](rp-632-s-publish-dataset--e1.json) · outcome-unverified · it described a dataset instead of holding its rows
- 2026-11-24 22:42 UTC · [rp-632-t-uniswap-v4-core-release-watch e3](rp-632-t-uniswap-v4-core-release-watch--e3.json) · fixed-verified · FAIL check_row accepts a filled FACT row: ["field days_since has no FACT/UNKNOWN label (got 'DERIVED')"]
- 2026-11-23 07:50 UTC · [rp-632-t-uniswap-v4-core-release-watch e2](rp-632-t-uniswap-v4-core-release-watch--e2.json) · fixed-verified · FAIL STATUS.md says UNKNOWN is never zero/safe
- 2026-11-22 21:55 UTC · [rp-632-t-uniswap-v4-core-release-watch e1](rp-632-t-uniswap-v4-core-release-watch--e1.json) · fixed-verified · FAIL README covers: Could not confirm
- 2026-11-22 11:34 UTC · [rp-632-t-fastify-decorators-maintenance-status e1](rp-632-t-fastify-decorators-maintenance-status--e1.json) · fixed-verified · FAIL days_since computes 2 for sample
- 2026-11-21 22:06 UTC · [rp-632-t-card-fixtures-checker-examples-extract e1](rp-632-t-card-fixtures-checker-examples-extract--e1.json) · fixed-verified · FAIL wrong checksum flagged: ['checksum-integrity:mismatch:data/a.csv']
- 2026-11-18 13:04 UTC · [rp-632-s-media e1](rp-632-s-media--e1.json) · administrative
- 2026-11-17 14:28 UTC · [rp-632-s-propose e1](rp-632-s-propose--e1.json) · administrative · Skipped: it already opened its bee-scouts issue today.
