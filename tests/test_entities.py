#!/usr/bin/env python3
"""Debug test to see what entities are extracted"""
import requests
import json

BASE_URL = "http://127.0.0.1:8000"

# Test 4: Missing info
print("=== Test 4: Missing Info ===")
request_data = {
    "content": "I want to book an appointment",
    "user_id": 1,
    "conversation_id": "test_case_4_debug"
}
response = requests.post(f"{BASE_URL}/api/chat/message", json=request_data)
data = response.json()

print(f"Intent: {data.get('intent')}")
print(f"Entities extracted: {json.dumps(data.get('entities'), indent=2)}")
print(f"Action Result: {json.dumps(data.get('action_result'), indent=2)}")
print(f"Bot Response: {data.get('bot_response')}")
