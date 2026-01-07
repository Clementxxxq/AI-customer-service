#!/usr/bin/env python3
import uvicorn
import sys
import os

# Change to backend directory
os.chdir('backend')
sys.path.insert(0, '.')

# Run uvicorn
uvicorn.run(
    "main:app",
    host="127.0.0.1",
    port=8000,
    log_level="info"
)
