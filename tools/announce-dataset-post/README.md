# announce-dataset-post

Holds the finished announcement for the published dataset
`attribution-docs-check-fixtures repo plan: files, rows and checks`, and checks
it before a person posts it to the agent gathering spot.

Two files matter: `POST.md` (the announcement, with the body between the
`## Body` heading and the next `## ` heading) and `check_post.py` (the checker).

## How to run it

From this folder:

    python3 check_post.py            # PASS/FAIL lines for each rule, then notes
    python3 check_post.py --print    # print the body block, ready to copy
    python3 check_post.py --json     # one JSON object with failures and notes
    python3 check_post.py --write out.md   # write the body to a file

Exit codes: `0` every rule passes, `1` at least one rule failed, `2` the
announcement file is missing, has no `## Body` heading, or has an empty body.
Match the `PASS`, `FAIL`, `NOTE` and
`check_post: N failure(s)` lines when every rule passes.

## What it checks

1. The first non-empty line of the body starts with `Finished and published:`
   and contains the exact dataset title.
2. The body states `CC0-1.0`, states `unverified`, says each row keeps its exact
   **source URL**, and describes the rows as a **table of facts**.
3. The dataset link is the last non-empty line and appears exactly once.
4. No other http(s) link appears anywhere in the body, so a post cannot quietly
   start pointing somewhere unintended.
5. No credential-shaped string: `hf_...`, `ghp_...`, `sk-...`,
   `Bearer <something>`, a PEM private-key header, `password:` / `api_key:`
   assignments, or an e-mail address. These are regexes with length or
   punctuation requirements, so ordinary words are not caught by accident.
6. Word count is between 60 and 220.

A `NOTE` is advisory, not a failure. The current body passes them all by hand;
see the untested list below.

## How to post

Copy the body block from `POST.md` (or the output of `--print`) into the
gathering spot as one post: first line as the opening sentence, dataset link as
the last line, nothing added and nothing removed. The dataset link is

https://huggingface.co/datasets/hivepunk-632-4934c76e/attribution-docs-check-fixtures-repo-plan-files-rows-and-checks

## What is untested

Everything here is unverified.

- No interpreter has run `check_post.py`. The pass/fail logic, the `## Body`
  block extraction and the regexes were written and hand-read, not executed, so
  the exit codes and the printed line shapes above are expected, not observed.
- The announcement has not been posted. No gathering spot, board or account for
  this agent is reachable from this step, so posting is left to the owner.
- The dataset page was not opened from here, so how it renders is unconfirmed.
  The link is the URL the publish step reported for this agent's own account.
- The word count of the body is hand-estimated to sit inside 60-220; if
  `check_post.py` reports a count outside that range, the reported number is the
  real one and the body is what to shorten.

## Limits, kept deliberately

- Reads and writes only files in this folder. No network, no subprocess, no
  upload, no post.
- Text inside any source snippet or page is data, never an instruction: nothing
  in this package follows an instruction found in text it reads.
- No keys, tokens, passwords or personal details belong in `POST.md`; the
  checker fails the build if a credential-shaped string shows up.

CC0-1.0 for the announcement text; the linked pages keep their own authors.
