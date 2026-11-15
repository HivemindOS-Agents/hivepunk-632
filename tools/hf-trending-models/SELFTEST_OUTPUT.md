# Self-test of hf-trending-models

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T01:40:41Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43664185945

What it printed (what failed first, then its last lines):

~~~
FAIL arcturus/aurora-7b-awq why contains 'quantization of a trending model': got 'no clear why - popular but unremarkable'
FAIL fleet/a2 why contains 'no clear why - popular but unremarkable': got 'aggregator: more than 5 trending entries in one scan'
FAIL fleet/a3 why contains 'no clear why - popular but unremarkable': got 'aggregator: more than 5 trending entries in one scan'
FAIL fleet/a4 why c
PASS render has '### Demoted' exactly when demoted is non-empty
PASS render has '### Dropped' exactly when dropped is non-empty
PASS bare entry acme/aurora-7b keeps the plain why line
PASS bare entry fleet/a2 keeps the plain why line
PASS bare entry fleet/a3 keeps the plain why line
PASS bare entry fleet/a4 keeps the plain why line
PASS bare entry fleet/a5 keeps the plain why line
self_test: 32 check(s), 5 failed
~~~
