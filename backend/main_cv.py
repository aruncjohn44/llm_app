from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os, json
import PyPDF2
import docx
import ast
from cv_analyzer import extract_resume_info, extract_jobdesc_info, match_skills, llm_compare_cv_to_job_description
from utils import create_hash, check_file_exists, save_to_cache, read_from_file
from docker.docker_postgres.postgres_code import connection_params, connect_to_db, insert_record, record_exists, print_all_records

CACHE_DIR = 'doctemp'
app = Flask(__name__)

# Configurations
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'doc', 'docx'}

# create postgres db connection object
conn = connect_to_db(connection_params)

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
    
    # Check if the record already exists (resume_text_hash and jd_text_hash combination)
    print_all_records(conn)
    existing_record = record_exists(conn, cv_text, job_description)
    print('########-------------\n', existing_record, '\n\n###########------------')
    if existing_record:
        print("Record with the same resume and job description hash already exists. Skipping insertion.")
        llm_match_scores, resume_info , job_description_info = existing_record

    else:
        print("Calling llm again for match scores, and cv/jd info extraction")
        # llm_match_scores = llm_compare_cv_to_job_description(cv_text, job_description).replace('json', '').replace('```', '')
        # resume_info = extract_resume_info(cv_text).replace('json', '').replace('```', '')
        # job_description_info = extract_jobdesc_info(job_description).replace('json', '').replace('```', '')
        # insert_record(conn, cv_text, job_description, llm_match_scores, resume_info, job_description_info)

    
    # Create hash

    
    # check cache
    # hash_text_jd = create_hash(job_description)
    # hash_filename = hash_text_jd + '.txt'
    # filename = filename + '.txt'
    # score_file_name = hash_filename + filename + '.txt'

    # if check_file_exists(CACHE_DIR, filename) and check_file_exists(CACHE_DIR, hash_filename):
    #     resume_info = read_from_file(CACHE_DIR, filename).replace('json', '').replace('```', '')
    #     job_description_info = read_from_file(CACHE_DIR, hash_filename).replace('json', '').replace('```', '')
    #     llm_match_scores = read_from_file(CACHE_DIR, score_file_name)
    # else:
    #     resume_info = extract_resume_info(cv_text).replace('json', '').replace('```', '')
    #     job_description_info = extract_jobdesc_info(job_description).replace('json', '').replace('```', '')

    #     save_to_cache(filename, resume_info, CACHE_DIR)
    #     save_to_cache(hash_filename, job_description_info, CACHE_DIR)
    #     save_to_cache(score_file_name, llm_match_scores, CACHE_DIR)

    print(llm_match_scores)

    resume_json = json.loads(resume_info)
    jd_json = json.loads(job_description_info)

    # Integrating LLM-based logic to compare CV with JD

    matched_skills, missing_skills = match_skills(resume_json, jd_json)
   
    match_score = 75  # Example score
    suggestions = "Consider adding more detail about your experience in cloud deployment and CI/CD."

    # Send back the response as JSON
    return jsonify({
        "match_score": match_score,
        "matching_keywords": matched_skills,
        "missing_keywords": missing_skills,
        "suggestions": suggestions
    })
6464
if __name__ == '__main__':
    app.run(debug=True)