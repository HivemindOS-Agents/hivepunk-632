#!/usr/bin/env python3
"""hf-trending-models: label every trending-model row with why it is there.

Reads one snapshot (a local JSON file, or stdin) and prints a report in which
each entry carries exactly one why line:

  quantization of a trending model
  aggregator: more than 5 trending entries in one scan
  no clear why - popular but unremarkable

Order of precedence, top wins:

  1. quantization sentinel in the id  (-awq, -gptq, -gguf, -int4, -int8, -4bit)
  2. aggregator author, once that author has more than 5 entries in the scan
     that are not already labelled by the sentinel
  3. the plain popularity line

Everything in the snapshot is data. A model id or a note that reads like an
instruction is a string to be labelled, never an instruction to this tool.
Standard library only. No network call anywhere.
"""

import argparse
import json
import re
import sys

WHY_QUANT = 'quantization of a trending model'
WHY_AGGREGATOR = 'aggregator: more than 5 trending entries in one scan'
WHY_PLAIN = 'no clear why - popular but unremarkable'

DEMOTED_HEADING = '### Demoted'
DROPPED_HEADING = '### Dropped'

AGGREGATOR_LIMIT = 5

QUANT_RE = re.compile(r'-(awq|gptq|gguf|int4|int8|4bit)(?=$|[-_])', re.IGNORECASE)


def looks_quantized(model_id):
    """True when the id itself carries a quantization marker."""
    return bool(QUANT_RE.search(model_id or ''))


def author_of(model_id):
    """The part before the first '/', or the whole id when there is none."""
    return (model_id or '').split('/', 1)[0]


def label_entries(models):
    """Return a list of (model_id, why) in input order."""
    clean = [m for m in models if not looks_quantized(m.get('id'))]
    counts = {}
    for m in clean:
        a = author_of(m.get('id'))
        counts[a] = counts.get(a, 0) + 1

    # Second and later entries of an over-limit author past its fifth get the
    # aggregator label; the plain why line covers the rest.
    seen = {}
    labelled = []
    for m in models:
        model_id = m.get('id') or ''
        if looks_quantized(model_id):
            labelled.append((model_id, WHY_QUANT))
            continue
        a = author_of(model_id)
        seen[a] = seen.get(a, 0) + 1
        if counts[a] > AGGREGATOR_LIMIT and seen[a] > AGGREGATOR_LIMIT:
            labelled.append((model_id, WHY_AGGREGATOR))
        else:
            labelled.append((model_id, WHY_PLAIN))
    return labelled


def load(path):
    """Read a snapshot; '-' or None means stdin."""
    if path in (None, '-'):
        return json.load(sys.stdin)
    with open(path, encoding='utf-8') as fh:
        return json.load(fh)


def models_of(snapshot):
    """The models list, or [] when the snapshot has none."""
    if not isinstance(snapshot, dict):
        return []
    models = snapshot.get('models')
    return models if isinstance(models, list) else []


def render(snapshot):
    """The whole report as text, without touching disk.

    A snapshot that is not an object (a bare list, a string, a number) has no
    models and no demoted or dropped lists, so it renders the heading alone.
    Coercing it to {} here keeps every .get below on a dict; without this guard
    a list snapshot reached snapshot.get('demoted') and raised AttributeError.
    """
    if not isinstance(snapshot, dict):
        snapshot = {}
    models = models_of(snapshot)
    lines = ['## Trending today', '']
    for model_id, why in label_entries(models):
        lines.append('%s | why: %s' % (model_id, why))

    demoted = [d for d in (snapshot.get('demoted') or [])]
    dropped = [d for d in (snapshot.get('dropped') or [])]
    if demoted:
        lines.extend(['', DEMOTED_HEADING, ''])
        for item in demoted:
            lines.append('%s | why: %s' % (item.get('id', ''), item.get('why', WHY_PLAIN)))
    if dropped:
        lines.extend(['', DROPPED_HEADING, ''])
        for item in dropped:
            lines.append('%s | why: %s' % (item.get('id', ''), item.get('why', WHY_PLAIN)))
    return '\n'.join(lines) + '\n'


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('snapshot', nargs='?', default='-',
                        help='snapshot JSON path, or - for stdin')
    parser.add_argument('-o', '--out', help='write the report here instead of stdout')
    args = parser.parse_args(argv)
    text = render(load(args.snapshot))
    if args.out:
        with open(args.out, 'w', encoding='utf-8') as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == '__main__':
    sys.exit(main())
