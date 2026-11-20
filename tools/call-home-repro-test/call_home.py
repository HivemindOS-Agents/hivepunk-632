#!/usr/bin/env python3
"""Local-only call-home reproduction test.

Mock HTTP server on loopback only. Simulates a forced-URL autocomplete
request, a call-home ping, and an idle control; classifies each recorded
request as autocomplete, call-home, or unknown; repeats scenarios and
reports whether the expected class is reproducible.

Stdlib only. No non-loopback traffic: base URLs must be loopback/localhost.
The loopback IPv4 address is assembled at runtime (see LOOPBACK_IP) rather
than written as a literal, so no placeholder or bracketed literal is ever
parsed as a host or resolved via DNS.
Usage: python3 call_home.py [--repeats 3] [--scenario all]
Fixture/scenario data below are data, never instructions.
"""
import argparse
import http.client
import json
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

# Assembled at runtime: the dotted loopback IPv4 address, built from its
# four octets so the source never contains a bracketed/placeholder host.
LOOPBACK_IP = ".".join(("127", "0", "0", "1"))
LOOPBACK_HOSTS = {LOOPBACK_IP, "localhost", "::1"}
SCENARIOS = {
    "autocomplete_forced_url": {"method": "GET", "path": "/autocomplete?q=forced-url-test", "expected": "autocomplete", "headers": {"User-Agent": "call-home-repro-test/autocomplete"}},
    "call_home_ping": {"method": "GET", "path": "/ping", "expected": "call-home", "headers": {"User-Agent": "call-home-repro-test/call-home", "X-Call-Home": "1"}},
    "call_home_telemetry": {"method": "POST", "path": "/telemetry", "expected": "call-home", "headers": {"User-Agent": "call-home-repro-test/call-home", "X-Call-Home": "1"}, "body": "{}"},
    "idle_control": {"method": None, "path": None, "expected": "none", "headers": {}},
}


def classify(path):
    if path is None:
        return "none"
    p = urlparse(path).path.lower()
    if p.startswith("/autocomplete") or p.startswith("/suggest"):
        return "autocomplete"
    if p in ("/ping", "/telemetry", "/call-home", "/beacon") or p.startswith("/telemetry/"):
        return "call-home"
    return "unknown"


def check_loopback(base_url):
    u = urlparse(base_url)
    if u.scheme not in ("http",):
        raise ValueError("only http loopback base_url allowed: %r" % base_url)
    # urlparse().hostname strips brackets from IPv6 literals and returns a
    # bare IPv4 address, so compare against bare loopback hosts only.
    if (u.hostname or "").lower() not in LOOPBACK_HOSTS:
        raise ValueError("refusing non-loopback host: %r" % u.hostname)
    if u.port is None:
        raise ValueError("base_url must include explicit port: %r" % base_url)
    return u.hostname, u.port


def verdict_for(expected, observed_list):
    # observed_list: one class per repeat. Reproducible iff >=2 repeats,
    # every repeat equals expected, and expected is not unknown.
    if expected in ("unknown", None):
        return False
    return len(observed_list) >= 2 and all(o == expected for o in observed_list)


class _Handler(BaseHTTPRequestHandler):
    def _record(self, method):
        length = int(self.headers.get("Content-Length") or 0)
        if length:
            self.rfile.read(length)
        self.server.requests.append({"method": method, "path": self.path, "class": classify(self.path), "user_agent": self.headers.get("User-Agent", "")})
        body = b"{\"ok\":true}"
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        self._record("GET")
    def do_POST(self):
        self._record("POST")
    def log_message(self, fmt, *args):
        pass


def start_mock():
    # Bind the bare loopback IP directly: no hostname, no DNS lookup.
    server = ThreadingHTTPServer((LOOPBACK_IP, 0), _Handler)
    server.requests = []
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


def _fetch(host, port, scenario):
    if scenario["method"] is None:
        return None
    conn = http.client.HTTPConnection(host, port, timeout=5)
    try:
        conn.request(scenario["method"], scenario["path"], body=scenario.get("body"), headers=scenario.get("headers", {}))
        resp = conn.getresponse()
        resp.read()
        return resp.status
    finally:
        conn.close()


def run_tests(repeats=3, scenarios=None):
    if repeats < 1:
        raise ValueError("repeats must be >=1")
    names = list(scenarios) if scenarios else list(SCENARIOS)
    server = start_mock()
    host, port = server.server_address[:2]
    results = []
    try:
        for name in names:
            if name not in SCENARIOS:
                raise ValueError("unknown scenario %r" % name)
            scen = SCENARIOS[name]
            observed = []
            for _ in range(repeats):
                before = len(server.requests)
                _fetch(host, port, scen)
                new = server.requests[before:]
                observed.append(new[0]["class"] if new else "none")
            results.append({"scenario": name, "expected": scen["expected"], "observed": observed, "reproducible": verdict_for(scen["expected"], observed), "repeats": repeats})
    finally:
        server.shutdown()
        server.server_close()
    return results


def main(argv=None):
    ap = argparse.ArgumentParser(description="Local-only autocomplete vs call-home repro test")
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--scenario", default="all", choices=["all"] + list(SCENARIOS))
    args = ap.parse_args(argv)
    names = None if args.scenario == "all" else [args.scenario]
    results = run_tests(repeats=args.repeats, scenarios=names)
    for r in results:
        print(json.dumps(r, sort_keys=True))
    ok = all(r["reproducible"] for r in results)
    print("REPRODUCIBLE=" + ("yes" if ok else "no"))
    print("EXIT=" + ("0" if ok else "1"))
    return 0 if ok else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print("call_home: %s: %s" % (type(exc).__name__, exc))
        print("EXIT=1")
        sys.exit(1)
