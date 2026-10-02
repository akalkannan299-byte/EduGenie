# EduGenie – Requirement Analysis

## Functional Requirements

### FR1 – Question & Answer
The system shall accept a question and return an educational answer.

### FR2 – Concept Explanation
The system shall explain a supplied topic at an appropriate learner level.

### FR3 – Quiz Generation
The system shall generate multiple-choice questions with answer options and correct answers.

### FR4 – Summarization
The system shall summarize supplied educational text.

### FR5 – Learning Recommendations
The system shall generate a beginner-to-advanced learning path for a selected topic and learner level.

### FR6 – Web Interface
The system shall provide a browser-based interface for accessing the learning functions.

### FR7 – API
The backend shall expose REST-style POST endpoints for the core learning operations.

## Non-Functional Requirements
- Simple and responsive user interface
- Modular backend
- Input validation
- Error handling
- Configurable Gemini API key
- Local development support through Uvicorn
- Automated basic tests
- API documentation through FastAPI Swagger

## Technology Requirements
- Python
- FastAPI
- Uvicorn
- Jinja2
- HTML/CSS/JavaScript
- Google Gemini
- Pydantic
- python-dotenv
- pytest

## Required API Endpoints
- POST /qa
- POST /explain
- POST /quiz
- POST /summarize
- POST /learn/recommendations