import os
import json
import uuid
from flask import Flask, render_template, request
from ultralytics import YOLO
from PIL import Image
from wound_detector import WoundDetector  # ✅ 必加這行

# 初始化 Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# 載入模型
model = YOLO('models/best.pt')

# 載入照護建議
with open("care_guidelines.json", "r", encoding="utf-8") as f:
    care_dict = json.load(f)

def get_care_advice(class_name):
    """取得照護建議"""
    advice = care_dict.get(class_name, "未提供建議")
    return f"鄭文昌醫師建議：{advice}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = None

    if request.method == "POST":
        file = request.files['image']
        if file:
            # 儲存上傳圖片
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # 執行 YOLO 預測
            results = model(file_path)[0]
            detections = results.boxes
            names = model.names

            # 處理結果
            labels = []
            for box in detections:
                class_id = int(box.cls[0])
                class_name = names[class_id]
                conf = round(float(box.conf[0]), 2)
                labels.append({
                    "class": class_name,
                    "confidence": conf,
                    "advice": get_care_advice(class_name)
                })

            result = {"labels": labels}

    return render_template("index.html", result=result, filename=filename)

# ✅ 重要！Render 要綁 PORT 變數
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
