#!/usr/bin/env python3
"""Capture a shell command's output into a run-record Markdown file.

Usage:
    python3 capture.py <command> [args...]

Reads 3 optional environment variables:
    RUN_RECORD_CAPTURE_TITLE   — short label, defaults to the command string
    RUN_RECORD_CAPTURE_TIMEOUT — timeout in seconds, default 60
    RUN_RECORD_CAPTURE_DIR     — output directory, default current working dir

Writes <dir>/run-record.md with the exact format that run-record-lint accepts:

    **Command:** `command line`
    **Exit status:** N
    **Output:**
    ```
    captured output block (stdout + stderr interleaved as they arrived)
    ```

Exits with the same exit code as the wrapped command.  Even if the command
fails (non-zero exit) the run-record file is still written.

Standard library only.  No network.  No files outside the output directory.
"""

import os
import subprocess
import sys


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: capture.py <command> [args...]", file=sys.stderr)
        sys.exit(1)

    title = os.environ.get("RUN_RECORD_CAPTURE_TITLE", " ".join(argv))
    timeout_val = float(os.environ.get("RUN_RECORD_CAPTURE_TIMEOUT", "60"))
    out_dir = os.environ.get("RUN_RECORD_CAPTURE_DIR", os.getcwd())

    command_line = " ".join(argv)

    # Build the output directory (create if missing)
    os.makedirs(out_dir, exist_ok=True)

    try:
        result = subprocess.run(
            argv,
            capture_output=True,
            timeout=timeout_val,
            text=True,
        )
        exit_code = result.returncode
        output_block = result.stdout
        if result.stderr:
            output_block += "\n" + result.stderr
    except subprocess.TimeoutExpired as exc:
        exit_code = -1
        output_block = exc.stdout or ""
        if exc.stderr:
            output_block += "\n" + exc.stderr
        output_block += "\n[timeout after %d seconds]" % timeout_val
    except FileNotFoundError:
        exit_code = 127
        output_block = "command not found: " + command_line
    except OSError as exc:
        exit_code = 126
        output_block = str(exc)

    # Build the run-record Markdown.  The three-backtick fence is built as a
    # concatenation so it survives any transport that strips triple backticks.
    bt = chr(96) * 3
    lines = [
        "**Command:** `" + command_line + "`",
        "",
        "**Exit status:** " + str(exit_code),
        "",
        "**Output:**",
        bt,
        output_block.rstrip("\n"),
        bt,
        "",
    ]

    out_path = os.path.join(out_dir, "run-record.md")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
