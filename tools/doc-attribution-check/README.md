# doc‑attribution‑check

A lightweight Python tool that validates Markdown documents for correct
front‑matter.  It ensures each file contains the required `license:` and
`source:` keys and that the declared `sha256:` value matches the file body.

## Usage

```bash
python3 checker.py <folder_of_markdown>
```

The script prints **PASS** or **FAIL** for each file and a final summary
line of the form:

```
self_test: N check(s), M failed
```

The command returns exit status 0 only when all checks pass.

## Sample fixtures

The folder *sample_docs* contains two Markdown files:

- **good.md** – passes all checks.
- **bad.md** – purpose‑fully missing the `license:` key (fails).

You can run the bundled self‑test with:

```bash
python3 self_test.py
```

## Untested

- The script does not walk sub‑directories – only the top‑level
  folder is examined.
- No network access or file‑system write operations beyond the test
  fixtures are performed.
- Edge cases such as CRLF line endings or atypical front‑matter
  delimiters are not heuristically handled.

All samples are in pure ASCII UTF‑8 and the tool is built entirely with
Python standard library.
