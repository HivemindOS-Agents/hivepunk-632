# Artifacts: call-home-repro-test

## GOAL.md update (first, this step)

Goal: test locally whether forced-URL autocomplete triggers a reproducible outbound call-home request, distinguishing autocomplete from call-home, without any external traffic. This tool is that local-only harness. (Recorded in README.md and here; no separate GOAL.md file is committed in this tool folder.)

## Files

- call_home.py: mock [redacted] server, scenarios, path classifier (autocomplete vs call-home vs unknown vs none), reproducibility verdict, loopback-only guard, CLI.
- self_test.py: standalone folder-local self-test, no args, stdlib only; classification, verdict, loopback rejection, and end-to-end mock runs including idle control and repeats=1.
- README.md: use, limits, untested, and goal update.
- ARTIFACTS.md: this inventory.
- SELFTEST_OUTPUT.md: written by the HivemindOS runner after commit; not hand-written here.

## Test record

Verified command: `cd tools/call-home-repro-test && python3 self_test.py; echo EXIT=$?` - pending runner execution for this commit, not run or confirmed in this step. Round-trip: self-test starts the mock server, repeats each scenario 3x, and compares observed classes to expected (autocomplete_forced_url=autocomplete, call_home_ping/telemetry=call-home, idle_control=none).

Untested: any real client/product autocomplete behaviour; non-HTTP/TLS/DNS channels; path classifications beyond the documented prefixes. Left for owner/HivemindOS: the standalone self-test run for this commit. tools/attribution-docs-check-fixtures/ untouched; nothing published.
