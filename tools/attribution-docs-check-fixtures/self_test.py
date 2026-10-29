"""Self-test for attribution_docs_check: runs the checker over its sample fixtures (data/fixtures.jsonl) and exits 0
only when every fixture gets the verdict it expects. HivemindOS runs this after every change to the tool
(https://github.com/HivemindOS-Agents/bee-self-test); the tool is listed as finished only while it passes."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from attribution_docs_check import main  # noqa: E402

sys.exit(main(["--selftest"]))
