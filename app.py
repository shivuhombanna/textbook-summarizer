from flask import Flask, request, render_template
from models.ai_model import generate_summary, generate_questions
import os
import tempfile

import PyPDF2
from docx import Document

app = Flask(__name__)

def extract_text_from_pdf(path):
    text = ""
    with open(path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text.strip()

def extract_text_from_docx(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs]).strip()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    
    pasted_text = request.form.get('user_text', '').strip()
    uploaded_file = request.files.get('file_upload')

    extracted_text = pasted_text
    # If a file is uploaded, use it instead
    if uploaded_file and uploaded_file.filename:
        filename = uploaded_file.filename.lower()

        # Save as temp file
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name

        if filename.endswith('.pdf'):
            extracted_text = extract_text_from_pdf(tmp_path)
        elif filename.endswith('.txt'):
            extracted_text = open(tmp_path, 'r', encoding='utf-8').read().strip()
        elif filename.endswith('.docx'):
            extracted_text = extract_text_from_docx(tmp_path)
        else:
            return render_template('index.html', error="Unsupported file type. Upload PDF, TXT, or DOCX.")

    if not extracted_text:
        return render_template('index.html', error="No text detected. Paste text or upload a file.")

    summary = generate_summary(extracted_text)
    questions = generate_questions(extracted_text)

    return render_template(
        'result.html',
        summary=summary,
        questions=questions,
        original=extracted_text
    )

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )
