# JOMB Core Score v1

`JOMB Core Score v1` is the headline quality metric for Japan OCR Mini Benchmark model comparisons.

## Formula

```text
Core Score / 100 = Exact * 10 + Top-level * 25 + Item fields * 50 + Item count * 15
```

The raw score is stored as `jomb_core_score_v1` in the 0-1 range and as `jomb_core_score_v1_points` in the 0-100 range.

## Weights

| Component | Weight | Reason |
| --- | ---: | --- |
| Exact match | 10% | Useful as a strict all-or-nothing signal, but capped so it does not dominate. |
| Top-level fields | 25% | Store/date/payment/total fields matter for receipt-level understanding. |
| Item fields | 50% | Line-item recovery is the main task for receipt OCR/VLM extraction. |
| Item count exact | 15% | A model must recover the right number of items before field-level scores are fully meaningful. |

## Component Definitions

- `Exact`: the record is treated as exact only when all evaluated top-level fields, all evaluated item fields, and item count match.
- `Top-level`: field accuracy over receipt-level fields such as store, branch, address, date, time, payment, tax, and totals.
- `Item fields`: field accuracy over item `name`, `quantity`, `unit_price`, and `amount`.
- `Item count`: exact match between predicted and ground-truth item row count.

## Missing or Invalid Predictions

Official leaderboard submissions should provide one valid prediction JSON per manifest row.

If a record is missing or has invalid JSON, it receives zero contribution for the affected record. The example evaluator applies this by scaling the core score by completion ratio.

## Runtime Policy

Runtime is intentionally not included in the core score. It depends on local hardware, quantization, LM Studio settings, and background load. Report runtime separately as `avg_seconds`.

## Current Official Run

- Dataset version: `v0.2.0`
- Evaluation version: `v0.3.0`
- Target run ID: `v020_target_20260613_221713`
- Records: `20`
- Runtime: `lmstudio_openai_compatible_api`
