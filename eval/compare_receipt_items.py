import json
import os
import re
import sys


def normalize_text(value):
    if value is None:
        return None
    return re.sub(r"\s+", "", str(value))


def normalize_amount(value):
    if value is None:
        return None

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        return int(value)

    text = str(value)
    text = text.replace("¥", "")
    text = text.replace(",", "")
    text = text.replace("P", "")
    text = text.strip()

    try:
        return int(text)
    except ValueError:
        return value


def compare_text(field_name, gt, pred):
    gt_value = gt.get(field_name)
    pred_value = pred.get(field_name)

    if normalize_text(gt_value) == normalize_text(pred_value):
        print(f"[OK] {field_name}: {pred_value}")
    else:
        print(f"[NG] {field_name}")
        print(f"  ground_truth: {gt_value}")
        print(f"  predicted   : {pred_value}")


def compare_amount(field_name, gt, pred):
    gt_value = normalize_amount(gt.get(field_name))
    pred_value = normalize_amount(pred.get(field_name))

    if gt_value == pred_value:
        print(f"[OK] {field_name}: {pred_value}")
    else:
        print(f"[NG] {field_name}")
        print(f"  ground_truth: {gt_value}")
        print(f"  predicted   : {pred_value}")


def compare_optional_amount(field_name, gt, pred):
    if field_name in gt or field_name in pred:
        compare_amount(field_name, gt, pred)


def compare_items(gt_items, pred_items):
    print("")
    print("=== Item Comparison ===")

    if not isinstance(pred_items, list):
        print("[NG] items is not a list")
        return

    if len(gt_items) == len(pred_items):
        print(f"[OK] item_count: {len(pred_items)}")
    else:
        print("[NG] item_count")
        print(f"  ground_truth: {len(gt_items)}")
        print(f"  predicted   : {len(pred_items)}")

    max_len = max(len(gt_items), len(pred_items))

    for i in range(max_len):
        print("")
        print(f"--- item {i + 1} ---")

        if i >= len(gt_items):
            print("[NG] extra predicted item")
            print(f"  predicted: {pred_items[i]}")
            continue

        if i >= len(pred_items):
            print("[NG] missing predicted item")
            print(f"  ground_truth: {gt_items[i]}")
            continue

        gt_item = gt_items[i]
        pred_item = pred_items[i]

        gt_name = gt_item.get("name")
        pred_name = pred_item.get("name")

        if normalize_text(gt_name) == normalize_text(pred_name):
            print(f"[OK] name: {pred_name}")
        else:
            print("[NG] name")
            print(f"  ground_truth: {gt_name}")
            print(f"  predicted   : {pred_name}")

        if "quantity" in gt_item or "quantity" in pred_item:
            gt_quantity = normalize_amount(gt_item.get("quantity"))
            pred_quantity = normalize_amount(pred_item.get("quantity"))

            if gt_quantity == pred_quantity:
                print(f"[OK] quantity: {pred_quantity}")
            else:
                print("[NG] quantity")
                print(f"  ground_truth: {gt_quantity}")
                print(f"  predicted   : {pred_quantity}")

        if "unit_price" in gt_item or "unit_price" in pred_item:
            gt_unit_price = normalize_amount(gt_item.get("unit_price"))
            pred_unit_price = normalize_amount(pred_item.get("unit_price"))

            if gt_unit_price == pred_unit_price:
                print(f"[OK] unit_price: {pred_unit_price}")
            else:
                print("[NG] unit_price")
                print(f"  ground_truth: {gt_unit_price}")
                print(f"  predicted   : {pred_unit_price}")

        gt_amount = normalize_amount(gt_item.get("amount"))
        pred_amount = normalize_amount(pred_item.get("amount"))

        if gt_amount == pred_amount:
            print(f"[OK] amount: {pred_amount}")
        else:
            print("[NG] amount")
            print(f"  ground_truth: {gt_amount}")
            print(f"  predicted   : {pred_amount}")


def main():
    if len(sys.argv) >= 2:
        receipt_id = sys.argv[1]
    else:
        receipt_id = "receipt_005"

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    gt_path = os.path.join(
        project_dir,
        "ground_truth",
        f"{receipt_id}_ground_truth.json"
    )

    pred_path = os.path.join(
        project_dir,
        "model_outputs",
        f"{receipt_id}_ocr_output_items.json"
    )

    with open(gt_path, "r", encoding="utf-8") as f:
        gt = json.load(f)

    with open(pred_path, "r", encoding="utf-8") as f:
        pred = json.load(f)

    print(f"=== Receipt Item-Level Comparison: {receipt_id} ===")

    compare_text("store_name", gt, pred)
    compare_text("date", gt, pred)
    compare_text("time", gt, pred)

    compare_amount("subtotal", gt, pred)
    compare_optional_amount("coupon_discount", gt, pred)
    compare_optional_amount("points_used", gt, pred)

    compare_amount("tax_8_target", gt, pred)
    compare_amount("tax_10_target", gt, pred)
    compare_amount("total", gt, pred)

    compare_text("payment_method", gt, pred)
    compare_amount("cash_received", gt, pred)
    compare_amount("change", gt, pred)

    compare_optional_amount("points_earned", gt, pred)
    compare_optional_amount("point_balance", gt, pred)

    compare_items(gt.get("items", []), pred.get("items", []))


if __name__ == "__main__":
    main()
