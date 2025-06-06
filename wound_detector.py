from ultralytics import YOLO
from PIL import Image, ImageDraw, ImageFont
import json
import os
from datetime import datetime


class WoundDetector:
    def __init__(self, model_path="models/best.pt", guideline_path="care_guidelines.json", conf_threshold=0.25, min_area=2000):
        self.model = YOLO(model_path)
        with open(guideline_path, "r", encoding="utf-8") as f:
            self.guidelines = json.load(f)
        self.conf_threshold = conf_threshold
        self.min_area = min_area

    def detect(self, image: Image.Image, save_json=False, json_path="output.json"):
        try:
            results = self.model(image)
        except Exception as e:
            return {"error": f"模型推論失敗: {str(e)}"}, image

        detections = []
        annotated_img = image.copy()
        draw = ImageDraw.Draw(annotated_img)

        for r in results:
            for box in r.boxes:
                confidence = float(box.conf[0])
                if confidence < self.conf_threshold:
                    continue

                class_id = int(box.cls[0])
                class_name = self.model.names[class_id]
                guideline = self.guidelines.get(class_name, {})

                xyxy = box.xyxy[0].tolist()
                width = xyxy[2] - xyxy[0]
                height = xyxy[3] - xyxy[1]
                if width * height < self.min_area:
                    continue

                draw.rectangle(xyxy, outline="white", width=6)
                draw.text((xyxy[0], xyxy[1]), f"{class_name}_{round(confidence, 2)}", fill="white")

                detections.append({
                    "class": class_name,
                    "confidence": round(confidence, 2),
                    "description": guideline.get("label", "未知分類"),
                    "healing_mechanism": guideline.get("mechanism", ""),
                    "care_advice": guideline.get("advice", ""),
                    "care_frequency": guideline.get("frequency", "")
                })

        result_dict = {
            "timestamp": datetime.now().isoformat(),
            "detections": detections
        }

        if save_json:
            try:
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(result_dict, f, ensure_ascii=False, indent=2)
            except Exception as e:
                result_dict["error"] = f"無法儲存 JSON: {str(e)}"

        return result_dict, annotated_img
