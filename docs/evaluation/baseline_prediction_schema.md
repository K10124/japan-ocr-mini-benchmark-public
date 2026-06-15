# Baseline Prediction Schema

This document defines the recommended JSON format for OCR/VLM baseline outputs
against Japan OCR Mini Benchmark v0.2.0.

The evaluator is:

```text
examples/evaluate_v020_baseline.py
```

## File Layout

Use one JSON file per receipt:

```text
model_outputs/<model_id>/
  receipt_v020_bakery_001.json
  receipt_v020_bakery_002.json
  ...
```

The file name is flexible, but each JSON file must contain `document_id`.

## Prediction File

```json
{
  "schema_version": "jomb-baseline-prediction-v1",
  "dataset_version": "v0.2.0",
  "model_id": "example-model",
  "document_id": "receipt_v020_bakery_001",
  "input_image": "images_noisy/receipt_v020_bakery_001_noisy.png",
  "created_at": "2026-06-14T00:00:00Z",
  "prediction": {
    "store_name": "...",
    "store_branch_name": "...",
    "store_address": "...",
    "date": "2026-06-11",
    "time": "09:33:42",
    "items": [
      {
        "name": "...",
        "quantity": 1,
        "unit_price": 120,
        "amount": 120
      }
    ],
    "subtotal": 1378,
    "coupon_discount": null,
    "points_used": null,
    "tax_8_target": 1260,
    "tax_10_target": 118,
    "tax_8_inner_tax": 93,
    "tax_10_inner_tax": 11,
    "total": 1378,
    "payment_method": "...",
    "cash_received": 2000,
    "change": 622
  }
}
```

The evaluator also accepts older flat JSON files where the extracted fields are
at the top level. The nested `prediction` form is preferred for new baselines.

## Evaluated Fields

Top-level text fields:

```text
store_name
store_branch_name
store_address
date
time
payment_method
invoice_registration_number
```

Top-level numeric fields:

```text
subtotal
coupon_discount
points_used
points_earned
point_balance
tax_8_target
tax_10_target
tax_8_inner_tax
tax_10_inner_tax
reduced_tax_target
standard_tax_target
tax_total
total
cash_received
change
```

Item fields are compared in receipt order:

```text
name
quantity
unit_price
amount
```

## Run Evaluation

```powershell
python .\examples\evaluate_v020_baseline.py `
  --data-root "..\hf_dataset_upload\data\v0.2.0" `
  --prediction-dir ".\model_outputs\example-model" `
  --output-dir ".\05_generation\generated_reports\baseline_eval_example"
```

Outputs:

```text
baseline_summary.json
baseline_record_scores.jsonl
baseline_field_diffs.csv
baseline_summary.md
```

The evaluator reports coverage separately from accuracy. A directory with only
some receipts can be evaluated, but missing predictions will be listed in the
summary. Use `--fail-on-missing` when all 20 predictions are required.
