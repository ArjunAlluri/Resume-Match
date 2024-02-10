from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import fitz

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

TECHNICAL_SKILLS_KEYWORD = "TECHNICAL SKILLS"
WORK_EXPERIENCE_KEYWORD = "WORK EXPERIENCE"


@app.route('/')
def hello():
    return 'hello'


@app.route('/preprocess', methods=['POST'])
def preprocess():

    if 'resume' not in request.files:
        return jsonify({'error': 'No file part'})

    resume = request.files['resume']
    if resume.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = resume.filename
    resume_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    resume.save(resume_path)

    # Extracting text
    try:
        text = extract_text_from_pdf(resume_path)
    except Exception as e:
        return jsonify({'error': f'Error extracting text: {e}'})

    # Extracting skills from technical skills section
    technical_skills_section = extract_technical_skills_section(text)
    if technical_skills_section:
        skills_mentioned = extract_skills_from_section(
            technical_skills_section)
        print("Skills mentioned:", skills_mentioned)
    else:
        skills_mentioned = []

    return jsonify({'message': 'Skills extracted successfully', 'skills_mentioned': skills_mentioned})


def extract_text_from_pdf(pdf_path):
    text = ""
    with fitz.open(pdf_path) as pdf_file:
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
    return text


def extract_technical_skills_section(text):
    start_index = text.find(TECHNICAL_SKILLS_KEYWORD)
    if start_index != -1:
        end_index = text.find(WORK_EXPERIENCE_KEYWORD, start_index)
        if end_index != -1:
            return text[start_index:end_index]
    return None


def extract_skills_from_section(section):
    lines = section.split('\n')
    skills = []
    for line in lines:
        if line.strip() and ':' not in line:
            skills.extend(line.strip().split(','))
    return skills[1:]


if __name__ == '__main__':
    app.run(debug=True, port=8000)
