# v0.2.0 Release Candidate Summary

- RC status: **release_candidate_ready**
- Target run ID: `v020_target_20260613_221713`
- Created at: `2026-06-13T22:42:40`
- Manual visual review: `ok_by_user_step148`

## Target Run

- Target run dir: `<LOCAL_PATH_REMOVED>\Desktop\japan_ocr_mini_benchmark\05_generation\target_runs\v020_target_20260613_221713`
- Summary JSON: `release_v0.2.0/reports/v020_target_run_summary.json`
- Validation JSON: `release_v0.2.0/reports/v020_target_run_validation_latest.json`
- Validation CSV: `release_v0.2.0/reports/v020_target_run_validation_latest.csv`

## Generation Summary

- Requested total: `20`
- Success total: `20`
- Warning total: `0`
- Failure total: `0`
- Documents with LLM items: `19`
- LLM approved items: `56`
- Item master items: `124`
- LLM mix ratio: `0.3111`

## Validation Summary

- Validation status: `warning`
- Record count: `20`
- Status counts: `{'ok': 8, 'warning': 12}`
- Issue code top counts: `{'clean_noisy_size_large_difference': 12}`
- Noisy profile counts: `{'light': 3, 'hard': 8, 'medium': 9}`

## Review Files

- Full review CSV: `release_v0.2.0/reports/v020_review_full_step147.csv`
- Full review HTML: `release_v0.2.0/reports/v020_review_gallery_step147.html`
- Shortlist CSV: `release_v0.2.0/reports/v020_review_shortlist_step147.csv`
- Shortlist HTML: `release_v0.2.0/reports/v020_review_shortlist_step147.html`

## Checklist

- [x] 20 records generated
- [x] 0 generation failures
- [x] validation status ok or warning
- [x] only allowed validation warnings
- [x] manual visual review ok
- [x] parking tax breakdown hidden
- [x] local Osaka/Kita-ku exclusion passed
- [x] all expected artifacts exist
- [x] no failed validation records
- [x] step146d noisy renderer metadata confirmed
- [x] review gallery and shortlist generated

## Notes

- `clean_noisy_size_large_difference` warning is allowed because noisy images include stronger degradation, rotation, canvas margins, and shadows.
- Manual visual review was completed and accepted before freezing this RC.
- Parking tax breakdown and nearby Osaka/Kita-ku style place-name exclusions were checked.
- This file marks the current run as the v0.2.0 release candidate, not the final public release.
