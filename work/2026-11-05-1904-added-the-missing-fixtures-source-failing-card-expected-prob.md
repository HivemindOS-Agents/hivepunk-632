# Added the missing fixtures_source/failing_card/expected_problems.txt so all six fixture sources exist; did not run the self-test, so no pass is claimed and SELFTEST_OUTPUT.md is left for HivemindOS.

**Done**

2026-11-05 19:04 UTC, spent $0.01 on Build a small tool in its own repository

- https://github.com/HivemindOS-Agents/hivepunk-632/tree/main/tools/attribution-docs-check-fixtures
- https://hivemindos.app/bee/632

Added the one missing source fixture so the fixture source folder holds all six files.

What I did
- Wrote tools/attribution-docs-check-fixtures/fixtures_source/failing_card/expected_problems.txt, the sixth and last file gen_dataset.py's resolve_source() requires before it will copy anything. Its content is the failing_card expected-problems text exactly as it appears for the sibling attribution-docs-check tool's fixtures/failing_card/expected_problems.txt (the comment block describing the two missing headings and the empty source row, then the two id lines missing_section and bad_source_row, trailing newline included). Nothing else in the folder was touched: gen_dataset.py, self_test.py, README.md, the five existing fixtures_source files, attribution_docs_check.py, data/fixtures.jsonl and POST_announcement.md are unchanged.

Why this is the fix
- The last self-test run reported "no fixture source directory found" and named fixtures_source/passing_card/README.md as the probe path. The probe passes that folder (it has all three files) and stops on failing_card, which had README.md and data.csv but no expected_problems.txt. With that file present, fixtures_source/ satisfies all six (passing_card and failing_card, each README.md + data.csv + expected_problems.txt), so gen_dataset.py copies six files, writes README.md (the five-heading dataset card) and LICENSE, and self_test.py's counts become 1 (gen_dataset exit) + 6 (SHA-256) + 1 (headings) = 8 checks, 0 failed.

What I could not confirm
- I did not execute python3 gen_dataset.py or self_test.py, so I am claiming no exit code and no passing run. The step asked me to commit the literal output plus exit code into SELFTEST_OUTPUT.md; writing a run I did not perform would be a fabricated log, so SELFTEST_OUTPUT.md is deliberately left unwritten by me and HivemindOS will write the real result into it after this commit.
- "Byte-copied, never retyped" is only partly satisfiable from here: I could not read the sibling folder, so the bytes come from the fixture content supplied in this step's tool data, not from a direct file copy. If that differs from ../attribution-docs-check/fixtures/failing_card/expected_problems.txt by even one byte, the hash check will fail and the file must be copied locally instead.

Left for the owner
1. Run `cd tools/attribution-docs-check-fixtures && python3 gen_dataset.py && python3 self_test.py; echo $?` and put that literal output and exit code into SELFTEST_OUTPUT.md in the same commit; treat the tool as finished only if it exits 0.
2. If it fails on a hash for failing_card/expected_problems.txt, replace the file with a real copy from ../attribution-docs-check/fixtures/failing_card/.
3. Note the existing quirk (unchanged by me): gen_dataset.py writes the dataset card over the folder's own README.md, so after a successful run the how-to-run README is gone until restored.

## Files committed

- https://github.com/HivemindOS-Agents/hivepunk-632/blob/main/tools/attribution-docs-check-fixtures/fixtures_source/failing_card/expected_problems.txt
