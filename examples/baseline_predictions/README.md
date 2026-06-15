# Baseline Prediction Examples

Place model output JSON files in one directory per model, for example:

```text
model_outputs/my-model/
  receipt_v020_bakery_001.json
  receipt_v020_bakery_002.json
```

Then run:

```powershell
python .\examples\evaluate_v020_baseline.py --data-root "..\hf_dataset_upload\data\v0.2.0" --prediction-dir ".\model_outputs\my-model"
```

See `docs/evaluation/baseline_prediction_schema.md` for the recommended JSON
schema.
