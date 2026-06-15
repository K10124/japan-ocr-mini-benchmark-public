from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


DATASET_VERSION = "v0.2.0"
PREDICTION_SCHEMA_VERSION = "jomb-baseline-prediction-v1"
REPORT_SCHEMA_VERSION = "jomb-baseline-evaluation-report-v1"

TEXT_FIELDS = (
    "store_name",
    "store_branch_name",
    "store_address",
    "date",
    "time",
    "payment_method",
    "invoice_registration_number",
)

AMOUNT_FIELDS = (
    "subtotal",
    "coupon_discount",
    "points_used",
    "points_earned",
    "point_balance",
    "tax_8_target",
    "tax_10_target",
    "tax_8_inner_tax",
    "tax_10_inner_tax",
    "reduced_tax_target",
    "standard_tax_target",
    "tax_total",
    "total",
    "cash_received",
    "change",
)

ITEM_TEXT_FIELDS = ("name",)
ITEM_AMOUNT_FIELDS = ("quantity", "unit_price", "amount")


def project_root_from_script() -> Path:
    return Path(__file__).resolve().parents[1]


def default_data_root_candidates() -> list[Path]:
    project_root = project_root_from_script()
    cwd = Path.cwd()
    desktop = project_root.parent
    return [
        cwd / "release_v0.2.0" / "data" / "v0.2.0",
        cwd / "data" / "v0.2.0",
        project_root / "release_v0.2.0" / "data" / "v0.2.0",
        project_root / "data" / "v0.2.0",
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


def default_output_dir() -> Path:
    timestamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    return Path("baseline_eval_reports") / timestamp


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def read_manifest(data_root: Path) -> list[dict[str, Any]]:
    manifest_path = data_root / "manifest.jsonl"
    rows: list[dict[str, Any]] = []
    with manifest_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            if "document_id" not in row or "source_json" not in row:
                raise ValueError(f"{manifest_path}:{line_number} missing document_id/source_json")
            rows.append(row)
    return rows


def normalize_text(value: Any) -> str | None:
    if value is None:
        return None
    text = unicodedata.normalize("NFKC", str(value))
    return re.sub(r"\s+", "", text)


def normalize_amount(value: Any) -> int | str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    text = unicodedata.normalize("NFKC", str(value))
    for token in ("¥", "￥", "円", ",", "P", "pt"):
        text = text.replace(token, "")
    text = re.sub(r"\s+", "", text)
    try:
        return int(text)
    except ValueError:
        return text


def load_prediction_file(path: Path) -> tuple[str, dict[str, Any], dict[str, Any]]:
    data = read_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"{path}: prediction file must be a JSON object")

    document_id = data.get("document_id")
    prediction = data.get("prediction")

    if isinstance(prediction, dict):
        meta = {key: value for key, value in data.items() if key != "prediction"}
    else:
        prediction = data
        meta = {"schema_version": "legacy-flat-json"}
        document_id = data.get("document_id") or path.stem.replace("_prediction", "")

    if not isinstance(document_id, str) or not document_id:
        raise ValueError(f"{path}: missing document_id")
    if not isinstance(prediction, dict):
        raise ValueError(f"{path}: prediction must be a JSON object")

    return document_id, meta, prediction


