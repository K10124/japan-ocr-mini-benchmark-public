# Model Run Workflow

This workflow prepares OCR/VLM model runs for v0.2.0 and compares finished
prediction files.

## Current Local Availability

The development environment may not include OCR or VLM runtimes. The benchmark
therefore separates model execution from evaluation:

1. Create a run pack with image paths, output templates, and a shared prompt.
2. Run a model manually or in another environment.
3. Save one prediction JSON file per receipt.
4. Run `examples/evaluate_v020_baseline.py`.
5. Aggregate multiple model reports with `examples/compare_v020_baselines.py`.

## Prepare A Run Pack

```powershell
python .\examples\prepare_v020_baseline_run_pack.py `
  --data-root "..\hf_dataset_upload\data\v0.2.0" `
  --model-id "qwen-vl-manual"
```

The run pack contains:

```text
image_manifest.csv
prompts/v020_receipt_extraction_prompt.md
prediction_templates/
predictions/<model-id>/
README.md
```

## Evaluate A Completed Model Directory

```powershell
python .\examples\evaluate_v020_baseline.py `
  --data-root "..\hf_dataset_upload\data\v0.2.0" `
  --prediction-dir ".\05_generation\baseline_runs\<run-pack>\predictions\qwen-vl-manual" `
  --output-dir ".\05_generation\generated_reports\baseline_eval_qwen_vl_manual" `
  --fail-on-missing
```

## Compare Multiple Models

```powershell
python .\examples\compare_v020_baselines.py `
  --reports-root ".\05_generation\generated_reports" `
  --output-dir ".\05_generation\generated_reports\baseline_comparison_latest"
```

This writes:

```text
baseline_comparison_summary.json
baseline_comparison_summary.csv
baseline_comparison_summary.md
```

## Recommended First Real Baselines

- `qwen-vl-*`: strong VLM baseline if a local or cloud runtime is available.
- `internvl-*`: second VLM baseline for structured extraction comparison.
- `paddleocr-*`: OCR-specialized baseline, useful even if structured JSON is
  created by a post-processing step.

Do not compare model scores unless the prompt, image variant, prediction schema,
and dataset version are recorded.
