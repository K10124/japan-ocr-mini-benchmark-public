\# Japan OCR Mini Benchmark - Experiment Log



\## Test 001: receipt\_001\_noisy.png



\### Document type



Synthetic Japanese convenience-store-style receipt.



\### Image file



02\_receipt\_images/receipt\_001\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Prompt



Read this Japanese receipt image and extract the following fields.



Output JSON only.

Do not use Markdown.

Do not explain anything.



Schema:

{

"document\_id": "receipt\_001",

"store\_name": "",

"date": "",

"time": "",

"total": 0

}



Rules:



\* date must be YYYY-MM-DD

\* total must be a number, not a string

\* If a field is unclear, use null



\### Ground truth



{

"store\_name": "天六ミニマート扇町通り店",

"date": "2026-06-06",

"time": "14:32:15",

"total": 1595

}



\### Model output



{

"store\_name": "天六ミニマート扇町通り店",

"date": "2026-06-06",

"time": "14:32:15",

"total": 1595

}



\### Comparison result



\* store\_name: OK

\* date: OK

\* time: OK

\* total: OK



\### Notes



The extraction was performed with Qwen3.6 35B A3B.



PaddleOCR VL 1.5 could not read or process the image in the current local setup, so it was not used for this test.



Qwen3.6 35B A3B correctly extracted all four target fields from the noisy synthetic Japanese receipt.



This receipt is still relatively easy:



\* Clean layout

\* Large text

\* No tax amount extraction

\* No item-level extraction

\* No handwritten text

\* No vertical text



Next tests should increase difficulty by adding:



\* smaller text

\* stronger rotation

\* lower contrast

\* tax extraction

\* item-level extraction

\* confusing amounts such as subtotal, total, cash received, and change



\---



\## Test 002: receipt\_002\_noisy.png



\### Document type



Synthetic Japanese drugstore-style receipt.



\### Image file



02\_receipt\_images/receipt\_002\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Prompt



Read this Japanese receipt image and extract the following fields.



Output JSON only.

Do not use Markdown.

Do not explain anything.



Schema:

{

"document\_id": "receipt\_002",

"store\_name": "",

"date": "",

"time": "",

"total": 0

}



Rules:



\* date must be YYYY-MM-DD

\* total must be a number, not a string

\* If a field is unclear, use null



\### Ground truth



{

"store\_name": "扇町ヘルスドラッグ架空店",

"date": "2026-06-07",

"time": "19:08:42",

"total": 3064

}



\### Model output



{

"store\_name": "扇町ヘルスドラッグ架空店",

"date": "2026-06-07",

"time": "19:08:42",

"total": 3064

}



\### Comparison result



\* store\_name: OK

\* date: OK

\* time: OK

\* total: OK



\### Notes



Qwen3.6 35B A3B correctly extracted all four target fields from the second noisy synthetic Japanese receipt.



This receipt is slightly harder than receipt\_001:



\* More items

\* Similar-looking amounts

\* Higher cash received amount

\* Larger change amount

\* Stronger blur, rotation, and noise



However, the task is still limited to four high-level fields:



\* store\_name

\* date

\* time

\* total



Next tests should increase difficulty by requiring:



\* item-level extraction

\* tax target extraction

\* cash received vs total distinction

\* stronger image degradation



\---



\## Test 003: receipt\_002\_noisy.png item-level extraction



\### Document type



Synthetic Japanese drugstore-style receipt.



\### Image file



02\_receipt\_images/receipt\_002\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Task



Extract item-level receipt data from the image.



Target fields:

\- store\_name

\- date

\- time

\- items

\- subtotal

\- tax\_8\_target

\- tax\_10\_target

\- total

\- payment\_method

\- cash\_received

\- change



\### Comparison result



All target fields were correctly extracted.



High-level fields:

\- store\_name: OK

\- date: OK

\- time: OK

\- subtotal: OK

\- tax\_8\_target: OK

\- tax\_10\_target: OK

\- total: OK

\- payment\_method: OK

\- cash\_received: OK

\- change: OK



Item-level fields:

\- item\_count: OK

\- item 1 name and amount: OK

\- item 2 name and amount: OK

\- item 3 name and amount: OK

\- item 4 name and amount: OK

\- item 5 name and amount: OK

\- item 6 name and amount: OK

\- item 7 name and amount: OK

\- item 8 name and amount: OK



\### Notes



Qwen3.6 35B A3B successfully extracted item-level data from the noisy synthetic Japanese drugstore-style receipt.



This result suggests that the current receipt image is still not difficult enough for Qwen3.6 35B A3B.



Next tests should make the receipt harder by adding:

\- smaller font size

\- more blur

\- stronger rotation

\- lower contrast

\- longer item names

\- similar-looking amounts

\- more confusing totals

\- possible OCR traps such as subtotal, total, cash received, change, and points



\---



\## Test 004: receipt\_003\_noisy.png item-level extraction



\### Document type



Synthetic Japanese bakery-style receipt.



\### Image file



02\_receipt\_images/receipt\_003\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Task



