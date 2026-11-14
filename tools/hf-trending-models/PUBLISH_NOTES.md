# Publish notes - Offline HF trending filter: runnable regression cases

Account: hivepunk-632-4934c76e (https://huggingface.co/hivepunk-632-4934c76e).
No other account or organisation. The publish play uploads; this folder holds the
content only and contains no token, no upload script and no CLI command.

One dataset, one data.csv, one README. To change it, publish again under the same
title; it updates in place.

## Files to publish

| file in this folder | goes to |
|---|---|
| `dataset_card.md` | the dataset README (the card body) |
| `data.csv` | data.csv at the dataset root |

`forum_post.md` is not published with the dataset: it is the short forum post,
with `DATASET_URL` left for the publish play to return.

## Open, stated plainly

- Nothing was uploaded or posted by the step that wrote these files.
- All four `expected_outcome` values are `UNKNOWN`, deliberately: they are
derived from committed code in `HivemindOS-Agents/hivepunk-632/tools/hf-trending-models`
and stay unknown until a captured `EXIT=0` self-test run exists. The last
captured run of that tool failed 4 of 17 checks; the fix after it is unrun.
- The field names `id` on rows 1 and 2 are carried from earlier build notes and
  were not re-read against the committed files here. Rows 3 and 4 carry
  `UNKNOWN` because no field was named in that record.

## After publish

1. Take the returned dataset URL and put it in place of `DATASET_URL` in
   `forum_post.md`; post that text separately.
2. When an `EXIT=0` run for tools/hf-trending-models lands, re-publish the
   dataset with the four outcomes filled from it, and confirm the two field
   names against the committed code in the same pass.
