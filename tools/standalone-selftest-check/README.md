# standalone-selftest-check

Proves that a tool folder's self-test **passes when that folder is run alone**.

It copies the named tool folder into a throwaway directory inside this folder,
runs `python3 self_test.py` with the copy as the working directory, and reports
the folder, the exit code, the last line the self-test printed, and PASS/FAIL.
The original folder is never modified and the copy is deleted afterwards.

## How to run

    python3 check.py tools/my-tool
    python3 check.py tools/my-tool --keep          # keep the copy, print its path
    python3 check.py tools/a tools/b tools/c      # several folders, one run
    python3 check.py tools/my-tool --timeout 30

The folder argument is resolved in this order, first hit wins:

1. the path as given (absolute or containing a separator)
2. `./<name>`
3. `./tools/<name>`
4. `<repo>/tools/<name>`, where `<repo>` is two levels above this folder
5. `<this folder>/<name>`

## Output and exit status

For each folder, four lines plus an optional fifth:

    folder: /abs/path/to/the/tool
    exit code: 0
    last output line: self_test: 12 check(s), 0 failed
    VERDICT: PASS
    note: ...            (only when something is off)

`exit code: none` and `VERDICT: FAIL` with a `note:` line mean the self-test
never ran to completion: no `self_test.py` in the folder, a timeout, or a script
that could not be started. `check.py` exits 0 only when **every** folder it was
given passed; one failure makes the whole run exit 1.

Everything the checked self-test prints is treated as data. `check.py` only
picks out the last non-empty line; it never obeys text found in that output.

## The self-test

    cd tools/standalone-selftest-check && python3 self_test.py; echo $?

`self_test.py` builds three throwaway fixture tool folders under
`_selftest_fixtures/` **inside this folder** — one whose `self_test.py` exits 0,
one whose `self_test.py` exits 1, and one with no `self_test.py` at all — then
runs 10 checks against `check.check_folder()`:

- the passing fixture is a PASS at exit code 0, and its last output line is kept;
- the failing fixture is a FAIL at exit code 1, with its last output line kept;
- the failing fixture really ran in the copy, not in the original folder;
- the fixture with no `self_test.py` is a FAIL with exit code `none` and a note;
- every throwaway copy was created inside this folder;
- every throwaway copy was removed afterwards;
- the checked folder is byte-identical (SHA-256) after the run;
- the fixture tree sits inside this folder, with no `..` in its relative path;
- `resolve_target()` finds a real folder and returns `None` for a missing name.

It prints `self_test: N check(s), M failed` and exits 0 only when all 10 pass.
The fixtures are deleted at the end, so the folder is left as it was.

**`SELFTEST_OUTPUT.md` in this folder is written by HivemindOS's runner, not by
hand.** Until it shows a real run with exit code 0, treat this tool as unrun.

## Untested

- Nothing here is claimed as an observed run. The self-test above is designed to
  fail loudly, but only a real runner output makes it evidence.
- The timeout path, `--keep`, multi-folder runs, and the argparse `main()` path
  (the self-test calls `check_folder()` directly) are not exercised.
- A self-test that prints nothing and exits 0 leaves `last output line:` empty
  (`(none)`); that case is not in the fixtures.
- Very large folders, symlinks, unreadable files, file names that collide with
  the ignore patterns, and non-Linux paths are untested.
- The copy proves the folder is self-contained, not that its checks are good: a
  self-test that passes trivially passes here too.

## Data handling

No network, no keys, no personal data. `check.py` reads only the folder it is
pointed at; both scripts write only inside `tools/standalone-selftest-check`.
