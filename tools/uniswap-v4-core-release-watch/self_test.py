#!/usr/bin/env python3
"""Folder-local self-test for uniswap-v4-core-release-watch.
Run: python3 self_test.py; echo EXIT=$?  No args, no network.
Imports verify.py, render_status.py and export_dataset.py by path,
c); runs their real checks on committed files and sample data, checks
STATUS.md matches renderer exactly (drift check), STATUS.md per-field
FACT/DERIVED/UNKNOWN labels + source URLs + UNKNOWN=null never 0/safe,
opp-632-313 issue #17 draft, data/status.json, GOAL.md and README.
Also checks dataset_rows.jsonl is the exporter output for HF publication.
"""
import importlib.util
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ENDPOINT = "https://api.github.com/repos/Uniswap/v4-core/releases/latest"
RELEASE_PAGE = "https://github.com/Uniswap/v4-core/releases/latest"
PARENT = "https://github.com/for-toolathlon/uniswap-v4-watch/issues/17"
HF_URL = "https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch"
EXPECTED_TAG = None

def load_mod(name, filename):
    spec = importlib.util.spec_from_file_location(name, BASE_DIR / filename)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

def filled_row():
    return {"dataset":"uniswap-v4-core-release-watch","row_id":"uniswap-v4-core-latest-release","source_endpoint":ENDPOINT,"as_of":"2026-11-22","tag":"v1.0.0","name":"v1.0.0","published_at":"2026-11-18T00:00:00Z","days_since":4,"html_url":"https://github.com/Uniswap/v4-core/releases/tag/v1.0.0","labels":{"tag":"FACT","name":"FACT","published_at":"FACT","days_since":"FACT","html_url":"FACT","prerelease_or_draft_newer":"UNKNOWN","newer_tag_without_release":"UNKNOWN","later_deletion_or_yank":"UNKNOWN","maintenance_verdict":"UNKNOWN"}}

