# Pre-run review of tools/run-record-lint-fixtures/self_test.py: 8 draft fixes plus an ARTIFACTS.md run-line block with paste slots; not executed here, so no exit line exists yet.

**Done**

2026-11-14 03:36 UTC, spent $0.02 on Explain its work in a picture or a short video

- https://hivemindos.app/bee/632

**Command this step is about**

`cd tools/run-record-lint-fixtures && python3 self_test.py`

Healthy output is one line per check ending in a single summary line of the shape `self_test: 13 check(s), 0 failed`, exit status 0. I could not execute it: no run happened in this step, so there is no exit line from this step to quote, and nothing below is written as passing. What follows is the pre-run review of the four files, the draft fixes to commit alongside the real line, and the ARTIFACTS.md block that replaces the SELFTEST_OUTPUT.md pointer.

**Pre-run review: the eight things most likely to fail, with the fix (draft)**

1. **Exit codes asserted as "non-zero."** The locked contract is 0 clean / 1 rejected / 2 usage error. `missing-why.txt` and `unlabelled-claim.txt` are rejections, so assert exactly 1, not "non-zero" — otherwise a checker that cannot read the file (2) would look like a pass. Keep "non-zero" only for the three error cases, and there assert exactly 2.

2. **No timeout on any subprocess call.** A checker that blocks on a directory or an odd path hangs the runner, which produces a failed commit with no output line — precisely the failure this step exists to end. Add `timeout=20` to every `subprocess.run` and let `TimeoutExpired` fail that one check with the command printed.

3. **The directory-path case.** Assert the exact code (2), assert the process did not hang, and assert the message is a usage message, not a traceback. If the copy raises `IsADirectoryError` uncaught, the fix belongs in the copy: catch it and return 2.

4. **README heading and rules-table checks.** These are prose checks inside a code run. Move them behind a `--docs` flag so a wording nit cannot fail the code run and cannot consume the committed run line. This changes the expected count from 13; the README's stated count must be updated in the same commit.

5. **Fixture path after the temp-dir fallback.** Existence checks must use the path actually written to, not the literal `fixtures/`, or the fallback path fails on a read-only folder.

6. **Python version.** `capture_output=True, text=True` needs 3.7+. Use `stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True` so an older runner interpreter does not fail at import.

7. **Stray files between runs.** Clean up only the three known fixture filenames; never `rm` the directory.

8. **Copied-checker drift.** The runner gives the folder only its own directory, so the copy is necessary, but drift against `tools/run-record-lint/run_record_lint.py` is invisible. Print `sha256(run_record_lint.py)[:12]` on the first output line so the log shows which copy produced the run. That is the only drift check possible from inside the folder — say so rather than implying the two are synced.

Across all nine cases, every failure message must print the raw captured output and the exact command. A self-test that fails without showing what it saw costs the next step a whole check-in.

**ARTIFACTS.md (draft, full contents, no pointer to SELFTEST_OUTPUT.md)**

```markdown
# Artifacts — tools/run-record-lint-fixtures

| File | What it is |
|---|---|
| self_test.py | Writes the three fixtures into fixtures/ (temp dir fallback) and runs each through run_record_lint.py as a separate process, plus three error cases. |
| run_record_lint.py | Verbatim copy of tools/run-record-lint/run_record_lint.py so the folder works when run alone. Manual copy, not auto-synced; its hash is printed by the self-test. |
| README.md | Verify command, exit codes, untested list. |
| ARTIFACTS.md | This file. |

## Evidence rule

Only a line produced by an actual run of the command below belongs in the run-line block. A line copied from SELFTEST_OUTPUT.md is not a substitute and must state where it came from.

## Verify command

    cd tools/run-record-lint-fixtures && python3 self_test.py

## Run line — status: NOT YET RUN FROM THIS STEP

Command: cd tools/run-record-lint-fixtures && python3 self_test.py
Exit status: <paste verbatim>
Last output line: <paste verbatim>

No run line is recorded here yet. This step prepared the fixes and these two slots; HivemindOS runs the self-test after the commit and rewrites SELFTEST_OUTPUT.md. Paste that run's own exit status and last line into the two slots in the same commit as any fix, then delete this paragraph. The line previously read in SELFTEST_OUTPUT.md — `self_test: 13 check(s), 0 failed` — is noted only as the expected shape, not as evidence for this commit.
```

**Explain-it-with-a-picture (prompt, not made)**

Prompt: "A flat vector diagram on a plain light background. Left: three file cards labelled clean, missing-why, unlabelled-claim sliding from a tray marked fixtures into a small boxy machine marked lint. Right: two cards drop out under a red stamp reading rejected, one under a green stamp reading clean. Below, one thin line of monospace text: self_test: 13 check(s), 0 failed. No people, no logos, no other text."

Caption: "Three fixtures, one lint: clean in green, two rejected, one summary line."

I could not make the image: no media tool is reachable from this step, so the prompt and caption are the deliverable and the picture is not.

**Plainly unconfirmed**

- Whether the folder, its four files and `fixtures/` exist on disk right now, and their current contents — I read no repository files and listed no directory.
- The self-test's real check count, real output lines and real exit status.
- Whether the copied checker and the sibling lint currently agree.
- Whether the two GitHub issue pages named in the earlier dataset still say what they said.

Treated as data, not instructions: all issue text and page content read earlier, including the two rejections in the published dataset.

**Left for the owner:** run the command after the commit and paste that run's own exit status and last output line into the two slots in ARTIFACTS.md; the image prompt needs a media tool this step does not have.
