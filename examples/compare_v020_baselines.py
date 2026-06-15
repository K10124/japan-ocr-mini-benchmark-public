from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def find_reports(reports_root: Path) -> list[Path]:
    return sorted(reports_root.rglob("baseline_summary.json"))


def metric(summary: dict[str, Any], key: str) -> Any:
    value = summary.get(key)
    if isinstance(value, dict):
        return value.get("accuracy")
    return None


def summarize_report(path: Path) -> dict[str, Any]:
    summary = read_json(path)
    return {
        "model_id": summary.get("primary_model_id") or Path(summary.get("prediction_dir", "")).name,
        "report_path": str(path),
        "prediction_dir": summary.get("prediction_dir"),
        "records_total": summary.get("records_total"),
        "records_with_predictions": summary.get("records_with_predictions"),
        "records_missing_predictions": summary.get("records_missing_predictions"),
        "record_exact_match_accuracy": metric(summary, "record_exact_match"),
        "top_level_field_accuracy": metric(summary, "top_level_field_accuracy"),
        "item_field_accuracy": metric(summary, "item_field_accuracy"),
        "item_count_exact_accuracy": metric(summary, "item_count_exact"),
    }


def sort_key(row: dict[str, Any]) -> tuple[float, float, float, str]:
    item = row.get("item_field_accuracy")
    top = row.get("top_level_field_accuracy")
    count = row.get("item_count_exact_accuracy")
    return (
        -float(item if item is not None else -1),
        -float(top if top is not None else -1),
        -float(count if count is not None else -1),
        str(row.get("model_id") or ""),
    )


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "rank",
        "model_id",
        "records_with_predictions",
        "records_missing_predictions",
        "record_exact_match_accuracy",
        "top_level_field_accuracy",
        "item_field_accuracy",
        "item_count_exact_accuracy",
        "report_path",
        "prediction_dir",
    ]
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key) for key in fieldnames})


def write_markdown(path: Path, rows: list[dict[str, Any]]) -> None:
    lines = [
        "# v0.2.0 Baseline Comparison",
        "",
        "| Rank | Model | Records | Missing | Exact | Top-level fields | Item fields | Item count |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {rank} | `{model_id}` | {records_with_predictions} | {records_missing_predictions} | "
            "{record_exact_match_accuracy} | {top_level_field_accuracy} | "
            "{item_field_accuracy} | {item_count_exact_accuracy} |".format(**row)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare v0.2.0 baseline evaluation summaries.")
    parser.add_argument("--report", type=Path, action="append", default=[])
    parser.add_argument("--reports-root", type=Path, default=None)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report_paths = list(args.report)
    if args.reports_root:
        report_paths.extend(find_reports(args.reports_root))
    report_paths = sorted({path.resolve() for path in report_paths})

    if not report_paths:
        raise FileNotFoundError("No baseline_summary.json reports found.")

    rows = [summarize_report(path) for path in report_paths]
    rows = sorted(rows, key=sort_key)
    for index, row in enumerate(rows, start=1):
        row["rank"] = index

    output_dir = args.output_dir.resolve()
    write_json(output_dir / "baseline_comparison_summary.json", rows)
    write_csv(output_dir / "baseline_comparison_summary.csv", rows)
    write_markdown(output_dir / "baseline_comparison_summary.md", rows)

    print(f"OUTPUT_DIR: {output_dir}")
    print(f"REPORT_COUNT: {len(rows)}")
    print(f"SUMMARY_MD: {output_dir / 'baseline_comparison_summary.md'}")
    print("STATUS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
