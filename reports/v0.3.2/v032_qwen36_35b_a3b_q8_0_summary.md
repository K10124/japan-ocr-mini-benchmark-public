# v0.3.2 Qwen3.6 35B A3B Q8_0 Result Snapshot

v0.3.2 adds a Q8_0 quantization comparison run for Qwen3.6 35B A3B on the same frozen v0.2.0 noisy-image dataset.

- Dataset payload: `v0.2.0`
- Evaluation protocol: `v0.3.0`
- Target run ID: `v020_target_20260613_221713`
- Records per model: `20`
- Image variant: `noisy`
- Runtime: `lmstudio_openai_compatible_api`
- Score: `JOMB Core Score v1`

## Results

| Rank | Model | Core /100 | Quant | Completed | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `qwen36_35b_a3b_q8_0` | 94.79 | `Q8_0` | 20/20 | 4.633 | 0.55 | 0.977273 | 0.997222 | 1 |

## Takeaways

- `qwen36_35b_a3b_q8_0` completed all 20 records and scored `94.79` / 100.
- Compared with the earlier Q4_K_M row at `93.61` / 100, this Q8_0 run is slightly stronger on the same noisy 20-image dataset.
- The item-field score is `0.997222`, with perfect unit-price and amount accuracy in this run.
