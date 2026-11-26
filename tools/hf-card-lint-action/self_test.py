#!/usr/bin/env python3
"""Folder-local self-test for hf-card-lint-action.

Run from this folder with no arguments and no network:
  python3 self_test.py; echo EXIT=$?

It exercises the entry script (hf_card_lint_action.py) against the committed
sample_card.md and 12 broken variants, checks the exit codes and that the action
wiring names its inputs, and exits 0 only when every check passes. It writes no
run log; HivemindOS writes each run into SELFTEST_OUTPUT.md.
"""
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
ENTRY = BASE / "hf_card_lint_action.py"
SAMPLE = (BASE / "sample_card.md").read_text(encoding="utf-8")
PASSED = []
FAILED = []


def check(name, fn):
    try:
        fn()
        PASSED.append(name)
    except Exception as exc:
        FAILED.append("%s (%r)" % (name, exc))


def expect(condition, message):
    if not condition:
        raise AssertionError(message)


def run_entry(card_path):
    proc = subprocess.run(
        [sys.executable, str(ENTRY), "--card", str(card_path)],
        cwd=str(BASE),
        capture_output=True,
        text=True,
    )
    return proc


TMP = []


def variant(name, text):
    path = BASE / ("self_test_tmp_" + name.replace(" ", "_") + ".md")
    path.write_text(text, encoding="utf-8")
    TMP.append(path)
    return path


def accepts_sample():
    proc = run_entry(BASE / "sample_card.md")
    expect(proc.returncode == 0, proc.stdout + proc.stderr)
    expect("EXIT=0" in proc.stdout, proc.stdout)


def accepts_sample_via_env():
    import os

    env = dict(os.environ, CARD_PATH=str(BASE / "sample_card.md"))
    proc = subprocess.run([sys.executable, str(ENTRY)], capture_output=True, text=True, env=env)
    expect(proc.returncode == 0, proc.stdout + proc.stderr)


def rejects(name, text):
    def run():
        proc = run_entry(variant(name, text))
        expect(proc.returncode == 1, "%s returned %d\n%s" % (name, proc.returncode, proc.stdout))
        expect("FAIL" in proc.stdout, proc.stdout)
    return run


def missing_card_is_two():
    proc = run_entry(BASE / "definitely_not_here.md")
    expect(proc.returncode == 2, proc.stdout + proc.stderr)
    expect("missing card" in proc.stdout, proc.stdout)


def annotations_emitted():
    text = SAMPLE.replace("| null | UNKNOWN |", "| 0 | UNKNOWN |", 1)
    proc = run_entry(variant("annotation", text))
    expect(proc.returncode == 1, proc.stdout)
    expect("::error file=" in proc.stdout, proc.stdout)
    expect("UNKNOWN must be stored as null" in proc.stdout, proc.stdout)


def no_annotation_flag():
    text = SAMPLE.replace("| null | UNKNOWN |", "| 0 | UNKNOWN |", 1)
    path = variant("no_annotation", text)
    proc = subprocess.run(
        [sys.executable, str(ENTRY), "--card", str(path), "--no-annotations"],
        capture_output=True,
        text=True,
    )
    expect(proc.returncode == 1, proc.stdout)
    expect("::error" not in proc.stdout, proc.stdout)


def action_wiring():
    action = (BASE / "action.yml").read_text(encoding="utf-8")
    expect("using: composite" in action, "action.yml is not composite")
    for needle in ("card-path", "python-version", "CARD_PATH", "hf_card_lint_action.py"):
        expect(needle in action, "action.yml missing " + needle)
    expect("::error" in action, "action.yml does not raise an annotation on failure")


def vendored_fallback_works():
    sys.path.insert(0, str(BASE))
    import hf_card_lint_action as entry

    linter = entry._VendoredLinter()
    expect(linter.lint(SAMPLE) == [], linter.lint(SAMPLE))
    expect(linter.lint(SAMPLE.replace("| null | UNKNOWN |", "| safe | UNKNOWN |", 1)), "vendored linter accepted safe")


def main():
    tests = [
        ("entry script accepts the sample card (exit 0)", accepts_sample),
        ("entry script honours $CARD_PATH", accepts_sample_via_env),
        ("missing card exits 2", missing_card_is_two),
        ("violations become GitHub annotations", annotations_emitted),
        ("--no-annotations prints plain FAIL lines", no_annotation_flag),
        ("action.yml names its inputs and entry script", action_wiring),
        ("vendored fallback linter matches the checks", vendored_fallback_works),
        ("no front matter rejected", rejects("no_front_matter", "license: cc0-1.0\n")),
        ("unclosed front matter rejected", rejects("unclosed", "---\nlicense: cc0-1.0\n")),
        ("missing required key rejected", rejects("missing_license", SAMPLE.replace("license: cc0-1.0\n", "", 1))),
        ("empty required key rejected", rejects("empty_pretty_name", SAMPLE.replace("pretty_name: Sample labelled dataset card", "pretty_name:", 1))),
        ("MAYBE label rejected", rejects("maybe", SAMPLE.replace("| FACT |", "| MAYBE |", 1))),
        ("lower-case derived rejected", rejects("lower_derived", SAMPLE.replace("| DERIVED |", "| derived |", 1))),
        ("UNKNOWN as 0 rejected", rejects("unknown_zero", SAMPLE.replace("| null | UNKNOWN |", "| 0 | UNKNOWN |", 1))),
        ("UNKNOWN as safe rejected", rejects("unknown_safe", SAMPLE.replace("| null | UNKNOWN |", "| safe | UNKNOWN |", 1))),
        ("UNKNOWN empty rejected", rejects("unknown_empty", SAMPLE.replace("| null | UNKNOWN |", "|  | UNKNOWN |", 1))),
        ("row without a source URL rejected", rejects("no_source", SAMPLE.replace("| null | UNKNOWN | https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 |", "| null | UNKNOWN | internal notes |", 1))),
        ("FACT with null value rejected", rejects("fact_null", SAMPLE.replace("| v4.0.0 | FACT |", "| null | FACT |", 1))),
        ("missing source column rejected", rejects("no_source_column", SAMPLE.replace("| field | value | label | source |", "| field | value | label | note |", 1))),
        ("missing Claims section rejected", rejects("no_claims", SAMPLE.replace("## Claims", "## Rows", 1))),
    ]
    try:
        for name, fn in tests:
            check(name, fn)
    finally:
        for path in TMP:
            try:
                path.unlink()
            except OSError:
                pass

    for name in PASSED:
        print("PASS " + name)
    for name in FAILED:
        print("FAIL " + name)
    print("self_test: %d check(s), %d failed" % (len(PASSED) + len(FAILED), len(FAILED)))
    print("EXIT=%d" % (0 if not FAILED else 1))
    return 0 if not FAILED else 1


if __name__ == "__main__":
    sys.exit(main())
