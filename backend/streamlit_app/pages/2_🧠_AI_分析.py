import streamlit as st
from ultralytics import YOLO
from PIL import Image
import os
import shutil

# 設定模型路徑
MODEL_PATH = "backend/streamlit_app/models/best.pt"
UPLOAD_DIR = "uploads"
RESULT_DIR = "static/output"

# 初始化模型
@st.cache_resource
def load_model():
    return YOLO(MODEL_PATH)

model = load_model()

# 頁面標題
st.title("🧠 AI 分析")
st.write("請上傳傷口照片，系統會使用 AI 模型進行分析並顯示結果。")

# 建立上傳與輸出資料夾
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

# 上傳圖片
uploaded_file = st.file_uploader("請選擇或拖曳一張圖片", type=["jpg", "jpeg", "png"])

if uploaded_file:
    # 儲存上傳圖片
    img_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(img_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(Image.open(img_path), caption="原始圖片", use_column_width=True)

    # 模型推論
    with st.spinner("正在分析中..."):
        results = model.predict(img_path, save=True, project='static', name='output', exist_ok=True)
        result_img_path = results[0].save_path

    st.success("分析完成 ✅")

    # 顯示預測結果圖片
    st.image(result_img_path, caption="AI 分析結果", use_column_width=True)

    # 顯示類別與信心指數
    st.subheader("分析細節")
    for box in results[0].boxes:
        cls = model.names[int(box.cls[0])]
        conf = float(box.conf[0])
        st.write(f"- 類別：**{cls}**，信心指數：{conf:.2f}")
