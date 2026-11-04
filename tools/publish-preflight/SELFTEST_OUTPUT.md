# Self-test of publish-preflight

Written by HivemindOS from the self-test runner's record after the last commit to this folder. It is replaced at every run, and a copy written by the agent is not kept.

- Result: **failed**
- Ran: 2026-11-04T08:38:25Z
- Run: https://github.com/HivemindOS-Agents/bee-self-test/actions/runs/41801035435

What it printed (what failed first, then its last lines):

~~~
Traceback (most recent call last):
  File "[redacted], line 79, in <module>
    sys.exit(main())
             ~~^^
  File "[redacted], line 64, in main
    for case, _, _ in EXPECTED:
        ^^^^^^^^^^
ValueError: too many values to unpack (expected 3)
~~~
