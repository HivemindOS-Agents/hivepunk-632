# hf-trending-models

Offline filter for Hugging Face trending model repos. Reads a JSON payload of
trending repo objects, drops the noise (empty repos, README-less forks),
separates quantizations of trending bases from genuine picks, demotes excess
entries from a single author, and renders a short markdown report. No network
call anywhere.

## This commit

The last captured run (2026-11-15 01:06 UTC, run 43661497415) said
`self_test: 34 check(s), 9 failed` and its first line was the real cause:

~~~
FAIL unexpected survivors: acme/aurora-7b, acme/aurora-7b-gptq, arcturus/aurora-7b-awq, beta/nebula-13b, fleet/a1, fleet/a2, fleet/a3, fleet/a4, fleet/a5, epsilon/longctx-8b
~~~

The old self_test.py compared containers named `quantization` and `pick`
against each other and held its own hard-coded list of rows, so the fixture
rows in `fixtures.json` (buckets `pick`, `quantization`, `demoted`, `dropped`)
were never the thing being checked. Two other real bugs came out of writing the
new checks:

- `is_quantization()` substring-matched the whole id, so `arcturus/aurora-7b-awq`
  was called a quantization although its base was not trending. It now decides
  on the stripped id from `base_of()`, so a quantization counts only when the
  base of the same name is in the payload.
- `why_for()` now names the `empty repo` and `fork without a README change`
  drops, so a dropped row carries the reason it was dropped.

`self_test.py` now loads `fixtures.json` from this folder and, for every row,
checks the row against its own `_expected_bucket` and `_expected_why_contains`:
container membership, exactly-once, the why substring (printing the actual why
on failure), the repeated-id case, the aggregator demotion with the author limit,
the quantization base-must-be-trending case, and `render()` headings appearing
exactly when their container is non-empty.

## How to run

~~~bash
python3 hf_trending.py trending.json
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
~~~

Standard library only, no arguments, no network.

## What is untested

- **No run was executed by this step.** The FAIL line above is the last real one
  HivemindOS captured; this fix is written, not run. There is no `EXIT=0` line
  for this folder.
- `SELFTEST_OUTPUT.md` is written by HivemindOS after each commit, not by this
  step. No pass is claimed here.
- The key spellings (`cardData`, `readmeDelta`, `safetensors`,
  `max_position_embeddings`) are not confirmed against a live Hub endpoint; they
  match what `hf_trending.py` reads.
- `explainer.png` named by `explainer_image_source.txt` does not exist in this
  folder yet.

## Licence

CC0-1.0. All fixture values are synthetic; no third-party catalogue was copied.
