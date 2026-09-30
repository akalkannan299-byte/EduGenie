import os
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY=os.getenv('GOOGLE_API_KEY','').strip()
GEMINI_MODEL=os.getenv('GEMINI_MODEL','gemini-2.5-flash')
USE_LOCAL_EXPLANATION=os.getenv('USE_LOCAL_EXPLANATION','false').lower()=='true'
LOCAL_EXPLANATION_MODEL=os.getenv('LOCAL_EXPLANATION_MODEL','MBZUAI/LaMini-Flan-T5-783M')
