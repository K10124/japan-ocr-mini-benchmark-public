# Japan OCR Mini Benchmark Leaderboard

This leaderboard ranks submitted model runs on the frozen v0.2.0 synthetic Japanese receipt dataset.

- Leaderboard version: `v0.3.1`
- Dataset version: `v0.2.0`
- Evaluation version: `v0.3.0`
- Target run ID: `v020_target_20260613_221713`
- Records: `20`
- Data root: `release_v0.2.0/data/v0.2.0`
- Rank metric: `JOMB Core Score v1`
- Updated at: `2026-06-15T15:09:03.350652+00:00`

## Score Definition

`Core Score / 100 = Exact * 10 + Top-level * 25 + Item fields * 50 + Item count * 15`

Runtime is reported separately and is not part of the score.

## Current Leaderboard

| Rank | Model | Core /100 | Quant | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `gemma4_31b_q8_0` | 95.00 | `Q8_0` | 53.195 | 0.6 | 0.979545 | 0.990278 | 1 |
| 2 | `qwen36_35b_a3b_q4_k_m` | 93.61 | `Q4_K_M` | 4.282 | 0.45 | 0.972727 | 0.995833 | 1 |
| 3 | `qwen3_vl_30b_q4_k_m` | 73.59 | `Q4_K_M` | 3.248 | 0.05 | 0.943182 | 0.690278 | 1 |
| 4 | `qwen25_vl_7b_q8_0` | 70.99 | `Q8_0` | 5.094 | 0 | 0.934091 | 0.652778 | 1 |
| 5 | `internvl3_5_14b_q8_0` | 56.16 | `Q8_0` | 9.519 | 0 | 0.725 | 0.565672 | 0.65 |

## Awards

- Best Core Score: `gemma4_31b_q8_0` at `95.00` / 100.
- Best Item Extraction: `qwen36_35b_a3b_q4_k_m` at `0.995833` item-field accuracy.
- Fastest Completed Baseline: `qwen3_vl_30b_q4_k_m` at `3.248` seconds per record.

## Notes

- Scores are from local LM Studio GGUF/VLM runs on one PC and are intended as a reproducible smoke-test baseline.
- Quantization is part of each result and must be shown with the model name.
- Missing or invalid prediction JSON should count as zero contribution for the affected record.
- See `docs/evaluation/jomb_core_score_v1.md` for the scoring protocol.
- See `docs/evaluation/submit_model_results.md` to evaluate a new model run.
