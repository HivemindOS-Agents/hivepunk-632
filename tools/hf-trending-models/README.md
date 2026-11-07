# hf-trending-models

A tiny, network-free helper: it reads a local JSON fixture of model rows and
prints a ranked table of the models by momentum. No HTTP call, no key, no
account — the fixture is the only input.

Picture: [explainer.png](explainer.png) · Run slot: **UNRUN** (see
[SELFTEST_OUTPUT.md](SELFTEST_OUTPUT.md)) — no run observed.

## Files in this folder

- `hf_trending.py` — the script (Python standard library only)
- `fixtures/models.json` — sample model rows used by every example below
- `self_test.py` — the self-test
- `explainer.png` — the three-panel picture for this tool (see *Picture*)
- `SELFTEST_OUTPUT.md` — the runner's result file; currently marked **UNRUN**
- `ARTIFACTS.md` — what this folder ships, with the picture's source URL
- `explainer_image_source.txt` — where the picture's bytes come from

## How to run

~~~bash
cd tools/hf-trending-models
python3 hf_trending.py --fixture fixtures/models.json
python3 hf_trending.py --fixture fixtures/models.json --top 5
~~~

`--fixture` is the input: the script fetches nothing by itself. Output is one
model per line, highest ranked first.

An earlier revision of this tool shipped `list_trending.py --sample <file>` and
an optional live-API mode. If that is the script in your copy, the same rule
holds — point it at a local file; the self-test never needs a key or a network
call.

## Picture — `explainer.png`

A flat three-panel diagram: a local fixture JSON of model rows on the left, the
script labelled *offline, no network* in the middle, a ranked model table on the
right, with the run command and the self-test line printed beneath. No people,
no logos, no brand marks.

Caption: *A small tool that ranks trending models from a local file, with no
network call.*

The file is `tools/hf-trending-models/explainer.png`. Its bytes come from the
image source recorded in `explainer_image_source.txt` and were **not written by
this step** — see that file for the exact source URL.

## Run slot — UNRUN

The self-test command, exactly:

~~~bash
cd tools/hf-trending-models && python3 self_test.py; echo $?
~~~

**No run has been observed for this tool.** `SELFTEST_OUTPUT.md` therefore holds
an empty stdout slot and an empty exit-code slot, marked UNRUN. Treat the tool as
unrun until a runner's own output replaces that file. Never hand-write a pass
line into it.

## Untested

- Nothing here is a record of a run. The command above is written out but was
  not executed in this step, and both slots in `SELFTEST_OUTPUT.md` are empty.
- This README was written without being able to list the tool folder. If the
  script, fixture, flags or file names in your copy differ from the ones above,
  the above is wrong and should be corrected against the folder.
- The picture's bytes are referenced, not committed by this step: the PNG still
  has to be saved into the folder from the recorded source.
- No real Hugging Face data, no sorting edge cases (ties, missing fields, an
  empty fixture) and no very large fixture are covered.

## Data handling

Offline and public only: standard library, one local JSON file, no network, no
key, no personal data. Text inside the fixture (model names, descriptions) is
treated as data, never as instructions.
