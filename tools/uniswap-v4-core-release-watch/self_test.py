#!/usr/bin/env python3
"""Folder-local self-test for uniswap-v4-core-release-watch.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Imports verify.py, render_status.py, export_dataset.py, publish_check.py
and status_check.py by path and runs their real checks on the committed
files and on sample data.
"""
import importlib.util
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
SOURCE_REPO = "https://github.com/Uniswap/v4-core"
PARENT = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/17"
HF_URL = "https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch"


def load_mod(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE_DIR / filename)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def filled_row():
    return {
        "dataset": "uniswap-v4-core-release-watch",
        "row_id": "uniswap-v4-core-latest-release",
        "source_endpoint": ENDPOINT,
        "as_of": "2026-11-22",
        "licence": "CC0-1.0",
        "tag": "v1.0.0",
        "name": "v1.0.0",
        "published_at": "2026-11-18T00:00:00Z",
        "days_since": 4,
        "html_url": "https://github.com/Uniswap/v4-core/releases/tag/v1.0.0",
        "asset_count": 2,
        "total_asset_downloads": 10,
        "labels": {
            "tag": "FACT",
            "name": "FACT",
            "published_at": "FACT",
            "days_since": "DERIVED",
            "html_url": "FACT",
            "asset_count": "FACT",
            "total_asset_downloads": "FACT",
            "prerelease_or_draft_newer": "UNKNOWN",
            "newer_tag_without_release": "UNKNOWN",
            "later_deletion_or_yank": "UNKNOWN",
            "maintenance_verdict": "UNKNOWN",
        },
    }


def variant(row, field, value):
    copy = json.loads(json.dumps(row))
    copy[field] = value
    return copy


def relabel(row, field, label, value=None):
    copy = json.loads(json.dumps(row))
    copy["labels"][field] = label
    if label == "UNKNOWN":
        copy[field] = value
    return copy


