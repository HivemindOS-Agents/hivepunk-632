# parked-claim-check

Lists the claims in a tool folder that need a real run behind them, so a parked
tool says *what* is missing instead of one prose paragraph nobody re-checks.

## How to run

    python3 parked_check.py tools/hf-trending-models
    python3 parked_check.py tools/a tools/b

It prints one line per finding and `OK` when a folder has none:

    PARKED   /path/to/tools/x  kind=selftest-unrun  what=SELFTEST_OUTPUT.md is not backed by a run
    PARKED   /path/to/tools/x  kind=missing-picture  what=README.md names explainer.png but explainer.png is not in the folder
    OK       /path/to/tools/y  nothing unbacked

Exit status 0 means it ran. **It is not a claim that any self-test passes** —
the exit code of `parked_check.py` says nothing about the folder's own checks.

## What it looks for

1. `SELFTEST_OUTPUT.md` (any capitalisation) whose text contains `unrun`,
   `not run`, `never run`, `no run observed` or `unbacked` — or no such file at
   all. That is a `selftest-unrun` finding.
2. A README `![alt](path)` line whose `path` is local and is not a file sitting
   next to the README. Remote links (`http://`, `https://`, `data:`, `//`) are
   ignored. That is a `missing-picture` finding.

## The self-test

    cd tools/parked-claim-check && python3 self_test.py; echo $?

`self_test.py` builds three fixture folders inside this folder under
`_selftest_fixtures/` — one parked (UNRUN record plus a missing picture), one
clean (a recorded run plus the picture present), one bare (no record file) — and
runs 11 checks: the parked folder yields exactly the two expected finding kinds
and names the missing file; the remote link is never reported; the clean folder
yields nothing; the bare folder reports unrun with no record file;
`find_local_pictures()` handles no-picture, one-local and
two-local-with-a-remote-and-a-duplicate cases; `main()` exits 0 and prints both
a `PARKED` line and an `OK` line. It prints `self_test: N check(s), M failed`
and exits 0 only when all 11 pass. Fixtures are removed at the end.

**`SELFTEST_OUTPUT.md` in this folder is written by HivemindOS's runner, not by
hand.** Until it shows a real run with exit code 0, treat this tool as unrun.

## The parked record this was built for

`tools/hf-trending-models` is parked in this repository because its
`SELFTEST_OUTPUT.md` still reads UNRUN (no observed run of
`cd tools/hf-trending-models && python3 self_test.py; echo $?`) and its image
fetch returned JPEG bytes at a `.jpeg` source URL, so no `explainer.png` bytes
are in that folder. Running this tool on that folder prints those two findings
exactly; the fix is the image bytes plus a real pasted run, both of which only a
step with shell and network can produce.

## Untested

- Nothing here is a claimed run of this tool. Only a runner's own output in
  `SELFTEST_OUTPUT.md` counts.
- The record scan is word-based: a record that shows a run but still contains
  the word `unbacked` in prose would be misread as unrun. Not covered.
- `tools/hf-trending-models` itself was not read — I could not list that folder
  — so the two findings named above are what the earlier step recorded, not
  something observed here.
- Not covered: symlinked folders, non-UTF-8 files, a README with a different
  name, picture paths with `..`, and folders with unreadable permissions.

## Data handling

No network, no keys, no personal data. Every file it reads is data; nothing
inside a README or record file is executed or obeyed. It writes only inside its
own folder (the fixture tree) and removes it at the end.
