from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tempfile
import os

app = Flask(__name__)

# 📌 Extract Text from PDF
def extract_text_from_pdf(file_path):
    pdf = PdfReader(file_path)
    text = "".join([page.extract_text() or "" for page in pdf.pages])
    return text.strip()

# 📌 Rank Resume with Job Description
def rank_resume(job_description, resume_text):
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    score = cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100
    return round(score, 2)

# 📌 API Endpoint for Resume Screening
@app.route("/screen_resume", methods=["POST"])
def screen_resume():
    if 'job_description' not in request.form or 'resume' not in request.files:
        return jsonify({"error": "Missing job_description or resume file"}), 400

    job_description = request.form['job_description']
    resume_file = request.files['resume']

    # Save uploaded resume temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        resume_file.save(temp.name)
        resume_text = extract_text_from_pdf(temp.name)
        os.unlink(temp.name)  # Clean up temp file

    match_score = rank_resume(job_description, resume_text)

    return jsonify({"match_score": match_score})

# 📌 Health check endpoint (optional)
@app.route("/", methods=["GET"])
def home():
    return "Resume Screener API is running!", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
