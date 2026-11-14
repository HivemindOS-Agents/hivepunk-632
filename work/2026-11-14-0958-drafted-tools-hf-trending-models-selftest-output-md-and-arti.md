# Drafted tools/hf-trending-models SELFTEST_OUTPUT.md and ARTIFACTS.md with the verbatim self-test command, marked test-pending since no exit line could be captured here.

**Done**

2026-11-14 09:58 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/632

# tools/hf-trending-models — self-test record, drafted (not run)

## Status, stated plainly
I performed no execution in this step. I can write files here; nothing runs, and only HivemindOS runs a self-test and rewrites `SELFTEST_OUTPUT.md` after the commit. So every file below is a **draft** and the run is **test-pending**. I have no captured `EXIT=` line, so nothing below says "passes" or "0 failed" as a result. I also could not read the current `self_test.py` or `hf_trending.py` contents in this step, so I cannot confirm the check count, the fixture count, or that the module import path is exactly as the previous build reported.

## Exact command (verbatim — this string is what goes in README.md and both logs)

```bash
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
```

## Draft `tools/hf-trending-models/SELFTEST_OUTPUT.md`

```markdown
# Self-test output - tools/hf-trending-models

Status: test-pending (the step that wrote this file can only write files; it cannot run python3)

Command, verbatim, run from inside this folder:
    cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?

Exit code:     not captured
Last line:     not captured
Captured at:   not captured

Nothing in this file is a result. HivemindOS rewrites it after the commit with
real captured stdout and the real EXIT= value; that rewritten line is the only
line anyone should quote.

Success looks like this shape (shape only - never to be copied as a result):
    self_test: N check(s), 0 failed
    EXIT=0

If HivemindOS captures a non-zero EXIT, replace this whole file with the real
stdout+stderr tail, the real EXIT= value and the name of the failing check, and
fix that check in the same commit as the row that reports it. Never edit a row
to make it look greener than the captured line.
```

## Draft `tools/hf-trending-models/ARTIFACTS.md`

```markdown
# Artifacts - tools/hf-trending-models

Self-test runs (one row per run; the exit column shows only what was captured):

| date | command | exit | last output line |
|---|---|---|---|
| 2026-11-14 | `cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?` | not captured | not captured - test-pending |

Files in this folder:

| file | what it is |
|---|---|
| `hf_trending.py` | offline filter/ranker over HF API JSON; no network calls |
| `self_test.py` | imports `hf_trending`, runs the inline fixture payload, exits 0 only if every check passes |
| `README.md` | the one runnable line, above |
| `SELFTEST_OUTPUT.md` | rewritten by HivemindOS with the real captured line |

No rendered page is committed in `artifacts/` yet. That is the one known owner-visible
gap; the report is text-only until a render is added.
```

## Draft README line (for `README.md`, exact)

```bash
cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?
```

## The fix path if the captured run fails

I cannot see the failing line yet. The likely failure classes, in the order I would check them once a real line exists: (1) `ModuleNotFoundError: hf_trending` — only if the runner changes directory away from the folder; the command already covers this by folding the `cd` in; (2) a fixture-count or why-rule mismatch, where `self_test.py`'s expected survivors no longer match `hf_trending.py`'s rules after a filter edit; (3) an optional-field branch (the size-step case gated on `safetensors`) that is skipped in one direction and asserted in the other. Each of these is a same-commit edit to the tool, never a softened expectation in the test.

## Explainer image for this run (prompt + caption; render left)

One square image, own budget, standard tier, flat vector, no people, no logos, no text beyond the one strip named below.

**Prompt:** Flat vector diagram, square 1:1, plain off-white background. Left: a slanted tray holding four identical grey rounded rectangles, each carrying only a small bar-chart glyph. An arrow leads right into a plain open box in the middle. Below the box, two exits: the left exit drops two rectangles downward under a red hexagonal stamp reading only "rejected"; the right exit carries one rectangle onward to a tidy stack, under a green hexagonal stamp reading only "clean". Across the bottom, one monospace line of small text, verbatim: `cd tools/hf-trending-models && python3 self_test.py; echo EXIT=$?`. Palette greys with one red and one green, no gradients, no shadows, no figures, no logos, no other lettering.

**Caption (one line):** Fixture entries enter the hf-trending filter and the ones that break a rule drop out under the red stamp while the clean one stacks; the strip below is the exact command whose result is still test-pending.

The image was not rendered here — this step has no render capability. The prompt and caption above are the full deliverable.

## Left for the owner
Commit this folder, read the `SELFTEST_OUTPUT.md` HivemindOS rewrites, and if that captured `EXIT=` is non-zero, the failing line there is the next fix; the image prompt above still needs one render pass to become the artifact row.
