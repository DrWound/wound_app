# wound_app/app.py（擴充版）
from flask import Flask, request, render_template, send_from_directory, redirect, url_for, Response, session
import os
import shutil
import uuid
import json

app = Flask(__name__)
app.secret_key = 'super_secret_key'

UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'static/output'
ANNOTATED_FOLDER = 'static/sample_annotated'
EXPLANATION_FILE = 'wound_explanations.json'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ANNOTATED_FOLDER, exist_ok=True)
if not os.path.exists(EXPLANATION_FILE):
    with open(EXPLANATION_FILE, 'w') as f:
        json.dump({}, f)

def dummy_ai_inference(uploaded_filename):
    basename = os.path.basename(uploaded_filename)
    result_img_name = "result_" + basename
    result_img_path = os.path.join(OUTPUT_FOLDER, result_img_name)
    possible_annotated_path = os.path.join(ANNOTATED_FOLDER, basename)

    if os.path.exists(possible_annotated_path):
        shutil.copy(possible_annotated_path, result_img_path)
        return result_img_name, "AI 檢測結果：此區域為腐肉（壞死組織），需清創處理。"
    else:
        return None, "⚠️ 尚未建立對應的標註圖片，請確認上傳圖檔名稱與人工標示圖一致。"

def get_explanation(filename):
    with open(EXPLANATION_FILE, 'r') as f:
        explanations = json.load(f)
    entry = explanations.get(filename, {})
    if isinstance(entry, dict):
        return entry.get("explanation", "尚無醫師解說。")
    else:
        return entry

def set_explanation(filename, text):
    with open(EXPLANATION_FILE, 'r') as f:
        explanations = json.load(f)
    explanations[filename] = {"explanation": text}
    with open(EXPLANATION_FILE, 'w') as f:
        json.dump(explanations, f, indent=2, ensure_ascii=False)

def archive_to_csv():
    with open(EXPLANATION_FILE, 'r') as f:
        archive_data = json.load(f)
    return archive_data

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        files = request.files.getlist("images")
        wound_location = request.form.get("wound_location", "")
        results = []

        for file in files:
            if file:
                original_filename = file.filename
                unique_filename = str(uuid.uuid4()) + "_" + original_filename
                saved_path = os.path.join(UPLOAD_FOLDER, unique_filename)
                file.save(saved_path)

                result_img_name, _ = dummy_ai_inference(original_filename)
                explanation = get_explanation(original_filename)
                results.append({
                    'original': url_for('uploaded_file', filename=unique_filename),
                    'result': url_for('result_file', filename=result_img_name) if result_img_name else None,
                    'explanation': explanation,
                    'filename': original_filename
                })

        return render_template("index.html", results=results)

    return render_template("index.html")

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/static/output/<filename>")
def result_file(filename):
    return send_from_directory(OUTPUT_FOLDER, filename)

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "doctor" and password == "1234":
            session['logged_in'] = True
            return redirect(url_for('add_explanation'))
        else:
            error = "帳號或密碼錯誤"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.route("/add_explanation", methods=["GET", "POST"])
def add_explanation():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    message = ""
    if request.method == "POST":
        filename = request.form.get("filename")
        explanation = request.form.get("explanation")
        if filename and explanation:
            set_explanation(filename, explanation)
            message = f"已為 {filename} 儲存解說內容。"
    return render_template("add_explanation.html", message=message)

@app.route("/cases")
def cases():
    with open(EXPLANATION_FILE, 'r') as f:
        explanation_data = json.load(f)

    case_list = []
    for filename, data in explanation_data.items():
        if isinstance(data, dict):
            explanation = data.get("explanation", "")
        else:
            explanation = data
        case_list.append({
            'filename': filename,
            'explanation': explanation
        })

    return render_template("cases.html", cases=case_list)

@app.route("/archive")
def archive():
    archive_data = archive_to_csv()
    return render_template("archive.html", archive=archive_data)

@app.route("/export_archive")
def export_archive():
    if not os.path.exists(EXPLANATION_FILE):
        return "No data to export", 404

    with open(EXPLANATION_FILE, 'r') as f:
        archive_data = json.load(f)

    def generate():
        yield "filename,explanation\n"
        for filename, data in archive_data.items():
            if isinstance(data, dict):
                explanation = data.get("explanation", "").replace("\n", " ")
            else:
                explanation = str(data).replace("\n", " ")
            yield f"{filename},{explanation}\n"

    return Response(generate(), mimetype='text/csv',
                    headers={"Content-Disposition": "attachment;filename=wound_archive.csv"})

@app.route("/patient", methods=["GET", "POST"])
def patient():
    result = None
    message = ""

    if request.method == "POST":
        filename = request.form.get("filename")
        explanation = get_explanation(filename)

        annotated_path = os.path.join(OUTPUT_FOLDER, "result_" + filename)
        annotated_url = url_for('result_file', filename="result_" + filename) if os.path.exists(annotated_path) else None

        if explanation:
            result = {"explanation": explanation, "annotated_url": annotated_url}
        else:
            message = "找不到該檔名的分析結果，請確認拼字或稍後再試。"

    return render_template("patient.html", result=result, message=message)

if __name__ == "__main__":
    app.run(debug=True)
