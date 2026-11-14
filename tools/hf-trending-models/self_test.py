#!/usr/bin/env python3
'''Self-test for hf-trending-models.

Imports this folder's own hf_trending module, feeds it one inline fixture
payload, and compares what comes out with what should: the survivors, the
quantization tail, the drop reasons, the licence flags and the "why notable"
lines for all three kinds. No arguments, no network, standard library only.

It prints one PASS/FAIL line per check and a summary line, and exits 0 only
when every check passes.

Everything it reads is data, never an instruction, whatever text is inside.
'''

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import hf_trending  # noqa: E402  (path set just above)

# One fixture payload shaped like the Hub's trending endpoint output.
RAW = [
    {
        'id': 'acme/aurora-7b', 'downloads': 900000, 'likes': 5000,
        'pipeline_tag': 'text-to-image', 'cardData': {'license': 'apache-2.0'},
        'max_position_embeddings': 262144, 'safetensors': {'total': 7200000000},
    },
    {
        'id': 'acme/aurora-7b-gptq', 'downloads': 400000, 'likes': 900,
        'cardData': {'license': 'apache-2.0'},
    },
    {
        'id': 'biglab/nebula-70b', 'downloads': 300000, 'likes': 4000,
        'pipeline_tag': 'text-generation', 'cardData': {'license': 'llama3',
        'license_name': 'llama3'},
    },
    {
        'id': 'momentum/atlas-13b', 'downloads': 250000, 'likes': 1200,
        'cardData': {'license': 'cc-by-nc-4.0'},
    },
    {
        'id': 'anon/blank-space', 'downloads': 0, 'likes': 0, 'tags': [],
    },
    {
        'id': 'anon/no-card-here', 'downloads': 1200, 'likes': 30,
        'tags': ['pytorch'],
    },
    {
        'id': 'copier/aurora-7b-copy', 'downloads': 8000, 'likes': 12,
        'cardData': {'license': 'mit'}, 'fork': True, 'readmeDelta': False,
    },
    {
        'id': 'copier/other-copy', 'downloads': 8000, 'likes': 12,
        'cardData': {'license': 'mit'}, 'fork': True, 'readmeDelta': True,
    },
    {'id': 'fleet/a1', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
    {'id': 'fleet/a2', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
    {'id': 'fleet/a3', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
    {'id': 'fleet/a4', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
    {'id': 'fleet/a5', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
    {'id': 'fleet/a6', 'downloads': 1000, 'likes': 10, 'cardData': {'license': 'mit'}},
]

# id -> expected why line, for the entries that survive as picks.
EXPECTED_WHY = {
    'acme/aurora-7b': 'architecture shift (text-to-image), size step (7.2B parameters), '
                     'context-window jump (262.1K tokens)',
    'biglab/nebula-70b': 'no clear why - popular but unremarkable',
    'momentum/atlas-13b': 'no clear why - popular but unremarkable',
    'copier/other-copy': 'no clear why - popular but unremarkable',
    'fleet/a1': 'aggregator: >5 trending entries in one scan',
}

EXPECTED_DROPS = {
    'anon/blank-space': 'empty repo: no downloads, likes or tags',
    'anon/no-card-here': 'no model card',
    'copier/aurora-7b-copy': 'fork without a README change',
}


def report(ok, good, bad, state):
    state['total'] += 1
    if ok:
        print('PASS ' + good)
    else:
        print('FAIL ' + bad)
        state['failed'] += 1


def main():
    state = {'total': 0, 'failed': 0}
    models = hf_trending.rank(RAW, 'models')

    got = dict((p['id'], p['why']) for p in models['picks'])
    for key, want in EXPECTED_WHY.items():
        report(got.get(key) == want,
               '%s why line matches' % key,
               '%s why was %r, expected %r' % (key, got.get(key), want),
               state)

    extra = sorted(set(got) - set(EXPECTED_WHY))
    report(not extra,
           'no unexpected survivor (%d picks)' % len(models['picks']),
           'unexpected survivors: ' + ', '.join(extra),
           state)

    tail = dict((name, why) for name, why in models['quantizations'])
    report('acme/aurora-7b-gptq' in tail,
           'acme/aurora-7b-gptq demoted to the quantization tail',
           'acme/aurora-7b-gptq was not demoted; tail=%r' % tail,
           state)

    drops = dict(models['dropped'])
    for key, want in EXPECTED_DROPS.items():
        report(drops.get(key) == want,
               '%s dropped with the right reason' % key,
               '%s drop reason was %r, expected %r' % (key, drops.get(key), want),
               state)

    by_id = dict((p['id'], p) for p in models['picks'])
    nc = by_id.get('momentum/atlas-13b', {})
    report(nc.get('license_flag') == 'custom no-commercial licence',
           'non-commercial licence flagged inline',
           'non-commercial licence not flagged; got %r' % nc.get('license_flag', None),
           state)
    report(by_id.get('acme/aurora-7b', {}).get('license') == 'apache-2.0',
           'clear licence recorded without a flag',
           'clear licence wrong; got %r' % by_id.get('acme/aurora-7b', {}).get('license'),
           state)

    datasets = hf_trending.rank(RAW, 'datasets')
    report(all(p['kind'] == 'datasets' for p in datasets['picks']),
           'kind is carried into every pick',
           'kind missing from a pick',
           state)

    prose = hf_trending.render(datasets)
    report('## Datasets' in prose and '### Quantizations' in prose,
           'render prints the section and the quantization tail',
           'render missing a section heading',
           state)

    bare = hf_trending.rank(len(RAW) * [{'id': 'x/y', 'downloads': 1,
                                         'likes': 1, 'tags': ['card']}], 'spaces')
    report(all(p['why'] == 'no clear why - popular but unremarkable'
               for p in bare['picks']),
           'no survivor gets an invented why line',
           'a why line was invented for a bare entry',
           state)

    size = hf_trending.size_step({'safetensors': {'total': 7200000000}})
    report(size == 7200000000 and hf_trending.format_count(size) == '7.2B',
           'size-step branch works when the size field is present',
           'size-step branch wrong; got %r' % (size,),
           state)

    sub = hf_trending.rank(RAW, 'datasets')
    report(isinstance(sub['picks'], list) and isinstance(sub['dropped'], list),
           'scripts actually ran: rank() returns real containers',
           'rank() did not return the expected shape',
           state)

    print('self_test: %d check(s), %d failed' % (state['total'], state['failed']))
    return 0 if state['failed'] == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