def load_predictions(prediction_dir: Path) -> tuple[dict[str, dict[str, Any]], list[str]]:
    errors: list[str] = []
    predictions: dict[str, dict[str, Any]] = {}
    for path in sorted(prediction_dir.rglob("*.json")):
        try:
            document_id, meta, prediction = load_prediction_file(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if document_id in predictions:
            errors.append(f"duplicate prediction for {document_id}: {path}")
            continue
        predictions[document_id] = {
            "path": str(path),
            "meta": meta,
            "prediction": prediction,
        }
    return predictions, errors


def compare_field(
    document_id: str,
    area: str,
    field: str,
    index: int | None,
    expected: Any,
    predicted: Any,
    field_type: str,
) -> dict[str, Any]:
    if field_type == "amount":
        expected_norm = normalize_amount(expected)
        predicted_norm = normalize_amount(predicted)
    else:
        expected_norm = normalize_text(expected)
        predicted_norm = normalize_text(predicted)
    is_match = expected_norm == predicted_norm
    return {
        "document_id": document_id,
        "area": area,
        "field": field,
        "index": "" if index is None else index,
        "expected": expected,
        "predicted": predicted,
        "expected_normalized": expected_norm,
        "predicted_normalized": predicted_norm,
        "match": is_match,
    }


def fields_to_evaluate(source: dict[str, Any], prediction: dict[str, Any]) -> list[tuple[str, str]]:
    fields: list[tuple[str, str]] = []
    for field in TEXT_FIELDS:
        if field in source or field in prediction:
            fields.append((field, "text"))
    for field in AMOUNT_FIELDS:
        if field in source or field in prediction:
            fields.append((field, "amount"))
    return fields


def item_fields_to_evaluate(gt_item: dict[str, Any], pred_item: dict[str, Any]) -> list[tuple[str, str]]:
    fields: list[tuple[str, str]] = []
    for field in ITEM_TEXT_FIELDS:
        if field in gt_item or field in pred_item:
            fields.append((field, "text"))
    for field in ITEM_AMOUNT_FIELDS:
        if field in gt_item or field in pred_item:
            fields.append((field, "amount"))
    return fields


def evaluate_record(
    manifest_row: dict[str, Any],
    source: dict[str, Any],
    prediction_info: dict[str, Any] | None,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    document_id = manifest_row["document_id"]
    if prediction_info is None:
        record_score = {
            "document_id": document_id,
            "template_id": manifest_row.get("template_id"),
            "noisy_profile": manifest_row.get("noisy_profile"),
            "prediction_status": "missing",
            "prediction_path": None,
            "top_level_correct": 0,
            "top_level_total": 0,
            "item_field_correct": 0,
            "item_field_total": 0,
            "item_count_expected": len(source.get("items", [])),
            "item_count_predicted": None,
            "item_count_match": False,
            "record_exact_match": False,
        }
        return record_score, [], []

    prediction = prediction_info["prediction"]
    all_rows: list[dict[str, Any]] = []

    for field, field_type in fields_to_evaluate(source, prediction):
        all_rows.append(
            compare_field(
                document_id,
                "top_level",
                field,
                None,
                source.get(field),
                prediction.get(field),
                field_type,
            )
        )

    gt_items = source.get("items", [])
    pred_items = prediction.get("items", [])
    if not isinstance(gt_items, list):
        gt_items = []
    if not isinstance(pred_items, list):
        pred_items = []

    item_count_match = len(gt_items) == len(pred_items)
    max_len = max(len(gt_items), len(pred_items))
    for index in range(max_len):
        if index >= len(gt_items):
            all_rows.append(
                {
                    "document_id": document_id,
                    "area": "items",
                    "field": "extra_item",
                    "index": index,
                    "expected": None,
                    "predicted": pred_items[index],
                    "expected_normalized": None,
                    "predicted_normalized": None,
                    "match": False,
                }
            )
            continue
        gt_item = gt_items[index]
        pred_item = pred_items[index] if index < len(pred_items) and isinstance(pred_items[index], dict) else {}
        if not isinstance(gt_item, dict):
            gt_item = {}
        for field, field_type in item_fields_to_evaluate(gt_item, pred_item):
            all_rows.append(
                compare_field(
                    document_id,
                    "items",
                    field,
                    index,
                    gt_item.get(field),
                    pred_item.get(field),
                    field_type,
                )
            )

    top_rows = [row for row in all_rows if row["area"] == "top_level"]
    item_rows = [row for row in all_rows if row["area"] == "items" and row["field"] != "extra_item"]
    top_correct = sum(1 for row in top_rows if row["match"])
    item_correct = sum(1 for row in item_rows if row["match"])
    record_exact_match = bool(all_rows) and all(row["match"] for row in all_rows) and item_count_match

    record_score = {
        "document_id": document_id,
        "template_id": manifest_row.get("template_id"),
        "noisy_profile": manifest_row.get("noisy_profile"),
        "prediction_status": "present",
        "prediction_path": prediction_info["path"],
        "top_level_correct": top_correct,
        "top_level_total": len(top_rows),
        "item_field_correct": item_correct,
        "item_field_total": len(item_rows),
        "item_count_expected": len(gt_items),
        "item_count_predicted": len(pred_items),
        "item_count_match": item_count_match,
        "record_exact_match": record_exact_match,
    }

    mismatch_rows = [row for row in all_rows if not row["match"]]
    return record_score, all_rows, mismatch_rows


def accuracy(correct: int, total: int) -> float | None:
    if total == 0:
        return None
    return round(correct / total, 6)


def build_summary(
    data_root: Path,
    prediction_dir: Path,
    output_dir: Path,
    manifest_rows: list[dict[str, Any]],
    predictions: dict[str, dict[str, Any]],
    prediction_errors: list[str],
    record_scores: list[dict[str, Any]],
    all_field_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    field_counts: dict[str, Counter] = defaultdict(Counter)
    item_field_counts: dict[str, Counter] = defaultdict(Counter)

    for row in all_field_rows:
        key = str(row["field"])
        if row["area"] == "items":
            counter = item_field_counts[key]
        else:
            counter = field_counts[key]
        counter["total"] += 1
        if row["match"]:
            counter["correct"] += 1

    def metrics_from_counts(counts: dict[str, Counter]) -> dict[str, dict[str, Any]]:
        return {
            key: {
                "correct": int(counter["correct"]),
                "total": int(counter["total"]),
                "accuracy": accuracy(int(counter["correct"]), int(counter["total"])),
            }
            for key, counter in sorted(counts.items())
        }

    present_scores = [row for row in record_scores if row["prediction_status"] == "present"]
    exact_records = sum(1 for row in present_scores if row["record_exact_match"])
    item_count_exact = sum(1 for row in present_scores if row["item_count_match"])
    top_correct = sum(int(row["top_level_correct"]) for row in present_scores)
    top_total = sum(int(row["top_level_total"]) for row in present_scores)
    item_correct = sum(int(row["item_field_correct"]) for row in present_scores)
    item_total = sum(int(row["item_field_total"]) for row in present_scores)
    model_ids = Counter(
        str(info["meta"].get("model_id", "unknown"))
        for info in predictions.values()
        if isinstance(info.get("meta"), dict)
    )

    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "dataset_version": DATASET_VERSION,
        "created_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "data_root": str(data_root),
        "prediction_dir": str(prediction_dir),
        "output_dir": str(output_dir),
        "model_ids": dict(sorted(model_ids.items())),
        "primary_model_id": model_ids.most_common(1)[0][0] if model_ids else None,
        "records_total": len(manifest_rows),
        "records_with_predictions": len(present_scores),
        "records_missing_predictions": len(manifest_rows) - len(present_scores),
        "extra_prediction_files": sorted(set(predictions) - {row["document_id"] for row in manifest_rows}),
        "prediction_errors": prediction_errors,
        "record_exact_match": {
            "correct": exact_records,
            "total": len(present_scores),
            "accuracy": accuracy(exact_records, len(present_scores)),
        },
        "top_level_field_accuracy": {
            "correct": top_correct,
            "total": top_total,
            "accuracy": accuracy(top_correct, top_total),
        },
        "item_field_accuracy": {
            "correct": item_correct,
            "total": item_total,
            "accuracy": accuracy(item_correct, item_total),
        },
        "item_count_exact": {
            "correct": item_count_exact,
            "total": len(present_scores),
            "accuracy": accuracy(item_count_exact, len(present_scores)),
        },
        "top_level_fields": metrics_from_counts(field_counts),
        "item_fields": metrics_from_counts(item_field_counts),
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "document_id",
        "area",
        "field",
        "index",
        "expected",
        "predicted",
        "expected_normalized",
        "predicted_normalized",
        "match",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def write_markdown_summary(path: Path, summary: dict[str, Any]) -> None:
    lines = [
        "# Baseline Evaluation Summary",
        "",
        f"- schema_version: `{summary['schema_version']}`",
        f"- dataset_version: `{summary['dataset_version']}`",
        f"- records_total: `{summary['records_total']}`",
        f"- records_with_predictions: `{summary['records_with_predictions']}`",
        f"- records_missing_predictions: `{summary['records_missing_predictions']}`",
        f"- record_exact_match_accuracy: `{summary['record_exact_match']['accuracy']}`",
        f"- top_level_field_accuracy: `{summary['top_level_field_accuracy']['accuracy']}`",
        f"- item_field_accuracy: `{summary['item_field_accuracy']['accuracy']}`",
        f"- item_count_exact_accuracy: `{summary['item_count_exact']['accuracy']}`",
        "",
        "## Output Files",
        "",
        "- `baseline_summary.json`",
        "- `baseline_record_scores.jsonl`",
        "- `baseline_field_diffs.csv`",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate v0.2.0 baseline OCR/VLM prediction JSON files."
    )
    parser.add_argument("--data-root", type=Path, default=None)
    parser.add_argument("--prediction-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, default=None)
    parser.add_argument("--write-all-field-rows", action="store_true")
    parser.add_argument("--fail-on-missing", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_root = args.data_root.resolve() if args.data_root else infer_data_root().resolve()
    prediction_dir = args.prediction_dir.resolve()
    output_dir = (args.output_dir or default_output_dir()).resolve()

    if not prediction_dir.exists():
        raise FileNotFoundError(f"prediction directory not found: {prediction_dir}")

    manifest_rows = read_manifest(data_root)
    predictions, prediction_errors = load_predictions(prediction_dir)
    record_scores: list[dict[str, Any]] = []
    all_field_rows: list[dict[str, Any]] = []
    mismatch_rows: list[dict[str, Any]] = []

    for manifest_row in manifest_rows:
        source = read_json(data_root / manifest_row["source_json"])
        score, field_rows, diffs = evaluate_record(
            manifest_row,
            source,
            predictions.get(manifest_row["document_id"]),
        )
        record_scores.append(score)
        all_field_rows.extend(field_rows)
        mismatch_rows.extend(diffs)

    rows_to_write = all_field_rows if args.write_all_field_rows else mismatch_rows
    summary = build_summary(
        data_root,
        prediction_dir,
        output_dir,
        manifest_rows,
        predictions,
        prediction_errors,
        record_scores,
        all_field_rows,
    )

    write_json(output_dir / "baseline_summary.json", summary)
    write_jsonl(output_dir / "baseline_record_scores.jsonl", record_scores)
    write_csv(output_dir / "baseline_field_diffs.csv", rows_to_write)
    write_markdown_summary(output_dir / "baseline_summary.md", summary)

    print(f"OUTPUT_DIR: {output_dir}")
    print(f"RECORDS_TOTAL: {summary['records_total']}")
    print(f"RECORDS_WITH_PREDICTIONS: {summary['records_with_predictions']}")
    print(f"RECORDS_MISSING_PREDICTIONS: {summary['records_missing_predictions']}")
    print(f"TOP_LEVEL_FIELD_ACCURACY: {summary['top_level_field_accuracy']['accuracy']}")
    print(f"ITEM_FIELD_ACCURACY: {summary['item_field_accuracy']['accuracy']}")
    print(f"ITEM_COUNT_EXACT_ACCURACY: {summary['item_count_exact']['accuracy']}")
    print(f"REPORT: {output_dir / 'baseline_summary.md'}")

    if prediction_errors:
        print("PREDICTION_ERRORS: NG")
        for error in prediction_errors:
            print(f"ERROR: {error}")
        return 1
    if args.fail_on_missing and summary["records_missing_predictions"]:
        print("MISSING_PREDICTIONS: NG")
        return 1
    print("STATUS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
