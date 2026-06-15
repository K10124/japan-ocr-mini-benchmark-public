You are extracting structured data from a synthetic Japanese receipt image.

Return JSON only. Do not wrap the JSON in Markdown.

Use this JSON shape:

```json
{
  "schema_version": "jomb-baseline-prediction-v1",
  "dataset_version": "v0.2.0",
  "model_id": "<model-id>",
  "document_id": "<document-id>",
  "input_image": "<relative-image-path>",
  "prediction": {
    "store_name": null,
    "store_branch_name": null,
    "store_address": null,
    "date": null,
    "time": null,
    "items": [
      {
        "name": null,
        "quantity": null,
        "unit_price": null,
        "amount": null
      }
    ],
    "subtotal": null,
    "coupon_discount": null,
    "points_used": null,
    "points_earned": null,
    "point_balance": null,
    "tax_8_target": null,
    "tax_10_target": null,
    "tax_8_inner_tax": null,
    "tax_10_inner_tax": null,
    "reduced_tax_target": null,
    "standard_tax_target": null,
    "tax_total": null,
    "total": null,
    "payment_method": null,
    "cash_received": null,
    "change": null,
    "invoice_registration_number": null
  }
}
```

Rules:

- Use integers for money, quantities, unit prices, point counts, and tax fields when visible.
- Use null when a field is not visible or not applicable.
- Keep item order as it appears on the receipt.
- Do not infer hidden fields from arithmetic unless the field is explicitly visible.
- Preserve Japanese text as seen in the image.
