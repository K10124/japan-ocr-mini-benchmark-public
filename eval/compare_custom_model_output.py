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

        for field in ["quantity", "unit_price", "amount"]:
            if field in gt_item or field in pred_item:
                gt_value = normalize_amount(gt_item.get(field))
                pred_value = normalize_amount(pred_item.get(field))

                if gt_value == pred_value:
                    print(f"[OK] {field}: {pred_value}")
                else:
                    print(f"[NG] {field}")
                    print(f"  ground_truth: {gt_value}")
                    print(f"  predicted   : {pred_value}")


def main():
    if len(sys.argv) < 3:
        print("Usage:")
        print("python .\\04_eval\\compare_custom_model_output.py receipt_005 .\\04_eval\\model_output.json")
        return

    receipt_id = sys.argv[1]
    pred_file = sys.argv[2]

    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    gt_path = os.path.join(
        project_dir,
        "03_ground_truth",
        f"{receipt_id}_ground_truth.json"
    )

    with open(gt_path, "r", encoding="utf-8") as f:
        gt = json.load(f)

    with open(pred_file, "r", encoding="utf-8") as f:
        pred = json.load(f)

    print(f"=== Custom Model Comparison: {receipt_id} ===")
    print(f"Model output file: {pred_file}")

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