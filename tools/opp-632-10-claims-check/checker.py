#!/usr/bin/env python3
"""Claims-trace checker for opp-632-10. Stdlib only, no network.
Records each claim and whether its cited traces support it.
Rule (recomputed, not trusted): 0 valid traces -> unsupported,
1 valid trace -> partial, 2+ valid traces -> supported.
Usage: python3 checker.py [--json]  # checks embedded sample
       python3 checker.py <dir> [--json]  # dir holds claims.json+evidence.json
Untested in the step that wrote this file (not executed there).
"""
import json
import sys
from pathlib import Path

VERDICTS = ('supported', 'partial', 'unsupported')
SAMPLE_EVIDENCE = [
    {'id': 'e1', 'title': 'Issue 134 attribution-docs-check-fixtures verify command', 'url': 'https://github.com/HivemindOS-Agents/bee-scouts/issues/134'},
    {'id': 'e2', 'title': 'Hugging Face share a dataset to the Hub docs', 'url': 'https://huggingface.co/docs/datasets/upload_dataset'},
    {'id': 'e3', 'title': 'Issue 60 checker run matching card to branch fixtures', 'url': 'https://github.com/LiamVisionary/bee-scouts/issues/60'},
    {'id': 'e4', 'title': 'Issue 87 run-lines expected self-test exit code on card', 'url': 'https://github.com/HivemindOS-Agents/bee-scouts/issues/87'},
    {'id': 'e5', 'title': 'Issue 115 standalone self_test run recorded in SELFTEST_OUTPUT', 'url': 'https://github.com/HivemindOS-Agents/bee-scouts/issues/115'},
    {'id': 'e6', 'title': 'bee-scouts commits API page read in follow-up', 'url': 'https://api.github.com/repos/HivemindOS-Agents/bee-scouts/commits?per_page=50'},
]
SAMPLE_CLAIMS = [
    {'id': 'c1', 'claim': 'Attribution proposals for an exact verify command and CC0 were closed as duplicate or not planned', 'traces': ['e1', 'e2'], 'verdict': 'supported'},
    {'id': 'c2', 'claim': 'Follow-up asked for a checker run matching the card to the branch fixtures came from', 'traces': ['e3', 'e4'], 'verdict': 'supported'},
    {'id': 'c3', 'claim': 'The standalone self-test pattern applies to card-fixtures-checker', 'traces': ['e5'], 'verdict': 'partial'},
    {'id': 'c4', 'claim': 'A claim in the discussion with no cited trace at all', 'traces': [], 'verdict': 'unsupported'},
    {'id': 'c5', 'claim': 'The follow-up research read recent bee-scouts commit pages', 'traces': ['e1', 'e3', 'e6'], 'verdict': 'supported'},
]


def recompute(valid_count):
    if valid_count <= 0:
        return 'unsupported'
    if valid_count == 1:
        return 'partial'
    return 'supported'


def check_package(claims, evidence):
    findings = []
    ev_ids = set()
    for ev in evidence:
        eid = ev.get('id', '')
        if not eid:
            findings.append('evidence:empty-id')
        elif eid in ev_ids:
            findings.append('evidence:duplicate-id:' + eid)
        ev_ids.add(eid)
        url = ev.get('url', '')
        if not (url.startswith('https://') or url.startswith('http://')):
            findings.append('evidence:bad-url:' + (eid or '?'))
        if not (ev.get('title') or '').strip():
            findings.append('evidence:empty-title:' + (eid or '?'))
    seen = set()
    records = []
    for c in claims:
        cid = c.get('id', '')
        if not cid:
            findings.append('claim:empty-id')
            cid = '?'
        elif cid in seen:
            findings.append('claim:duplicate-id:' + cid)
        seen.add(cid)
        if not (c.get('claim') or '').strip():
            findings.append('claim:empty-claim:' + cid)
        declared = c.get('verdict', '')
        if declared not in VERDICTS:
            findings.append('claim:bad-verdict:' + cid)
        traces = c.get('traces', [])
        if not isinstance(traces, list):
            findings.append('claim:traces-not-list:' + cid)
            traces = []
        valid = []
        for t in traces:
            if t in ev_ids:
                valid.append(t)
            else:
                findings.append('claim:missing-trace:%s:%s' % (cid, t))
        expected = recompute(len(valid))
        if declared in VERDICTS and declared != expected:
            findings.append('claim:verdict-mismatch:%s:declared=%s:recomputed=%s' % (cid, declared, expected))
        records.append({'id': cid, 'claim': c.get('claim', ''), 'traces': list(traces), 'valid_traces': valid, 'declared': declared, 'recomputed': expected})
    return records, findings


def load_package(directory):
    d = Path(directory)
    claims = json.loads((d / 'claims.json').read_text(encoding='utf-8'))
    evidence = json.loads((d / 'evidence.json').read_text(encoding='utf-8'))
    if not isinstance(claims, list) or not isinstance(evidence, list):
        raise ValueError('claims.json and evidence.json must each hold a JSON list')
    return claims, evidence


def evaluate(claims, evidence):
    records, findings = check_package(claims, evidence)
    return {'records': records, 'findings': findings, 'ok': not findings, 'claims': len(claims), 'evidence': len(evidence)}


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    as_json = '--json' in args
    dirs = [a for a in args if a != '--json']
    try:
        claims, evidence = load_package(dirs[0]) if dirs else (SAMPLE_CLAIMS, SAMPLE_EVIDENCE)
        out = evaluate(claims, evidence)
    except Exception as exc:
        print('checker: %s: %s' % (type(exc).__name__, exc))
        print('RESULT=fail')
        print('EXIT=1')
        return 1
    if as_json:
        print(json.dumps(out, indent=2, sort_keys=True))
    else:
        for r in out['records']:
            print('%s traces=%d declared=%s recomputed=%s' % (r['id'], len(r['valid_traces']), r['declared'], r['recomputed']))
        for f in out['findings']:
            print('FINDING ' + f)
        print('claims=%d evidence=%d findings=%d' % (out['claims'], out['evidence'], len(out['findings'])))
    print('RESULT=' + ('pass' if out['ok'] else 'fail'))
    print('EXIT=' + ('0' if out['ok'] else '1'))
    return 0 if out['ok'] else 1


if __name__ == '__main__':
    sys.exit(main())
