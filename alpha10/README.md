# Japan OCR Mini Benchmark Alpha10 Approved Payload

## Overview

Alpha10 is a small synthetic Japanese receipt OCR and VLM evaluation payload. It contains 10 clean receipt images with paired public JSON labels and metadata.

## License

License: CC BY 4.0.

License confirmed for Alpha10 approved payload. This license confirmation applies only to the Alpha10 approved payload.

## Public Safety

- CASE-000048 is excluded.
- Public safety scan is pass.
- Synthetic data notice is retained.
- No real reference images are included.
- The receipts are synthetic data and do not intentionally represent any real store, real person, real brand, or real transaction.
- Phone numbers and registration numbers are synthetic or unverified OCR benchmark fields.

## Intended Uses

Use this payload for Japanese receipt OCR, document AI, visual question answering, and structured extraction evaluation.

## Out-of-Scope Uses

Do not use this payload as proof of a real transaction, identity evidence, accounting evidence, tax advice, or a large training corpus.

## Contents

- `images/`: clean synthetic receipt images
- `source_json/`: public source labels
- `metadata/`: public metadata
- `alpha10_approved_manifest_latest.json`: approved payload manifest
- `ALPHA10_LICENSE_FINAL_CONFIRMATION.md`: license confirmation

## Publication Status

This approved payload is ready for actual GitHub and Hugging Face publication execution after the operator confirms the destination repositories. No GitHub push or Hugging Face upload is executed by this packaging step.
