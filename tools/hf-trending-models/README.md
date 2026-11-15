# hf-trending-models

Offline filter for Hugging Face trending model repos. Reads a JSON payload of
trending repo objects, drops the noise (empty repos, README-less forks),
separates quantizations of trending bases from genuine picks, demotes excess
entries from a single author, and renders a short markdown report.

## What the fix changed

The last captured run (2026-11-15 00:31 UTC, run 43658576782) failed 4 of 17:

~~~
FAIL unexpected survivors: acme/aurora-7b-gptq, fleet/a2, fleet/a3, fleet/a4, fleet/a5, fleet/a6
FAIL acme/aurora-7b-gptq was not demoted; tail={}
FAIL render missing a section heading
FAIL a why line was invented for a bare entry
~~~

- `QUANT_MARKERS` now holds both marker spellings: leading/embedded
  (`gptq`, `awq`, `gguf`, `int4`, `int8`, `-4bit`) and trailing hyphenated
  (`-gptq`, `-awq`, `-gguf`, `-int4`, `-4bit`). `base_of()` strips each, so
  `acme/aurora-7b-gptq` with a trending `acme/aurora-7b` lands in
  `quantizations`.
- `rank()` dedupes repeated ids across a payload before counting, so a repo the
  endpoint returns twice counts once and does not inflate the aggregator count.
- `rank()` moves entries past `AUTHOR_LIMIT = 5` under one author into the
  `demoted` bucket: `fleet/a6` is demoted, not simply ordered last.
- `render()` emits `### Quantizations` and `### Demoted` when their buckets are
  non-empty, and never invents a why line: a bare entry gets
  `no clear why - popular but unremarkable`.

## How to run

~~~bash
python3 hf_trending.py trending.json
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
~~~

The self-test takes no arguments and needs no network; standard library only.
It loads `fixtures.json`, imports `hf_trending.py`, and compares each entry's
bucket and why line against that entry's `_expected_*` keys. Exit 0 only when
every check passes.

## What is untested

- **No run was executed by this step.** The four FAIL lines above are the last
  real ones HivemindOS captured; this fix is written, not run. There is no
  `EXIT=0` line for this folder.
- `SELFTEST_OUTPUT.md` is written by HivemindOS after each commit, not by this
  step. No pass is claimed here.
- The key spellings (`cardData`, `readmeDelta`, `safetensors`,
  `max_position_embeddings`) are not confirmed against a live endpoint; they
  match what `hf_trending.py` reads.

## Licence

CC0-1.0. All fixture values are synthetic; no third-party catalogue was copied.
