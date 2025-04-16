from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import base64
import tempfile
import os

app = Flask(__name__)

def extract_text_from_pdf(file_path):
    pdf = PdfReader(file_path)
    text = "".join([page.extract_text() or "" for page in pdf.pages])
    return text.strip()

def rank_resume(job_description, resume_text):
    documents = [job_description, resume_text]
    vectorizer = TfidfVectorizer().fit_transform(documents)
    vectors = vectorizer.toarray()
    score = cosine_similarity([vectors[0]], [vectors[1]])[0][0] * 100
    return round(score, 2)

@app.route("/screen_resume", methods=["POST"])
def screen_resume():
    data = request.get_json()
    job_description = data.get('job_description')
    resume_base64 = data.get('resume_base64')

    if not job_description or not resume_base64:
        return jsonify({"error": "Missing job_description or resume_base64"}), 400

    # Decode PDF base64 to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp:
        temp.write(base64.b64decode(resume_base64))
        resume_text = extract_text_from_pdf(temp.name)
        os.unlink(temp.name)

    match_score = rank_resume(job_description, resume_text)
    return jsonify({"match_score": match_score})

@app.route("/", methods=["GET"])
def home():
    return "Resume Screener API (base64 JSON) is running!", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
