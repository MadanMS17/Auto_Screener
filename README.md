# 📄 AI-Powered Resume Screener (API)

A lightweight, AI-powered Resume Screener REST API built in Python + Flask, currently using Hugging Face Sentence Transformers for semantic similarity scoring between job descriptions and resumes.

---

## 📌 Features
- Upload **base64-encoded PDF resumes** via JSON
- Compare resume content against a provided **job description**
- Calculate **semantic similarity score (0–100)** using `all-MiniLM-L6-v2`
- Return match score via JSON response
- Health check endpoint (`/`)
- Integrates cleanly with Google Apps Script & Google Sheets workflows
- Zero cloud API cost (runs locally / on Render.com)

---

## 📦 Current Stack

- Python 3.10+
- Flask
- PyPDF2
- Hugging Face Sentence Transformers (`all-MiniLM-L6-v2`)
- Gunicorn (for production serving)
- Hosted on **Render.com**

---

## 📂 API Endpoints

### `POST /screen_resume`

**Request JSON**
json
{
  "job_description": "AI/ML Engineer with Python and ML deployment skills.",
  "resume_base64": "<base64-encoded PDF content>"
}


Response

{
  "match_score": 78.23
}
GET /
Health check endpoint — returns:

Resume Screener API (Hugging Face Transformers) is running!
📜 Setup Instructions (Local Dev)
Clone the repo

git clone https://github.com/yourusername/ai-resume-screener.git
cd ai-resume-screener
Create a virtual environment

python -m venv venv
source venv/bin/activate
Install dependencies

pip install -r requirements.txt
Run locally

python app.py
Production serving (Render/Gunicorn)

gunicorn app:app

📊 Roadmap
✅ TF-IDF based screener
✅ Sentence Transformer-based semantic screener
🔜 LLM-powered scoring (GPT / Gemini)
🔜 Resume parsing & skill extraction
🔜 Fine-tuned classifier models


## 🖼️ AI Screener Deployment Diagram

![AI Screener Deployment Flowchart](assets/A_flowchart_in_a_digital_diagram_illustrates_an_AI.png)


------

