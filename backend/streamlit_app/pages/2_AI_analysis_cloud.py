import streamlit as st
st.set_page_config(page_title="AI 分析（雲端部署版本）", layout="centered")

import os
import uuid
from PIL import Image

st.title("🧠 AI 分析（雲端部署版本）")
st.write("這裡可以上傳圖片，未來將整合 AI 模型進行分析。")
st.write("🚀 Debug：頁面成功載入，請嘗試上傳圖片。")

uploaded_file = st.file_uploader("請上傳傷口圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    uploads_dir = "uploads"
    os.makedirs(uploads_dir, exist_ok=True)

    ext = os.path.splitext(uploaded_file.name)[-1].lower()
    unique_filename = f"{uuid.uuid4()}{ext}"
    file_path = os.path.join(uploads_dir, unique_filename)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    try:
        image = Image.open(file_path)
        st.image(image, caption="已上傳圖片", use_column_width=True)
    except Exception as e:
        st.error(f"圖片載入失敗：{e}")

    st.warning("⚠️ 雲端版本尚未啟用 AI 模型，請於本地端執行以進行推論分析。")

