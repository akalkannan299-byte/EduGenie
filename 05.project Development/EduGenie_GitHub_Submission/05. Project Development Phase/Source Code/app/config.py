import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from Source Code .env first, then root if present
load_dotenv(BASE_DIR / ".env")
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
USE_LOCAL_EXPLANATION = os.getenv("USE_LOCAL_EXPLANATION", "false").lower() == "true"
LOCAL_EXPLANATION_MODEL = os.getenv("LOCAL_EXPLANATION_MODEL", "MBZUAI/LaMini-Flan-T5-783M").strip()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./edugenie.db").strip()
DEMO_MODE = os.getenv("DEMO_MODE", "auto").strip().lower()
