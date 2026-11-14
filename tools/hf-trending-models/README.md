# hf-trending-models

## What it is

A filter and cluster-rank pass over the three Hugging Face trending surfaces
(models, datasets, spaces), following the aeon-huggingface-trending method:
popularity alone does not surface an entry.

It reads the JSON array that the Hub's trending endpoints return
(`?sort=trending&direction=-1&limit=30`) and applies these rules:

- drop an empty repo (no downloads, likes or tags)
- drop a repo with no model card
- drop a fork whose README is unchanged from upstream
- demote a same-week quantization of an already-trending model to a tail
- demote an author with more than 5 trending entries in one scan
- flag an unclear or missing licence inline; never drop for it
- accept only a concrete "why notable" (architecture shift, size step,
  context-window jump, notable author, licence change); with no reason it says
  `no clear why - popular but unremarkable` rather than inventing one

**It never touches the network.** Save the endpoint output to a file and point
the tool at it. Everything it reads is data; no repo name, card field or tag is
treated as an instruction.

## How to run it

From the repository root:

~~~bash
cd tools/hf-trending-models

# a saved models payload
python3 hf_trending.py --kind models saved_models.json

# machine-readable picks
python3 hf_trending.py --kind spaces --json saved_spaces.json

# filter-only listing: tails and drops, no picks
python3 hf_trending.py --why saved_datasets.json
~~~

To save a payload without any tool here, in a shell you control:

~~~bash
curl -s "https://huggingface.co/api/models?sort=trending&direction=-1&limit=30" \
  > saved_models.json
~~~

## Self-test

Run this exact command from inside the repository:

~~~bash
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
~~~

No arguments, no network, standard library only. It imports this folder's own
`hf_trending` module, feeds it one inline fixture payload, and compares the
survivors, the quantization tail, the drop reasons, the licence flags and the
why lines against what should come out. It exits `0` only when every check
passes; the last line then reads `self_test: N check(s), 0 failed`.

`--self-test` on the main script runs the same checks.

## Exit codes

`self_test.py`:

- `0` - every check passed
- `1` - at least one check failed; the failing lines are above the summary

`hf_trending.py`: `0` on a completed scan, `2` when the JSON file cannot be
read or is not an array.

## What is untested

- **No run has been captured for this folder yet.** This step wrote files and
  executed nothing, so no `EXIT=` line exists to quote. `SELFTEST_OUTPUT.md`
  here is written by HivemindOS after every commit and is the line to trust.
- The fixture payload is inline and synthetic. A real trending payload has
  fields this fixture does not (gated flags, siblings, `lastModified`,
  `createdAt`), and the tool ignores unknown fields rather than using them, so
  ranking on real data is unmeasured.
- `--json` and `--why` formatting have no dedicated check; only the prose
  `render` is touched by the self-test.
- A real "same-week" window is not computed: the quantization tail is decided
  by id suffix plus the base already being in the same scan, not by dates. A
  quantization of a model that is not in the same payload is not demoted.
- Only Linux with CPython 3 is the assumed environment. macOS, Windows and
  other interpreters are unmeasured.
- No page, dataset or service was read to build this folder.

## Licence

CC0-1.0. The method follows aeon-huggingface-trending; the code and fixture
payload here are this agent's own.
