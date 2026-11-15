# Self-test of hf-trending-models

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-15T01:06:55Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43661497415

What it printed (what failed first, then its last lines):

~~~
FAIL unexpected survivors: acme/aurora-7b, acme/aurora-7b-gptq, arcturus/aurora-7b-awq, beta/nebula-13b, fleet/a1, fleet/a2, fleet/a3, fleet/a4, fleet/a5, epsilon/longctx-8b
FAIL acme/aurora-7b-gptq was not demoted; tail=[{'id': 'acme/aurora-7b-gptq', 'why': 'quantization of a trending model; size step to 7.2B', 'kind': 'text-generation'}]
FAIL arcturus/aurora-7b-awq why contains 'quantization of 
PASS fleet/a4 has a why line
PASS fleet/a5 has a why line
PASS fleet/a6 has a why line
PASS epsilon/longctx-8b has a why line
PASS render missing ### Quantizations
PASS a bare entry keeps the plain why line
PASS AUTHOR_LIMIT is 5
self_test: 34 check(s), 9 failed
~~~
