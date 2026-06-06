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