def main():
    print("uniswap-v4-core-release-watch self-test - folder-local, no network")
    checks = failed = 0
    def check(ok, desc, extra=""):
        nonlocal checks, failed
        checks += 1
        print(("PASS " if ok else "FAIL ") + desc + ((": " + extra) if (extra and not ok) else ""))
        failed += 0 if ok else 1
    def read(name):
        p = BASE_DIR / name
        return p.read_text(encoding="utf-8") if p.is_file() else ""
    try:
        mod = load_mod("verify", "verify.py"); check(True, "verify.py imports cleanly")
    except Exception as exc:
        check(False, "verify.py imports cleanly", repr(exc)); print("self_test: %d check(s), %d failed" % (checks, failed)); print("EXIT=1"); return 1
    check(mod.days_between("2026-11-18T00:00:00Z", "2026-11-22") == 4, "days_between computes 4")
    check(mod.days_between(None, "2026-11-22") is None, "days_between None -> None")
    check(mod.days_between("garbage", "2026-11-22") is None, "days_between garbage -> None")
    ok_row = filled_row()
    check(mod.check_row(ok_row) == [], "check_row accepts a filled FACT row", repr(mod.check_row(ok_row)))
    bad = dict(ok_row); bad["labels"] = dict(ok_row["labels"]); bad["labels"]["tag"] = "MAYBE"
    check(mod.check_row(bad) != [], "check_row rejects a non FACT/UNKNOWN label")
    bad2 = dict(ok_row); bad2["days_since"] = 99
    check(mod.check_row(bad2) != [], "check_row rejects a wrong days_since")
    try:
        rows = mod.load_rows(); check(len(rows) == 1, "release_watch.jsonl holds exactly one row", str(len(rows)))
        row = rows[0]; check(mod.check_row(row) == [], "committed row passes the label check", repr(mod.check_row(row)))
        check(row.get("tag") is None, "committed row tag is null (unfetched)")
        check((row.get("labels") or {}).get("tag") == "UNKNOWN", "committed row tag label is UNKNOWN")
        check(row.get("source_endpoint") == ENDPOINT, "row records source endpoint")
        check(row.get("licence") == "CC0-1.0", "row records CC0-1.0")
    except Exception as exc:
        check(False, "committed release_watch.jsonl loads and checks", repr(exc))
    status = read("STATUS.md")
    check(bool(status), "STATUS.md exists and is non-empty")
    check("opp-632-313" in status, "STATUS.md carries opportunity opp-632-313")
    check(ENDPOINT in status, "STATUS.md cites the releases/latest source URL")
    check(RELEASE_PAGE in status, "STATUS.md cites the release page URL")
    check(PARENT in status, "STATUS.md cites parent issue #17 URL")
    check("## Upgrade summary" in status, "STATUS.md has Upgrade summary section")
    check("## Headline numbers" in status, "STATUS.md has Headline numbers section")
    check("## Could not confirm" in status, "STATUS.md has Could not confirm section")
    check("## Parent-tracking draft for issue #17" in status, "STATUS.md has parent-tracking draft section")
    check("UNKNOWN" in status, "STATUS.md preserves UNKNOWN")
    check("never read as zero/safe" in status, "STATUS.md says UNKNOWN never zero/safe")
    check("never 0/safe" in status, "STATUS.md says UNKNOWN never 0/safe")
    check("DRAFT ONLY" in status, "STATUS.md draft is DRAFT ONLY")
    check("FACT" in status and "DERIVED" in status, "STATUS.md explains FACT/DERIVED labels")
    check("asset_count=None" in status, "STATUS.md headline numbers UNKNOWN until fetched")
    for f in ("tag","name","published_at","days_since","html_url","asset_count","total_asset_downloads"):
        check((f + ": UNKNOWN") in status, "STATUS.md per-field UNKNOWN line: " + f)
        check(("[source: " + ENDPOINT + "]") in status, "STATUS.md source link present (endpoint)")
    check("tag: FACT: 0" not in status and "days_since: FACT: 0" not in status, "STATUS.md never renders UNKNOWN as zero")
    check("Could not confirm" in status and "null" in status, "STATUS.md Could-not-confirm says null")
    try:
        data = json.loads(read("data/status.json"))
        check(data.get("source_endpoint") == ENDPOINT, "status.json source_endpoint matches")
        check(data.get("source_url") == ENDPOINT, "status.json source_url matches")
        for f in ("tag","name","published_at","days_since","html_url"):
            check(f in data, "status.json has field " + f)
            lab = (data.get("labels") or {}).get(f)
            check(lab in ("FACT","DERIVED","UNKNOWN"), "status.json label for " + f + " is FACT/DERIVED/UNKNOWN", repr(lab))
            if lab == "UNKNOWN": check(data.get(f) is None, "status.json UNKNOWN field " + f + " is null, not zero")
        check(data.get("tag") is None and data.get("published_at") is None and data.get("days_since") is None, "status.json tag/date/days are null while UNKNOWN")
        lines = data.get("summary_lines") or []
        check(len(lines) >= 4, "status.json summary_lines present", str(len(lines)))
        check(all(ln.get("label") in ("FACT","DERIVED","UNKNOWN") for ln in lines), "status.json every summary_line labeled")
        check(all(ln.get("source") == ENDPOINT for ln in lines), "status.json every summary_line sourced")
        check((data.get("labels") or {}).get("maintenance_verdict") == "UNKNOWN", "status.json maintenance_verdict UNKNOWN")
    except Exception as exc:
        check(False, "data/status.json loads as JSON", repr(exc)); data = {}
    goal = read("GOAL.md"); check(bool(goal), "GOAL.md exists and is non-empty")
    for w in ("uniswap-v4-core-release-watch","STATUS.md","data/status.json","Could not confirm",ENDPOINT): check(w in goal, "GOAL.md covers: " + w)
    readme = read("README.md"); check(bool(readme), "README.md exists and is non-empty")
    for w in ("api.github.com/repos/Uniswap/v4-core/releases/latest","CC0-1.0","verify.py","self_test.py","UNKNOWN","FACT","Untested","Could not confirm","render_status.py","issue #17","opp-632-313","STATUS.md","drift"): check(w.lower() in readme.lower(), "README covers: " + w)
    check("python3 verify.py" in readme, "README states the verify command")
    check("python3 render_status.py" in readme, "README states the renderer command")
    try:
        rend = load_mod("render_status", "render_status.py"); check(True, "render_status.py imports cleanly")
        filled_status = {"tag":"v1.0.0","name":"v1.0.0","published_at":"2026-11-18T00:00:00Z","days_since":4,"html_url":"https://github.com/Uniswap/v4-core/releases/tag/v1.0.0","headline_numbers":{"asset_count":3,"total_asset_downloads":42},"labels":{"tag":"FACT","name":"FACT","published_at":"FACT","days_since":"DERIVED","html_url":"FACT","asset_count":"FACT","total_asset_downloads":"FACT"}}
        out = rend.render_summary(filled_status, filled_row())
        check("tag: FACT: v1.0.0" in out, "renderer renders FACT tag on filled data")
        check("published_at: FACT: 2026-11-18T00:00:00Z" in out, "renderer renders published date on filled data")
        check("asset_count: FACT: 3" in out and "total_asset_downloads: FACT: 42" in out, "renderer renders headline numbers on filled data")
        check("days_since: DERIVED: 4" in out, "renderer renders DERIVED days_since")
        check(ENDPOINT in out and RELEASE_PAGE in out, "renderer cites both source URLs")
        check("opp-632-313" in out, "renderer carries opp-632-313")
        check(PARENT in out, "renderer draft cites parent issue #17 URL")
        check("DRAFT ONLY" in out, "renderer draft is marked DRAFT ONLY")
        unknown_out = rend.render_summary(data, {})
        check("tag: UNKNOWN" in unknown_out, "renderer renders UNKNOWN tag on committed null data")
        check("asset_count: UNKNOWN" in unknown_out, "renderer renders UNKNOWN headline on null data")
        check("days_since=0" not in unknown_out and "FACT: 0" not in unknown_out, "renderer never renders UNKNOWN as zero")
        check("never read as zero/safe" in unknown_out and "never 0/safe" in unknown_out, "renderer states UNKNOWN never zero/safe")
        check("## Could not confirm" in unknown_out, "renderer renders Could-not-confirm section")
        check(any("issue #17" in ln for ln in rend.render_draft(data, {})), "renderer draft mentions issue #17")
        check(any(ENDPOINT in ln for ln in rend.render_draft(data, {})), "renderer draft cites source endpoint")
        check(rend.fmt("UNKNOWN", None, "tag").startswith("tag: UNKNOWN"), "renderer fmt UNKNOWN+null stays UNKNOWN")
        check(rend.fmt("FACT", "v9", "tag") == "tag: FACT: v9 [source: " + ENDPOINT + "]", "renderer fmt FACT formats value with source")
        loaded = rend.render_summary(rend.load_status(), rend.load_row())
        check("Upgrade summary" in loaded and "Headline numbers" in loaded and "Could not confirm" in loaded, "renderer loads committed files and renders sections")
        check(loaded == status, "STATUS.md matches renderer output exactly (drift check)", "regenerate: python3 render_status.py --output STATUS.md")
        check(rend.main(["--draft-only"]) == 0, "renderer --draft-only main returns 0")
    except Exception as exc:
        check(False, "renderer checks run", repr(exc))
    try:
        exp = load_mod("export_dataset", "export_dataset.py"); check(True, "export_dataset.py imports cleanly")
        check(exp.validate_row(filled_row()) == [], "exporter accepts filled FACT row", repr(exp.validate_row(filled_row())))
        committed = exp.load_rows(); check(committed and exp.validate_row(committed[0]) == [], "exporter accepts committed row", repr(exp.validate_row(committed[0]) if committed else "empty"))
        text = exp.export_rows(committed); exported = json.loads(text.splitlines()[0]) if text.strip() else {}
        check(exported.get("labels") == committed[0].get("labels"), "exporter preserves FACT/DERIVED/UNKNOWN labels exactly")
        check(exported.get("tag") is None and '"tag": null' in text, "exporter keeps UNKNOWN tag null, never zero")
        check(exp.main(["--output", str(BASE_DIR / "_export_tmp.jsonl")]) == 0, "exporter main writes output file")
        tmp = BASE_DIR / "_export_tmp.jsonl"; check(tmp.is_file() and tmp.read_text(encoding="utf-8") == text, "exporter file output matches export_rows"); tmp.unlink(missing_ok=True)
        ds_text = read("dataset_rows.jsonl")
        check(bool(ds_text), "dataset_rows.jsonl exists and is non-empty")
        check(ds_text == text, "dataset_rows.jsonl matches exporter output exactly", "regenerate: python3 export_dataset.py --output dataset_rows.jsonl")
        ds_rows = [json.loads(ln) for ln in ds_text.splitlines() if ln.strip()]
        check(len(ds_rows) == 1, "dataset_rows.jsonl holds exactly one row")
        ds0 = ds_rows[0] if ds_rows else {}
        check(ds0.get("labels") == committed[0].get("labels"), "dataset_rows.jsonl preserves labels exactly")
        check(ds0.get("tag") is None and ds0.get("published_at") is None, "dataset_rows.jsonl UNKNOWN fields are null, never zero")
        check(ds0.get("source_endpoint") == ENDPOINT, "dataset_rows.jsonl cites source endpoint")
        check('"tag": 0' not in ds_text and '"published_at": 0' not in ds_text, "dataset_rows.jsonl never renders UNKNOWN as zero")
    except Exception as exc:
        check(False, "exporter checks run", repr(exc))
    card = read("dataset_card.md"); check(bool(card), "dataset_card.md exists and is non-empty")
    for w in ("hivepunk-632-4934c76e","uniswap-v4-core-release-watch","https://github.com/Uniswap/v4-core",ENDPOINT,"python3 verify.py","CC0-1.0","FACT","DERIVED","UNKNOWN","never zero/safe","Could not confirm","Untested"): check(w in card, "dataset_card.md covers: " + w)
    check("export_dataset.py" in card, "dataset_card.md states export command")
    check(HF_URL in card, "dataset_card.md gives the Hugging Face dataset URL")
    check('load_dataset("hivepunk-632-4934c76e/uniswap-v4-core-release-watch")' in card, "dataset_card.md shows load_dataset example")
    check("dataset_rows.jsonl" in card, "dataset_card.md names the exported rows file")
    print("self_test: %d check(s), %d failed" % (checks, failed))
    code = 0 if failed == 0 else 1; print("EXIT=%d" % code); return code

if __name__ == "__main__":
    sys.exit(main())
