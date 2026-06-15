# Manifest Loading

Use `manifest.jsonl` as the entry point for the v0.2.0 payload.

Each line is one JSON object. Artifact paths inside each row are relative to the
v0.2.0 data root.

## Data Roots

```text
GitHub public payload: release_v0.2.0/data/v0.2.0
Hugging Face payload: data/v0.2.0
Local sibling mirror: ../hf_dataset_upload/data/v0.2.0
```

## Run The Example

From this development workspace:

```powershell
python .\examples\load_v020_manifest.py --data-root "..\hf_dataset_upload\data\v0.2.0" --limit 5 --show-paths
```

The script checks that every listed JSON and PNG artifact exists, then prints a
short summary of template counts, noisy profile counts, and the first records.

## Minimal Python Pattern

```python
from pathlib import Path
import json

data_root = Path("release_v0.2.0/data/v0.2.0")
manifest_path = data_root / "manifest.jsonl"

with manifest_path.open("r", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f if line.strip()]

first = rows[0]
noisy_image_path = data_root / first["noisy_image"]
source_json_path = data_root / first["source_json"]

print(first["document_id"])
print(noisy_image_path)
print(source_json_path)
```

## Important Notes

- Use `manifest.jsonl` or the publication payload directories as the current
  v0.2.0 source of truth.
- Do not treat `05_generation/generated_*` as the public payload index; those
  folders can contain intermediate generation artifacts.
- The legacy 5-receipt prototype is preserved under
  `legacy/initial_5_receipt_sample/` for historical comparison only.
