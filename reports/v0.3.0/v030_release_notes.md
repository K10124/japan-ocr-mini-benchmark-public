# Japan OCR Mini Benchmark v0.3.0

v0.3.0 is the first official five-model LM Studio baseline comparison for the frozen v0.2.0 synthetic Japanese receipt dataset.

## What Changed

- Added official local LM Studio evaluation results for five VLM baselines.
- Promoted `JOMB Core Score v1` as the official headline ranking metric.
- Kept the underlying dataset payload fixed at v0.2.0.
- Added v0.3.0 model registry, prompt, run-pack, probe, checker, and inference entrypoints.
- Published sanitized comparison artifacts without local absolute paths.

## Official Models

| Rank | Model | Core /100 | Quant | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `gemma4_31b_q8_0` | 95.00 | `Q8_0` | 53.195 | 0.6 | 0.979545 | 0.990278 | 1 |
| 2 | `qwen36_35b_a3b_q4_k_m` | 93.61 | `Q4_K_M` | 4.282 | 0.45 | 0.972727 | 0.995833 | 1 |
| 3 | `qwen3_vl_30b_q4_k_m` | 73.59 | `Q4_K_M` | 3.248 | 0.05 | 0.943182 | 0.690278 | 1 |
| 4 | `qwen25_vl_7b_q8_0` | 70.99 | `Q8_0` | 5.094 | 0 | 0.934091 | 0.652778 | 1 |
| 5 | `internvl3_5_14b_q8_0` | 56.16 | `Q8_0` | 9.519 | 0 | 0.725 | 0.565672 | 0.65 |

## Score Definition

`Core Score / 100 = Exact * 10 + Top-level * 25 + Item fields * 50 + Item count * 15`

Runtime is reported separately and is not part of the score.

## Recommendation

- Use `gemma4_31b_q8_0` when the highest JOMB Core Score and exact-match score matter and runtime is acceptable.
- Use `qwen36_35b_a3b_q4_k_m` when item-level extraction quality and speed/quality balance are the priority.
- Use `qwen25_vl_7b_q8_0` for fast smoke tests and lightweight comparison runs.

## Compatibility

- Dataset root remains `release_v0.2.0/data/v0.2.0` on GitHub public mirrors.
- Dataset root remains `data/v0.2.0` on Hugging Face.
- Evaluation version is `v0.3.0`; dataset version remains `v0.2.0`.

Created at: `2026-06-15T14:27:19.370783+00:00`
