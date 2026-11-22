# ARTIFACTS — simon-says-permission-request

opportunity: opp-632-193

Committed together in this folder:

- `permission-request.md` - short draft permission request to host a playable Simon Says game on the Microduck simulator, quoting the ask at https://huggingface.co/spaces/pollen-robotics/microduck-simulator/discussions/10 with sections: The ask quoted, Short request, What we would provide, Limits and acknowledgement, Next step, References.
- `README.md` - how to use, contents, use/limits/untested notes, and what could not be confirmed.
- `self_test.py` - folder-local self-test (no args, no network); verifies the draft contains the quoted ask verbatim, the discussion URL, and all required sections, plus README/ARTIFACTS coverage. Run: `python3 self_test.py; echo EXIT=$?`
- `ARTIFACTS.md` - this file.
- `SELFTEST_OUTPUT.md` - **not hand-written here**: written by the HivemindOS runner after copying this folder alone to a temp dir and running `python3 self_test.py` there. Owner left: read that file and confirm it ends `EXIT=0`, then post the draft to discussion #10 only if approved.

## Verify command

~~~bash
cd tools/simon-says-permission-request && python3 self_test.py; echo EXIT=$?
~~~

Expected on a passing run: every check prints PASS, the summary reports 0 failed, and the final line is EXIT=0.

## Notes

- No sibling folder was created; `tools/attribution-docs-check-fixtures/` was not touched; nothing was published.
- Licence: CC0-1.0. Account: hivepunk-632-4934c76e.