Extract item-level receipt data from a more degraded synthetic Japanese receipt image.



Target fields:



\* store\_name

\* date

\* time

\* items

\* subtotal

\* tax\_8\_target

\* tax\_10\_target

\* total

\* payment\_method

\* cash\_received

\* change



\### Comparison result



All target fields were correctly extracted.



High-level fields:



\* store\_name: OK

\* date: OK

\* time: OK

\* subtotal: OK

\* tax\_8\_target: OK

\* tax\_10\_target: OK

\* total: OK

\* payment\_method: OK

\* cash\_received: OK

\* change: OK



Item-level fields:



\* item\_count: OK

\* item 1 name and amount: OK

\* item 2 name and amount: OK

\* item 3 name and amount: OK

\* item 4 name and amount: OK

\* item 5 name and amount: OK

\* item 6 name and amount: OK

\* item 7 name and amount: OK

\* item 8 name and amount: OK

\* item 9 name and amount: OK

\* item 10 name and amount: OK

\* item 11 name and amount: OK

\* item 12 name and amount: OK



\### Notes



Qwen3.6 35B A3B successfully extracted all item-level data from the third noisy synthetic Japanese receipt.



This image was harder than the previous tests:



\* stronger blur

\* stronger rotation

\* lower contrast

\* more noise

\* 12 receipt items

\* confusing nearby amounts

\* total: 2,957

\* cash received: 3,000

\* change: 43

\* tax\_8\_target: 2,484

\* tax\_10\_target: 473



Despite these difficulties, Qwen3.6 35B A3B extracted all tested fields correctly.



This suggests that the current synthetic receipt format is still too easy for Qwen3.6 35B A3B.



Next tests should introduce harder real-world-like conditions:



\* smaller font size

\* narrower receipt width

\* cropped edges

\* partial shadows

\* stronger paper texture

\* thermal printer fading

\* distorted perspective

\* handwritten notes

\* receipt folding lines

\* multiple similar totals

\* point usage and discounts



\---



\## Test 005: receipt\_004\_noisy.png item-level extraction with discount and points



\### Document type



Synthetic Japanese supermarket-style receipt.



\### Image file



02\_receipt\_images/receipt\_004\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Task



Extract item-level receipt data from a heavily degraded synthetic Japanese receipt image with discount and point fields.



Target fields:



\* store\_name

\* date

\* time

\* items

\* subtotal

\* coupon\_discount

\* tax\_8\_target

\* tax\_10\_target

\* total

\* payment\_method

\* cash\_received

\* change

\* points\_earned

\* point\_balance



\### Comparison result



All target fields were correctly extracted.



High-level fields:



\* store\_name: OK

\* date: OK

\* time: OK

\* subtotal: OK

\* coupon\_discount: OK

\* tax\_8\_target: OK

\* tax\_10\_target: OK

\* total: OK

\* payment\_method: OK

\* cash\_received: OK

\* change: OK

\* points\_earned: OK

\* point\_balance: OK



Item-level fields:



\* item\_count: OK

\* item 1 name and amount: OK

\* item 2 name and amount: OK

\* item 3 name and amount: OK

\* item 4 name and amount: OK

\* item 5 name and amount: OK

\* item 6 name and amount: OK

\* item 7 name and amount: OK

\* item 8 name and amount: OK

\* item 9 name and amount: OK

\* item 10 name and amount: OK

\* item 11 name and amount: OK

\* item 12 name and amount: OK

\* item 13 name and amount: OK

\* item 14 name and amount: OK

\* item 15 name and amount: OK



\### Notes



Qwen3.6 35B A3B successfully extracted all item-level data from a heavily degraded synthetic Japanese supermarket-style receipt.



This receipt included several confusing fields:



\* subtotal: 4,421

\* coupon\_discount: 100

\* total: 4,321

\* cash\_received: 5,000

\* change: 679

\* points\_earned: 43

\* point\_balance: 2,957



The image was intentionally degraded with:



\* stronger blur

\* stronger rotation

\* lower contrast

\* partial shadow

\* vertical noise lines

\* fold-like horizontal line

\* reduced readability in the lower section



Despite these conditions, Qwen3.6 35B A3B extracted all tested fields correctly.



This suggests that the current synthetic receipt design is still too structured and too clean for this model.



Next tests should introduce more realistic failure conditions:



\* narrower receipt layout

\* smaller font size

\* cropped left or right edge

\* stronger perspective distortion

\* partially cut-off totals

\* thermal printer fading

\* duplicate amount labels

\* handwritten notes over printed text

\* item quantity and unit price columns

\* tax included / tax excluded mixed notation



\---



\## Test 006: receipt\_005\_noisy.png item-level extraction with quantity, unit price, discounts, and points



\### Document type



Synthetic Japanese narrow station-store-style receipt.



\### Image file



02\_receipt\_images/receipt\_005\_noisy.png



\### Model tested



Qwen3.6 35B A3B



\### Task



Extract item-level receipt data from a narrow, degraded synthetic Japanese receipt image with quantity, unit price, discounts, point usage, and point balance.



Target fields:



\* store\_name