def main():
    print("uniswap-v4-core-release-watch self-test - folder-local, no network")
    checks = 0
    failed = 0

    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        if ok:
            print("PASS " + desc)
        else:
            failed += 1
            print("FAIL " + desc + ((": " + extra) if extra else ""))

    def read(name):
        path = BASE_DIR / name
        return path.read_text(encoding="utf-8") if path.is_file() else ""

    def done():
        print("self_test: %d check(s), %d failed" % (checks, failed))
        code = 0 if failed == 0 else 1
        print("EXIT=%d" % code)
        return code

    try:
        verify = load_mod("verify", "verify.py")
        check(True, "verify.py imports cleanly")
    except Exception as exc:
        check(False, "verify.py imports cleanly", repr(exc))
        return done()

    # days_between: DERIVED helper.
    check(verify.days_between("2026-11-18T00:00:00Z", "2026-11-22") == 4, "days_between computes 4")
    check(verify.days_between(None, "2026-11-22") is None, "days_between None -> None")
    check(verify.days_between("garbage", "2026-11-22") is None, "days_between bad input -> None")

    # The check this step fixes: DERIVED is a valid label for days_since.
    sample = filled_row()
    check(verify.check_row(sample) == [], "check_row accepts a filled FACT row", repr(verify.check_row(sample)))
    derived_days = relabel(sample, "days_since", "DERIVED", 4)
    check(verify.check_row(derived_days) == [], "check_row accepts DERIVED days_since", repr(verify.check_row(derived_days)))
    check(derived_days["labels"]["days_since"] == "DERIVED" and derived_days["days_since"] == 4, "DERIVED days_since keeps its computed value")
    fact_days = relabel(sample, "days_since", "FACT", 4)
    check(verify.check_row(fact_days) == [], "check_row still accepts FACT days_since")

    # Other labels are rejected, with the label named.
    maybe = relabel(sample, "days_since", "MAYBE", 4)
    problems = verify.check_row(maybe)
    check(problems != [], "check_row rejects MAYBE label")
    check(any("MAYBE" in p for p in problems), "MAYBE rejection names the label", repr(problems))
    guess = relabel(sample, "tag", "GUESS", "v1.0.0")
    check(verify.check_row(guess) != [], "check_row rejects GUESS label")
    lower = relabel(sample, "tag", "fact", "v1.0.0")
    check(verify.check_row(lower) != [], "check_row rejects lower-case 'fact' label")

    # DERIVED only on computed fields.
    derived_tag = relabel(sample, "tag", "DERIVED", "v1.0.0")
    check(verify.check_row(derived_tag) != [], "check_row rejects DERIVED on a raw response field")

    # UNKNOWN stays null: never 0, never a value, never "safe".
    unknown_zero = relabel(sample, "days_since", "UNKNOWN", 0)
    problems = verify.check_row(unknown_zero)
    check(problems != [], "check_row rejects UNKNOWN days_since as 0")
    check(any("never 0/safe" in p for p in problems), "UNKNOWN-as-0 rejection says never 0/safe", repr(problems))
    check(verify.check_row(relabel(sample, "days_since", "UNKNOWN", None)) == [], "check_row accepts UNKNOWN days_since as null")
    check(verify.check_row(relabel(sample, "tag", "UNKNOWN", None)) == [], "check_row accepts UNKNOWN tag as null")
    check(verify.check_row(relabel(sample, "tag", "UNKNOWN", 0)) != [], "check_row rejects UNKNOWN tag as 0")
    check(verify.check_row(relabel(sample, "tag", "UNKNOWN", "v1.0.0")) != [], "check_row rejects UNKNOWN tag with a value")
    check(verify.check_row(relabel(sample, "tag", "UNKNOWN", "safe")) != [], "check_row rejects UNKNOWN written as 'safe'")
    check(verify.check_row(relabel(sample, "maintenance_verdict", "FACT", True)) != [], "check_row keeps always-UNKNOWN fields UNKNOWN")

    # Malformed rows.
    check(verify.check_row({}) != [], "check_row rejects a row with no labels")
    no_tag_label = json.loads(json.dumps(sample))
    del no_tag_label["labels"]["tag"]
    check(verify.check_row(no_tag_label) != [], "check_row rejects a row missing a field label")
    wrong_endpoint = variant(sample, "source_endpoint", "https://example.invalid")
    check(verify.check_row(wrong_endpoint) != [], "check_row rejects a wrong source endpoint")
    string_days = variant(sample, "days_since", "4")
    check(verify.check_row(string_days) != [], "check_row rejects days_since sent as a string")

    # Committed data.
    try:
        rows = verify.load_rows()
        check(len(rows) == 1, "release_watch.jsonl holds exactly one row")
        check(verify.check_row(rows[0]) == [], "committed row passes the label check", repr(verify.check_row(rows[0])))
        check(rows[0].get("tag") is None, "committed row tag is null (unfetched)")
        check(rows[0].get("source_endpoint") == ENDPOINT, "row records source endpoint")
        check(rows[0].get("licence") == "CC0-1.0", "row records CC0-1.0")
    except Exception as exc:
        check(False, "committed release_watch.jsonl loads and checks", repr(exc))

    # STATUS.md through status_check.py.
    status = read("STATUS.md")
    try:
        sc = load_mod("status_check", "status_check.py")
        check(True, "status_check.py imports cleanly")
        problems = sc.check_status(status)
        check(problems == [], "status_check accepts committed STATUS.md", repr(problems))
        check(sc.main(["--status", str(BASE_DIR / "STATUS.md")]) == 0, "status_check main returns 0 on STATUS.md")
        check(sc.check_status(status.replace("tag: UNKNOWN", "tag: v1.0.0", 1)) != [], "status_check rejects a live tag claimed without a fetch")
        check(sc.check_status(status.replace("asset_count=None", "asset_count=0")) != [], "status_check rejects UNKNOWN shown as 0")
        check(sc.check_status(status.replace(ENDPOINT, "https://example.invalid")) != [], "status_check rejects STATUS.md without the source endpoint")
        check(sc.check_status("") != [], "status_check rejects an empty STATUS.md")
    except Exception as exc:
        check(False, "status_check checks run", repr(exc))

    check(bool(status), "STATUS.md exists and is non-empty")
    check("opp-632-313" in status, "STATUS.md carries opportunity opp-632-313")
    check(ENDPOINT in status, "STATUS.md cites the releases/latest source URL")
    check(SOURCE_REPO in status or "https://github.com/Uniswap/v4-core/releases/latest" in status, "STATUS.md cites source repo/release page")
    check(PARENT in status and "issue #17" in status, "STATUS.md cites parent-tracking issue #17")
    check("## Upgrade summary" in status and "## Headline numbers" in status, "STATUS.md has summary sections")
    check("## Could not confirm" in status and "DRAFT ONLY" in status, "STATUS.md Could-not-confirm and DRAFT ONLY")
    check("never read as zero/safe" in status and "never 0/safe" in status, "STATUS.md says UNKNOWN never zero/safe")
    check("asset_count=None" in status, "STATUS.md headline numbers UNKNOWN until fetched")
    for field in ("tag", "name", "published_at", "days_since", "html_url", "asset_count", "total_asset_downloads"):
        check((field + ": UNKNOWN") in status, "STATUS.md per-field UNKNOWN line: " + field)
    for label in ("FACT", "DERIVED", "UNKNOWN"):
        check(label in status, "STATUS.md explains label " + label)

    try:
        data = json.loads(read("data/status.json"))
        check(data.get("source_endpoint") == ENDPOINT, "status.json source_endpoint matches")
        for field in ("tag", "name", "published_at", "days_since", "html_url"):
            label = (data.get("labels") or {}).get(field)
            check(label in ("FACT", "DERIVED", "UNKNOWN"), "status.json label for " + field + " is FACT/DERIVED/UNKNOWN", repr(label))
            if label == "UNKNOWN":
                check(data.get(field) is None, "status.json UNKNOWN field " + field + " is null, not zero")
        lines = data.get("summary_lines") or []
        check(all(ln.get("label") in ("FACT", "DERIVED", "UNKNOWN") for ln in lines), "status.json every summary_line labeled")
    except Exception as exc:
        check(False, "data/status.json loads as JSON", repr(exc))

    goal = read("GOAL.md")
    check(bool(goal), "GOAL.md exists and is non-empty")
    check("opp-632-313" in goal, "GOAL.md carries opp-632-313")
    check("issue #17" in goal and PARENT in goal, "GOAL.md carries parent-tracking issue #17")
    check(ENDPOINT in goal, "GOAL.md cites source endpoint")
    check("UNKNOWN" in goal and "null" in goal and "never 0" in goal, "GOAL.md states UNKNOWN null never 0")

    readme = read("README.md")
    check(bool(readme), "README.md exists and is non-empty")
    for word in ("api.github.com/repos/Uniswap/v4-core/releases/latest", "CC0-1.0", "verify.py", "self_test.py", "UNKNOWN", "FACT", "DERIVED", "Untested", "Could not confirm", "render_status.py", "issue #17", "opp-632-313", "STATUS.md", "publish_check.py", "python3 publish_check.py", "https://github.com/Uniswap/v4-core"):
        check(word in readme, "README covers: " + word)
    check("python3 verify.py" in readme, "README states the verify command")
    check("python3 status_check.py" in readme, "README states the status check command")
    check("days_since" in readme and "DERIVED" in readme, "README explains DERIVED for computed fields")

    try:
        rend = load_mod("render_status", "render_status.py")
        check(True, "render_status.py imports cleanly")
        rendered = rend.render_summary(rend.load_status(), rend.load_row())
        check(rendered == status, "STATUS.md matches renderer output exactly (drift check)", "regenerate: python3 render_status.py --output STATUS.md")
        check(rend.main(["--draft-only"]) == 0, "renderer --draft-only main returns 0")
    except Exception as exc:
        check(False, "renderer checks run", repr(exc))

    try:
        exporter = load_mod("export_dataset", "export_dataset.py")
        check(True, "export_dataset.py imports cleanly")
        text = exporter.export_rows(exporter.load_rows())
        check(read("dataset_rows.jsonl") == text, "dataset_rows.jsonl matches exporter output exactly")
        ds_rows = [json.loads(ln) for ln in read("dataset_rows.jsonl").splitlines() if ln.strip()]
        check(len(ds_rows) == 1 and ds_rows[0].get("tag") is None, "dataset_rows.jsonl one row, UNKNOWN tag null")
    except Exception as exc:
        check(False, "exporter checks run", repr(exc))

    card = read("dataset_card.md")
    check(bool(card), "dataset_card.md exists and is non-empty")
    for word in ("hivepunk-632-4934c76e", SOURCE_REPO, ENDPOINT, "python3 verify.py", "CC0-1.0", "FACT", "DERIVED", "UNKNOWN", "never zero/safe", "Could not confirm", "Untested", "export_dataset.py", HF_URL, "dataset_rows.jsonl"):
        check(word in card, "dataset_card.md covers: " + word)

    try:
        pc = load_mod("publish_check", "publish_check.py")
        check(True, "publish_check.py imports cleanly")
        check(pc.check_rows([filled_row()]) == [], "publish_check accepts filled FACT row", repr(pc.check_rows([filled_row()])))
        committed = pc.load_rows(BASE_DIR / "dataset_rows.jsonl")
        check(pc.check_rows(committed) == [], "publish_check accepts committed dataset_rows.jsonl", repr(pc.check_rows(committed)))
        check(pc.check_rows([relabel(sample, "tag", "MAYBE", "v1.0.0")]) != [], "publish_check rejects non FACT/DERIVED/UNKNOWN label")
        bad0 = relabel(sample, "tag", "UNKNOWN", 0)
        check(any("never 0/safe" in p for p in pc.check_rows([bad0])), "publish_check rejects UNKNOWN as 0 (never 0/safe)")
        check(pc.check_rows([relabel(sample, "name", "UNKNOWN", "v1.0.0")]) != [], "publish_check rejects UNKNOWN non-null value")
        check(pc.check_rows([]) != [], "publish_check rejects empty rows")
        check(pc.check_card(card) == [], "publish_check accepts committed dataset_card.md", repr(pc.check_card(card)))
        check(any(SOURCE_REPO in p for p in pc.check_card(card.replace(SOURCE_REPO, "https://example.invalid"))), "publish_check rejects card missing source repo")
        check(any("python3 verify.py" in p for p in pc.check_card(card.replace("python3 verify.py", "verify it"))), "publish_check rejects card missing verify command")
        check(pc.check_card("") != [], "publish_check rejects empty card")
    except Exception as exc:
        check(False, "publish_check checks run", repr(exc))

    return done()


if __name__ == "__main__":
    sys.exit(main())
