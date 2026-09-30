import json,re
from .gemini_client import generate_text

def clean_json_block(text:str)->str:
    text=re.sub(r'^```(?:json)?\s*','',text.strip(),flags=re.I)
    return re.sub(r'\s*```$','',text).strip()

def _validate(data):
    if not isinstance(data,list) or len(data)!=3: raise ValueError('Exactly three questions are required.')
    out=[]
    for x in data:
        if not isinstance(x,dict) or not isinstance(x.get('question'),str): raise ValueError('Invalid quiz question.')
        opts=x.get('options'); ans=x.get('correct_answer')
        if not isinstance(opts,list) or len(opts)!=4 or not all(isinstance(o,str) for o in opts): raise ValueError('Each question must have four string options.')
        if not isinstance(ans,str) or ans not in opts: raise ValueError('Invalid correct answer.')
        out.append({'question':x['question'],'options':opts,'correct_answer':ans})
    return out

def generate_quiz(passage:str):
    prompt=f'''Create exactly 3 multiple-choice questions from the passage below. Return ONLY valid JSON, no Markdown. Format: [{{"question":"...","options":["A","B","C","D"],"correct_answer":"A"}}]. The correct answer must be one of the options and every question must be answerable from the passage.\nPASSAGE:\n{passage}'''
    raw=generate_text(prompt,1400,0.3)
    try: return _validate(json.loads(clean_json_block(raw)))
    except Exception as e: raise RuntimeError(f'Quiz generation returned invalid JSON: {e}')
