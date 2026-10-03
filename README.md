# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is an intelligent, full-stack educational assistant powered by FastAPI, HTML5/CSS3/JavaScript, SQLite, and Google Gemini AI.

## Key Capabilities
- **Academic Question & Answer**: Direct answers backed by step-by-step principles and examples.
- **Adaptive Concept Explanations**: Tailors explanations for beginner, intermediate, or advanced learners with real-world analogies.
- **Interactive Quiz Arena**: Generates 3-to-4 option MCQs with instant browser checking, scoring, answer explanations, and attempt history.
- **Concise Summaries**: Generates high-yield exam revision notes from lengthy passages.
- **Personalized Roadmaps**: Provides week-by-week learning paths with prerequisites, milestones, and project goals.
- **Study Notes & Bookmarking**: SQLite database storage for saving notes and bookmarking AI responses.
- **Learning Analytics**: Visual dashboard tracking queries, quiz scores, and subject engagement.
- **Voice Learning**: Speech recognition dictation and text-to-speech audio playback.
- **Resilient AI Pipeline**: Live Google Gemini 2.5 Flash integration with automatic demo fallback when API keys are not yet configured.

---

## Repository Structure

```text
EduGenie_GitHub_Submission/
├── 01. Brainstorming & Ideation/          # Problem statement, idea formulation
├── 02. Requirement Analysis/              # Functional & non-functional requirements
├── 03. Project Design Phase/              # System architecture & data flow
├── 04. Project Planning Phase/            # Project milestones & schedule
├── 05. Project Development Phase/         # Source code & application
│   └── Source Code/
│       ├── app/                           # Backend application modules & database
│       ├── static/                        # CSS styles and JavaScript logic
│       ├── templates/                     # Jinja2 HTML web interface
│       ├── tests/                         # Pytest test suite
│       ├── requirements.txt               # Dependencies
│       ├── .env                           # Environment configuration
│       └── run.py                         # Startup launcher
├── 06. Project Testing/                   # Test plan and test execution results
├── 07. Project Documentation/             # Comprehensive report & user guide
├── 08. Project Demonstration/             # Demo script and presentation outline
├── conftest.py                            # Pytest path resolver
├── run.py                                 # Root application launcher
└── README.md                              # This document
```

---

## How to Install and Run

### 1. Prerequisites
- Python 3.10 or higher installed.

### 2. Option A: Run directly from Repository Root
```bash
# 1. Install dependencies
pip install -r "05. Project Development Phase/Source Code/requirements.txt"

# 2. Start the application
python run.py
```

### 3. Option B: Run from the Source Code Folder
```bash
# 1. Change to the Source Code directory
cd "05. Project Development Phase/Source Code"

# 2. Create and activate a virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) Add your Gemini API key in .env
# GOOGLE_API_KEY=your_actual_gemini_api_key_here

# 5. Start the server
python run.py
# OR
uvicorn app.main:app --reload
```

---

## Access Points
- **Web User Interface**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## Running the Automated Tests
From the project root or from `Source Code/`:
```bash
pytest
```
All 13 automated tests will execute and pass, verifying the frontend templates, API routes, database CRUD, quiz submission logic, and fallback responses.