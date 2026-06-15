from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


REQUIRED_MANIFEST_FIELDS = (
    "document_id",
    "template_id",
    "clean_image",
    "noisy_image",
    "source_json",
    "metadata_json",
    "degradation_metadata",
    "noisy_profile",
    "item_count",
    "llm_item_count",
    "total",
)


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


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def read_manifest(data_root: Path) -> list[dict[str, Any]]:
    manifest_path = data_root / "manifest.jsonl"
    rows: list[dict[str, Any]] = []
    with manifest_path.open("r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            missing = [field for field in REQUIRED_MANIFEST_FIELDS if field not in row]
            if missing:
                raise ValueError(f"{manifest_path}:{line_number} missing fields: {missing}")
            rows.append(row)
    return rows


def resolve_artifact_paths(data_root: Path, row: dict[str, Any]) -> dict[str, Path]:
    return {
        "clean_image": data_root / row["clean_image"],
        "noisy_image": data_root / row["noisy_image"],
        "source_json": data_root / row["source_json"],
        "metadata_json": data_root / row["metadata_json"],
        "degradation_metadata": data_root / row["degradation_metadata"],
    }


def validate_artifacts(data_root: Path, rows: list[dict[str, Any]]) -> list[str]:
    errors: list[str] = []
    for row in rows:
        for label, path in resolve_artifact_paths(data_root, row).items():
            if not path.exists():
                errors.append(f"{row['document_id']}: missing {label}: {path}")
    return errors


def print_summary(data_root: Path, rows: list[dict[str, Any]], limit: int, show_paths: bool) -> None:
    template_counts = Counter(row["template_id"] for row in rows)
    noisy_counts = Counter(row["noisy_profile"] for row in rows)
    total_items = sum(int(row["item_count"]) for row in rows)
    total_llm_items = sum(int(row["llm_item_count"]) for row in rows)

    print(f"DATA_ROOT: {data_root}")
    print(f"RECORDS: {len(rows)}")
    print(f"TOTAL_ITEMS: {total_items}")
    print(f"TOTAL_LLM_ITEMS: {total_llm_items}")
    print(f"TEMPLATE_COUNTS: {dict(sorted(template_counts.items()))}")
    print(f"NOISY_PROFILE_COUNTS: {dict(sorted(noisy_counts.items()))}")
    print()
    print(f"FIRST_{min(limit, len(rows))}_RECORDS:")

    for row in rows[:limit]:
        paths = resolve_artifact_paths(data_root, row)
        source = read_json(paths["source_json"])
        metadata = read_json(paths["metadata_json"])
        degradation = read_json(paths["degradation_metadata"])
        print(
            "- "
            f"{row['document_id']} | "
            f"template={row['template_id']} | "
            f"noisy={row['noisy_profile']} | "
            f"items={row['item_count']} | "
            f"llm_items={row['llm_item_count']} | "
            f"total={row['total']} | "
            f"metadata_difficulty={metadata.get('difficulty')} | "
            f"degradation={degradation.get('resolved_difficulty_profile')}"
        )
        if len(source.get("items", [])) != int(row["item_count"]):
            print(
                "  WARNING: source_json item count does not match manifest "
                f"({len(source.get('items', []))} != {row['item_count']})"
            )
        if show_paths:
            print(f"  noisy_image: {paths['noisy_image']}")
            print(f"  source_json: {paths['source_json']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Load the Japan OCR Mini Benchmark v0.2.0 manifest.jsonl."
    )
    parser.add_argument(
        "--data-root",
        type=Path,
        default=None,
        help="Path to the v0.2.0 data root containing manifest.jsonl.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="Number of records to print.",
    )
    parser.add_argument(
        "--show-paths",
        action="store_true",
        help="Print resolved artifact paths for each displayed record.",
    )
    parser.add_argument(
        "--no-validate-files",
        action="store_true",
        help="Skip checking that every artifact path exists.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    data_root = args.data_root.resolve() if args.data_root else infer_data_root().resolve()
    rows = read_manifest(data_root)

    if not args.no_validate_files:
        errors = validate_artifacts(data_root, rows)
        if errors:
            print("ARTIFACT_VALIDATION: NG")
            for error in errors[:20]:
                print(f"ERROR: {error}")
            if len(errors) > 20:
                print(f"ERROR: ... {len(errors) - 20} more")
            return 1
        print("ARTIFACT_VALIDATION: OK")

    print_summary(data_root, rows, max(args.limit, 0), args.show_paths)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
