# Self-test of hf-trending-models

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-16T05:47:58Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/43812542599

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
             ~~^^
  File "[redacted], line 121, in main
    check(T.render([1, 2, 3]).count('why:') == 0, 'non-dict snapshot renders no why lines')
          ~~^^^^^^^^^^^
  File "[redacted], line 99, in render
    demoted = [d for d in (snapshot.get('demoted') or [])]
                           ^^^^^^^^^^^^
AttributeError: 'list' object has no attribute 'get'
~~~
