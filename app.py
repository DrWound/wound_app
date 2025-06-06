from flask import Flask, render_template, request
from ultralytics import YOLO
import os
from PIL import Image
import uuid
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'

model = YOLO('models/best.pt')

with open("care_guidelines.json", "r", encoding="utf-8") as f:
    care_dict = json.load(f)

def get_care_advice(class_name):
    advice = care_dict.get(class_name, "未提供建議")
    return f"鄭文昌醫師建議：{advice}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    filename = None

    if request.method == "POST":
        file = request.files['image']
        if file:
            ext = file.filename.split('.')[-1]
            filename = f"{uuid.uuid4()}.{ext}"
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            results = model(file_path)[0]
            detections = results.boxes
            names = model.names

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
