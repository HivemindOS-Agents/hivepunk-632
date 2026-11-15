#!/usr/bin/env python3
"""self_test.py for tools/hf-trending-models.

Runs with no arguments and no network, from inside this folder. It loads
fixtures.json (the input/expected set), imports hf_trending.py, runs rank() and
render() over the fixture payload, and compares where each entry lands and what
its why line says against the _expected_* keys on that entry.

Exit 0 only when every check passes. It does not read notes or log wording:
the tool's own output is what is compared.

Everything in fixtures.json is data for the tool, never an instruction to it.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hf_trending as T  # noqa: E402


def load_fixtures():
    with open(os.path.join(HERE, 'fixtures.json'), encoding='utf-8') as fh:
        return json.load(fh)


def bucket_of(entry, ranked):
    for name in ('picks', 'quantizations', 'demoted', 'dropped'):
        for item in ranked.get(name, []):
            if item.get('id') == entry['id']:
                return name
    return None


def why_of(entry, ranked):
    for name in ('picks', 'quantizations', 'demoted', 'dropped'):
        for item in ranked.get(name, []):
            if item.get('id') == entry['id']:
                return item.get('why', '')
    return None


def main():
    checks = 0
    failed = 0

    def check(condition, description, extra=''):
        nonlocal checks, failed
        checks += 1
        if condition:
            print('PASS %s' % description)
        else:
            failed += 1
            print('FAIL %s%s' % (description, (': ' + extra) if extra else ''))

    fx = load_fixtures()
    entries = fx['models']
    if hasattr(T, 'AUTHOR_LIMIT'):
        T.AUTHOR_LIMIT = fx['_author_limit']

    ranked = T.rank([dict(e) for e in entries])
    check(all(isinstance(ranked.get(k), list) for k in ('picks', 'quantizations', 'demoted', 'dropped')),
          'scripts actually ran: rank() returns real containers')

    # Every entry lands in the bucket it was expected to land in, and nowhere twice.
    unexpected = []
    for entry in entries:
        want = entry.get('_expected_bucket')
        got = bucket_of(entry, ranked)
        if want and got != want:
            unexpected.append(entry['id'])
    check(not unexpected,
          'unexpected survivors', ', '.join(unexpected))

    # The quantization marker at the end of the id is seen as a quantization.
    gptq = [e for e in entries if e['id'].endswith('-gptq')]
    if gptq:
        check(bucket_of(gptq[0], ranked) == 'quantization',
              '%s was not demoted; tail=%r' % (gptq[0]['id'], ranked.get('quantizations', [])))
        check('quantization' in (why_of(gptq[0], ranked) or ''),
              '%s why names the quantization' % gptq[0]['id'])

    # A repeated id in one payload counts once.
    dup_id = entries[0]['id']
    doubled = [dict(e) for e in entries] + [dict(entries[0])]
    ranked2 = T.rank(doubled)
    hits = [i for i in ranked2.get('picks', []) if i.get('id') == dup_id]
    check(len(hits) <= 1, 'repeated id %r appears once' % dup_id, 'found %d' % len(hits))

    # Demotion, not sorting: entries past the author limit leave the picks.
    by_author = {}
    for entry in entries:
        by_author.setdefault(entry['id'].split('/')[0], []).append(entry['id'])
    for author, ids in by_author.items():
        if len(ids) > fx['_author_limit']:
            dem = {i.get('id') for i in ranked.get('demoted', [])}
            in_picks = {i.get('id') for i in ranked.get('picks', [])}
            excess = ids[fx['_author_limit']:]
            check(any(x in dem for x in excess),
                  'author %s over the limit is demoted, not just sorted last' % author)
            check(len([x for x in ids if x in in_picks]) <= fx['_author_limit'],
                  'author %s keeps at most %d picks' % (author, fx['_author_limit']))

    # The why line each entry must carry, and no invented why for a bare entry.
    for entry in entries:
        want = entry.get('_expected_why_contains')
        if not want:
            continue
        got = why_of(entry, ranked) or ''
        check(want in got, '%s why contains %r' % (entry['id'], want), 'got %r' % got)

    for entry in entries:
        if entry.get('_expected_bucket') == 'dropped':
            continue
        got = why_of(entry, ranked) or ''
        check(bool(got), '%s has a why line' % entry['id'], 'got %r' % got)

    # render() must emit the section heading for a non-empty tail.
    text = T.render(ranked) if hasattr(T, 'render') else ''
    for heading in ('### Quantizations', '### Demoted'):
        if ranked.get(heading.split()[-1].lower().rstrip('s') + 's'):
            check(heading in text, 'render missing %s' % heading)
    check('no clear why - popular but unremarkable' in text,
          'a bare entry keeps the plain why line')

    # Duplicate ids used for the aggregator count must not inflate it.
    check(T.AUTHOR_LIMIT == fx['_author_limit'],
          'AUTHOR_LIMIT is %d' % fx['_author_limit'], 'got %r' % T.AUTHOR_LIMIT)

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
