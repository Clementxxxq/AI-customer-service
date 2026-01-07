#!/usr/bin/env python3
"""Simple test to debug the API"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"

# Test health
print("=== Health Check ===")
try:
    response = requests.get(f"{BASE_URL}/api/chat/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
    exit(1)

# Test 4: Missing info
print("\n=== Test 4: Missing Info ===")
request_data = {
    "content": "I want to book an appointment",
    "user_id": 1,
    "conversation_id": "test_case_4"
}
response = requests.post(f"{BASE_URL}/api/chat/message", json=request_data)
print(f"Status: {response.status_code}")
data = response.json()
print(f"Action Result: {json.dumps(data.get('action_result'), indent=2)}")
print(f"Bot Response: {data.get('bot_response')}")

print("\nTest 4 passed!" if "Missing required information" in str(data.get('action_result', {})) else "Test 4 FAILED!")
