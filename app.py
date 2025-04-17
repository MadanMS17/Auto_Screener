from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer, util
import base64
import tempfile
import os

app = Flask(__name__)

# 📌 Load Hugging Face Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# 📌 Extract text from PDF
def extract_text_from_pdf(file_path):
    pdf = PdfReader(file_path)
    text = "".join([page.extract_text() or "" for page in pdf.pages])
    return text.strip()

# 📌 Rank Resume with Job Description using sentence embeddings
def rank_resume(job_description, resume_text):
    jd_embedding = model.encode(job_description, convert_to_tensor=True)
    resume_embedding = model.encode(resume_text, convert_to_tensor=True)

    similarity = util.cos_sim(jd_embedding, resume_embedding).item() * 100
    return round(similarity, 2)

# 📌 API Endpoint for Resume Screening
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

# 📌 Health check endpoint
@app.route("/", methods=["GET"])
def home():
    return "Resume Screener API (Hugging Face Transformers) is running!", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
