from google import genai
from google.genai import types
from .config import GEMINI_MODEL, GOOGLE_API_KEY

def generate_text(prompt:str,max_output_tokens:int=1200,temperature:float=0.4)->str:
    if not GOOGLE_API_KEY:
        raise RuntimeError('GOOGLE_API_KEY is missing. Create a .env file and add your Gemini API key.')
    client=genai.Client(api_key=GOOGLE_API_KEY)
    response=client.models.generate_content(model=GEMINI_MODEL,contents=prompt,config=types.GenerateContentConfig(temperature=temperature,max_output_tokens=max_output_tokens))
    text=getattr(response,'text',None)
    if not text: raise RuntimeError('Gemini returned an empty response.')
    return text.strip()
