#!/usr/bin/env python
"""
Test if FastAPI app starts correctly
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from backend.main import app
    print("✅ App imported successfully")
    print(f"App routes: {[r.path for r in app.routes[:5]]}")
except Exception as e:
    print(f"❌ Failed to import app: {e}")
    import traceback
    traceback.print_exc()
