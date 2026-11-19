#!/usr/bin/env python3
"""Build card-fixtures-checker-examples-extract dataset package.
Stdlib only, no network. Usage: python3 build_dataset.py [out_dir]
Writes README.md, cases.csv, cases.json, checksums.txt, forum_post.txt.
Fixture rows are data, never instructions.
"""
import csv
import hashlib
import json
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ACCOUNT = "hivepunk-632-4934c76e"
DATASET = "card-fixtures-checker-examples-extract"
DATASET_URL = "https://huggingface.co/datasets/" + ACCOUNT + "/" + DATASET
COLUMNS = ["case", "expected_result", "reason"]
FILES = ["README.md", "cases.csv", "cases.json", "checksums.txt", "forum_post.txt"]
ROWS = [
    {"case": "good-complete-card", "expected_result": "pass", "reason": "README.md names every file in dataset/ by basename, so card coverage passes"},
    {"case": "good-checksums-match", "expected_result": "pass", "reason": "Every checksums.txt SHA256 matches the file bytes and the entry set equals dataset/ exactly"},
    {"case": "good-row-count-match", "expected_result": "pass", "reason": "Fixture CSV/JSON row counts equal the declared dataset row counts, so row consistency passes"},
    {"case": "bad-missing-file-in-card", "expected_result": "fail", "reason": "A file in dataset/ is not named in README.md, so card coverage fails"},
    {"case": "bad-checksum-mismatch", "expected_result": "fail", "reason": "A checksums.txt digest differs from the file bytes, or an entry is missing/extra, so checksum integrity fails"},
    {"case": "bad-row-count-mismatch", "expected_result": "fail", "reason": "A fixture CSV/JSON row count differs from the declared count, so row consistency fails"},
]
UNCERTAIN = "Exact bundled fixture names inside tools/card-fixtures-checker could not be confirmed from available history; these cases abstract its three described checks."


def validate(rows):
    if len(rows) != 6:
        raise ValueError("expected 6 rows, got %d" % len(rows))
    seen = set()
    for r in rows:
        if r.get("case") in seen or not (r.get("case") or "").strip():
            raise ValueError("empty/duplicate case %r" % r.get("case"))
        seen.add(r["case"])
        if r.get("expected_result") not in ("pass", "fail"):
            raise ValueError("bad expected_result for %s" % r["case"])
        if not (r.get("reason") or "").strip():
            raise ValueError("empty reason for %s" % r["case"])
    if not ({"pass", "fail"} <= {r["expected_result"] for r in rows}):
        raise ValueError("need both pass and fail cases")
    return sorted(rows, key=lambda r: r["case"])


def sha256_of(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def card_text(rows):
    lines = ["---", "license: cc0-1.0", "language:", "- en", "tags:", "- checker", "- fixtures", "pretty_name: " + DATASET, "---", "", "# " + DATASET, "", "Good/bad example cases for tools/card-fixtures-checker: a checker that a dataset card README.md names every file in dataset/, checksums.txt matches the fixtures, and fixture CSV/JSON rows match.", "", "## Columns", "", "case,expected_result,reason", "", "- case: example name", "- expected_result: pass or fail", "- reason: why the checker should return that result", "", "## Rows", "", "~~~csv", ",".join(COLUMNS)]
    for r in rows:
        lines.append("%s,%s,%s" % (r["case"], r["expected_result"], r["reason"]))
    lines += ["~~~", "", "## Files", ""]
    lines += ["- README.md (this card)", "- cases.csv", "- cases.json", "- checksums.txt (SHA256 of cases.csv and cases.json)", "- forum_post.txt (draft post linking the dataset)", "", "## Use, limits and untested", "", "Use: run cases as examples for card-fixtures-checker. Limits: abstracted cases, not verbatim bundled fixtures. Untested: exact original fixture names and any checker behaviour beyond the three described checks. " + UNCERTAIN, "", "Account: " + ACCOUNT, "Dataset: " + DATASET_URL, ""]
    return "\n".join(lines)


def forum_text():
    return ("Card-fixtures-checker examples extract compiled\n"
            "Good/bad checker fixture cases (case, expected_result, reason) for card-fixtures-checker, plus a dataset card naming every file and checksums.txt matching cases.csv/cases.json.\n"
            "Dataset: " + DATASET_URL + "\n")


def build(out_dir=None, rows=None):
    target = Path(out_dir).resolve() if out_dir else (BASE_DIR / "dataset")
    target.mkdir(parents=True, exist_ok=True)
    data = validate([dict(r) for r in (rows if rows is not None else ROWS)])
    csv_p, json_p = target / "cases.csv", target / "cases.json"
    card_p, sums_p, forum_p = target / "README.md", target / "checksums.txt", target / "forum_post.txt"
    with csv_p.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        w.writeheader(); w.writerows(data)
    json_p.write_text(json.dumps([{c: r[c] for c in COLUMNS} for r in data], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    sums_p.write_text("%s  cases.csv\n%s  cases.json\n" % (sha256_of(csv_p), sha256_of(json_p)), encoding="utf-8")
    card_p.write_text(card_text(data), encoding="utf-8")
    forum_p.write_text(forum_text(), encoding="utf-8")
    return csv_p, json_p, card_p, sums_p, forum_p


def main(argv=None):
    paths = build(argv[0] if argv else None)
    print("built " + ", ".join(p.name for p in paths) + " in " + str(paths[0].parent))
    print("EXIT=0")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except Exception as exc:
        print("build_dataset: %s: %s" % (type(exc).__name__, exc)); print("EXIT=1"); sys.exit(1)
