# EduGenie – Google Gemini Powered Learning Assistant

EduGenie is a Generative AI educational assistant built with FastAPI, HTML/CSS/JavaScript, and Google Gemini.

## Features
- Question & Answer
- Concept Explanation
- Quiz Generation
- Text Summarization
- Personalized Learning Path Recommendations

## GitHub Submission Structure

1. `01. Brainstorming & Ideation/`
2. `02. Requirement Analysis/`
3. `03. Project Design Phase/`
4. `04. Project Planning Phase/`
5. `05. Project Development Phase/`
6. `06. Project Testing/`
7. `07. Project Documentation/`
8. `08. Project Demonstration/`

The complete application source code is inside:

`05. Project Development Phase/Source Code/`

## Quick Start

```bash
cd "05. Project Development Phase/Source Code"
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create `.env` from `.env.example` and add your Gemini API key.

Run:

```bash
uvicorn app.main:app --reload
```

Open:

- `http://127.0.0.1:8000`
- `http://127.0.0.1:8000/docs`

Run tests:

```bash
pytest
```

## Security
Do not commit your real `.env` file or API key. The included `.gitignore` excludes `.env`.

## Important Note
The source project was syntax-checked, but live Gemini API calls depend on your own API key, network access, and configured model availability.