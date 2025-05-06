import streamlit as st
from PIL import Image
import os
import uuid

st.title("🧠 AI 分析 (雲端部署版本)")
st.write("這裡可以上傳圖片，未來將整合 AI 模型進行分析。")

# 上傳圖片
uploaded_file = st.file_uploader("請上傳傷口圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 建立 uploads 資料夾
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    # 儲存圖片
    unique_filename = f"{uuid.uuid4()}_{uploaded_file.name}"
    file_path = os.path.join(uploads_dir, unique_filename)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # 顯示圖片
    image = Image.open(file_path)
    st.image(image, caption="已上傳圖片", use_column_width=True)

    # 模擬分析結果（未連結模型）
    st.info("⚠️ 雲端版本尚未啟用 AI 模型，請於本地端執行以進行推論分析。")
