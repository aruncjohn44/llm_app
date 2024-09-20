from flask import Flask, render_template, request, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
import os

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

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

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
    else:
        return jsonify({"error": "Invalid file format"}), 400

    # Placeholder for integrating LLM-based logic to compare CV with JD
    # Here you'd load the CV content, compare with job description using LLM, etc.
    # Example dummy response:
    match_score = 85  # Example score
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
