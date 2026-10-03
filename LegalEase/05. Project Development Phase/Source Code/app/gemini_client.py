import json
import logging
import re
from .config import GEMINI_MODEL, GOOGLE_API_KEY, DEMO_MODE

logger = logging.getLogger("edugenie.gemini")

def is_api_configured() -> bool:
    if not GOOGLE_API_KEY:
        return False
    lower = GOOGLE_API_KEY.lower().strip()
    if lower.startswith("your_") or "api_key_here" in lower or lower == "none" or len(lower) < 10:
        return False
    return True

def get_offline_educational_response(prompt: str) -> str:
    """Provides high-quality structured educational fallback when Gemini API key is not configured or network is offline."""
    prompt_lower = prompt.lower()

    # Quiz detection
    if "multiple-choice questions" in prompt_lower or "create exactly" in prompt_lower or "format: [{" in prompt_lower:
        topic_match = re.search(r'passage:\s*(.*)', prompt, re.DOTALL | re.IGNORECASE)
        topic = topic_match.group(1).strip() if topic_match else "General Knowledge"
        topic_clean = topic.split('\n')[0][:80]

        return json.dumps([
            {
                "question": f"Which of the following represents a foundational principle of {topic_clean}?",
                "options": [
                    "Modular structure with clear separation of concerns",
                    "Random execution without structured logic",
                    "Monolithic coupling of unrelated components",
                    "Ignoring standard protocols and standards"
                ],
                "correct_answer": "Modular structure with clear separation of concerns",
                "explanation": "Separation of concerns and modularity are fundamental principles ensuring maintainability, scalability, and clarity."
            },
            {
                "question": f"What is a primary advantage of understanding {topic_clean} in practical applications?",
                "options": [
                    "Reduces system complexity and enhances problem-solving efficiency",
                    "Prevents the need for testing and validation",
                    "Completely eliminates all computational overhead",
                    "Bypasses foundational theory without consequence"
                ],
                "correct_answer": "Reduces system complexity and enhances problem-solving efficiency",
                "explanation": "Deep domain knowledge enables engineers and students to systematically decompose complex problems and build efficient solutions."
            },
            {
                "question": f"In real-world workflows related to {topic_clean}, which step is recommended for continuous verification?",
                "options": [
                    "Systematic evaluation, practical feedback, and iterative revision",
                    "Deploying once without monitoring or logging",
                    "Avoiding documentation and peer reviews",
                    "Relying solely on intuition without measurement"
                ],
                "correct_answer": "Systematic evaluation, practical feedback, and iterative revision",
                "explanation": "Continuous assessment and iterative improvement ensure reliable, robust, and verified learning outcomes."
            }
        ])

    # Learning path detection (check before concept explanation so 'learning roadmap' matches)
    if "learning path" in prompt_lower or "learning roadmap" in prompt_lower or "roadmap" in prompt_lower or "structured learning" in prompt_lower:
        topic_match = re.search(r'(?:for:\s*topic:\s*|for\s*")"?([^"\n]+)"?', prompt, re.IGNORECASE)
        topic = topic_match.group(1).strip() if topic_match else "the chosen subject"

        return f"""# 🗺️ Master Learning Roadmap: {topic}

### 🎯 Essential Prerequisites
- Basic familiarity with logical reasoning, foundational terminology, and system concepts.
- Motivation for hands-on experimentation, daily note-taking, and problem-solving.

---

### 🟢 Stage 1: Foundations (Weeks 1 - 2)
- **Core Topics**: Syntax, core terminology, environment setup, and baseline execution models.
- **Hands-on Milestone**: Build a starter prototype or foundational module proving basic concepts.
- **Key Focus**: Solidify foundational principles before tackling complex abstractions.

---

### 🟡 Stage 2: Intermediate Application (Weeks 3 - 5)
- **Core Topics**: Design patterns, modular architecture, error handling, standard libraries, and APIs.
- **Hands-on Milestone**: Develop an interactive tool or project solving a realistic use case.
- **Key Focus**: Emphasize clean structure, maintainability, and algorithmic complexity.

---

### 🔴 Stage 3: Advanced Mastery (Weeks 6 - 8)
- **Core Topics**: Performance optimization, asynchronous paradigms, automated testing, and security.
- **Hands-on Milestone**: Deploy a production-ready, well-documented capstone project.
- **Key Focus**: Architectural scalability, resilient error boundaries, and benchmark evaluations.

---

### ⏱️ Recommended Study Routine & Spaced Repetition
- **Daily Focus**: 45–60 minutes of active coding, reading, and conceptual mapping.
- **Active Recall**: Test yourself with quizzes and build mini prototypes every weekend.
- **Spaced Repetition**: Review prior stage milestones every 10 days to solidify retention.

*(⚡ Note: Demo Mode active. Configure `GOOGLE_API_KEY` in `.env` for customized Gemini AI roadmaps.)*"""

    # Concept explanation detection
    if "explain this concept" in prompt_lower or "explain the concept" in prompt_lower or "explain" in prompt_lower:
        concept_match = re.search(r'concept(?:\s+of)?\s*"?([^"\n]+)"?', prompt, re.IGNORECASE)
        concept = concept_match.group(1).strip() if concept_match else "the requested concept"

        return f"""### 📘 1. Simple Definition
**{concept}** is a core concept that provides a structured method to understand, organize, and solve problems in its domain. At its heart, it helps simplify complex processes into manageable, predictable components.

---

### 🔍 2. Step-by-Step Explanation
1. **Foundation & Initiation**: The process begins by establishing baseline rules and required inputs.
2. **Core Transformation**: Specific rules or operations act on the input data or state.
3. **Outcome & Verification**: The resulting output is checked against expected criteria to ensure accuracy.
4. **Integration**: The result seamlessly connects into larger workflows or systems.

---

### 💡 3. Real-World Analogy
Think of **{concept}** like an **efficient airport traffic control tower**:
- Incoming requests arrive like airplanes requesting runway clearance.
- Standardized protocols govern which plane moves when, avoiding collisions.
- Clear signals ensure that every passenger reaches their destination safely and on schedule.

---

### 💻 4. Practical Example
Consider a simple illustrative application:
```text
Input State  --> [ Applying {concept} ] --> Optimal Output
Example:
Raw query    --> Processed & Structured --> Clear educational outcome
```

---

### 🔑 5. Key Takeaways
- **Simplicity**: Breaks complicated problems into understandable steps.
- **Reliability**: Ensures predictable, consistent behavior.
- **Versatility**: Widely used across engineering, science, and everyday problem-solving.

*(⚡ Note: Demo Mode active. Configure `GOOGLE_API_KEY` in `.env` to unlock live Gemini 2.5 Flash explanations.)*"""

    # Summarization detection
    if "summarize" in prompt_lower:
        return """### 📋 Executive Summary
Here is a concise educational breakdown of the provided passage:

#### 📌 Core Findings & Main Points
- **Primary Focus**: The text outlines the foundational principles and key mechanisms governing the subject matter.
- **Key Relationships**: Elements operate cohesively, where each component directly influences overall efficiency and accuracy.
- **Practical Application**: Emphasizes standard methodologies, practical verification, and adherence to proven guidelines.

#### 💡 High-Yield Revision Bullets
1. Core terminology and fundamental definitions must be thoroughly understood before advanced application.
2. Systematic execution yields significantly higher predictability compared to ad-hoc methods.
3. Iterative review and active testing are essential to consolidate knowledge.

*(⚡ Note: Demo Mode active. Configure `GOOGLE_API_KEY` in `.env` to generate live Gemini summaries.)*"""

    # General Q&A fallback
    return f"""### 🎓 Educational Answer

**Direct Answer:**
Understanding the requested subject requires examining its primary purpose, core working mechanism, and practical significance in academic and real-world contexts.

---

### 📖 In-Depth Explanation
1. **Core Concept**: The topic addresses specific challenges by implementing well-defined principles and structured rules.
2. **Mechanism**: Operations follow a clear pipeline: input reception, processing according to established constraints, and final output generation.
3. **Best Practices**: Consistency, rigorous verification, and clear documentation ensure optimal comprehension and execution.

---

### 💡 Example in Action
When applied in practice, this allows learners and engineers to systematically debug issues, anticipate edge cases, and design robust architectures.

*(⚡ Note: Demo Mode active. Configure `GOOGLE_API_KEY` in `.env` for real-time live answers from Google Gemini.)*"""

def generate_text(prompt: str, max_output_tokens: int = 1500, temperature: float = 0.4) -> str:
    # If API key is configured and not in forced demo mode, call Google Gemini
    if is_api_configured() and DEMO_MODE != "true":
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=GOOGLE_API_KEY)
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_output_tokens,
                ),
            )
            text = getattr(response, "text", None)
            if text and text.strip():
                return text.strip()
            raise RuntimeError("Gemini returned an empty response.")
        except Exception as e:
            logger.warning(f"Live Gemini API call failed: {e}. Falling back to offline educational response.")
            if DEMO_MODE == "false":
                raise RuntimeError(f"Gemini API Error: {e}")
            return get_offline_educational_response(prompt)

    # Demo / Offline generator
    return get_offline_educational_response(prompt)
