~~~markdown
# counts_check

`counts_check` is a tiny standalone script that verifies that the
statements about the number of rows and source URLs that are present in a
dataset card (typically a `README.md`) match the actual contents of the
corresponding JSONL data file.

## Usage
```
python3 counts_check.py path/to/README.md path/to/data.jsonl
```
The script will print:
```
counts_check: card <card_rows>/<card_source_fields>/<card_distinct_pages> vs file <file_rows>/<file_source_fields>/<file_distinct_pages> — PASS/FAIL
```
and exit with status `0` if the two sets of numbers agree, or `1` otherwise.

## Example – PASS
Below is a minimal working example where the card and the file are in
perfect agreement.

---
**Card (README.md)**
~~~
rows: 2
source fields: 2
distinct source pages: 2
~~~

**File (data.jsonl)**
~~~
{"id": "a1", "source": "https://example.com/page1"}
{"id": "a2", "source": "https://example.com/page2"}
~~~
Running the tool on these two files produces:
```
counts_check: card 2/2/2 vs file 2/2/2 — PASS
```

## Example – FAIL
In this example the card claims there are two distinct source pages, but the
JSONL file only contains one URL.

---
**Card (README.md)**
~~~
rows: 2
source fields: 2
distinct source pages: 2
~~~

**File (data.jsonl)**
~~~
{"id": "a1", "source": "https://example.com/page1"}
{"id": "a2", "source": "https://example.com/page1"}
~~~
Output of the tool:
```
counts_check: card 2/2/2 vs file 2/2/1 — FAIL
```

## What is untested
The tool is designed, tested, and documented only against the fixtures
included in its own repository.  No external files or network resources are
accessed.  Beyond those fixtures the behaviour remains unverified.

---
For more details on how the script works, see the source file
`counts_check.py`.
~~~
