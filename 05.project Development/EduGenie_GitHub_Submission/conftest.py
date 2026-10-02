import sys
from pathlib import Path

source_dir = Path(__file__).resolve().parent / "05. Project Development Phase" / "Source Code"
if str(source_dir) not in sys.path:
    sys.path.insert(0, str(source_dir))
