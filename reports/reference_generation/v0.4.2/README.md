# v0.4.2 Accepted Receipt Structure Library

This report is a curated synthetic receipt-structure snapshot for Japan OCR Mini Benchmark.

It promotes the selected `採用` rows from the receipt structure review into a versioned reference-generation report. The goal is to preserve the strongest clean receipt layouts before expanding toward a larger 100-structure synthetic benchmark.

![v0.4.2 accepted receipt contact sheet](contact_sheet.png)

## Snapshot

- Version: `v0.4.2`
- Accepted structures: `83`
- Selection source: `05_generation/generated_reports/receipt_structure_selection_review_20260621_001622`
- Source inventory: `05_generation/generated_reports/receipt_structure_inventory_canonical_20260621_000439`
- Public data safety: fictional synthetic receipts only

## Structure Mix

- `blogger_v4_reference_derived`: `10`
- `generated_receipt_batch`: `23`
- `japanese_typography_prototype`: `5`
- `logo_style_prototype`: `23`
- `store_unique_v5_reference_derived`: `22`

## Files

- `index.html`: visual review gallery
- `contact_sheet.png`: all accepted structures at a glance
- `manifest.jsonl`: programmatic list of accepted images and metadata
- `summary.json`: aggregate counts
- `images_clean/`: clean synthetic receipt images
- `metadata/`: per-receipt metadata
- `thumbs/`: small review thumbnails

## Audit Note

This is a structure library rather than the final randomized benchmark dataset. Amount parsing and image readability checks are expected to pass, while a small number of cross-receipt item-name/quantity/amount overlaps can remain here because several accepted structures intentionally share a family before the next randomization pass. The next 100-type generation step should resolve those product-value overlaps.

## Notes

Real receipt images uploaded during development are not copied into this report. They are used only as layout and category references. Store names, addresses, phone numbers, registration numbers, products, and transaction details in this report are synthetic.
