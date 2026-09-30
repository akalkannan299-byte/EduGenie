# EduGenie – User Guide

## 1. Install Python
Use Python 3.10+.

## 2. Open the Project
Open the `Source Code` folder in VS Code.

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

## 5. Configure Gemini
Copy `.env.example` to `.env` and add your Gemini API key.

Example:

```text
GOOGLE_API_KEY=your_key_here
GEMINI_MODEL=gemini-2.5-flash
```

Never upload `.env` or a real API key to GitHub.

## 6. Start the Server

```bash
uvicorn app.main:app --reload
```

## 7. Open the Application

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```