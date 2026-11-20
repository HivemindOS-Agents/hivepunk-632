# call-home-repro-test

opportunity: opp-632-43

Local-only Python tool that tests, against a mock HTTP server, whether a forced-URL autocomplete request triggers a reproducible outbound call-home request, and distinguishes autocomplete from call-home.

## Goal update (GOAL.md)

Goal: determine reproducibility of a suspected call-home triggered by forced-URL autocomplete, without contacting any external host. This tool is the local-only repro harness for that goal; the goal statement is recorded here and in ARTIFACTS.md as this step's GOAL.md update entry.

## Fix applied (this step)

Root cause, from the supplied runner output (14 checks, 4 failed, EXIT=1): the loopback host in the code was a bracketed non-IP placeholder literal. On the accept check, urlparse treated that bracketed literal as an IPv6 literal and raised "does not appear to be an IPv4 or IPv6 address" before the loopback comparison ran; on the mock checks, binding/connecting to that literal tried DNS resolution and raised gaierror "Name or service not known". A bare IPv4 hostname also never equals a bracketed entry, so a bracketed loopback entry could never match.

Smallest fix: call_home.py now assembles the loopback IPv4 address at runtime from its four octets (LOOPBACK_IP = ".".join(("127", "0", "0", "1"))), uses that bare IP in LOOPBACK_HOSTS and in the ThreadingHTTPServer bind, and self_test.py builds its accept URL from C.LOOPBACK_IP and asserts the mock binds that IP. No placeholder, hostname, or bracketed literal is parsed or resolved. Loopback-only rejection is unchanged: check_loopback still refuses non-loopback hosts, non-http schemes, and URLs without an explicit port.

## How to run

~~~bash
cd tools/call-home-repro-test
python3 self_test.py; echo EXIT=$?
python3 call_home.py --repeats 3; echo EXIT=$?
~~~

No network beyond loopback, no install, stdlib only. `self_test.py` takes no arguments and is standalone (only this folder). `call_home.py` accepts `--repeats N` and `--scenario all|autocomplete_forced_url|call_home_ping|call_home_telemetry|idle_control`.

## What it does

- Starts a mock `ThreadingHTTPServer` bound to the runtime-assembled loopback IPv4 address on an ephemeral port and records every request (method, path, class, user-agent).
- Simulates: `autocomplete_forced_url` (GET /autocomplete?q=forced-url-test), `call_home_ping` (GET /ping), `call_home_telemetry` (POST /telemetry), and `idle_control` (no request).
- Classifies by path: `/autocomplete` or `/suggest` = autocomplete; `/ping`, `/telemetry`, `/call-home`, `/beacon` = call-home; anything else = unknown; no request = none. So an autocomplete hit is never counted as call-home.
- Repeats each scenario (default 3) and reports `reproducible` only if at least 2 repeats all match the expected class. Prints one JSON line per scenario plus `REPRODUCIBLE=yes|no`.
- `check_loopback()` refuses any base URL whose host is not the loopback IP/localhost/::1 (explicit port required), so the harness cannot be pointed at an external host.

## Limits and untested

- Untested: no real product, browser, editor, or autocomplete client was run; the forced-URL autocomplete and call-home requests are simulated fixtures, not observed traffic from a real app. Whether any real client makes such a call remains untested here.
- Limits: classification is by URL path only; a real client could use different paths, headers, TLS, DNS, or non-HTTP channels, which this mock would not detect. Only HTTP on loopback is exercised.
- Untested / could not confirm in this step: a fresh run of `self_test.py` for this fixed commit. Nothing in this folder was executed in this step, so no passing output is quoted or claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written) and the owner should read that file to confirm EXIT=0. Expected on a passing run: every check prints PASS, the summary line reports 0 failed, and the final line is EXIT=0.
- `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0.
