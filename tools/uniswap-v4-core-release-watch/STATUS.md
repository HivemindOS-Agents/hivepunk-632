# STATUS - Uniswap v4-core latest release

opportunity: opp-632-201

Source endpoint for every line below:
https://api.github.com/repos/Uniswap/v4-core/releases/latest
Release page pattern: https://github.com/Uniswap/v4-core/releases/latest
Repository: https://github.com/Uniswap/v4-core

Labels: FACT = carried by the live response fetched for this status.
DERIVED = computed from a FACT value in this status. UNKNOWN = not
proven by a live fetch in this step; never read UNKNOWN as zero or safe.

## Summary lines

- FACT: the intended source endpoint is https://api.github.com/repos/Uniswap/v4-core/releases/latest - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: latest release tag (tag_name) - not fetched in this step - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: release name (name) - not fetched in this step - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: published date (published_at) - not fetched in this step - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: headline numbers from the release payload (assets, asset downloads, body length) - not fetched in this step - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: release page URL (html_url) - not fetched in this step - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- DERIVED: days_since cannot be derived because published_at is UNKNOWN; no day count is claimed - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: whether a newer prerelease or draft tag exists (the endpoint excludes both) - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: whether a newer tag with no published release exists - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: later deletion, retag or yank of the latest tag - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: maintenance verdict for Uniswap/v4-core - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: earlier tracker-page reports of v4.0.0 on 2025-01-23 are second-hand and were not verified against the API in this step, so they are not FACT here - source: https://github.com/Uniswap/v4-core/releases/latest

## Headline numbers

- UNKNOWN: asset count - not fetched - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: total asset downloads - not fetched - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- UNKNOWN: days_since published - not derived, published_at is UNKNOWN - source: https://api.github.com/repos/Uniswap/v4-core/releases/latest

## How to refresh

1. With network run `python3 verify.py --fetch` in this folder.
2. Rewrite the UNKNOWN lines above only from the live response,
   flipping a line to FACT only where the response carried the value.
3. Recompute days_since as the calendar-day difference and label it DERIVED.
4. Run `python3 self_test.py` and read SELFTEST_OUTPUT.md.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
