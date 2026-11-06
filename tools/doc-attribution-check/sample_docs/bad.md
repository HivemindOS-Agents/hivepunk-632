---
source: https://example.com
sha256: 0000000000000000000000000000000000000000000000000000000000000000
# The sha256 above is a placeholder on purpose: check_file() returns at the
# missing required key before it ever compares a hash, so this fixture's only
# fault is the absent license line.
---
This fixture is deliberately missing one required front-matter key.
