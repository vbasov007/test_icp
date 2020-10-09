import os
from flask import Flask, render_template, request, send_file, redirect
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'tmp'
DOWNLOAD_FOLDER = 'tmp'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


def create_working_folders():

    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    if not os.path.exists(app.config['DOWNLOAD_FOLDER']):
        os.makedirs(app.config['DOWNLOAD_FOLDER'])


@app.route('/')
def start():
    create_working_folders()

    return render_template("templ.html", result="not ready", list_dir=os.listdir(app.config['DOWNLOAD_FOLDER']))


@app.route('/read_file', methods=['POST'])
def read_file():
    file_path = request.form['file_path']

    try:
        with open(file_path, "r") as f:
            display_text = f.readline()
    except Exception as e:
        display_text = str(e)

    return render_template('templ.html', file_path=file_path, result=display_text)


@app.route('/download', methods=['POST'])
def download():
    file_name = request.form['download_file']
    try:
        return send_file(os.path.join(app.config['DOWNLOAD_FOLDER'], file_name), as_attachment=True)
    except Exception as e:
        return str(e)


@app.route('/upload', methods=['POST'])
def upload():
    upload_file = request.files['upload_file']

    filename = secure_filename(upload_file.filename)

    try:
        upload_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    except Exception as e:
        return str(e)

    return redirect('/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
