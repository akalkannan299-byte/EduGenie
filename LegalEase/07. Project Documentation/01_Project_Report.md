# EduGenie – Project Report

## Abstract
EduGenie is a Google Gemini powered learning assistant developed using FastAPI, modern JavaScript, and an SQLite database. It seamlessly combines question answering, concept explanation, interactive quiz generation with real-time scoring, text summarization, personalized learning path roadmaps, study notes management, and learning analytics into a unified browser-based application.

## Objectives
1. Provide AI-assisted educational answers with step-by-step principles and examples.
2. Explain difficult concepts tailored for different learner levels (beginner, intermediate, advanced) using real-world analogies.
3. Generate practice quizzes with instant grading, score calculation, and answer explanations.
4. Summarize long educational content into high-yield revision points.
5. Recommend structured, week-by-week personalized learning paths.
6. Provide persistent local database storage for query history, bookmarks, quiz performance, and custom study notes.
7. Deliver a voice-enabled educational experience with speech-to-text dictation and text-to-speech audio narration.
8. Provide full API-based Generative AI integration with automated testing and offline demo resilience.

## Technology Stack
- **Backend Framework**: Python, FastAPI, Uvicorn, Starlette
- **Database Layer**: SQLite, SQLAlchemy 2.0
- **AI Engine**: Google Gemini (google-genai SDK 2.x) with intelligent demo fallback
- **Frontend Layer**: HTML5, CSS3 (Custom Responsive Dark Theme), Vanilla JavaScript (ES6+)
- **Templating**: Jinja2
- **Data Validation**: Pydantic v2
- **Testing**: Pytest, HTTPX

## Project Structure
The source code is located under:
`05. Project Development Phase/Source Code/`

Key modules:
- `app/main.py`: Application entry point, static asset mounting, and lifecycle management.
- `app/database.py` & `app/models.py`: SQLite engine and database tables (`HistoryItem`, `QuizAttempt`, `StudyNote`).
- `app/crud.py`: Database operations for queries, bookmarks, quiz attempts, and notes.
- `app/gemini_client.py`: Gemini client integration and offline demo generation.
- `app/routes.py`: Complete REST API endpoints and web interface routes.
- `templates/index.html`: Responsive single-page web interface with 5 dedicated functional tabs.
- `static/app.js`: Frontend controller managing tabs, voice recognition, speech synthesis, quiz grading, and API requests.
- `static/style.css`: Modern design system with responsive layouts and dark-mode aesthetics.

## Implemented API Endpoints
- `GET /`: Home web interface
- `GET /health`: System health and model connectivity
- `POST /qa`: Question & Answer
- `POST /explain`: Concept explanation with learner levels
- `POST /quiz`: Quiz generation
- `POST /summarize`: Text summarization
- `POST /learn/recommendations`: Personalized learning path roadmap
- `GET /api/history`: Searchable learning history
- `DELETE /api/history/{id}`: Delete specific history item
- `DELETE /api/history`: Clear all history
- `POST /api/history/{id}/bookmark`: Toggle bookmark
- `GET /api/bookmarks`: Retrieve bookmarked responses
- `POST /api/quiz/submit`: Submit answers, calculate score & percentage, and save attempt
- `GET /api/quiz/history`: Retrieve quiz performance history
- `GET /api/notes`: Retrieve custom study notes
- `POST /api/notes`: Create custom study note
- `DELETE /api/notes/{id}`: Delete study note
- `GET /api/stats`: Real-time user learning engagement metrics
- `GET /api/config`: System metadata and active feature configuration

## Future Enhancements
- User multi-tenant authentication (OAuth2 / JWT)
- PDF/document upload for textbook summarization
- Export study notes and quizzes to Anki flashcards
- Teacher & classroom collaboration dashboard