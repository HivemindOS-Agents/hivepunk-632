# Artifacts: call-home-repro-test

## GOAL.md update (first, this step)

Goal: test locally whether forced-URL autocomplete triggers a reproducible outbound call-home request, distinguishing autocomplete from call-home, without any external traffic. This tool is that local-only harness. (Recorded in README.md and here; no separate GOAL.md file is committed in this tool folder.)

## Fix record (this step)

Problem (prior supplied runner result, quoted as data): self-test failed 4 of 14 checks with EXIT=1 - 'accept' failed with "does not appear to be an IPv4 or IPv6 address" and the mock-bind, mock-server-run and repeats=1 checks failed with gaierror "Name or service not known". Cause: the loopback host was a bracketed non-IP placeholder literal. urlparse parsed the bracketed literal as an IPv6 literal and raised before the loopback comparison; the server bind/connect tried DNS for that literal; and a bracketed entry could never equal the bare IPv4 hostname urlparse returns.

Smallest change, in this folder only: call_home.py assembles the loopback IPv4 address at runtime from its four octets (LOOPBACK_IP) and uses that bare IP in LOOPBACK_HOSTS and the ThreadingHTTPServer bind; self_test.py builds the accept URL from C.LOOPBACK_IP, adds an explicit non-http rejection check, and asserts the mock binds C.LOOPBACK_IP. Loopback-only rejection kept: example.com and any other non-loopback host, non-http scheme, or missing port still raise ValueError. No other folder touched; tools/attribution-docs-check-fixtures/ untouched; nothing published.

## Files

- call_home.py: mock loopback server, scenarios, path classifier (autocomplete vs call-home vs unknown vs none), reproducibility verdict, loopback-only guard, CLI; LOOPBACK_IP assembled at runtime.
- self_test.py: standalone folder-local self-test, no args, stdlib only; classification, verdict, loopback rejection/acceptance, mock bind check, and end-to-end mock runs including idle control and repeats=1.
- README.md: use, limits, untested, goal update, and this fix.
- ARTIFACTS.md: this inventory.
- SELFTEST_OUTPUT.md: written by the HivemindOS runner after commit; not hand-written here.

## Test record

Verified command: `cd tools/call-home-repro-test && python3 self_test.py; echo EXIT=$?` - NOT run in this step and NOT confirmed here, so no passing output or EXIT line is quoted or claimed for this commit. The prior failing pattern is described above from the supplied runner data. The fresh verbatim output for this commit must be read from SELFTEST_OUTPUT.md once HivemindOS writes it; that file is the logged result the owner should check. Expected on a passing run: all checks PASS, summary reports 0 failed, final line EXIT=0. Round-trip expected: self-test starts the mock server on loopback, repeats each scenario 3x, and compares observed classes to expected (autocomplete_forced_url=autocomplete, call_home_ping/telemetry=call-home, idle_control=none).

Untested: any real client/product autocomplete behaviour; non-HTTP/TLS/DNS channels; path classifications beyond the documented prefixes; and the fresh standalone run for this commit (pending runner). Left for owner/HivemindOS: read SELFTEST_OUTPUT.md after the runner executes. tools/attribution-docs-check-fixtures/ untouched; nothing published.
