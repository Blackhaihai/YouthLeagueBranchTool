from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash, jsonify
import os
from datetime import datetime
from PIL import Image
import pytesseract
import shutil
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'allimg'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB 上传限制
app.secret_key = 'your_secret_key'

# 添加关键词
REQUIRED_TEXTS = ["中"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

def check_text_in_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.convert('L')  # 将图像转换为灰度模式，以提高 OCR 的准确性
        text = pytesseract.image_to_string(img, lang='img')
        return all(text_word in text for text_word in REQUIRED_TEXTS)
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index')
def Bindex():
    return render_template('index.html')

@app.route('/check_name', methods=['POST'])
def check_name():
    name = request.form.get('name')
    id_number = request.form.get('id_number')
    file = request.files.get('file')

    if file:
        file_ext = os.path.splitext(file.filename)[1]
        new_filename = f"{name}{file_ext}"
        existing_file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)

        id_match = False

        if os.path.exists('imgalllog.log'):
            with open('imgalllog.log', 'r') as log_file:
                logs = log_file.readlines()
                for log in logs:
                    log_parts = log.split()
                    if log_parts[0] == name and log_parts[1] == id_number:
                        id_match = True
                        break

        if id_match:
            os.remove(existing_file_path)
            with open('imgalllog.log', 'w') as log_file:
                for log in logs:
                    if log.split()[0] != name or log.split()[1] != id_number:
                        log_file.write(log)

        return jsonify({'exists': id_match})
    else:
        return jsonify({'exists': False})



@app.route('/upload', methods=['POST'])
def upload_file():
    name = request.form.get('name')
    class_name = request.form.get('class')
    id_number = request.form.get('id_number')
    file = request.files.get('file')

    if file and allowed_file(file.filename):
        try:
            file_ext = os.path.splitext(file.filename)[1]
            new_filename = f"{name}{file_ext}"
            new_filepath = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            if os.path.exists(new_filepath):
                os.remove(new_filepath)
            file.save(new_filepath)

            if not check_text_in_image(new_filepath):
                flash('您上传不是所需截图或图片模糊请重试，上传失败。')
                os.remove(new_filepath)
                return redirect(url_for('index'))
            now = datetime.now()
            formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
            log_entry = f"{name} {id_number} {formatted_now} {new_filename}\n"
            with open('imgalllog.log', 'a') as log_file:
                log_file.write(log_entry)

            flash('文件上传成功！')
            return redirect(url_for('allimg_view'))

        except Exception as e:
            flash(f'上传过程中发生错误: {e}')
            return redirect(url_for('index'))
    else:
        flash('无效的文件格式。请上传PNG、JPG、JPEG或GIF格式的文件。')
        return redirect(url_for('index'))

@app.route('/allimg')
def allimg_view():
    logs = []
    if os.path.exists('imgalllog.log'):
        with open('imgalllog.log', 'r') as log_file:
            logs = log_file.readlines()

    return render_template('allimg.html', logs=logs)

@app.route('/allimg/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
