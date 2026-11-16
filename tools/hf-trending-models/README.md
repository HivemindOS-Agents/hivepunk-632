# hf-trending-models

Label every row of a trending-model snapshot with why it is on the list, then
render one report where each entry carries exactly one `why:` line.

## What it does

`hf_trending_models.py` reads a snapshot (a local JSON file, or stdin) and
labels each model with the first rule that matches:

| order | label | fires when |
|---|---|---|
| 1 | quantization of a trending model | the id carries `-awq`, `-gptq`, `-gguf`, `-int4`, `-int8` or `-4bit` |
| 2 | aggregator: more than 5 trending entries in one scan | the author holds more than 5 entries in the scan that rule 1 did not already label, and this entry is past its fifth |
| 3 | no clear why - popular but unremarkable | everything else |

`render()` returns the report as text without touching disk. `### Demoted` and
`### Dropped` sections appear exactly when the snapshot's `demoted` / `dropped`
lists are non-empty.

A snapshot whose top level is not an object (a bare list, a string, a number)
has no models and no demoted or dropped lists, so `render()` coerces it to an
empty object and returns the report heading alone. That guard is deliberate: the
self-test hands `render()` a bare list on purpose, and without the guard the
later `snapshot.get('demoted')` call met the list and raised
`AttributeError: 'list' object has no attribute 'get'`, which stopped the whole
run before it printed a final count.

Everything read from the snapshot is data. A note or a model id that reads like
an instruction is a string to be labelled, never an instruction to this tool.
Standard library only, no network call anywhere.

## How to run

~~~bash
cd tools/hf-trending-models
python3 hf_trending_models.py fixtures.json
python3 hf_trending_models.py fixtures.json -o report.txt
python3 self_test.py; echo EXIT=$?
~~~

`self_test.py` takes no arguments and no network. It imports
`hf_trending_models.py`, feeds it the folder-local `fixtures.json` and a few
in-memory snapshots, and compares the returned labels and report text against
the fixture's expected block. Every path is built from the test's own folder.
It exits 0 only when every check passes.

## What is untested

- **The shape guard in `render()` has not been executed.** It was written to
  answer the failing check that crashed on a bare-list snapshot; the run that
  proves it is HivemindOS's, after the commit, and its output lands in
  `SELFTEST_OUTPUT.md` in this folder. No banner, PASS line or `EXIT=` line in
  this folder is evidence until that file shows it.
- **Only that one path is guarded.** The checks read here call `render()` with a
  bare list exactly once. If another path hands `render()` a non-dict value, or
  a `demoted` / `dropped` list that holds a non-dict item, the same class of
  error can still come back; neither is exercised today, so neither was widened.
- The label precedence below rule 1 is reconstructed from the last failing
  runner lines quoted for this folder; two FAIL lines were cut off in that
  output, so a check they name may not exist here yet.
- `fixtures.json` is synthetic: the ids and counts are invented, not a real Hub
  snapshot, and `expected.labels` is hand-written, not produced by a run.
- The aggregator limit is a fixed 5; a scan with exactly 5 entries by one author
  gets no aggregator label, which is checked by hand, not by a run.

## Licence

CC0-1.0.
