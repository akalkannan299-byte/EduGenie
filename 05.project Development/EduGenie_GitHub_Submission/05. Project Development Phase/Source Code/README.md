# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a comprehensive Generative AI educational assistant built with FastAPI, HTML/CSS/JavaScript, SQLite, and Google Gemini.

## Features
- **Question & Answer**: Instant academic and conceptual responses with structured in-depth explanations.
- **Concept Explanation**: Explains complex topics tailored for beginner, intermediate, or advanced learners.
- **Interactive Quiz Arena**: Generates 3-to-4 option MCQs with real-time selection, scoring, educational explanations for each question, and progress tracking.
- **Text Summarization**: Summarizes lengthy educational articles and chapters into concise high-yield revision points.
- **Personalized Learning Paths**: Generates week-by-week structured roadmaps with prerequisites, milestones, and project goals.
- **Study Notes & Bookmarking**: Save any AI answer or custom note directly into a local SQLite database.
- **Learning Analytics Dashboard**: Tracks total queries, completed quizzes, average quiz score, and task distribution.
- **Speech Recognition & Text-to-Speech**: Dictate questions using voice and listen to explanations read aloud.
- **Offline / Demo Mode**: Automatic fallback ensures the app runs seamlessly even without an external API key.

## Project Structure
```text
EduGenie_GitHub_Submission/
├── run.py                                    # Root one-click launcher
├── conftest.py                               # Pytest configuration
├── 05. Project Development Phase/Source Code/
│   ├── run.py                                # Launcher inside Source Code
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                         # Environment & settings
│   │   ├── database.py                       # SQLAlchemy SQLite engine & session
│   │   ├── models.py                         # Database tables (History, QuizAttempt, StudyNote)
│   │   ├── crud.py                           # Database operations
│   │   ├── gemini_client.py                  # Google Gemini API & fallback engine
│   │   ├── qna.py                            # Q&A module
│   │   ├── explanation_module.py             # Concept explanation module
│   │   ├── quiz_module.py                    # Quiz generator & validator
│   │   ├── summary_module.py                 # Text summarization module
│   │   ├── learning_path.py                  # Roadmap generator
│   │   ├── routes.py                         # FastAPI web & REST API routes
│   │   └── main.py                           # App entrypoint & static mount
│   ├── templates/
│   │   └── index.html                        # Modern multi-tab educational web interface
│   ├── static/
│   │   ├── style.css                         # Dark theme design system & responsive UI
│   │   └── app.js                            # Frontend controller, speech API, quiz logic
│   ├── tests/
│   │   └── test_app.py                       # Automated test suite (13 test cases)
│   ├── requirements.txt                      # Production Python dependencies
│   ├── requirements-local.txt                # Optional local HuggingFace dependencies
│   ├── .env.example                          # Example environment variables
│   ├── .env                                  # Active environment configuration
│   ├── .gitignore                            # Git exclusion rules
│   └── README.md
```

## Quick Start Guide

### 1. Prerequisites
- Python 3.10+ (Tested on Python 3.10, 3.11, 3.12, 3.14)

### 2. Setup Virtual Environment
From the `Source Code` folder:
```bash
python -m venv venv
```

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```
**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```
**macOS / Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key
Open `.env` (or copy `.env.example` to `.env`) and add your Gemini API key:
```ini
GOOGLE_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
DATABASE_URL=sqlite:///./edugenie.db
DEMO_MODE=auto
```
> **Note**: If `GOOGLE_API_KEY` is not provided, EduGenie automatically runs in **Demo Mode**, allowing full evaluation of all features without crashing!

### 5. Run the Application
You can run the application with either command:

**Option A (Using run.py):**
```bash
python run.py
```

**Option B (Using Uvicorn):**
```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### 6. Access EduGenie
- Web Application: **http://127.0.0.1:8000**
- Interactive Swagger API Documentation: **http://127.0.0.1:8000/docs**
- Health Check: **http://127.0.0.1:8000/health**

### 7. Run Automated Tests
```bash
pytest
```
All 13 test cases covering validation, database CRUD, quiz submission, and AI endpoints will run and pass.

## REST API Endpoints
- `GET /` - Web Application UI
- `GET /health` - System health and model connectivity
- `POST /qa` - Educational Q&A
- `POST /explain` - Concept explanation with learner level
- `POST /quiz` - Interactive multiple-choice quiz generator
- `POST /summarize` - Educational passage summarization
- `POST /learn/recommendations` - Structured learning roadmap
- `GET /api/history` - Searchable activity history
- `DELETE /api/history/{id}` - Delete history entry
- `DELETE /api/history` - Clear entire history
- `POST /api/history/{id}/bookmark` - Toggle bookmark
- `GET /api/bookmarks` - View bookmarked responses
- `POST /api/quiz/submit` - Grade quiz attempt and record performance
- `GET /api/quiz/history` - List past quiz scores and progress
- `GET /api/notes` - List study notes
- `POST /api/notes` - Create custom study note
- `DELETE /api/notes/{id}` - Delete study note
- `GET /api/stats` - Learning engagement analytics
- `GET /api/config` - System configuration and active features
