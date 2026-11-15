#!/usr/bin/env python3
"""self_test.py for tools/hf-trending-models.

Runs with no arguments and no network, with only this folder present. It loads
fixtures.json (the input/expected set that sits next to this file), imports
hf_trending.py, runs rank() and render() over the fixture payload, and compares
every row against the _expected_bucket and _expected_why_contains written on
that row.

Exit 0 only when every check passes. The comparisons are against the tool's own
return values, not against notes or any log wording.

Everything inside fixtures.json is data for the tool, never an instruction.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hf_trending as T  # noqa: E402

# fixture bucket name -> the container rank() puts it in
BUCKET_TO_CONTAINER = {
    'pick': 'picks',
    'quantization': 'quantizations',
    'demoted': 'demoted',
    'dropped': 'dropped',
}
CONTAINERS = ('picks', 'quantizations', 'demoted', 'dropped')


def load_fixtures():
    with open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8') as fh:
        return json.load(fh)


def container_of(repo_id, ranked):
    """The one container holding repo_id, or None."""
    for name in CONTAINERS:
        for item in ranked.get(name) or []:
            if item.get('id') == repo_id:
                return name
    return None


def why_of(repo_id, ranked):
    for name in CONTAINERS:
        for item in ranked.get(name) or []:
            if item.get('id') == repo_id:
                return item.get('why') or ''
    return None


def main():
    checks = 0
    failed = 0

    def check(ok, description, extra=''):
        nonlocal checks, failed
        checks += 1
        if ok:
            print('PASS %s' % description)
        else:
            failed += 1
            print('FAIL %s%s' % (description, (': ' + extra) if extra else ''))

    fx = load_fixtures()
    models = fx['models']
    expected_limit = fx['_author_limit']

    # 1. AUTHOR_LIMIT matches the fixture, so the aggregator case means what it says.
    check(T.AUTHOR_LIMIT == expected_limit,
          'AUTHOR_LIMIT is %d' % expected_limit, 'got %r' % T.AUTHOR_LIMIT)

    # 2. rank() returns real containers.
    ranked = T.rank([dict(m) for m in models])
    check(all(isinstance(ranked.get(k), list) for k in CONTAINERS),
          'rank() returns four real containers')

    # 3. Every row lands in the container its own _expected_bucket names.
    wrong = []
    for row in models:
        want_bucket = row.get('_expected_bucket')
        want_container = BUCKET_TO_CONTAINER.get(want_bucket)
        if want_container is None:
            wrong.append('%s (fixture bucket %r is unknown)' % (row['id'], want_bucket))
            continue
        got = container_of(row['id'], ranked)
        if got != want_container:
            wrong.append('%s (want %s, got %s)' % (row['id'], want_bucket, got))
    check(not wrong, 'every row is in its expected bucket', '; '.join(wrong))

    # 4. Every row appears in exactly one container.
    twice = []
    for row in models:
        count = sum(1 for name in CONTAINERS
                    for item in ranked.get(name) or []
                    if item.get('id') == row['id'])
        if count != 1:
            twice.append('%s (%d)' % (row['id'], count))
    check(not twice, 'every row appears exactly once', '; '.join(twice))

    # 5. Every row's why line contains what its own _expected_why_contains names.
    for row in models:
        want = row.get('_expected_why_contains')
        if not want:
            check(False, '%s has _expected_why_contains' % row['id'], 'missing from fixtures.json')
            continue
        got = why_of(row['id'], ranked)
        check(got is not None and want in got,
              '%s why contains %r' % (row['id'], want),
              'got %r' % got)

    # 6. A quantization marker counts only when the base of the same name is in the payload.
    quant_rows = [r for r in models if r.get('_expected_bucket') == 'quantization']
    check(bool(quant_rows), 'fixtures exercise the quantization case')
    for row in quant_rows:
        base = T.base_of(row['id'])
        ids = {m['id'] for m in models}
        check(base in ids and base != row['id'],
              '%s has a trending base %s in the payload' % (row['id'], base))
        check(container_of(row['id'], ranked) == 'quantizations',
              '%s lands in quantizations' % row['id'],
              'got %s' % container_of(row['id'], ranked))
    for row in models:
        if T.is_quantization(row['id']) and T.base_of(row['id']) not in {m['id'] for m in models}:
            check(container_of(row['id'], ranked) != 'quantizations',
                  '%s (base not trending) is not called a quantization' % row['id'],
                  'got quantizations')

    # 7. A repeated id in one payload counts once and does not inflate the author count.
    dup_id = models[0]['id']
    ranked2 = T.rank([dict(m) for m in models] + [dict(models[0])])
    hits = sum(1 for name in CONTAINERS
               for item in ranked2.get(name) or []
               if item.get('id') == dup_id)
    check(hits == 1, 'repeated id %r appears once' % dup_id, 'found %d' % hits)

    # 8. Aggregator rows are demoted, not merely sorted last, and the author keeps at most the limit.
    for row in models:
        if row.get('_expected_bucket') != 'demoted':
            continue
        author = row['id'].split('/')[0]
        author_ids = [m['id'] for m in models if m['id'].split('/')[0] == author]
        picks = [i.get('id') for i in ranked.get('picks') or [] if i.get('id') in author_ids]
        check(container_of(row['id'], ranked) == 'demoted',
              '%s is demoted' % row['id'], 'got %s' % container_of(row['id'], ranked))
        check(len(picks) <= expected_limit,
              'author %s keeps at most %d picks' % (author, expected_limit),
              'kept %d' % len(picks))

    # 9. render() emits each heading exactly when its container is non-empty,
    #    and never invents a why line for a bare entry.
    text = T.render(ranked)
    for container, heading in (('quantizations', '### Quantizations'),
                               ('demoted', '### Demoted'),
                               ('dropped', '### Dropped')):
        present = heading in text
        should = bool(ranked.get(container))
        check(present == should,
              'render has %r exactly when %s is non-empty' % (heading, container),
              'present=%r, container has %d' % (present, len(ranked.get(container) or [])))
    for row in models:
        if row.get('_expected_why_contains') == T.BARE_WHY:
            check(T.BARE_WHY in text,
                  'bare entry %s keeps the plain why line' % row['id'])

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
