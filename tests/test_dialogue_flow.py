#!/usr/bin/env python3
"""
Dialogue Flow Test - Demonstrates multi-turn conversation with context memory
Tests the new dialogue state management system
"""
import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"

# Use consistent conversation ID for this test
CONVERSATION_ID = "dialogue_test_conv"

def send_message(content: str, conversation_id: str) -> dict:
    """Send a chat message and get response"""
    payload = {
        "content": content,
        "user_id": 1,
        "conversation_id": conversation_id
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.status_code < 400 else None,
            "error": response.text if response.status_code >= 400 else None
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": None,
            "error": str(e)
        }


def print_turn(turn_num: int, user_msg: str, response: dict):
    """Print a conversation turn"""
    print(f"\n{'='*70}")
    print(f"TURN {turn_num}")
    print(f"{'='*70}")
    print(f"👤 User: {user_msg}")
    
    if response["status_code"] == 200:
        data = response["data"]
        if data is None:
            print(f"❌ Error: No response data received")
        else:
            print(f"🤖 AI: {data['bot_response']}")
            print(f"📊 Intent: {data['intent']} (confidence: {data['confidence']})")
            print(f"📋 Collected Info:")
            for key, val in data['entities'].items():
                if val:
                    print(f"   - {key}: {val}")
    else:
        print(f"❌ Error: {response['error']}")


def test_dialogue_flow():
    """Test the multi-turn dialogue flow"""
    print(f"\n{'='*70}")
    print("MULTI-TURN DIALOGUE TEST WITH CONTEXT MEMORY")
    print(f"{'='*70}")
    print(f"Conversation ID: {CONVERSATION_ID}")
    print("Expected Flow:")
    print("1. User wants to book appointment")
    print("2. AI asks for doctor")
    print("3. User provides doctor")
    print("4. AI asks for service")
    print("5. User provides service")
    print("6. AI asks for date")
    print("7. User provides date")
    print("8. AI asks for time")
    print("9. User provides time")
    print("10. AI confirms and books appointment")
    
    # Turn 1: User initiates booking
    resp1 = send_message("I want to book an appointment", CONVERSATION_ID)
    print_turn(1, "I want to book an appointment", resp1)
    
    # Turn 2: User provides doctor
    resp2 = send_message("Dr. Wang", CONVERSATION_ID)
    print_turn(2, "Dr. Wang", resp2)
    
    # Turn 3: User provides service
    resp3 = send_message("Cleaning", CONVERSATION_ID)
    print_turn(3, "Cleaning", resp3)
    
    # Turn 4: User provides date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    resp4 = send_message(f"Tomorrow ({tomorrow})", CONVERSATION_ID)
    print_turn(4, f"Tomorrow ({tomorrow})", resp4)
    
    # Turn 5: User provides time
    resp5 = send_message("2 PM", CONVERSATION_ID)
    print_turn(5, "2 PM", resp5)
    
    # Check if booking succeeded
    print(f"\n{'='*70}")
    print("FINAL STATUS")
    print(f"{'='*70}")
    
    if resp5["status_code"] == 200:
        data = resp5["data"]
        if data is None:
            print("⚠️ Response received but data is empty")
            print("This may indicate the backend needs to be running")
        elif data.get("action_result") and data["action_result"].get("success"):
            print("✅ APPOINTMENT SUCCESSFULLY BOOKED!")
            print(f"Appointment ID: {data['action_result'].get('appointment_id')}")
            print(f"Date: {data['action_result'].get('appointment_date')}")
            print(f"Time: {data['action_result'].get('appointment_time')}")
        else:
            print("⚠️ Booking intent was processed but status unclear")
            print(f"Response: {data.get('bot_response')}")
            if data.get("action_result") is None:
                print("(No appointment action was taken)")
    else:
        print("❌ Test failed")
        print(f"Status Code: {resp5['status_code']}")
        if resp5["error"]:
            print(f"Error: {resp5['error']}")


if __name__ == "__main__":
    print("\n🚀 Starting dialogue flow test...")
    print("ℹ️  Make sure:")
    print("   - Ollama is running (ollama serve)")
    print("   - Backend is running (cd backend && uvicorn main:app --reload)")
    print("   - Database is initialized (python init_db.py)")
    
    input("\nPress Enter to start test...")
    
    test_dialogue_flow()
    
    print(f"\n{'='*70}")
    print("✅ TEST COMPLETE")
    print(f"{'='*70}\n")
