# Wound AI Detection App (Gradio版)

本應用為醫療團隊設計之 AI 傷口辨識工具，透過 Gradio 界面，支援直接上傳傷口照片，自動辨識分類 + 照護建議。

**主要功能：**
- 傷口分類 (W1～W4)
- 多區塊標註（polygon）
- 顯示粗線條 + 大字說明，方便臨床觀看
- 自動對應照護建議 (care_guidelines.json)

**操作說明：**
- 上傳傷口照片
- AI 自動辨識傷口區塊 + 類別
- 生成視覺化結果 + 照護建議文字

**部署環境：**
- Gradio 4.x
- YOLOv8 模型 (models/best.pt)
- Python >= 3.10
- Hugging Face Spaces 部署最佳化

**目錄結構：**
```
├── app.py # 主程式
├── models/best.pt # AI 模型
├── care_guidelines.json # 照護建議對應檔
├── requirements.txt # 依賴套件
├── README.md # 本說明文件
├── log/ # 使用紀錄 (自動生成)
```
**作者:** 鄭文昌 醫師  
**應用用途:** 團隊內部與病患照護使用，教育與研究推廣，非商業化用途。

---

🚀 **Deploy to Hugging Face Spaces**  
- 建議直接將此專案上傳 GitHub → 連接 HF Space → 自動 build 即可。
- HF Space 會自動使用 `app.py` 啟動 Gradio App。

---

**注意事項：**
- 部署前確認 `models/best.pt` 已放入 models 資料夾。
- 若有更新 `care_guidelines.json`，重新 deploy 即可。
