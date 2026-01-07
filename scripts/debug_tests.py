#!/usr/bin/env python3
"""
Test only Test 1, then check database state
"""
import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"

# Test 1
request_data = {
    "content": "What dental services do you offer?",
    "user_id": 1,
    "conversation_id": "test_case_1"
}

print("Sending Test 1...")
response = requests.post(CHAT_ENDPOINT, json=request_data, timeout=30)
print(f"Status: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=2)}")

# Now check database
import sqlite3
conn = sqlite3.connect('clinic.db')
c = conn.cursor()
appts = c.execute('SELECT COUNT(*) FROM appointments').fetchone()[0]
print(f"\nAfter Test 1: {appts} appointments in database")
conn.close()

print("\n" + "="*70)
print("Now sending Test 2...")

request_data = {
    "content": "I'd like to book a cleaning with Dr. Wang on 2026-01-07 at 2 PM. My name is John Smith and my phone is 555-1234",
    "user_id": 1,
    "conversation_id": "test_case_2"
}

response = requests.post(CHAT_ENDPOINT, json=request_data, timeout=30)
print(f"Status: {response.status_code}")
resp_data = response.json()
print(f"Intent: {resp_data.get('intent')}")
print(f"Success: {resp_data.get('action_result', {}).get('success') if resp_data.get('action_result') else 'N/A'}")
print(f"Message: {resp_data.get('bot_response')}")

# Check database after Test 2
conn = sqlite3.connect('clinic.db')
c = conn.cursor()
appts = c.execute('SELECT * FROM appointments WHERE doctor_id=1 AND date="2026-01-07"').fetchall()
print(f"\nAfter Test 2: Found {len(appts)} appointments for Dr. Wang on 2026-01-07")
for appt in appts:
    print(f"  {appt}")
conn.close()
