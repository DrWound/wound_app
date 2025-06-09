import gradio as gr
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image
import json

# 載入模型
model = YOLO('models/best.pt')

# 載入照護建議
with open("care_guidelines.json", "r", encoding="utf-8") as f:
    care_dict = json.load(f)

def get_care_advice(class_name):
    advice = care_dict.get(class_name, "未提供建議")
    return f"鄭文昌醫師建議：{advice}"

# 主推論 function
def predict_image(image):

    # 預測
    results = model.predict(image, save=False, conf=0.25)[0]

    # 讀入原圖，轉換格式 (BGR → RGB)
    orig_img = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    img_rgb = orig_img.copy()

    # 獲取檢測結果
    names = model.names
    polygons = results.masks.xy if results.masks is not None else []
    classes = results.boxes.cls.tolist()
    scores = results.boxes.conf.tolist()
    boxes = results.boxes.xyxy.cpu().numpy()

    labels = []

    for i, (cls_id, conf) in enumerate(zip(classes, scores)):
        class_name = names[int(cls_id)]
        advice = get_care_advice(class_name)
        label_text = f"{class_name} {conf:.2f}"

        # 如果有 polygon mask → 畫 polygon
        if len(polygons) > i and len(polygons[i]) > 0:
            poly = np.array(polygons[i], dtype=np.int32)
            cv2.polylines(img_rgb, [poly], isClosed=True, color=(255, 255, 255), thickness=3)
            pt = poly[0]
        else:
            # fallback → 畫 box fake polygon
            xyxy = boxes[i].astype(int)
            pts = np.array([[xyxy[0], xyxy[1]], [xyxy[2], xyxy[1]],
                            [xyxy[2], xyxy[3]], [xyxy[0], xyxy[3]]], np.int32)
            cv2.polylines(img_rgb, [pts], isClosed=True, color=(255, 255, 255), thickness=3)
            pt = pts[0]

        # 畫 label 文字 → 白字 + 黑邊
        cv2.putText(img_rgb, label_text, (int(pt[0]), int(pt[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 0), 4, cv2.LINE_AA)  # 黑邊
        cv2.putText(img_rgb, label_text, (int(pt[0]), int(pt[1]) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2, cv2.LINE_AA)  # 白字

        # 組文字說明
        label_info = {
            "class": class_name,
            "confidence": round(conf, 2),
            "advice": advice
        }
        labels.append(label_info)

    # 準備顯示文字說明
    advice_text = ""
    for label in labels:
        advice_text += f"- **{label['class']}** (信心值: {label['confidence']})\n建議：{label['advice']}\n\n"

    # 回傳 PIL Image 格式
    img_rgb_show = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb_show)

    return image, img_pil, advice_text

# Gradio UI
demo = gr.Interface(
    fn=predict_image,
    inputs=gr.Image(label="上傳傷口圖片，系統自動辨識傷口並提供照護建議", type="pil"),
    outputs=[
        gr.Image(label="原圖"),
        gr.Image(label="框出傷口結果 (Polygon + Box 版)"),
        gr.Markdown(label="建議文字")
    ],
    title="AI 傷口辨識系統 - Polygon + Box 有框版",
    description="鄭文昌醫師 傷口照護 AI 系統"
)

if __name__ == "__main__":
    demo.launch()
