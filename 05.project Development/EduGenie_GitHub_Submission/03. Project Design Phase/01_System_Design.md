# EduGenie – Project Design

## High-Level Architecture

```text
+----------------------+
|      Web Browser     |
| HTML/CSS/JavaScript  |
+----------+-----------+
           |
           | HTTP
           v
+----------------------+
|      FastAPI         |
|   Routes / API       |
+----------+-----------+
           |
           v
+----------------------+
| Learning Modules     |
| Q&A | Explain | Quiz|
| Summary | Learning  |
+----------+-----------+
           |
           v
+----------------------+
|   Gemini Client      |
| Google Gemini API    |
+----------------------+
```

## Module Design

### main.py
Creates the FastAPI application and serves the web application.

### routes.py
Defines API request models and the required endpoints.

### gemini_client.py
Provides the common Gemini API integration.

### qna.py
Handles question-answer prompts.

### explanation_module.py
Handles concept explanations and can optionally use the local model described in the project document.

### quiz_module.py
Generates and validates quiz JSON.

### summary_module.py
Handles summarization.

### learning_path.py
Generates structured learning recommendations.

## Data Flow
1. User selects a learning task.
2. Browser sends an HTTP POST request.
3. FastAPI validates the request.
4. The corresponding module prepares the prompt.
5. Gemini generates the response.
6. Backend returns JSON.
7. JavaScript displays the result.