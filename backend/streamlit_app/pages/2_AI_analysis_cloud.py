import streamlit as st
from PIL import Image
import io

st.set_page_config(page_title="AI 分析（雲端部署版本）", layout="centered")

st.title("🧠 AI 分析（雲端部署版本）")
st.write("這裡可以上傳圖片，未來將整合 AI 模型進行分析。")

# 上傳圖片
uploaded_file = st.file_uploader("請上傳傷口圖片", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # 使用 BytesIO 直接讀入圖片，不寫入磁碟
    image = Image.open(io.BytesIO(uploaded_file.read()))
    st.image(image, caption="已上傳圖片", use_column_width=True)

    # 提示尚未接入模型
    st.warning("⚠️ 雲端版本尚未啟用 AI 模型，請於本地端執行以進行推論分析。")

