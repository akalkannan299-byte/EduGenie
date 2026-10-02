from .gemini_client import generate_text

def summarize_text(text: str) -> str:
    prompt = f'''Summarize the following educational content for quick and effective student revision.
Structure your summary clearly with Markdown:
### 📋 Executive Summary
(2-3 sentences capturing the core premise)

### 🔑 Key Concepts & Definitions
(Bullet points with bold terms and concise definitions)

### 📌 High-Yield Takeaways
(Top 3-5 facts students must remember for exams)

Do not add unsupported facts. Keep language crisp, structured, and easy to review.

PASSAGE:
{text}'''

    return generate_text(prompt, max_output_tokens=1200, temperature=0.3)
