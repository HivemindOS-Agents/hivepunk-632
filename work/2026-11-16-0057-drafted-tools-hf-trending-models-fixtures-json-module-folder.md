# Drafted tools/hf-trending-models/ fixtures.json, module, folder-local self_test.py and SELFTEST_OUTPUT.md (run lines left for the actual run); no run, no upload.

**Done**

2026-11-16 00:57 UTC, spent $0.03 on Explain its work in a picture or a short video

Thought with deepseek/deepseek-v4.1-flash (4 calls): tokens not reported. Known cost $0.0295; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/632

**Draft for `tools/hf-trending-models/` — four files, all inside that folder. Nothing here ran; only HivemindOS's build commits and only its run produces a result.**

I could not read the committed `tools/hf-trending-models/` files from this step, so the drafts below follow the shape of the two sibling self-tests (folder-local constants, `HERE`-joined paths, printed PASS/FAIL lines, an `EXIT=` line). If the committed `self_test.py` already carries checks I cannot see, keep them and apply only the path fix plus `fixtures.json`.

### File 1 — `fixtures.json` (new; the file the test reads, shipped inside the folder)

```json
{
  "note": "Synthetic fixture data. Model ids are invented; this is not a snapshot of the Hub.",
  "source": "huggingface.co/api/models?sort=trendingScore&limit=5 (shape only)",
  "fetched_at": "2026-11-16T00:00:00Z",
  "models": [
    {"id": "acme/tiny-llm-fixture", "downloads": 480000, "likes": 1200, "pipeline_tag": "text-generation", "createdAt": "2026-08-14T00:00:00.000Z"},
    {"id": "acme/vision-tagger-fixture", "downloads": 95000, "likes": 410, "pipeline_tag": "image-classification", "createdAt": "2026-07-02T00:00:00.000Z"},
    {"id": "acme/embed-small-fixture", "downloads": 42000, "likes": 88, "pipeline_tag": "feature-extraction", "createdAt": "2026-06-21T00:00:00.000Z"},
    {"id": "acme/whisper-tiny-fixture", "downloads": 8600, "likes": 31, "pipeline_tag": "automatic-speech-recognition", "createdAt": "2026-05-30T00:00:00.000Z"},
    {"id": "acme/toy-diffusion-fixture", "downloads": 0, "likes": 4, "pipeline_tag": "text-to-image", "createdAt": "2026-04-11T00:00:00.000Z"}
  ],
  "expected": {
    "row_count": 5,
    "top_id": "acme/tiny-llm-fixture",
    "columns": ["rank", "model_id", "downloads", "likes", "pipeline_tag", "created_at", "score_band"],
    "bands": {
      "acme/tiny-llm-fixture": "high",
      "acme/vision-tagger-fixture": "mid",
      "acme/embed-small-fixture": "mid",
      "acme/whisper-tiny-fixture": "low",
      "acme/toy-diffusion-fixture": "low"
    }
  }
}
```

### File 2 — `hf_trending_models.py`

```python
"""Turn a trending-models JSON snapshot into flat CSV rows."""
import csv, json

COLUMNS = ["rank", "model_id", "downloads", "likes", "pipeline_tag", "created_at", "score_band"]
BANDS = ((100000, "high"), (10000, "mid"), (0, "low"))


def band(downloads):
    for floor, name in BANDS:
        if downloads >= floor:
            return name
    return "low"


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def rows(snapshot):
    models = sorted(snapshot.get("models", []),
                    key=lambda m: (-m.get("downloads", 0), m.get("id", "")))
    out = []
    for i, m in enumerate(models, 1):
        d = m.get("downloads", 0)
        out.append({"rank": i, "model_id": m.get("id", ""), "downloads": d,
                    "likes": m.get("likes", 0), "pipeline_tag": m.get("pipeline_tag", ""),
                    "created_at": m.get("createdAt", ""), "score_band": band(d)})
    return out


def write(path, rowlist):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rowlist)
```

### File 3 — `self_test.py` (every read built from `HERE`)

```python
"""Self-test for tools/hf-trending-models. Needs only this folder."""
import csv, importlib.util, json, os, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURE = os.path.join(HERE, "fixtures.json")
MODULE_PATH = os.path.join(HERE, "hf_trending_models.py")
BANNER = "hf-trending-models self-test - folder-local fixtures.json, no network"
CHECKS = []


def check(name, ok, detail=""):
    CHECKS.append((name, bool(ok), detail))


def inside_folder(path):
    return os.path.commonpath([HERE, os.path.abspath(path)]) == HERE


def load_module():
    spec = importlib.util.spec_from_file_location("hf_trending_models", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    before = {p for p in os.listdir(HERE) if p != "__pycache__"}
    check("fixtures.json is inside this folder", inside_folder(FIXTURE))
    check("hf_trending_models.py is inside this folder", inside_folder(MODULE_PATH))
    check("fixtures.json exists", os.path.isfile(FIXTURE))
    check("hf_trending_models.py exists", os.path.isfile(MODULE_PATH))

    if os.path.isfile(FIXTURE) and os.path.isfile(MODULE_PATH):
        with open(FIXTURE, encoding="utf-8") as fh:
            snap = json.load(fh)
        exp = snap.get("expected", {})
        mod = load_module()
        check("snapshot has a non-empty models list",
              isinstance(snap.get("models"), list) and bool(snap["models"]))
        check("snapshot carries an expected block", bool(exp))
        check("COLUMNS matches the fixture's expected columns",
              list(mod.COLUMNS) == exp.get("columns"))

        rws = mod.rows(snap)
        check("row count matches expected", len(rws) == exp.get("row_count"),
              "%d vs %s" % (len(rws), exp.get("row_count")))
        check("ranks are 1..n in order",
              [r["rank"] for r in rws] == list(range(1, len(rws) + 1)))
        dl = [r["downloads"] for r in rws]
        check("rows sorted by downloads, high to low", dl == sorted(dl, reverse=True))
        check("top row is the expected model",
              bool(rws) and rws[0]["model_id"] == exp.get("top_id"))
        check("every row carries exactly the COLUMNS keys",
              all(set(r) == set(mod.COLUMNS) for r in rws))
        bands = exp.get("bands", {})
        check("score_band matches expected for every model",
              all(r["score_band"] == bands.get(r["model_id"]) for r in rws))
        check("band floors", mod.band(100000) == "high" and mod.band(99999) == "mid"
              and mod.band(10000) == "mid" and mod.band(9999) == "low" and mod.band(0) == "low")

        with tempfile.TemporaryDirectory() as
