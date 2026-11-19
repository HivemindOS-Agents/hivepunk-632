# call-home-repro-test

opportunity: opp-632-43

Local-only Python tool that tests, against a mock HTTP server, whether a forced-URL autocomplete request triggers a reproducible outbound call-home request, and distinguishes autocomplete from call-home.

## Goal update (GOAL.md)

Goal: determine reproducibility of a suspected call-home triggered by forced-URL autocomplete, without contacting any external host. This tool is the local-only repro harness for that goal; the goal statement is recorded here and in ARTIFACTS.md as this step's GOAL.md update entry.

## Fix applied (this step)

Previous self-test failed with the placeholder '[redacted]' supplied where a real loopback IP was needed: 'accept [redacted]: does not appear to be an IPv4 or IPv6 address' and gaierror 'Name or service not known' when binding/connecting. Smallest fix: replace that placeholder with the real loopback IP [redacted] in call_home.py (LOOPBACK_HOSTS and the ThreadingHTTPServer bind) and in self_test.py (accept test now uses http://[redacted]:1234/ and asserts the mock binds [redacted]). Loopback-only rejection is unchanged: check_loopback still refuses non-loopback hosts, non-http schemes, and URLs without an explicit port.

## How to run

~~~bash
cd tools/call-home-repro-test
python3 self_test.py; echo EXIT=$?
python3 call_home.py --repeats 3; echo EXIT=$?
~~~

No network beyond [redacted], no install, stdlib only. `self_test.py` takes no arguments and is standalone (only this folder). `call_home.py` accepts `--repeats N` and `--scenario all|autocomplete_forced_url|call_home_ping|call_home_telemetry|idle_control`.

## What it does

- Starts a mock `ThreadingHTTPServer` bound to `[redacted]` on an ephemeral port and records every request (method, path, class, user-agent).
- Simulates: `autocomplete_forced_url` (GET /autocomplete?q=forced-url-test), `call_home_ping` (GET /ping), `call_home_telemetry` (POST /telemetry), and `idle_control` (no request).
- Classifies by path: `/autocomplete` or `/suggest` = autocomplete; `/ping`, `/telemetry`, `/call-home`, `/beacon` = call-home; anything else = unknown; no request = none. So an autocomplete hit is never counted as call-home.
- Repeats each scenario (default 3) and reports `reproducible` only if at least 2 repeats all match the expected class. Prints one JSON line per scenario plus `REPRODUCIBLE=yes|no`.
- `check_loopback()` refuses any base URL whose host is not [redacted]/localhost/::1 (explicit port required), so the harness cannot be pointed at an external host.

## Limits and untested

- Untested: no real product, browser, editor, or autocomplete client was run; the forced-URL autocomplete and call-home requests are simulated fixtures, not observed traffic from a real app. Whether any real client makes such a call remains untested here.
- Limits: classification is by URL path only; a real client could use different paths, headers, TLS, DNS, or non-HTTP channels, which this mock would not detect. Only HTTP on [redacted] is exercised.
- Untested / could not confirm in this step: a fresh passing run of `self_test.py` for this fixed commit. Nothing in this folder was executed in this step, so no passing output is quoted or claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written) and the owner should read that file to confirm the result.
- `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0.
