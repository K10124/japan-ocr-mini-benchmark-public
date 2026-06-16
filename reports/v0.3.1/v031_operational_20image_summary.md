# v0.3.1 Operational 20-Image Result Snapshot

v0.3.1 adds a refreshed local LM Studio result snapshot for four currently operational GGUF/VLM models.

- Dataset payload: `v0.2.0`
- Evaluation protocol: `v0.3.0`
- Target run ID: `v020_target_20260613_221713`
- Records per model: `20`
- Runtime: `lmstudio_openai_compatible_api`
- Score: `JOMB Core Score v1`

## Results

| Rank | Model | Core /100 | Quant | Completed | Avg sec | Exact | Top-level | Item fields | Item count |
| ---: | --- | ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `gemma4_31b_qat_q4_0` | 95.29 | `Q4_0` | 20/20 | 35.128 | 0.6 | 0.977273 | 0.997222 | 1 |
| 2 | `gemma4_31b_q4_k_m_retest` | 94.92 | `Q4_K_M` | 20/20 | 57.263 | 0.6 | 0.981818 | 0.9875 | 1 |
| 3 | `qwen36_27b_q8_0` | 88.31 | `Q8_0` | 20/20 | 17.754 | 0.5 | 0.979545 | 0.876389 | 1 |
| 4 | `gemma4_26b_a4b_qat_q4_0` | 64.22 | `Q4_0` | 17/20 | 15.236 | 0.2 | 0.797727 | 0.635621 | 0.7 |

## Takeaways

- `gemma4_31b_qat_q4_0` is the new top-scoring run at `95.29` / 100.
- `gemma4_31b_q4_k_m_retest` is very close at `94.92` / 100, with slightly better top-level accuracy but lower item-field accuracy.
- `qwen36_27b_q8_0` completed all 20 records and is the fastest fully completed v0.3.1 run.
- `gemma4_26b_a4b_qat_q4_0` is fast, but 3 of 20 outputs were not clean final JSON, which makes it less suitable as a default benchmark model without prompt/runtime tuning.
