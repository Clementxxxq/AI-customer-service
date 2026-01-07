#!/usr/bin/env python
"""
Test server startup
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

try:
    import uvicorn
    from main import app
    
    print("🚀 Starting server...")
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
