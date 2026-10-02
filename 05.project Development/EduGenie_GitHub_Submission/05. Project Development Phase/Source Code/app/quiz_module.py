import json
import re
from .gemini_client import generate_text

def clean_json_block(text: str) -> str:
    cleaned = text.strip()
    # Match markdown fence
    match = re.search(r'```(?:json)?\s*(\[.*?\])\s*```', cleaned, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    # Match any JSON array block
    match_arr = re.search(r'(\[\s*\{.*\}\s*\])', cleaned, re.DOTALL)
    if match_arr:
        return match_arr.group(1).strip()
    # Fallback stripping
    cleaned = re.sub(r'^```(?:json)?\s*', '', cleaned, flags=re.I)
    cleaned = re.sub(r'\s*```$', '', cleaned)
    return cleaned.strip()

def _validate(data):
    if not isinstance(data, list) or len(data) == 0:
        raise ValueError("A non-empty list of questions is required.")
    out = []
    for x in data:
        if not isinstance(x, dict) or not isinstance(x.get("question"), str):
            continue
        opts = x.get("options")
        ans = x.get("correct_answer")
        if not isinstance(opts, list) or len(opts) < 2 or not all(isinstance(o, str) for o in opts):
            continue
        if not isinstance(ans, str) or ans not in opts:
            ans = opts[0]
        explanation = x.get("explanation") or f"'{ans}' is the correct answer according to core principles."
        out.append({
            "question": x["question"].strip(),
            "options": [str(o).strip() for o in opts],
            "correct_answer": ans.strip(),
            "explanation": explanation.strip()
        })
    if len(out) < 2:
        raise ValueError("At least two valid questions could be verified.")
    return out

def generate_quiz(passage_or_topic: str):
    prompt = f'''Create exactly 3 multiple-choice questions from the topic or passage below.
Return ONLY valid JSON, no surrounding commentary, no Markdown backticks if possible.
Format:
[
  {{
    "question": "What is...",
    "options": ["Option A", "Option B", "Option C", "Option D"],
    "correct_answer": "Option A",
    "explanation": "Why Option A is correct..."
  }}
]
Rules:
- Exactly 4 distinct options per question.
- 'correct_answer' must match one of the 4 options verbatim.
- Include a helpful educational explanation for each answer.

TOPIC / PASSAGE:
{passage_or_topic}'''

    raw = generate_text(prompt, max_output_tokens=1500, temperature=0.3)
    try:
        cleaned = clean_json_block(raw)
        parsed = json.loads(cleaned)
        return _validate(parsed)
    except Exception as e:
        # Fallback quiz structure if parsing fails
        from .gemini_client import get_offline_educational_response
        fallback_json = get_offline_educational_response(f"Create exactly 3 multiple-choice questions passage: {passage_or_topic}")
        try:
            return _validate(json.loads(fallback_json))
        except Exception:
            raise RuntimeError(f"Quiz generation error: {e}")
