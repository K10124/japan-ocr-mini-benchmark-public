from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
from pathlib import Path
from typing import Any


DATASET_VERSION = "v0.2.0"
PREDICTION_SCHEMA_VERSION = "jomb-baseline-prediction-v1"


PROMPT_TEXT = """You are extracting structured data from a synthetic Japanese receipt image.

Return JSON only. Do not wrap the JSON in Markdown.

Use this JSON shape:

{
  "schema_version": "jomb-baseline-prediction-v1",
  "dataset_version": "v0.2.0",
  "model_id": "<model-id>",
  "document_id": "<document-id>",
  "input_image": "<relative-image-path>",
  "prediction": {
    "store_name": null,
    "store_branch_name": null,
    "store_address": null,
    "date": null,
    "time": null,
    "items": [
      {
        "name": null,
        "quantity": null,
        "unit_price": null,
        "amount": null
      }
    ],
    "subtotal": null,
    "coupon_discount": null,
    "points_used": null,
    "points_earned": null,
    "point_balance": null,
    "tax_8_target": null,
    "tax_10_target": null,
    "tax_8_inner_tax": null,
    "tax_10_inner_tax": null,
    "reduced_tax_target": null,
    "standard_tax_target": null,
    "tax_total": null,
    "total": null,
    "payment_method": null,
    "cash_received": null,
    "change": null,
    "invoice_registration_number": null
  }
}

Rules:

- Use integers for money, quantities, unit prices, point counts, and tax fields when visible.
- Use null when a field is not visible or not applicable.
- Keep item order as it appears on the receipt.
- Do not infer hidden fields from arithmetic unless the field is explicitly visible.
- Preserve Japanese text as seen in the image.
"""


README_TEMPLATE = """# v0.2.0 Baseline Run Pack

- dataset_version: `{dataset_version}`
- created_at: `{created_at}`
- data_root: `{data_root}`
- model_id: `{model_id}`

## Files

- `image_manifest.csv`: image paths and expected output paths.
- `prompts/v020_receipt_extraction_prompt.md`: shared extraction prompt.
- `prediction_templates/`: one JSON template per document.
- `predictions/{model_id}/`: place completed model outputs here.

## Run Evaluation

```powershell
python ..\\..\\examples\\evaluate_v020_baseline.py `
  --data-root "{data_root}" `
  --prediction-dir ".\\predictions\\{model_id}" `
  --output-dir ".\\evaluation\\{model_id}"
```
"""


def project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def default_data_root_candidates() -> list[Path]:
    project_root = project_root_from_script()
    cwd = Path.cwd()
    desktop = project_root.parent
    return [
        cwd / "release_v0.2.0" / "data" / "v0.2.0",
        cwd / "data" / "v0.2.0",
        desktop / "japan-ocr-mini-benchmark-public" / "release_v0.2.0" / "data" / "v0.2.0",
        desktop / "hf_dataset_upload" / "data" / "v0.2.0",
    ]


def infer_data_root() -> Path:
    for candidate in default_data_root_candidates():
        if (candidate / "manifest.jsonl").exists():
            return candidate
    searched = "\n".join(f"  - {candidate}" for candidate in default_data_root_candidates())
    raise FileNotFoundError(
        "Could not find manifest.jsonl automatically. Pass --data-root.\n"
        f"Searched:\n{searched}"
    )


def read_manifest(data_root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with (data_root / "manifest.jsonl").open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def prediction_template(row: dict[str, Any], model_id: str) -> dict[str, Any]:
    return {
        "schema_version": PREDICTION_SCHEMA_VERSION,
        "dataset_version": DATASET_VERSION,
        "model_id": model_id,
        "document_id": row["document_id"],
        "input_image": row["noisy_image"],
        "created_at": None,
        "prediction": {
            "store_name": None,
            "store_branch_name": None,
            "store_address": None,
            "date": None,
            "time": None,
            "items": [],
            "subtotal": None,
            "coupon_discount": None,
            "points_used": None,
            "points_earned": None,
            "point_balance": None,
            "tax_8_target": None,
            "tax_10_target": None,
            "tax_8_inner_tax": None,
            "tax_10_inner_tax": None,
            "reduced_tax_target": None,
            "standard_tax_target": None,
            "tax_total": None,
            "total": None,
            "payment_method": None,
            "cash_received": None,
            "change": None,
            "invoice_registration_number": None,
        },
    }


def write_image_manifest(path: Path, data_root: Path, rows: list[dict[str, Any]], model_id: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "document_id",
                "template_id",
                "noisy_profile",
                "image_path",
                "prediction_template",
                "prediction_output",
            ],
        )
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    "document_id": row["document_id"],
                    "template_id": row["template_id"],
                    "noisy_profile": row["noisy_profile"],
                    "image_path": str((data_root / row["noisy_image"]).resolve()),
                    "prediction_template": f"prediction_templates/{row['document_id']}.json",
                    "prediction_output": f"predictions/{model_id}/{row['document_id']}.json",
                }
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a v0.2.0 baseline model run pack.")
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument("--model-id", default="manual_model")
    parser.add_argument("--output-dir", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_root = args.data_root.resolve() if args.data_root else infer_data_root().resolve()
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = (
        args.output_dir
        or Path("05_generation") / "baseline_runs" / f"v020_baseline_{args.model_id}_{timestamp}"
    ).resolve()
    rows = read_manifest(data_root)

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "prompts").mkdir(parents=True, exist_ok=True)
    (output_dir / "prediction_templates").mkdir(parents=True, exist_ok=True)
    (output_dir / "predictions" / args.model_id).mkdir(parents=True, exist_ok=True)

    (output_dir / "prompts" / "v020_receipt_extraction_prompt.md").write_text(
        PROMPT_TEXT,
        encoding="utf-8",
        newline="\n",
    )
    for row in rows:
        write_json(
            output_dir / "prediction_templates" / f"{row['document_id']}.json",
            prediction_template(row, args.model_id),
        )
    write_image_manifest(output_dir / "image_manifest.csv", data_root, rows, args.model_id)
    (output_dir / "README.md").write_text(
        README_TEMPLATE.format(
            dataset_version=DATASET_VERSION,
            created_at=dt.datetime.now(dt.timezone.utc).isoformat(),
            data_root=data_root,
            model_id=args.model_id,
        ),
        encoding="utf-8",
        newline="\n",
    )

    print(f"OUTPUT_DIR: {output_dir}")
    print(f"RECORDS: {len(rows)}")
    print(f"PROMPT: {output_dir / 'prompts' / 'v020_receipt_extraction_prompt.md'}")
    print(f"IMAGE_MANIFEST: {output_dir / 'image_manifest.csv'}")
    print(f"PREDICTION_DIR: {output_dir / 'predictions' / args.model_id}")
    print("STATUS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
