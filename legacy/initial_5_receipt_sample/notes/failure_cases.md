\# Failure Cases



This file summarizes OCR/VLM failure cases found in the Japan OCR Mini Benchmark.



\## Failure Case 001: receipt\_005\_noisy.png



\### Image



`02\_receipt\_images/receipt\_005\_noisy.png`



\### Model



Qwen3.6 35B A3B



\### Task



Item-level extraction from a degraded narrow Japanese receipt with:



\* quantity

\* unit price

\* item amount

\* coupon discount

\* point usage

\* tax target amounts

\* payment amount

\* cash received

\* change

\* points earned

\* point balance



\---



\## Summary



Qwen3.6 35B A3B extracted most fields correctly, but made several errors in tax target amounts and Japanese item names.



\---



\## Error 1: tax\_8\_target



\### Ground truth



```json

"tax\_8\_target": 2597

```



\### Model output



```json

"tax\_8\_target": 2607

```



\### Notes



The model misread `2,597` as `2,607`.



This is a small numerical error, but it is important for receipt extraction because tax target amounts are structured financial fields.



\---



\## Error 2: tax\_10\_target



\### Ground truth



```json

"tax\_10\_target": 2595

```



\### Model output



```json

"tax\_10\_target": 2605

```



\### Notes



The model misread `2,595` as `2,605`.



This suggests that degraded image quality can cause errors in visually similar numbers.



\---



\## Error 3: item name - バウムクーヘン



\### Ground truth



```json

{

&#x20; "name": "バウムクーヘン",

&#x20; "quantity": 2,

&#x20; "unit\_price": 158,

&#x20; "amount": 316

}

```



\### Model output



```json

{

&#x20; "name": "パウムクーヘン",

&#x20; "quantity": 2,

&#x20; "unit\_price": 158,

&#x20; "amount": 316

}

```



\### Notes



The model confused `バ` with `パ`.



The quantity, unit price, and amount were correct, but the item name contained a Japanese dakuten/handakuten error.



\---



\## Error 4: item name - ボックスティッシュ



\### Ground truth



```json

{

&#x20; "name": "ボックスティッシュ",

&#x20; "quantity": 1,

&#x20; "unit\_price": 248,

&#x20; "amount": 248

}

```



\### Model output



```json

{

&#x20; "name": "ポックスティッシュ",

&#x20; "quantity": 1,

&#x20; "unit\_price": 248,

&#x20; "amount": 248

}

```



\### Notes



The model confused `ボ` with `ポ`.



This is another Japanese dakuten/handakuten-related error.



\---



\## Observations



The model correctly extracted:



\* store name

\* date

\* time

\* item count

\* quantities

\* unit prices

\* item amounts

\* subtotal

\* coupon discount

\* points used

\* final total

\* payment method

\* cash received

\* change

\* points earned

\* point balance



The main failures were:



\* small numerical errors in tax target amounts

\* Japanese character recognition errors involving dakuten and handakuten



\---



\## Why this failure case matters



This case is useful because it shows that even a strong vision-language model can make realistic Japanese receipt OCR errors under degraded image conditions.



The errors are not random. They are related to common OCR/VLM challenges:



\* blurry small text

\* degraded receipt image quality

\* narrow receipt layout

\* visually similar numbers

\* Japanese voiced and semi-voiced sound marks

\* dense financial fields near the bottom of the receipt



\---



\## Potential future tests



Future receipts should include:



\* stronger thermal printer fading

\* handwritten notes

\* overlapping stamps

\* cropped totals

\* duplicate total fields

\* mixed tax-included and tax-excluded labels

\* actual tax amount fields in addition to tax target amount fields

\* darker shadows

\* stronger perspective distortion


---

## Failure Case 002: InternVL3.5-14B Q8_0 on receipt_005_noisy.png

### Image

`02_receipt_images/receipt_005_noisy.png`

### Model

InternVL3.5-14B Q8_0 GGUF

### Runtime

LM Studio

### Task

Item-level structured extraction from a degraded narrow Japanese receipt with:

* quantity
* unit price
* item amount
* coupon discount
* point usage
* tax target amounts
* payment amount
* cash received
* change
* points earned
* point balance

---

## Summary

InternVL3.5-14B Q8_0 correctly extracted many basic fields, but made several significant errors in structured receipt extraction.

Compared with Qwen3.6 35B A3B Q4_K_M, InternVL3.5-14B Q8_0 produced more errors on the same `receipt_005_noisy.png` sample.

---

## Error 1: coupon_discount

### Ground truth

```json
"coupon_discount": 150
```

### Model output

```json
"coupon_discount": 1050
```

### Notes

The model misread the coupon discount amount.

This is a significant structured extraction error because the coupon discount directly affects payment calculation.

---

## Error 2: tax_8_target

### Ground truth

```json
"tax_8_target": 2597
```

### Model output

```json
"tax_8_target": 4671
```

### Notes

The model incorrectly extracted the 8% tax target amount.

This suggests confusion in the lower financial summary section of the degraded receipt image.

---

## Error 3: tax_10_target

### Ground truth

```json
"tax_10_target": 2595
```

### Model output

```json
"tax_10_target": 2655
```

### Notes

The model made a numerical extraction error in the 10% tax target amount.

---

## Error 4: item count

### Ground truth

```json
"item_count": 15
```

### Model output

```json
"item_count": 13
```

### Notes

The model omitted two items near the lower part of the item list.

Missing items:

```json
[
  {
    "name": "充電ケーブル短",
    "quantity": 1,
    "unit_price": 780,
    "amount": 780
  },
  {
    "name": "靴下 無地",
    "quantity": 2,
    "unit_price": 330,
    "amount": 660
  }
]
```

---

## Error 5: item name - バウムクーヘン

### Ground truth

```json
{
  "name": "バウムクーヘン",
  "quantity": 2,
  "unit_price": 158,
  "amount": 316
}
```

### Model output

```json
{
  "name": "パワムクーン",
  "quantity": 2,
  "unit_price": 158,
  "amount": 316
}
```

### Notes

The model produced a more severe item-name recognition error than Qwen3.6 35B A3B.

---

## Error 6: item name - ボックスティッシュ

### Ground truth

```json
{
  "name": "ボックスティッシュ",
  "quantity": 1,
  "unit_price": 248,
  "amount": 248
}
```

### Model output

```json
{
  "name": "ポックスティッシュ",
  "quantity": 1,
  "unit_price": 248,
  "amount": 248
}
```

### Notes

The model confused `ボ` with `ポ`, similar to the Qwen failure case.

---

## Observations

InternVL3.5-14B Q8_0 correctly extracted:

* store name
* date
* time
* subtotal
* points used
* total
* payment method
* cash received
* change
* points earned
* point balance
* many item quantities, unit prices, and amounts

However, it struggled with:

* coupon discount
* tax target amounts
* item count completeness
* Japanese item names
* lower-section receipt fields
* degraded narrow receipt layout

---

## Why this failure case matters

This failure case shows that a high-quality quantized VLM can still struggle with Japanese receipt structured extraction under degraded image conditions.

It also provides a useful comparison point:

* Qwen3.6 35B A3B Q4_K_M produced relatively small errors on this sample.
* InternVL3.5-14B Q8_0 produced larger structured extraction errors.

This suggests that `receipt_005_noisy.png` is useful for comparing model robustness, not just general OCR ability.

