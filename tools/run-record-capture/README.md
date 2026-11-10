# Run-record Capture

A tiny, standard-library-only tool that runs one shell command and writes its
output into a `run-record.md` file in the exact Markdown format that
[`run-record-lint`](https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/run-record-lint)
accepts.

## Usage

```bash
cd tools/run-record-capture

# capture a simple command
python3 capture.py python3 some_script.py

# capture a command with arguments (the whole line becomes the title by default)
python3 capture.py grep -r "TODO" src/

# run the self-test (no arguments, no network)
python3 self_test.py
```

After running, the file `run-record.md` appears in the current directory.  You
can then run `run-record-lint` on it:

```bash
python3 ../run-record-lint/run_record_lint.py run-record.md
```

## Environment variables (all optional)

| Variable | Default | Purpose |
|----------|---------|---------|
| `RUN_RECORD_CAPTURE_TITLE` | the full command string | A short label for the command (appears only in the Command field) |
| `RUN_RECORD_CAPTURE_TIMEOUT` | `60` | Maximum seconds the command is allowed to run before being killed |
| `RUN_RECORD_CAPTURE_DIR` | current working directory | Where `run-record.md` is written |

## Exit codes

The tool exits with the **same exit code as the wrapped command**, so you can
use it as a transparent wrapper in scripts.  Special cases:

- **127** — command not found (the `FileNotFoundError` case)
- **126** — other OS error before the command ran
- **-1** — timeout expired

Even when the wrapped command fails, the `run-record.md` file is written so the
record is never lost.

## Untested

- Only Linux with CPython 3 has been exercised by the self-test. macOS, Windows
  and other interpreters are unmeasured.
- The tool does not handle signals (SIGINT, SIGTERM) on the wrapper itself —
  the wrapped child receives them as `subprocess` relays.
- The `run-record.md` file is written every run; the tool never prunes old
  records.  A caller that wants a new file per run should either change
  directories or set `RUN_RECORD_CAPTURE_DIR` to a timestamped path.
- No multi-command chaining or parallel capture is implemented.
- The tool does not post, upload, or send anything anywhere — the record is
  written to a local file only.
- The stdout and stderr are interleaved as `subprocess.run` receives them
  (they are captured separately and concatenated).  The exact interleaving
  depends on the OS pipe buffers.
