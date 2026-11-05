# card-lint (copy)

A copy of `tools/card-lint/card_lint.py` and two of its fixtures, so this package's self-test can run on its own:
the self-test runner checks out only `tools/publish-attribution-run-lines-package/`.

The original is `tools/card-lint/` in this repository. When both folders are present, `self_test.py` checks that
these files are byte-identical to the originals and fails if they drift.
