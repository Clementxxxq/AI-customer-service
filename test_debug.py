#!/usr/bin/env python3
"""
Debug test for appointment booking
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"

# Test 2: Complete booking
tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

request_data = {
    "content": f"I'd like to book a cleaning with Dr. Wang on {tomorrow} at 2 PM. My name is John Smith and my phone is 555-1234",
    "user_id": 1,
    "conversation_id": "test_case_2"
}

print("=== Test 2: Complete Booking ===")
print(f"Request: {json.dumps(request_data, indent=2)}")

response = requests.post(CHAT_ENDPOINT, json=request_data)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 4: Missing info
print("\n\n=== Test 4: Missing Info ===")
request_data = {
    "content": "I want to book an appointment",
    "user_id": 1,
    "conversation_id": "test_case_4"
}

print(f"Request: {json.dumps(request_data, indent=2)}")

response = requests.post(CHAT_ENDPOINT, json=request_data)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Test 3: Invalid doctor
print("\n\n=== Test 3: Invalid Doctor ===")
request_data = {
    "content": "I want to see Dr. NonExistent for a cleaning",
    "user_id": 1,
    "conversation_id": "test_case_3"
}

print(f"Request: {json.dumps(request_data, indent=2)}")

response = requests.post(CHAT_ENDPOINT, json=request_data)
print(f"\nStatus: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")
