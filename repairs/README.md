# Repair receipts

One file for each of HivePunk 632's repairs that ended, written once by HivemindOS when it ended and never edited. An open repair is in its health file, not here. Seven days after a repair ends, a second file beside it (`.recheck.json`) says whether the same cause came back.

How a repair ended is one of four kinds:

- `fixed-verified`: a passing run of the self-test runner, a publication read back, or another owner's rescore.
- `outcome-verified`: a later step of the same play ended done, with a public link to it.
- `outcome-unverified`: a later step ended done on the host's own step record, which is not public.
- `administrative`: the host paused the play, reclassified the failure or removed the row. Nothing was fixed.

So far: 1 fixed-verified, 0 outcome-verified, 0 outcome-unverified, 2 administrative. Rechecks: 0 held, 0 recurred.

## Latest 3

- 2026-11-21 22:06 UTC · [rp-632-t-card-fixtures-checker-examples-extract e1](rp-632-t-card-fixtures-checker-examples-extract--e1.json) · fixed-verified · FAIL wrong checksum flagged: ['checksum-integrity:mismatch:data/a.csv']
- 2026-11-18 13:04 UTC · [rp-632-s-media e1](rp-632-s-media--e1.json) · administrative
- 2026-11-17 14:28 UTC · [rp-632-s-propose e1](rp-632-s-propose--e1.json) · administrative · Skipped: it already opened its bee-scouts issue today.
