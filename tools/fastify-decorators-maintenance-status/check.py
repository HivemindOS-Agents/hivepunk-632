#!/usr/bin/env python3
"""Maintenance-status check for L2jLiga/fastify-decorators.

Reads the GitHub API for recent commits and releases and writes
summary.md (next to this file) with FACT/UNKNOWN labels.
FACT = value returned by the API in this run.
UNKNOWN = anything not proven by that data (e.g. a maintenance verdict).

Usage:
  python3 check.py            # live: fetch GitHub API, write summary.md
  python3 check.py --sample   # offline demo: use embedded sample data
No arguments are required. Requires network only in live mode.
"""
import json
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

REPO = "L2jLiga/fastify-decorators"
ISSUE_URL = "https://github.com/L2jLiga/fastify-decorators/issues/1078"
REPO_URL = "https://github.com/" + REPO
API_COMMITS = "https://api.github.com/repos/" + REPO + "/commits?per_page=10"
API_RELEASES = "https://api.github.com/repos/" + REPO + "/releases?per_page=10"
API_REPO = "https://api.github.com/repos/" + REPO
BASE_DIR = Path(__file__).resolve().parent


def parse_dt(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    except ValueError:
        return None


def summarise_commits(commits):
    """Return dict with latest commit date/sha/message, or None fields."""
    out = {"latest_date": None, "latest_sha": None, "latest_message": None, "count": 0}
    if not commits:
        return out
    out["count"] = len(commits)
    best = None
    best_dt = None
    for c in commits:
        dt = parse_dt((c.get("commit") or {}).get("committer", {}).get("date"))
        if dt and (best_dt is None or dt > best_dt):
            best, best_dt = c, dt
    if best:
        out["latest_date"] = best_dt.isoformat()
        out["latest_sha"] = best.get("sha")
        msg = (best.get("commit") or {}).get("message") or ""
        out["latest_message"] = msg.splitlines()[0] if msg else None
    return out


def summarise_releases(releases):
    """Return dict with latest release tag/name/date, or None fields."""
    out = {"latest_date": None, "latest_tag": None, "latest_name": None, "count": 0}
    if not releases:
        return out
    out["count"] = len(releases)
    best, best_dt = None, None
    for r in releases:
        dt = parse_dt(r.get("published_at") or r.get("created_at"))
        if dt and (best_dt is None or dt > best_dt):
            best, best_dt = r, dt
    if best:
        out["latest_date"] = best_dt.isoformat()
        out["latest_tag"] = best.get("tag_name")
        out["latest_name"] = best.get("name")
    return out


def days_since(iso_date, now=None):
    dt = parse_dt(iso_date)
    if dt is None:
        return None
    now = now or datetime.now(timezone.utc)
    return max(0, (now - dt).days)


def render_summary(commits, releases, repo_info=None, now=None, fetched=True):
    """Render summary.md text. Never invents a maintenance verdict."""
    now = now or datetime.now(timezone.utc)
    cs = summarise_commits(commits or [])
    rs = summarise_releases(releases or [])
    lines = []
    lines.append("# Maintenance status - L2jLiga/fastify-decorators")
    lines.append("")
    lines.append("Opportunity: opp-632-44")
    lines.append("Issue: " + ISSUE_URL)
    lines.append("Repo: " + REPO_URL)
    lines.append("Generated: " + now.isoformat())
    lines.append("Source: GitHub API (commits, releases" + (", repo" if repo_info else "") + ")")
    lines.append("")
    lines.append("## Labels")
    lines.append("")
    lines.append("- FACT: value returned by the GitHub API in this run.")
    lines.append("- UNKNOWN: not proven by this data; do not quote as fact.")
    lines.append("")
    lines.append("## FACT - latest commit")
    lines.append("")
    if cs["latest_date"]:
        lines.append("- FACT: latest commit date: " + cs["latest_date"])
        lines.append("- FACT: days since latest commit: " + str(days_since(cs["latest_date"], now)))
        if cs["latest_sha"]:
            lines.append("- FACT: latest commit sha: " + cs["latest_sha"])
        if cs["latest_message"]:
            lines.append("- FACT: latest commit message: " + cs["latest_message"])
        lines.append("- FACT: commits returned by API: " + str(cs["count"]))
    else:
        lines.append("- UNKNOWN: no commit data returned by the API in this run.")
    lines.append("")
    lines.append("## FACT - latest release")
    lines.append("")
    if rs["latest_date"]:
        lines.append("- FACT: latest release date: " + rs["latest_date"])
        lines.append("- FACT: days since latest release: " + str(days_since(rs["latest_date"], now)))
        if rs["latest_tag"]:
            lines.append("- FACT: latest release tag: " + rs["latest_tag"])
        if rs["latest_name"]:
            lines.append("- FACT: latest release name: " + rs["latest_name"])
        lines.append("- FACT: releases returned by API: " + str(rs["count"]))
    else:
        lines.append("- UNKNOWN: no release data returned by the API in this run.")
    if repo_info:
        lines.append("")
        lines.append("## FACT - repo fields")
        lines.append("")
        if repo_info.get("archived") is not None:
            lines.append("- FACT: archived flag: " + str(repo_info["archived"]))
        if repo_info.get("pushed_at"):
            lines.append("- FACT: pushed_at: " + str(repo_info["pushed_at"]))
        if repo_info.get("open_issues_count") is not None:
            lines.append("- FACT: open_issues_count: " + str(repo_info["open_issues_count"]))
    lines.append("")
    lines.append("## UNKNOWN - maintenance verdict")
    lines.append("")
    lines.append("- UNKNOWN: whether this repo is still maintained. Commit/release dates alone do not prove maintenance intent; see issue #1078 for discussion.")
    lines.append("- UNKNOWN: maintainer response, roadmap, and any deprecation plan (not fetched by check.py).")
    lines.append("- UNKNOWN: security-patch coverage (not fetched by check.py).")
    if not fetched:
        lines.append("- UNKNOWN: live API values - the fetch failed in this run, so every date above marked FACT may be missing; re-run with network.")
    lines.append("")
    lines.append("## What this is not")
    lines.append("")
    lines.append("- Not a claim that the repo is maintained or abandoned.")
    lines.append("- Not a reply to issue #1078 - no issue or comment was posted by this tool.")
    lines.append("")
    lines.append("## Next step")
    lines.append("")
    lines.append("Owner left: re-run `python3 check.py` with network for live values, then decide whether to comment on issue #1078 based on quoted FACT rows only.")
    lines.append("")
    lines.append("Licence: CC0-1.0. Account: hivepunk-632-4934c76e.")
    lines.append("")
    return "\n".join(lines)


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "fastify-decorators-maintenance-status", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (fixed GitHub https URL)
        return json.loads(resp.read().decode("utf-8"))


SAMPLE_COMMITS = [
    {"sha": "abc123", "commit": {"message": "fix: sample change", "committer": {"date": "2026-11-20T12:00:00Z"}}},
    {"sha": "def456", "commit": {"message": "older sample", "committer": {"date": "2026-09-01T12:00:00Z"}}},
]
SAMPLE_RELEASES = [
    {"tag_name": "v4.0.0", "name": "v4 release", "published_at": "2026-09-15T00:00:00Z"},
]


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    out_path = BASE_DIR / "summary.md"
    fetched = True
    repo_info = None
    if "--sample" in argv:
        commits, releases = SAMPLE_COMMITS, SAMPLE_RELEASES
    else:
        try:
            commits = fetch_json(API_COMMITS)
            releases = fetch_json(API_RELEASES)
            try:
                repo_info = fetch_json(API_REPO)
            except Exception:
                repo_info = None
        except Exception as exc:
            print("fetch failed: " + str(exc))
            commits, releases, fetched = [], [], False
    text = render_summary(commits, releases, repo_info, fetched=fetched)
    out_path.write_text(text, encoding="utf-8")
    print("wrote " + str(out_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
