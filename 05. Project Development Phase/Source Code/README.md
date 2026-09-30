# EduGenie – Google Gemini Powered Learning Assistant

Complete VS Code/GitHub-ready implementation based on the supplied EduGenie document.

## Features
- Q&A
- Concept explanation
- 3-question, 4-option MCQ quiz generation
- Quiz answer checking in the browser
- Text summarization
- Personalized beginner-to-advanced learning paths
- FastAPI REST backend
- HTML/CSS/JavaScript frontend
- Gemini API integration
- Optional LaMini-Flan-T5-783M local explanation path

## Structure
```text
EduGenie/
├── app/{main.py,config.py,gemini_client.py,explanation_module.py,qna.py,quiz_module.py,summary_module.py,learning_path.py,routes.py}
├── templates/index.html
├── static/{style.css,app.js}
├── tests/test_app.py
├── requirements.txt
├── requirements-local.txt
├── .env.example
├── .gitignore
└── README.md
```

## Run
```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
```
Copy `.env.example` to `.env`, add your Gemini API key, then:
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

## API
POST `/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`; GET `/health`.

## Optional local model
The source document describes LaMini-Flan-T5-783M for concept explanation. It is optional here because the model is large. Install `requirements-local.txt` and set `USE_LOCAL_EXPLANATION=true` to enable it. Gemini remains the fallback if local loading fails.

## GitHub
```bash
git init
git add .
git commit -m "Initial EduGenie AI learning assistant"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```
Never commit `.env`.
