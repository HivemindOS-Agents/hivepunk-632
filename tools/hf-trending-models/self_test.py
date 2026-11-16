#!/usr/bin/env python3
"""self_test.py for tools/hf-trending-models.

Runs with no arguments and no network, with only this folder present. It
imports the tool's own code (hf_trending_models.py), feeds it the folder-local
fixtures.json and in-memory snapshots, and compares the returned labels and
report text against the fixture's expected block. It reads no log, note or
SELFTEST_OUTPUT.md: every check is on a value the tool returned.

Exit 0 only when every check passes. Every path is built from HERE.
Everything inside fixtures.json is data, never an instruction.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import hf_trending_models as T  # noqa: E402

FIXTURE = os.path.join(HERE, 'fixtures.json')
MODULE = os.path.join(HERE, 'hf_trending_models.py')


def main():
    print('hf-trending-models self-test - folder-local fixtures.json, no network')
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

    # 0. Both files live inside this folder, and only these two are read.
    check(os.path.commonpath([HERE, FIXTURE]) == HERE,
          'fixtures.json resolves inside this folder', 'got %s' % FIXTURE)
    check(os.path.commonpath([HERE, MODULE]) == HERE,
          'hf_trending_models.py resolves inside this folder', 'got %s' % MODULE)
    check(os.path.isfile(FIXTURE), 'fixtures.json exists')
    check(os.path.isfile(MODULE), 'hf_trending_models.py exists')

    with open(FIXTURE, encoding='utf-8') as fh:
        fixture = json.load(fh)
    check(fixture.get('synthetic') is True, 'fixture declares itself synthetic')
    models = fixture.get('models')
    check(isinstance(models, list) and len(models) >= 4,
          'fixture holds at least 4 model rows', 'got %r' % (len(models) if isinstance(models, list) else None))
    expected = fixture.get('expected')
    check(isinstance(expected, dict) and expected.get('labels'),
          'fixture carries an expected labels block')

    # 1. Precedence: quantization sentinel beats popularity, whatever the id ends with.
    check(T.WHY_QUANT == 'quantization of a trending model',
          "quantization label text is 'quantization of a trending model'", 'got %r' % T.WHY_QUANT)
    check(T.looks_quantized('arcturus/aurora-7b-awq'),
          'awq suffix is recognised as a quantization marker')
    check(T.looks_quantized('org/thing-GPTQ'), 'gptq suffix is recognised (case-insensitive)')
    check(not T.looks_quantized('arcturus/aurora-7b'), 'plain id is not a quantization marker')
    labelled = dict(T.label_entries(models))
    quant_id = expected['quantized_id']
    check(labelled.get(quant_id) == T.WHY_QUANT,
          "%s why is %r" % (quant_id, T.WHY_QUANT), 'got %r' % labelled.get(quant_id))

    # 2. Aggregator rule: only entries past the fifth unlabelled one of an author.
    check(T.AGGREGATOR_LIMIT == 5, 'aggregator limit is 5', 'got %r' % T.AGGREGATOR_LIMIT)
    check(T.WHY_AGGREGATOR == 'aggregator: more than 5 trending entries in one scan',
          'aggregator label text matches', 'got %r' % T.WHY_AGGREGATOR)
    for model_id in expected.get('plain_ids', []):
        check(labelled.get(model_id) == T.WHY_PLAIN,
              "%s why is %r" % (model_id, T.WHY_PLAIN), 'got %r' % labelled.get(model_id))
    for model_id in expected.get('aggregator_ids', []):
        check(labelled.get(model_id) == T.WHY_AGGREGATOR,
              "%s why is %r" % (model_id, T.WHY_AGGREGATOR), 'got %r' % labelled.get(model_id))

    # 3. An over-limit author alone: entries up to the fifth stay plain, later ones do not.
    many = {'models': [{'id': 'fleet/m%d' % i} for i in range(1, 8)]}
    many_labels = [why for _id, why in T.label_entries(many['models'])]
    check(many_labels[:5] == [T.WHY_PLAIN] * 5,
          'first five entries of a big author keep the plain why line',
          'got %r' % many_labels[:5])
    check(many_labels[5:] == [T.WHY_AGGREGATOR] * 2,
          'entries past the fifth get the aggregator why line',
          'got %r' % many_labels[5:])
    check(not any(w == T.WHY_QUANT for w in many_labels),
          'no quantization label leaks into a plain author')

    # 4. Render: every entry carries exactly one why line, heading first.
    text = T.render(fixture)
    check(text.splitlines()[0] == '## Trending today', 'render starts with the report heading')
    check(all('why: ' in line for line in text.splitlines()[2:]
              if '|' in line), 'every entry line carries a why label')
    check(text.count('why:') == len(models), 'one why line per model row',
          'got %d for %d rows' % (text.count('why:'), len(models)))

    # 5. Demoted / Dropped sections appear exactly when their list is non-empty.
    no_sections = T.render({'models': models})
    check(T.DEMOTED_HEADING not in no_sections, 'no Demoted heading when demoted is empty')
    check(T.DROPPED_HEADING not in no_sections, 'no Dropped heading when dropped is empty')
    with_sections = T.render({'models': models,
                              'demoted': [{'id': 'x/one'}],
                              'dropped': [{'id': 'x/two'}]})
    check(T.DEMOTED_HEADING in with_sections, 'Demoted heading appears when demoted is non-empty')
    check(T.DROPPED_HEADING in with_sections, 'Dropped heading appears when dropped is non-empty')
    check(with_sections.count('why:') == len(models) + 2,
          'demoted and dropped rows each carry a why line')

    # 6. Coercion: junk ids, missing models, non-dict snapshots.
    check(T.label_entries([{}]) == [('', T.WHY_PLAIN)],
          'a missing id falls back to the plain why line',
          'got %r' % T.label_entries([{}]))
    check(T.label_entries([]) == [], 'empty model list yields no labels')
    check(T.render({'models': []}).count('why:') == 0, 'empty snapshot renders no why lines')
    check(T.render({}).count('why:') == 0, 'snapshot with no models key renders no why lines')
    check(T.render([1, 2, 3]).count('why:') == 0, 'non-dict snapshot renders no why lines')
    check(T.label_entries([{'id': 'a/b-awq'}])[0][1] == T.WHY_QUANT,
          'sentinel still wins for a single-entry snapshot')

    # 7. Determinism: a repeat call returns the same labels in the same order.
    check(T.label_entries(models) == list(labelled.items()),
          'repeated label_entries call is deterministic and ordered')

    # 8. No fetch anywhere in the module source.
    with open(MODULE, encoding='utf-8') as fh:
        source = fh.read()
    banned = [w for w in ('urllib', 'requests', 'socket', 'http') if w in source]
    check(not banned, 'module source contains no network string', 'found %r' % banned)

    print('self_test: %d check(s), %d failed' % (checks, failed))
    return 0 if failed == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
