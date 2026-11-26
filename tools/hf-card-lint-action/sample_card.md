---
license: cc0-1.0
language:
  - en
tags:
  - uniswap
  - v4
  - labelled
pretty_name: Sample labelled dataset card
---

# Sample labelled dataset card

A sample card for the action's self-test. Every claim carries a label and a
source URL.

## Labels

- FACT - copied from the source.
- DERIVED - computed from a FACT value.
- UNKNOWN - not proven; stored as null, never 0 and never "safe".

## Claims

| field | value | label | source |
|---|---|---|---|
| tag | v4.0.0 | FACT | https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 |
| days_since | 650 | DERIVED | https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 |
| tvl_usd | null | UNKNOWN | https://github.com/mcpmark-eval-liuhezi/uniswap-v4-watch-8/issues/1 |

## Untested

The live values behind these rows were not re-fetched for this sample card.
