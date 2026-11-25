---
license: cc0-1.0
language:
  - en
tags:
  - uniswap
  - v4-core
  - release-watch
  - labelled
pretty_name: Uniswap v4-core release watch (labelled)
---

# Uniswap v4-core release watch (labelled)

A one-row watch record for the latest release of Uniswap/v4-core. Nothing here
was fetched for the published copy: every value is UNKNOWN and stored as null,
never 0 and never "safe" (never zero/safe).

- Source repo: https://github.com/Uniswap/v4-core
- Source endpoint: https://api.github.com/repos/Uniswap/v4-core/releases/latest
- Release page: https://github.com/Uniswap/v4-core/releases/latest
- Account: hivepunk-632-4934c76e
- Target: https://huggingface.co/datasets/hivepunk-632-4934c76e/uniswap-v4-core-release-watch
- Licence: CC0-1.0

## Files

| This repo file | Published as | Note |
|---|---|---|
| dataset_card.md | README.md | this card, verbatim |
| dataset_rows.jsonl | data/dataset_rows.jsonl | the labelled rows, verbatim |

## Labels

- **FACT** - carried by the live response, copied unchanged.
- **DERIVED** - computed from a FACT value. Today only `days_since`.
- **UNKNOWN** - not proven. Stored as **null**, never as 0, and never as the
  word "safe" (never zero/safe). An unknown number is not a zero.

## Fields in the published row

Every field below is UNKNOWN with a null value in the published copy.

| field | label | value |
|---|---|---|
| tag | UNKNOWN | null |
| name | UNKNOWN | null |
| published_at | UNKNOWN | null |
| days_since | UNKNOWN | null |
| html_url | UNKNOWN | null |
| prerelease_or_draft_newer | UNKNOWN | null |
| newer_tag_without_release | UNKNOWN | null |
| later_deletion_or_yank | UNKNOWN | null |
| maintenance_verdict | UNKNOWN | null |

`asset_count` and `total_asset_downloads` are left out rather than written as 0,
because the release response was not fetched; a 0 would claim a measured zero.
The four risk fields stay UNKNOWN always: nothing in the latest-release response
proves them.

## Check the labels

~~~bash
python3 verify.py          # checks the committed rows, no network
python3 publish_model.py   # checks this card and the rows, prints the manifest
~~~

Verify command: python3 verify.py

## Load

~~~python
from datasets import load_dataset
ds = load_dataset("hivepunk-632-4934c76e/uniswap-v4-core-release-watch", split="train")
print(ds[0]["labels"])
~~~

## Publish status

Publish status: NOT PUBLISHED
Live URL: none
Publish date: none

The upload is the owner Publish a small open dataset step under
hivepunk-632-4934c76e with the same title; this card claims no live dataset page
and no publish date.

## Could not confirm

The latest tag, name, published date, days_since, release page URL, asset count,
total asset downloads and maintenance status: the endpoint was not fetched, so
all are UNKNOWN/null here. Also could not confirm that the Hugging Face page
exists, because publishing has not run.

## Untested

The live fetch path `python3 verify.py --fetch` and this dataset once downloaded
from Hugging Face. Live-fetch values have not been checked into this card.

## Licence and scope

CC0-1.0. Not advice and not financial information.
