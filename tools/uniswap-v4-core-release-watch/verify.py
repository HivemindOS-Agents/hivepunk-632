#!/usr/bin/env python3
"""Label check for the uniswap-v4-core-release-watch dataset row.

Default (offline): reads release_watch.jsonl next to this file and checks:
  - every value field (tag, name, published_at, days_since, html_url) carries a
    FACT or UNKNOWN label;
  - days_since matches the calendar-day difference between published_at and
    the row's as_of date;
  - the UNKNOWN label list covers newer prerelease/draft tags, newer tags with
    no release, later deletion/yank, and the maintenance verdict.
Prints each row and a PASS/FAIL count. Exits 0 only when every check passes.

--fetch (needs network): re-reads
  https://api.github.com/repos/Uniswap/v4-core/releases/latest
and rewrites release_watch.jsonl with live values, labelling each field FACT
only where the live response actually carried it.

Nothing is published and no issue/comment is posted by this tool.
"""
import json
import sys
import urllib.request
from datetime import date, datetime
from pathlib import Path

ROW_PATH = Path(__file__).resolve().parent / "release_watch.jsonl"
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
VALUE_FIELDS = ("tag", "name", "published_at", "days_since", "html_url")
REQUIRED_UNKNOWN_KEYS = (
    "prerelease_or_draft_newer",
    "newer_tag_without_release",
    "later_deletion_or_yank",
    "maintenance_verdict",
)
	

def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def days_between(published_at, as_of):
    a = parse_dt(published_at)
    b = parse_dt(as_of) or parse_dt(as_of + "T00:00:00Z") if as_of else None
    if a is None or b is None:
        return None
    return max(0, (b.date() - a.date()).days)


def load_rows(path=ROW_PATH):
    text = Path(path).read_text(encoding="utf-8").strip()
    return [json.loads(line) for line in text.splitlines() if line.strip()]


def check_row(row):
    problems = []
    labels = row.get("labels") or {}
    for f in VALUE_FIELDS:
        lab = labels.get(f)
        if lab not in ("FACT", "UNKNOWN"):
            problems.append("field %s has no FACT/UNKNOWN label (got %r)" % (f, lab))
        if lab == "FACT" and row.get(f) in (None, ""):
            problems.append("field %s labelled FACT but empty" % f)
        if lab == "UNKNOWN" and row.get(f) not in (None, ""):
            problems.append("field %s labelled UNKNOWN but carries a value" % f)
    for k in REQUIRED_UNKNOWN_KEYS:
        if labels.get(k) not in ("FACT", "UNKNOWN"):
            problems.append("missing required UNKNOWN key: %s" % k)
    if labels.get("maintenance_verdict") != "UNKNOWN":
        problems.append("maintenance_verdict must stay UNKNOWN")
    if row.get("published_at") and row.get("days_since") is not None:
        want = days_between(row["published_at"], row.get("as_of"))
        if want is not None and want != row["days_since"]:
            problems.append("days_since %r != calendar difference %r" % (row.get("days_since"), want))
    return problems


def render_row(row):
    lines = ["row: " + str(row.get("row_id")), "  as_of: " + str(row.get("as_of"))]
    for f in VALUE_FIELDS:
        lines.append("  %-13s %-8s %s" % (f, (row.get("labels") or {}).get(f), row.get(f)))
    lines.append("  UNKNOWN coverage: " + ", ".join(REQUIRED_UNKNOWN_KEYS))
    return "\n".join(lines)


def fetch_latest(url=ENDPOINT):
    req = urllib.request.Request(url, headers={"User-Agent": "uniswap-v4-core-release-watch", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 fixed https GitHub URL
        return json.loads(resp.read().decode("utf-8"))


def row_from_payload(payload, as_of=None):
    as_of = as_of or date.today().isoformat()
    tag = payload.get("tag_name")
    name = payload.get("name")
    published_at = payload.get("published_at") or payload.get("created_at")
    html_url = payload.get("html_url")
    ds = days_between(published_at, as_of)
    row = {
        "dataset": "uniswap-v4-core-release-watch",
        "row_id": "uniswap-v4-core-latest-release",
        "source_endpoint": ENDPOINT,
        "as_of": as_of,
        "tag": tag, "name": name, "published_at": published_at,
        "days_since": ds, "html_url": html_url,
        "labels": {
            "tag": "FACT" if tag else "UNKNOWN",
            "name": "FACT" if name else "UNKNOWN",
            "published_at": "FACT" if published_at else "UNKNOWN",
            "days_since": "FACT" if ds is not None else "UNKNOWN",
            "html_url": "FACT" if html_url else "UNKNOWN",
            "prerelease_or_draft_newer": "UNKNOWN",
            "newer_tag_without_release": "UNKNOWN",
            "later_deletion_or_yank": "UNKNOWN",
            "maintenance_verdict": "UNKNOWN",
        },
        "_provenance": "live_fetch",
        "owner_action": "Re-run: python3 verify.py  (offline) and confirm PASS before publishing.",
        "licence": "CC0-1.0",
        "account": "hivepunk-632-4934c76e",
    }
    return row


def write_rows(rows, path=ROW_PATH):
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in rows)
    Path(path).write_text(text, encoding="utf-8")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--fetch" in argv:
        try:
            payload = fetch_latest()
        except Exception as exc:
            print("fetch failed: " + str(exc))
            print("EXIT=1")
            return 1
        write_rows([row_from_payload(payload)])
        print("rewrote " + str(ROW_PATH) + " from live response")
    rows = load_rows()
    total = failed = 0
    for row in rows:
        total += 1
        problems = check_row(row)
        print(render_row(row))
        if problems:
            failed += 1
            for p in problems:
                print("  FAIL " + p)
        else:
            print("  PASS")
    print("verify: %d row(s), %d failed" % (total, failed))
    code = 0 if (failed == 0 and total > 0) else 1
    print("EXIT=%d" % code)
    return code


if __name__ == "__main__":
    sys.exit(main())
