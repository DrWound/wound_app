# wound_app/add.py（支援互動模式與批次導入）
import argparse
import json
import os
import csv

EXPLANATION_FILE = 'wound_explanations.json'

def set_explanation(filename, text):
    if not os.path.exists(EXPLANATION_FILE):
        with open(EXPLANATION_FILE, 'w') as f:
            json.dump({}, f)

    with open(EXPLANATION_FILE, 'r') as f:
        explanations = json.load(f)

    explanations[filename] = {"explanation": text}

    with open(EXPLANATION_FILE, 'w') as f:
        json.dump(explanations, f, indent=2, ensure_ascii=False)

    print(f"✅ 已儲存解說：{filename} → {text}")

def batch_import(csv_path):
    if not os.path.exists(csv_path):
        print("❌ 找不到指定的 CSV 檔案")
        return

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        for row in reader:
            if len(row) >= 2:
                filename, text = row[0].strip(), row[1].strip()
                set_explanation(filename, text)
        print("📦 批次匯入完成")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="新增醫師對照片的說明")
    parser.add_argument("--filename", help="圖檔名稱，例如 IMG_9028.JPG")
    parser.add_argument("--text", help="醫師解說文字")
    parser.add_argument("--csv", help="CSV 批次匯入檔案路徑")
    args = parser.parse_args()

    if args.csv:
        batch_import(args.csv)
    else:
        if not args.filename:
            args.filename = input("請輸入圖片檔名（例如 IMG_9028.JPG）：")
        if not args.text:
            args.text = input("請輸入解說內容：")
        set_explanation(args.filename, args.text)
