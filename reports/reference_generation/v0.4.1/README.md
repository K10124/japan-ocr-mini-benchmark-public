# v0.4.1 Reference Clean Generation Audit

This snapshot records the reference-derived synthetic receipt generator after the item-line audit fixes requested from the external review.

## Snapshot

- Version: `v0.4.1`
- Source batch: `reference_clean_audit_fixed_20260620_143526`
- Created at: `2026-06-20T14:35:29.657553`
- Seed: `34620260620`
- Selection policy: `shuffle_without_replacement`
- Duplicate template IDs allowed: `False`
- Batch source in working tree: `05_generation/reference_receipt_batches/reference_clean_audit_fixed_20260620_143526`

## Audit Result

- Audit status: `PASS`
- Receipt count: `23`
- Item/service line count: `118`
- Product duplicate audit line count: `107`
- Excluded semantic line count: `11`
- Normal item/service amount missing errors: `0`
- Zero amount semantic errors: `0`
- Name + quantity + amount duplicate count: `0`
- Same-receipt normalized name duplicate count: `0`
- Historical duplicate triples recorded for traceability: `107`

## Fixes Reflected

- Template-specific amount fields such as `line_amount` are now resolved by the audit.
- Set-child 0-yen rows are marked as `line_role=set_component` and `amount_semantics=included_in_set`.
- Receipt-level total-only rows are marked as `line_role=receipt_total_only` and excluded from product duplicate checks.
- Clean batch metadata now keeps `run_id`, `document_id`, `generation_index`, and seed values.
- Long lifestyle-goods receipts no longer repeat the same item name inside one generated receipt.

## Pass Conditions

- normal item/service rows have amount
- zero amount rows are explicitly marked as included_in_set or excluded from product audit
- receipt_total_only rows are excluded from product duplicate audit
- name + quantity + amount duplicate count is zero within this run
- same receipt normalized_name duplicates are zero

## Files

- Review page: `index.html`
- Contact sheet: `contact_sheet.png`
- Audit page: `duplicate_audit.html`
- Audit CSV: `item_line_duplicate_audit.csv`
- Audit summary: `duplicate_audit_summary.json`
- Clean images: `images_clean/`
- Metadata JSON: `metadata/`

## Template IDs

- `reference_style_shared_workspace_time_receipt`
- `reference_style_lifestyle_goods_long_receipt`
- `reference_style_cafe_campaign_code_receipt`
- `reference_style_airport_credit_pair_receipt`
- `reference_style_family_restaurant_long_item_receipt`
- `reference_style_monthly_supermarket_bulk_receipt`
- `reference_style_conveyor_sushi_coupon_receipt`
- `reference_style_karaoke_room_order_receipt`
- `reference_style_service_exchange_qr_receipt`
- `reference_style_electronics_barcode_point_receipt`
- `reference_style_parking_invoice_watermark_receipt`
- `reference_style_daily_bakery_paypay_receipt`
- `reference_style_gas_station_fuel_tax_receipt`
- `reference_style_taxi_short_receipt`
- `reference_style_convenience_credit_coupon_receipt`
- `reference_style_cinema_ticket_receipt`
- `reference_style_cafe_reward_receipt`
- `reference_style_dry_cleaning_adjustment_receipt`
- `reference_style_drugstore_id_receipt`
- `reference_style_dark_phone_coupon_receipt`
- `reference_style_fast_food_pickup_number_receipt`
- `reference_style_coin_laundry_machine_receipt`
- `reference_style_home_center_point_receipt`

## Public Data Safety

Only fictional synthetic receipt outputs and metadata are included here. Uploaded real receipt references are not copied into the public or Hugging Face payload.
