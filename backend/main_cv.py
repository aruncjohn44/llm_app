from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os, json
import PyPDF2
import docx
from cv_analyzer import extract_resume_info, extract_jobdesc_info

app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# Function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        pdf_reader = PyPDF2.PdfReader(f)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    return '\n'.join([paragraph.text for paragraph in doc.paragraphs])

# Route to render the main page
@app.route('/')
def index():
    return render_template('index_cv.html')

# Route to handle CV and JD comparison
@app.route('/compare_cv', methods=['POST'])
def compare_cv():
    if 'cv' not in request.files or 'jobDescription' not in request.form:
        return jsonify({"error": "Missing CV file or Job Description"}), 400

    cv_file = request.files['cv']
    job_description = request.form['jobDescription']

    # Check if the file is valid
    if cv_file and allowed_file(cv_file.filename):
        # Save the CV file securely
        filename = secure_filename(cv_file.filename)
        cv_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        cv_file.save(cv_path)
        # Extract text from the CV file
        if filename.endswith('.pdf'):
            cv_text = extract_text_from_pdf(cv_path)
        elif filename.endswith('.docx'):
            cv_text = extract_text_from_docx(cv_path)
        else:
            return jsonify({"error": "Unsupported file type"}), 400
    else:
        return jsonify({"error": "Invalid file format"}), 400
    
    resume_info = extract_resume_info(cv_text)
    job_description_info = extract_jobdesc_info(job_description)

    resume_json = json.loads(resume_info)
    jd_json = json.loads(resume_info)

    print(resume_json)
    print(jd_json)
    # Placeholder for integrating LLM-based logic to compare CV with JD
    # Here you'd load the CV content, compare with job description using LLM, etc.
    # Example dummy response:
    match_score = 75  # Example score
    missing_keywords = ["Python", "Data Pipelines", "Machine Learning"]
    suggestions = "Consider adding more detail about your experience in cloud deployment and CI/CD."

    # Send back the response as JSON
    return jsonify({
        "match_score": match_score,
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    })

if __name__ == '__main__':
    app.run(debug=True)
