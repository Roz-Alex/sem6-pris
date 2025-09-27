import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

from spark_service import analyze_dataset


app = Flask(__name__)
app.secret_key = 'bigdata-secret-key-for-flashing-messages'

SHARED_DIR = "/shared"
UPLOAD_FOLDER = os.path.join(SHARED_DIR, "upload")
RESULT_FOLDER = os.path.join(SHARED_DIR, "results")

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)


# ======= Flask ==========

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Файл не выбран')
        return redirect('/')
    file = request.files['file']
    if file.filename == '':
        flash('Файл не выбран')
        return redirect('/')
    if file and file.filename.endswith('.csv'):
        filename = f"{uuid.uuid4().hex}.csv"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('analyze', filename=filename))
    else:
        flash('Поддерживаются только CSV-файлы')
        return redirect('/')


@app.route('/analyze/<filename>')
def analyze(filename):
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(input_path):
        flash('Файл не найден')
        return redirect('/')

    result_id = str(uuid.uuid4())
    result_dir = os.path.join(app.config['RESULT_FOLDER'], result_id)
    os.makedirs(result_dir, exist_ok=True)

    try:
        results = analyze_dataset(input_path, result_dir)

        return render_template(
            'results.html',
            filename=filename,
            schema=results['schema'],
            row_count=results['row_count'],
            column_count=results['column_count'],
            sample=results['sample_html'],
            summary_file=f"{result_id}/{results['summary_file']}",
            plot_file=f"{result_id}/{results['plot_file']}" if results['plot_file'] else None,
            model_metrics=results.get('model_metrics'),  # ← добавь это
            prediction_plot=f"{results['prediction_plot']}" if results.get('prediction_plot') else None,
            _result_id=result_id
        )
    except Exception as e:
        flash(f"Ошибка при анализе: {str(e)}")
        return redirect('/')


@app.route('/results/<path:filepath>')
def download_result(filepath):
    return send_from_directory(app.config['RESULT_FOLDER'], filepath)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)