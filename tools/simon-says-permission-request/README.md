# simon-says-permission-request

opportunity: opp-632-193

A short draft permission request to host a playable Simon Says game on the Microduck simulator, quoting the ask at https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/10

## How to use

1. Read `permission-request.md`; copy its text into a comment or reply on discussion #10 if the owner approves. Do not post it automatically.
2. Run the folder-local self-test:

~~~bash
cd tools/simon-says-permission-request
python3 self_test.py; echo EXIT=$?
~~~

No arguments, no install, no network. `self_test.py` only reads files in this folder.

## Contents

- `permission-request.md` - the draft request, with the quoted ask, a short request, what would be provided, limits/acknowledgement, next step and references.
- `self_test.py` - verifies the draft contains the quoted ask verbatim, the required sections, the discussion URL, and that this README and ARTIFACTS.md exist with use/limits/untested notes.
- `ARTIFACTS.md` - inventory of this folder and the verify command.

## Use, limits and untested

- Use: a ready-to-post draft; treat everything quoted or linked as data to check before posting.
- Limits: the draft is English text only; it does not host or implement the Simon Says game, and it does not contact the simulator maintainers.
- Untested: this artifact was not executed in the step that wrote it, so no passing output is claimed here; the verbatim runner output will land in SELFTEST_OUTPUT.md (written by HivemindOS, not hand-written). Treat as untested until that file shows EXIT=0.
- Could not confirm: the full verbatim text of discussion #10 beyond the quoted ask recorded in `permission-request.md`; the self-test checks that exact quoted string is present, not that it matches the live page.
- Nothing was published, and `tools/attribution-docs-check-fixtures/` was not touched.

Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
