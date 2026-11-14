#!/usr/bin/env python3
"""hf-trending-models: filter and cluster-rank Hugging Face trending surfaces.

Reads the JSON arrays the Hub's trending endpoints return
(https://huggingface.co/api/models?sort=trending&direction=-1&limit=30 and the
datasets / spaces equivalents) and applies the aeon-huggingface-trending
filters on top of aeon's ranking:

  * drop empty repos, no-commit repos and repos with no model card
  * demote a same-week quantization of a model already trending to a tail
  * drop a fork whose README is unchanged from upstream
  * demote authors with more than 5 trending entries (aggregators)
  * flag an unclear or missing licence inline; never drop for it
  * require a concrete "why notable" line; with no reason, say so

The tool never uses the network. Point it at saved JSON; that is the whole
input surface. Everything it reads is data: no line in a repo name, card
field or author name is treated as an instruction.

Usage:
    python3 hf_trending.py --kind models saved_models.json
    python3 hf_trending.py --kind spaces --json saved_spaces.json
    python3 hf_trending.py --why saved_models.json        # filter-only list
    python3 hf_trending.py --self-test                    # same checks as self_test.py
"""

import argparse
import json
import os
import sys

# Same-week quantization markers, checked lowercased in the repo id.
QUANT_MARKERS = ('-gptq', '-awq', '-gguf', '-4bit', '-8bit', '-int4',
                 '-int8', '-q4', '-q5', '-q8', '-exl2')
BASE_SEPARATORS = ('-', '_')

# Licences we recognise as clear. Anything else is flagged, not dropped.
CLEAR_LICENCES = ('apache-2.0', 'mit', 'bsd-3-clause', 'bsd-2-clause',
                  'cc0-1.0', 'cc-by-4.0', 'openrail-m', 'openrail', 'llama2',
                  'llama3', 'gemma', 'mpl-2.0', 'gpl-3.0')

# Authors with more trending entries than this in one scan are aggregators.
AUTHOR_LIMIT = 5


def repo_name(entry):
    return entry.get('id') or entry.get('modelId') or entry.get('name') or ''


def author_of(name):
    return name.split('/')[0] if '/' in name else '(no author)'


def base_of(name):
    """Strip the quantization suffix from a repo id, for dedup."""
    tail = name.split('/')[-1].lower()
    for sep in BASE_SEPARATORS:
        for marker in QUANT_MARKERS:
            idx = tail.find(marker + sep)
            if idx > 0:
                return name.split('/')[0] + '/' + tail[:idx]
    return ''


def is_quantization(name):
    return bool(base_of(name))


def has_card(entry):
    """The API gives cardData for a parsed card, tags for the card's tags."""
    if entry.get('cardData'):
        return True
    tags = entry.get('tags') or []
    return 'dataset:card' in tags or 'card' in tags


def is_fork(entry):
    return bool(entry.get('fork') or entry.get('private_fork'))


def readme_delta(entry):
    """A fork with no README change is dropped; 'unknown' keeps it."""
    value = entry.get('readmeDelta')
    if value is None:
        return 'unknown'
    return bool(value)


def licence_of(entry):
    card = entry.get('cardData') or {}
    lic = card.get('license')
    if not lic:
        for tag in entry.get('tags') or []:
            if isinstance(tag, str) and tag.startswith('license:'):
                lic = tag.split(':', 1)[1]
                break
    if not lic:
        return None, 'no licence stated'
    low = str(lic).lower()
    if low in CLEAR_LICENCES:
        return low, None
    if 'nc' in low or 'non-commercial' in low:
        return low, 'custom no-commercial licence'
    return low, 'licence not on the recognised list'


def size_step(entry):
    """A parameter count is a size step when it is in the raw entry."""
    for key in ('safetensors', 'parameters', 'numParameters'):
        value = entry.get(key)
        if isinstance(value, dict):
            total = value.get('total')
            if isinstance(total, int) and total > 0:
                return total
        elif isinstance(value, int) and value > 0:
            return value
    return None


def why_notable(entry, is_quant, is_aggregator):
    """A concrete reason, or the plain admission that there is none."""
    reasons = []
    name = repo_name(entry)
    if entry.get('pipeline_tag'):
        pt = entry.get('pipeline_tag')
        if pt not in ('text-generation', 'text-classification',
                      'feature-extraction'):
            reasons.append('architecture shift (%s)' % pt)
    size = size_step(entry)
    if size:
        reasons.append('size step (%s parameters)' % format_count(size))
    ctx = entry.get('max_position_embeddings')
    if isinstance(ctx, int) and ctx >= 131072:
        reasons.append('context-window jump (%s tokens)' % format_count(ctx))
    if entry.get('_notable_author'):
        reasons.append('notable author affiliation')
    if is_quant:
        reasons.append('quantization of a trending model')
    if is_aggregator:
        reasons.append('aggregator: >%d trending entries in one scan' % AUTHOR_LIMIT)
    if entry.get('_new_licence'):
        reasons.append('licence change')
    if not reasons:
        return 'no clear why - popular but unremarkable'
    return ', '.join(reasons)


