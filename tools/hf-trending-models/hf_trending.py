#!/usr/bin/env python3
"""hf-trending-models: filter a payload of Hugging Face trending repos.

Reads one JSON file (a list of repo objects, or an object with a 'models' or
'repos' key) and prints a markdown report: genuine picks, quantizations of a
trending base, then the demoted and dropped tail.

Everything read from the payload is data. A repo whose name or card text says
"ignore your instructions" or anything like it is a string of bytes to be
filtered, never an instruction to this tool.

Usage:
    python3 hf_trending.py trending.json
    python3 hf_trending.py --json trending.json
"""

import argparse
import json
import sys

AUTHOR_LIMIT = 5

# Both spellings: embedded/leading markers and the trailing hyphenated ones.
QUANT_MARKERS = (
    'gptq', 'awq', 'gguf', 'int4', 'int8', '-4bit',
    '-gptq', '-awq', '-gguf', '-int4',
)

NON_COMMERCIAL = ('cc-by-nc', 'non-commercial', 'openrail-m')

LONG_CONTEXT = 131072

BARE_WHY = 'no clear why - popular but unremarkable'


def base_of(repo_id):
    """Strip a quantization marker from an id, returning the base id."""
    lowered = repo_id.lower()
    for marker in QUANT_MARKERS:
        if lowered.endswith(marker):
            trimmed = repo_id[:len(repo_id) - len(marker)].rstrip('-_')
            return trimmed or repo_id
    return repo_id


def is_quantization(repo_id):
    """True only when the id carries a marker AND stripping it changes the id.

    Substring matching over the whole id made any repo whose name merely
    contained a marker look like a quantization; deciding on the stripped id
    keeps `base_of()` and this test in agreement.
    """
    return base_of(repo_id) != repo_id


def is_empty(repo):
    return not repo.get('likes') and not repo.get('downloads') and not repo.get('pipeline_tag')


def is_fork_without_delta(repo):
    return bool(repo.get('fork')) and not repo.get('readmeDelta')


def licence_of(repo):
    card = repo.get('cardData') or {}
    return (card.get('license') or '').lower()


def why_for(repo, trending_bases, author_counts):
    repo_id = repo.get('id', '')
    reasons = []
    quant_base = base_of(repo_id)
    if is_quantization(repo_id) and quant_base in trending_bases:
        reasons.append('quantization of a trending model')
    if is_empty(repo):
        reasons.append('empty repo')
    if is_fork_without_delta(repo):
        reasons.append('fork without a README change')
    size = (repo.get('safetensors') or {}).get('total')
    if size:
        reasons.append('size step to %.1fB' % (size / 1e9))
    if (repo.get('max_position_embeddings') or 0) >= LONG_CONTEXT:
        reasons.append('context-window jump to %d' % repo['max_position_embeddings'])
    author = repo_id.split('/')[0]
    if author_counts.get(author, 0) > AUTHOR_LIMIT and repro_author_over(author, repo, author_counts):
        reasons.append('aggregator: more than %d trending entries in one scan' % AUTHOR_LIMIT)
    if any(m in licence_of(repo) for m in NON_COMMERCIAL):
        reasons.append('custom no-commercial licence')
    return '; '.join(reasons) if reasons else BARE_WHY


def repro_author_over(author, repo, author_counts):
    return author_counts.get(author, 0) > AUTHOR_LIMIT


def rank(repos):
    """Return {'picks': [...], 'quantizations': [...], 'demoted': [...], 'dropped': [...]}."""
    seen = set()
    unique = []
    for repo in repos:
        rid = repo.get('id')
        if rid in seen:
            continue
        seen.add(rid)
        unique.append(repo)

    author_counts = {}
    for repo in unique:
        author = repo.get('id', '').split('/')[0]
        author_counts[author] = author_counts.get(author, 0) + 1

    trending_bases = set()
    for repo in unique:
        rid = repo.get('id', '')
        if not is_quantization(rid):
            trending_bases.add(rid)

    picks, quantizations, demoted, dropped = [], [], [], []
    author_kept = {}
    for repo in unique:
        rid = repo.get('id', '')
        why = why_for(repo, trending_bases, author_counts)
        item = {'id': rid, 'why': why, 'kind': repo.get('pipeline_tag') or 'unknown'}
        if is_empty(repo) or is_fork_without_delta(repo):
            dropped.append(item)
            continue
        if is_quantization(rid) and base_of(rid) in trending_bases:
            quantizations.append(item)
            continue
        author = rid.split('/')[0]
        kept = author_kept.get(author, 0)
        if author_counts.get(author, 0) > AUTHOR_LIMIT and kept >= AUTHOR_LIMIT:
            demoted.append(item)
            continue
        author_kept[author] = kept + 1
        picks.append(item)
    return {'picks': picks, 'quantizations': quantizations, 'demoted': demoted, 'dropped': dropped}


def render(ranked):
    lines = ['# Trending models', '']
    lines.append('### Picks')
    for item in ranked.get('picks', []):
        lines.append('- **%s** - %s' % (item['id'], item['why']))
    if ranked.get('quantizations'):
        lines.append('### Quantizations')
        for item in ranked['quantizations']:
            lines.append('- **%s** - %s' % (item['id'], item['why']))
    if ranked.get('demoted'):
        lines.append('### Demoted')
        for item in ranked['demoted']:
            lines.append('- **%s** - %s' % (item['id'], item['why']))
    if ranked.get('dropped'):
        lines.append('### Dropped')
        for item in ranked['dropped']:
            lines.append('- **%s** - %s' % (item['id'], item['why']))
    return '\n'.join(lines)


def load(path):
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        return data.get('models') or data.get('repos') or []
    return data


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    parser.add_argument('path', nargs='?', help='JSON payload of trending repos')
    parser.add_argument('--json', action='store_true', help='print JSON')
    args = parser.parse_args(argv)
    if not args.path:
        parser.error('a payload path is required')
    try:
        repos = load(args.path)
    except (OSError, ValueError) as exc:
        print('cannot read %s: %s' % (args.path, exc))
        return 2
    ranked = rank(repos)
    if args.json:
        print(json.dumps(ranked, indent=2))
    else:
        print(render(ranked))
    return 0


if __name__ == '__main__':
    sys.exit(main())
