# Submit or Compare Model Results

This project is small enough to let you run a model locally and compare it against the official v0.3.0 baselines.

## Required Prediction Layout

Create one prediction JSON per `document_id` in `manifest.jsonl`.

```text
model_outputs/my-model/
  receipt_v020_supermarket_001.json
  receipt_v020_supermarket_002.json
  ...
```

Each JSON should follow the schema described in `docs/evaluation/baseline_prediction_schema.md`.

## Evaluate One Model

```powershell
python examples/evaluate_v020_baseline.py --data-root "..\hf_dataset_upload\data\v0.2.0" --prediction-dir ".\model_outputs\my-model"
```

The evaluator writes:

```text
baseline_summary.json
baseline_summary.md
baseline_record_scores.jsonl
baseline_field_diffs.csv
```

`baseline_summary.json` includes `jomb_core_score_v1` and `jomb_core_score_v1.points`.

## Compare Multiple Runs

```powershell
python examples/compare_v020_baselines.py `
  --report ".\runs\model-a\baseline_summary.json" `
  --report ".\runs\model-b\baseline_summary.json" `
  --output-dir ".\runs\comparison"
```

The comparison output is ranked by `JOMB Core Score v1`.

## What to Report

When adding a model to the leaderboard, include:

- model display name
- exact LM Studio or runtime model ID
- format and quantization
- mmproj quantization if applicable
- prompt version
- runtime and device
- `baseline_summary.json`
- average seconds per record

Do not compare runs that use different data roots, different image variants, or hand-corrected predictions.
