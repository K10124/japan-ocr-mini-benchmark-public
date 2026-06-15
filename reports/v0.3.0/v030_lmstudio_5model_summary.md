# v0.3.0 LM Studio 5-Model Baseline Report

- Created at: `2026-06-15T14:27:19.370783+00:00`
- Evaluation version: `v0.3.0`
- Dataset version: `v0.2.0`
- Frozen target run ID: `v020_target_20260613_221713`
- Runtime: `lmstudio_openai_compatible_api`
- Records: `20` synthetic Japanese receipt images
- Image variant: noisy PNG images from v0.2.0
- Rank metric: `JOMB Core Score v1`

## Summary

v0.3.0 publishes the first official local LM Studio comparison for the frozen v0.2.0 dataset.
The data payload remains v0.2.0; v0.3.0 is the evaluation/reporting release for five local VLM baselines.

- Best JOMB Core Score v1: `gemma4_31b_q8_0` at `95.00` / 100.
- Best item-field accuracy: `qwen36_35b_a3b_q4_k_m` at `0.995833`.
- Best exact-match accuracy: `gemma4_31b_q8_0` at `0.6`.
- Fastest completed model: `qwen3_vl_30b_q4_k_m` at `3.248` seconds/record.
- All five selected models produced 20 prediction JSON files with zero missing predictions.

## JOMB Core Score v1

`Core Score / 100 = Exact * 10 + Top-level * 25 + Item fields * 50 + Item count * 15`

- Exact match is useful, but intentionally capped at 10% so strict all-or-nothing JSON matching does not dominate.
- Item-field extraction receives 50% because line-item recovery is the main task for receipt understanding.
- Runtime is reported separately and is not included in the score.
- Missing or invalid prediction JSON should count as zero contribution for the affected record.

## Comparison

| Rank | Model | Core /100 | Quant | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `gemma4_31b_q8_0` | 95.00 | `Q8_0` | 53.195 | 0.6 | 0.979545 | 0.990278 | 1 |
| 2 | `qwen36_35b_a3b_q4_k_m` | 93.61 | `Q4_K_M` | 4.282 | 0.45 | 0.972727 | 0.995833 | 1 |
| 3 | `qwen3_vl_30b_q4_k_m` | 73.59 | `Q4_K_M` | 3.248 | 0.05 | 0.943182 | 0.690278 | 1 |
| 4 | `qwen25_vl_7b_q8_0` | 70.99 | `Q8_0` | 5.094 | 0 | 0.934091 | 0.652778 | 1 |
| 5 | `internvl3_5_14b_q8_0` | 56.16 | `Q8_0` | 9.519 | 0 | 0.725 | 0.565672 | 0.65 |

## Item Field Breakdown

| Model | Name | Quantity | Unit price | Amount |
| --- | ---: | ---: | ---: | ---: |
| `gemma4_31b_q8_0` | 0.988889 | 1 | 0.972222 | 1 |
| `qwen36_35b_a3b_q4_k_m` | 0.988889 | 0.994444 | 1 | 1 |
| `qwen3_vl_30b_q4_k_m` | 0.938889 | 0.411111 | 0.411111 | 1 |
| `qwen25_vl_7b_q8_0` | 0.95 | 0.622222 | 0.044444 | 0.994444 |
| `internvl3_5_14b_q8_0` | 0.544444 | 0.748387 | 0.316129 | 0.644444 |

## Interpretation

- `gemma4_31b_q8_0` has the best JOMB Core Score v1, exact-match score, and top-level-field accuracy, but is much slower.
- `qwen36_35b_a3b_q4_k_m` is the strongest item-level structured extraction baseline and the best speed/quality tradeoff among the top two.
- `qwen25_vl_7b_q8_0` is the speed/lightweight baseline; it is useful for smoke tests but weak on unit-price extraction.
- `qwen3_vl_30b_q4_k_m` reads receipt-level fields well but loses accuracy on item quantity and unit price.
- `internvl3_5_14b_q8_0` remains useful as a non-Qwen comparison, but trails the Qwen/Gemma results on this benchmark.

## Notes

- The v0.2.0 dataset payload is not regenerated or changed by this release.
- Results are local LM Studio GGUF runs on the user's PC, not cloud-hosted model scores.
- Quantization is part of the result definition and must be shown in comparison tables.
- Qwen3.6 uses the `reasoning_effort=none` mitigation to prevent reasoning-only or invalid JSON responses.
