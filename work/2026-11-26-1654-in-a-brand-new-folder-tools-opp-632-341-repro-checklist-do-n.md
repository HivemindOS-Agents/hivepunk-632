# In a brand-new folder tools/opp-632-341-repro-checklist/ (do not touch tools/hf-dataset-card-lint/, tools/hf-card-lint-action/, or any existing folder), build the opp-632-341 reproduction checklist: checklist.md with numbered steps for the Windows Open Design 0.27.1 window disappearing when Claude Code connects via MCP, each step giving observed vs expected with FACT/UNKNOWN labels and a source anchor (issue https://github.com/nexu-io/open-design/issues/9552), UNKNOWN never 0 or "safe"; checklist.py validator; a real folder-local self_test.py passing alone with no network; README.md with usage and what is untested.

**Draft: nothing was committed under tools/**

2026-11-26 16:54 UTC, spent $0.06 on Build a small tool in its own repository

Thought with meta/muse-ember, deepseek/deepseek-v4.1-flash, anthropic/claude-sonnet-5.5 (4 calls, 1 retry): tokens not reported. Known cost $0.0581; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/632

```json
{
  "id": "hmos_completion_439bfbab7f4b5527314584d1d92b6c74",
  "object": "chat.completion",
  "created": 1795712085,
  "model": "deepseek/deepseek-v4.1-flash",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "length",
      "message": {
        "role": "assistant",
        "content": "{\n  \"path\": \"tools/opp-632-341-repro-checklist/checklist.md\",\n  \"content\": \"# OPP-632-341 Reproduction Checklist — Windows Open Design 0.27.1 window disappearing after Claude Code MCP connect\\n\\nIssue anchor: https://github.com/nexu-io/open-design/issues/9552\\n\\nPurpose: reproduce and bound the bug where the Open Design 0.27.1 window disappears on Windows when Claude Code connects via MCP. Use FACT for something directly observed in the referenced environment/run, and UNKNOWN for something not yet established. UNKNOWN values must never be `0`, `safe`, or empty.\\n\\n1. Record the Windows and Open Design build context before launching the app.\\n  ",
        "refusal": null,
        "reasoning_details": [
          {
            "type": "reasoning.text",
            "text": "We need answer user asks build folder tools/opp-632-341-repro-checklist/ contents for four files. Need provide complete ready-to-write contents. We need not actually touch repo. Need ensure files contents. Need design checklist.md, checklist.py, self_test.py, README.md. Need satisfy constraints.\n\nWe need think carefully. Need create checklist with numbered steps for Windows Open Design 0.27.1 window disappearing when Claude Code connects via MCP. Each step gives observed vs expected with FACT/UNKNOWN labels and a source anchor (issue URL). UNKNOWN never 0 or \"safe\". Need validator checks rules: numbered steps present, observed vs expected present, FACT/UNKNOWN labels, source anchor URL on each step, UNKNOWN never 0 or \"safe\" or empty.\n\nSelf_test.py passing alone no network no args, imports checklist.py, verifying shipped checklist.md passes and broken variants fail.\n\nREADME usage and what is untested.\n\nNeed likely use Markdown format for checklist. Need decide schema for validator. Must ensure self_test works. Need be robust.\n\nWe need craft checklist.md with numbered steps. Each step needs observed vs expected with FACT/UNKNOWN labels. Source anchor URL on each step. Issue URL https://github.com/nexu-io/open-design/issues/9552. Need \"UNKNOWN never 0 or 'safe'\". Hmm wording: \"UNKNOWN never 0 or 'safe'\" likely means when a value is UNKNOWN, it cannot be 0 or \"safe\" as if known safe. We need ensure validator rejects UNKNOWN with value 0 or safe. But checklist steps need include observed/expected with labels. We can include status lines: Observed: FACT/UNKNOWN — ... Expected: FACT/UNKNOWN — ... Need each step contains source anchor. Need \"UNKNOWN never 0 or 'safe'\" and \"or empty\".\n\nCould create a strict line format:\n- Step 1. ...\n  - Observed: FACT: ...\n  - Expected: UNKNOWN: Need to confirm ... (not 0/safe)\n  - Source: https://github.com/nexu-io/open-design/issues/9552\n\nBut requirement: \"each step giving observed vs expected with FACT/UNKNOWN labels and a source anchor\". So each step can be numbered list item, with sub-bullets for Observed/Expected/Source. \"UNKNOWN never 0 or 'safe'.\" We can make sure any UNKNOWN line has non-empty and not 0, not safe. We can include UNKNOWN in checklist: e.g., \"UNKNOWN: Root cause likely in MCP handshake...\" Wait UNKNOWN must not be empty, not 0, not safe. It's okay.\n\nNeed design validator. Maybe parse checklist.md. Need checks:\n- numbered steps present. Could parse lines matching `^\\s*(\\d+)\\.\\s+` and maybe enforce sequential.\n- observed vs expected present: each step block must contain \"Observed:\" and \"Expected:\".\n- FACT/UNKNOWN labels: observed and expected lines start with `Observed: FACT` or `",
            "format": "unknown",
            "index": 0
          }
        ]
      }
    }
  ],
  "thoughtChargedCredits": 0.802
}
```
