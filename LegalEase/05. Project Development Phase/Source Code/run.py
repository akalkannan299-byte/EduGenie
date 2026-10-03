import os
import sys
from pathlib import Path

# Fix Windows console encoding if needed
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0" if os.getenv("PORT") else "127.0.0.1")
    reload_mode = False if os.getenv("PORT") else True

    print("\n" + "="*60)
    print("  [*] Starting EduGenie Learning Assistant Server")
    print("="*60)
    print(f"  Web Application:       http://{host}:{port}")
    print(f"  Interactive API Docs:  http://{host}:{port}/docs")
    print(f"  Health Check:          http://{host}:{port}/health")
    print("="*60 + "\n")
    uvicorn.run("app.main:app", host=host, port=port, reload=reload_mode)