\* date

\* time

\* items

\* quantity

\* unit\_price

\* amount

\* subtotal

\* coupon\_discount

\* points\_used

\* tax\_8\_target

\* tax\_10\_target

\* total

\* payment\_method

\* cash\_received

\* change

\* points\_earned

\* point\_balance



\### Comparison result



Most fields were correctly extracted, but several errors occurred.



High-level fields:



\* store\_name: OK

\* date: OK

\* time: OK

\* subtotal: OK

\* coupon\_discount: OK

\* points\_used: OK

\* tax\_8\_target: NG



&#x20; \* ground\_truth: 2597

&#x20; \* predicted: 2607

\* tax\_10\_target: NG



&#x20; \* ground\_truth: 2595

&#x20; \* predicted: 2605

\* total: OK

\* payment\_method: OK

\* cash\_received: OK

\* change: OK

\* points\_earned: OK

\* point\_balance: OK



Item-level fields:



\* item\_count: OK

\* item quantities: OK

\* item unit prices: OK

\* item amounts: OK



Item name errors:



\* item 7:



&#x20; \* ground\_truth: バウムクーヘン

&#x20; \* predicted: パウムクーヘン

\* item 9:



&#x20; \* ground\_truth: ボックスティッシュ

&#x20; \* predicted: ポックスティッシュ



\### Notes



This was the first test where Qwen3.6 35B A3B produced measurable errors.



The model correctly extracted most structured fields, including:



\* item count

\* quantities

\* unit prices

\* item amounts

\* subtotal

\* coupon discount

\* points used

\* total

\* cash received

\* change

\* points earned

\* point balance



However, it made errors in:



\* tax target amounts

\* Japanese voiced/semi-voiced sound marks in item names



The tax target errors were small but important:



\* 2,597 was read as 2,607

\* 2,595 was read as 2,605



The item name errors suggest that degraded image quality can cause confusion between similar-looking kana with dakuten or handakuten:



\* バ vs パ

\* ボ vs ポ



This result is useful because it shows that the dataset can reveal realistic OCR/VLM failure cases in Japanese receipts.



Potential next difficulty additions:



\* stronger thermal printer fading

\* lower resolution

\* handwritten correction marks

\* overlapping stamps

\* cropped totals

\* mixed tax-included and tax-excluded labels

\* duplicate subtotal and total fields

\* actual tax amount fields in addition to tax target amount fields



\---



\## Test 007: receipt\_005\_noisy.png item-level extraction with InternVL3.5-14B Q8\_0



\### Document type



Synthetic Japanese narrow station-store-style receipt.



\### Image file



02\_receipt\_images/receipt\_005\_noisy.png



\### Model tested



InternVL3.5-14B Q8\_0 GGUF



\### Runtime



LM Studio



\### Task



Extract item-level receipt data from a narrow, degraded synthetic Japanese receipt image with quantity, unit price, coupon discount, point usage, tax target fields, final payment amount, cash received, and change.



\### Comparison result



InternVL3.5-14B Q8\_0 correctly extracted many high-level fields, but produced several significant errors.



High-level fields:



\* store\_name: OK

\* date: OK

\* time: OK

\* subtotal: OK

\* coupon\_discount: NG



&#x20; \* ground\_truth: 150

&#x20; \* predicted: 1050

\* points\_used: OK

\* tax\_8\_target: NG



&#x20; \* ground\_truth: 2597

&#x20; \* predicted: 4671

\* tax\_10\_target: NG



&#x20; \* ground\_truth: 2595

&#x20; \* predicted: 2655

\* total: OK

\* payment\_method: OK

\* cash\_received: OK

\* change: OK

\* points\_earned: OK

\* point\_balance: OK



Item-level fields:



\* item\_count: NG



&#x20; \* ground\_truth: 15

&#x20; \* predicted: 13



Item name errors:



\* item 7:



&#x20; \* ground\_truth: バウムクーヘン

&#x20; \* predicted: パワムクーン

\* item 9:



&#x20; \* ground\_truth: ボックスティッシュ

&#x20; \* predicted: ポックスティッシュ



Missing items:



\* item 14:



&#x20; \* ground\_truth: 充電ケーブル短

\* item 15:



&#x20; \* ground\_truth: 靴下 無地



\### Notes



InternVL3.5-14B Q8\_0 showed weaker structured extraction performance than Qwen3.6 35B A3B Q4\_K\_M on receipt\_005\_noisy.png.



Although InternVL correctly extracted many basic fields, it struggled with:



\* coupon discount extraction

\* tax target amount extraction

\* item count completeness

\* Japanese item name recognition

\* lower-section receipt fields

\* degraded narrow receipt layout



This comparison is useful because InternVL3.5-14B was tested with Q8\_0 quantization, while the Qwen result was generated with Q4\_K\_M quantization.



Even under a higher quantization setting, InternVL3.5-14B produced more errors than Qwen3.6 35B A3B Q4\_K\_M on this sample.



This suggests that receipt\_005\_noisy.png is useful for comparing OCR/VLM structured extraction robustness across different vision-language models.



