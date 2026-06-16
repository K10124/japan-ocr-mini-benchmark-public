# Japan OCR Mini Benchmark Leaderboard

This leaderboard ranks model runs on the frozen v0.2.0 synthetic Japanese receipt dataset.

- Leaderboard version: `v0.3.2`
- Dataset version: `v0.2.0`
- Evaluation protocol: `v0.3.0`
- Target run ID: `v020_target_20260613_221713`
- Records per run: `20`
- Image variant: `noisy`
- Rank metric: `JOMB Core Score v1`
- Updated at: `2026-06-16T22:41:17.342157+00:00`

## Score Definition

`Core Score / 100 = Exact * 10 + Top-level * 25 + Item fields * 50 + Item count * 15`

Runtime is reported separately and is not part of the score. Invalid or non-final JSON outputs remain visible through `Completed` and contribute through their affected fields rather than being hidden.

## Current Leaderboard

| Rank | Run | Model | Core /100 | Quant | Completed | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `v0.3.1` | `gemma4_31b_qat_q4_0` | 95.29 | `Q4_0` | 20/20 | 35.128 | 0.6 | 0.977273 | 0.997222 | 1 |
| 2 | `v0.3.0` | `gemma4_31b_q8_0` | 95.00 | `Q8_0` | 20/20 | 53.195 | 0.6 | 0.979545 | 0.990278 | 1 |
| 3 | `v0.3.1` | `gemma4_31b_q4_k_m_retest` | 94.92 | `Q4_K_M` | 20/20 | 57.263 | 0.6 | 0.981818 | 0.9875 | 1 |
| 4 | `v0.3.2` | `qwen36_35b_a3b_q8_0` | 94.79 | `Q8_0` | 20/20 | 4.633 | 0.55 | 0.977273 | 0.997222 | 1 |
| 5 | `v0.3.0` | `qwen36_35b_a3b_q4_k_m` | 93.61 | `Q4_K_M` | 20/20 | 4.282 | 0.45 | 0.972727 | 0.995833 | 1 |
| 6 | `v0.3.1` | `qwen36_27b_q8_0` | 88.31 | `Q8_0` | 20/20 | 17.754 | 0.5 | 0.979545 | 0.876389 | 1 |
| 7 | `v0.3.0` | `qwen3_vl_30b_q4_k_m` | 73.59 | `Q4_K_M` | 20/20 | 3.248 | 0.05 | 0.943182 | 0.690278 | 1 |
| 8 | `v0.3.0` | `qwen25_vl_7b_q8_0` | 70.99 | `Q8_0` | 20/20 | 5.094 | 0 | 0.934091 | 0.652778 | 1 |
| 9 | `v0.3.1` | `gemma4_26b_a4b_qat_q4_0` | 64.22 | `Q4_0` | 17/20 | 15.236 | 0.2 | 0.797727 | 0.635621 | 0.7 |
| 10 | `v0.3.0` | `internvl3_5_14b_q8_0` | 56.16 | `Q8_0` | 20/20 | 9.519 | 0 | 0.725 | 0.565672 | 0.65 |

## Awards

- Best Core Score: `gemma4_31b_qat_q4_0` at `95.29` / 100.
- Best Item Extraction: `gemma4_31b_qat_q4_0` at `0.997222` item-field accuracy.
- Fastest 20/20 Completed Run: `qwen3_vl_30b_q4_k_m` at `3.248` seconds per record.

## Notes

- `v0.3.0` rows are the original five-model official LM Studio baseline.
- `v0.3.1` rows are the operational 20-image refresh run added on the same frozen dataset.
- `v0.3.2` adds the Qwen3.6 35B A3B Q8_0 quantization comparison row.
- Quantization is part of each result and must be shown with the model name.
- See `docs/evaluation/jomb_core_score_v1.md` for the scoring protocol.