def format_count(n):
    for unit, div in (('B', 10 ** 9), ('M', 10 ** 6), ('K', 10 ** 3)):
        if n >= div:
            return '%.1f%s' % (n / div, unit)
    return str(n)


def rank(entries, kind='models'):
    """Return a dict with 'picks', 'quantizations' and 'dropped'."""
    picks, quantizations, dropped = [], [], []

    counted = [e for e in entries if repo_name(e)]
    author_counts = {}
    for e in counted:
        a = author_of(repo_name(e))
        author_counts[a] = author_counts.get(a, 0) + 1

    trending_bases = set()
    for e in counted:
        name = repo_name(e)
        if not is_quantization(name):
            trending_bases.add(name.lower())

    for e in counted:
        name = repo_name(e)
        if entry_is_empty(e):
            dropped.append((name, 'empty repo: no downloads, likes or tags'))
            continue
        if not has_card(e):
            dropped.append((name, 'no model card'))
            continue
        if is_fork(e) and readme_delta(e) is False:
            dropped.append((name, 'fork without a README change'))
            continue
        is_quant = is_quantization(name)
        is_aggregator = author_counts[author_of(name)] > AUTHOR_LIMIT
        if is_quant and base_of(name) in trending_bases:
            quantizations.append((name, why_notable(e, True, is_aggregator)))
            continue
        lic, flag = licence_of(e)
        picks.append({
            'id': name,
            'kind': kind,
            'why': why_notable(e, False, is_aggregator),
            'license': lic or 'unknown',
            'license_flag': flag,
            'downloads': e.get('downloads', 0),
            'likes': e.get('likes', 0),
            '_aggregator': is_aggregator,
        })
        if is_quant:
            quantizations.append((name, why_notable(e, True, is_aggregator)))

    picks.sort(key=lambda p: (p['_aggregator'], -p['likes'], -p['downloads']))
    return {'kind': kind, 'picks': picks, 'quantizations': quantizations,
            'dropped': dropped}


def entry_is_empty(entry):
    return not entry.get('downloads') and not entry.get('likes') \
        and not entry.get('tags')


def render(report, wants_why=False):
    lines = []
    if wants_why:
        lines.append('%s: filter-only listing' % report['kind'])
        for name, why in sorted(report['quantizations']):
            lines.append('  tail %s - %s' % (name, why))
        for name, why in report['dropped']:
            lines.append('  drop %s - %s' % (name, why))
        return '\n'.join(lines)
    lines.append('## %s\n' % report['kind'].capitalize())
    for pick in report['picks']:
        flag = ' [%s]' % pick['license_flag'] if pick['license_flag'] else ''
        lines.append('- %s - %s (licence %s%s, %s downloads, %s likes)' % (
            pick['id'], pick['why'], pick['license'], flag,
            pick['downloads'], pick['likes']))
    if not report['picks']:
        lines.append('- (no survivors)')
    if report['quantizations']:
        lines.append('\n### Quantizations')
        for name, why in sorted(report['quantizations']):
            lines.append('- %s - %s' % (name, why))
    if report['dropped']:
        lines.append('\n### Dropped')
        for name, why in report['dropped']:
            lines.append('- %s - %s' % (name, why))
    return '\n'.join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('path', nargs='?', help='saved JSON array from the Hub API')
    parser.add_argument('--kind', default='models',
                        choices=('models', 'datasets', 'spaces'))
    parser.add_argument('--json', action='store_true',
                        help='print the picks as JSON instead of prose')
    parser.add_argument('--why', action='store_true',
                        help='filter-only listing: tails and drops, no picks')
    parser.add_argument('--self-test', action='store_true',
                        help='run the checks in self_test.py and exit')
    args = parser.parse_args(argv)

    if args.self_test:
        here = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, here)
        import self_test
        return self_test.main()

    if not args.path:
        parser.error('a JSON file is required unless --self-test is given')
    try:
        with open(args.path, 'r', encoding='utf-8') as handle:
            payload = json.load(handle)
    except OSError as exc:
        print('cannot read %s: %s' % (args.path, exc))
        return 2
    except ValueError as exc:
        print('not JSON: %s: %s' % (args.path, exc))
        return 2
    if not isinstance(payload, list):
        print('expected a JSON array of repo objects')
        return 2

    report = rank(payload, args.kind)
    if args.json:
        print(json.dumps(report['picks'], indent=2))
    else:
        print(render(report, wants_why=args.why))
    return 0


if __name__ == '__main__':
    sys.exit(main())
