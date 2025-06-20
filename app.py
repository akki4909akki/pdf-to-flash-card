
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pdfminer.high_level import extract_text
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def generate_flashcards(text):
    flashcards = []
    lines = text.split('\n')
    for line in lines:
        if ':' in line:
            q, a = line.split(':', 1)
            flashcards.append({'question': q.strip(), 'answer': a.strip()})
    return flashcards

@app.route('/', methods=['GET', 'POST'])
def index():
    flashcards = []
    if request.method == 'POST':
        file = request.files['pdf']
        if file.filename.endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            text = extract_text(filepath)
            flashcards = generate_flashcards(text)

    return render_template('index.html', flashcards=flashcards)

if __name__ == '__main__':
    app.run(debug=True)
