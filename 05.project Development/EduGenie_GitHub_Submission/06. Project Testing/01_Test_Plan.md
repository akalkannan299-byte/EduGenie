# EduGenie – Testing Plan

## Testing Objectives
- Verify that the FastAPI application starts correctly and mounts static assets.
- Verify core educational API routes (`/qa`, `/explain`, `/quiz`, `/summarize`, `/learn/recommendations`).
- Verify invalid and edge-case inputs are properly rejected with validation errors.
- Verify database tables auto-initialize in SQLite.
- Verify history logging, bookmarking, and deletion.
- Verify interactive quiz submission, scoring, and percentage calculation.
- Verify study notes CRUD operations.
- Verify learning analytics and system configuration endpoints.
- Verify Swagger API documentation loads.

## Test Cases

| ID | Test Case | Endpoint | Expected Result | Status |
|---|---|---|---|---|
| TC01 | Open Web Home | `GET /` | Returns 200, renders HTML with EduGenie interface | PASS |
| TC02 | Health Check | `GET /health` | Returns 200, service name, model, and SQLite status | PASS |
| TC03 | Swagger Docs | `GET /docs` | Returns 200 and loads interactive documentation | PASS |
| TC04 | Input Validation | `POST /qa` | Short input (< 3 chars) is rejected with 422 | PASS |
| TC05 | Question & Answer | `POST /qa` | Generates structured answer and saves history | PASS |
| TC06 | Concept Explanation | `POST /explain` | Generates level-tailored explanation and analogy | PASS |
| TC07 | Quiz Generation | `POST /quiz` | Returns multiple MCQs with 4 options and answer | PASS |
| TC08 | Text Summarization | `POST /summarize` | Summarizes text into high-yield revision points | PASS |
| TC09 | Learning Roadmap | `POST /learn/recommendations` | Returns week-by-week structured roadmap | PASS |
| TC10 | History & Bookmarking | `/api/history`, `/bookmark` | Logs queries, toggles bookmark status, deletes item | PASS |
| TC11 | Quiz Scoring & Attempts | `POST /api/quiz/submit` | Grades answers, computes score/pct, stores attempt | PASS |
| TC12 | Study Notes CRUD | `/api/notes` | Creates, lists, and deletes custom study notes | PASS |
| TC13 | Analytics & Config | `/api/stats`, `/api/config` | Returns real-time metrics and active feature list | PASS |

## Automated Testing Command
Run from project root or `Source Code/`:

```bash
pytest
```