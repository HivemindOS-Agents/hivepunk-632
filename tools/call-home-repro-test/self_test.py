#!/usr/bin/env python3
"""Folder-local self-test. Run: python3 self_test.py; echo EXIT=$? No args accepted."""
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))
import call_home as C

def main():
    print("call-home-repro-test self-test - folder-local, mock [redacted] only")
    checks = failed = 0
    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1
    # Classification distinguishes autocomplete from call-home.
    check(C.classify("/autocomplete?q=x") == "autocomplete", "classify autocomplete")
    check(C.classify("/ping") == "call-home", "classify call-home ping")
    check(C.classify("/telemetry") == "call-home", "classify call-home telemetry")
    check(C.classify("/other") == "unknown", "classify unknown path")
    check(C.classify(None) == "none", "classify none")
    # Verdict logic.
    check(C.verdict_for("autocomplete", ["autocomplete", "autocomplete"]) is True, "verdict reproducible when all match")
    check(C.verdict_for("autocomplete", ["autocomplete", "call-home"]) is False, "verdict not reproducible when mixed")
    check(C.verdict_for("autocomplete", ["autocomplete"]) is False, "verdict needs at least 2 repeats")
    check(C.verdict_for("unknown", ["unknown", "unknown"]) is False, "verdict rejects unknown expected")
    # Loopback-only guard.
    try:
        C.check_loopback("http://example.com:8080/"); check(False, "reject non-loopback host")
    except ValueError:
        check(True, "reject non-loopback host")
    try:
        C.check_loopback("http://[redacted]:1234/"); check(True, "accept [redacted]")
    except ValueError as e:
        check(False, "accept [redacted]", str(e))
    # End-to-end on mock server.
    try:
        results = C.run_tests(repeats=3)
        by = {r["scenario"]: r for r in results}
        check(set(by) == set(C.SCENARIOS), "run_tests covers all scenarios")
        check(by["autocomplete_forced_url"]["observed"] == ["autocomplete"] * 3 and by["autocomplete_forced_url"]["reproducible"], "autocomplete forced-URL reproducible as autocomplete, not call-home")
        check(by["call_home_ping"]["observed"] == ["call-home"] * 3 and by["call_home_ping"]["reproducible"], "call-home ping reproducible as call-home")
        check(by["call_home_telemetry"]["observed"] == ["call-home"] * 3, "call-home telemetry reproducible")
        check(by["idle_control"]["observed"] == ["none"] * 3 and by["idle_control"]["reproducible"], "idle control sends no request")
        # Distinction: autocomplete and call-home classes differ.
        check(by["autocomplete_forced_url"]["expected"] != by["call_home_ping"]["expected"], "autocomplete distinguished from call-home")
    except Exception as exc:
        check(False, "mock server run", "%s: %s" % (type(exc).__name__, exc))
    # Single-repeat run should not claim reproducibility.
    try:
        r1 = C.run_tests(repeats=1, scenarios=["autocomplete_forced_url"])
        check(r1[0]["reproducible"] is False, "repeats=1 not reproducible")
    except Exception as exc:
        check(False, "repeats=1 run", "%s: %s" % (type(exc).__name__, exc))
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1
    print("EXIT=%d" % code)
    return code

if __name__ == "__main__":
    sys.exit(main())
