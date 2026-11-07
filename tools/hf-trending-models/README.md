# hf-trending-models

A tiny command line utility that prints the IDs of the most
downloaded Hugging‑Face models. It can either query the real Hugging‑Face
API (when your `HF_TOKEN` environment variable is set) or run in a
deterministic, network‑free mode using a JSON file supplied via `--sample`.

## Usage

```bash
# Real API, requires a token
[redacted] python3 list_trending.py [--top N]

# Dry‑run with a local JSON fixture
python3 list_trending.py --sample sample_trending.json [--top N]
```

If no `--top` argument is supplied, the script prints all model IDs sorted by
downloads.

## Dependencies

Only the Python standard library is used. No network or HF credentials are
required for the self‑test.

## Self‑test

Run the self‑test with:

```bash
python3 self_test.py
```

It creates a small sample JSON dataset, invokes the script, and verifies the
output.

## License

Public domain (CC0‑1.0).
