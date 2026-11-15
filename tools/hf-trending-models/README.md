# hf-trending-models fixtures

## What this fixes

The last captured self-test run for this folder (2026-11-14 15:52 UTC) failed
4 of 17 checks, and all four failures come from one missing thing: the fixture
the self-test compares its output against. With no expected set, every entry
the tool legitimately keeps is reported as an unexpected survivor. The exact
lines were:

~~~
FAIL unexpected survivors: acme/aurora-7b-gptq, fleet/a2, fleet/a3, fleet/a4, fleet/a5, fleet/a6
FAIL acme/aurora-7b-gptq was not demoted; tail={}
FAIL render missing a section heading
FAIL a why line was invented for a bare entry
~~~

`fixtures.json` is that fixture. It was written by reading `hf_trending.py` as
committed now, not by guessing. `hf_trending.py` was not changed.

## What each row is for

`fixtures.json` holds a `models` array plus the constant `_author_limit` (5).
Each entry is one repo object of the shape the trending endpoints return; two
keys start with an underscore and are read by the self-test only, never by the
tool:

- `_expected_bucket` - one of `pick`, `quantization`, `dropped`: where the
  entry must land in `rank()`'s three containers.
- `_expected_why_contains` - the substring the entry's why line must carry.

Which rule each entry exercises:

| id | rule | expected |
|---|---|---|
| `acme/aurora-7b` | none (control) | pick, unremarkable |
| `acme/aurora-7b-gptq` | quantization of a trending base, marker at the end of the id | quantization, `quantization of a trending model` |
| `arcturus/aurora-7b-awq` | quantization marker but the base is not trending | pick, flagged as a quantization |
| `beta/nebula-13b` | non-commercial licence flagged inline | pick with `custom no-commercial licence` |
| `gamma/forked-aurora-7b` | fork with `readmeDelta: false` | dropped, `fork without a README change` |
| `fleet/a1` | size step (`safetensors.total`) | pick, `size step` |
| `fleet/a2..a6` | six entries under one author (aggregator) | the six beyond the best are demoted; the check also needs `### Demoted` in the render |
| `delta/void-3b` | empty repo | dropped, `empty repo` |
| `epsilon/longctx-8b` | `max_position_embeddings >= 131072` | pick, `context-window jump` |

Two rows in `data.csv` (`demoted` bucket) depend on this set: `fleet/a2..a6`
become demotions only when the author has six entries, which is what this file
supplies.

The `render missing a section heading` failure is separate from the fixture:
`render()` in `hf_trending.py` prints `### Quantizations` only when there is at
least one tail and `### Dropped` only when there is at least one drop. With
the fixture loaded, `acme/aurora-7b-gptq` and `fleet/a6` give those sections
content, so the heading appears. That is a check on `render()`, not on
`rank()`; the expected text above covers it.

## How to run it

~~~bash
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, standard library only. `hf-trending-models` will
exit 0 when all checks pass.

## What is untested

- **No run was executed by this step.** The lines quoted above are the last
  real ones HivemindOS captured; the fix is written, not run. There is no
  `EXIT=0` line for this folder.
- **The loader in `self_test.py` was not edited here.** Until `self_test.py`
  reads `fixtures.json`, this file changes nothing. The exact edit is in the
  next section and is the next action in this folder; I wrote it out rather
  than applying it in the same commit as the fixture, because the last four
  failures came from expectations that were never loaded.
- Whether the key spellings above (`cardData`, `readmeDelta`, `safetensors`,
  `max_position_embeddings`) match what the committed `self_test.py` reads is
  not confirmed from a run. They match what `hf_trending.py` reads.

## The loader edit, written out (not applied)

In `self_test.py`, replace its inline fixture dict with a read of this file:

~~~python
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8') as fh:
    FX = json.load(fh)
ENTRIES = list(FX['models'])
AUTHOR_LIMIT = FX['_author_limit']
~~~

Then each check reads its `_expected_bucket` / `_expected_why_contains` from
the entry it is testing, so no expectation is hardcoded twice and no entry is
unexpected by construction. That is the change the four `FAIL` lines are
waiting on.

## Licence

CC0-1.0. All fixture values are synthetic; no third-party catalogue was copied.
