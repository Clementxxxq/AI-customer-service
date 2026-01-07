"""
FULL API SIMULATION TEST
Simulates actual HTTP requests to verify the flow end-to-end
"""

import sys
sys.path.append('backend')

from routes.chat import send_message
from schemas.chat import ChatRequest
from fastapi import HTTPException
import json

def test_full_conversation():
    """Simulate full conversation"""
    
    conversation_id = "full_test_conv_001"
    
    print("\n" + "="*70)
    print("FULL CONVERSATION TEST WITH ACTUAL API LOGIC")
    print("="*70)
    
    # Turn 1: User says "Dr. Wang"
    print("\n[TURN 1] User: 'Dr. Wang'")
    print("-" * 70)
    
    try:
        req1 = ChatRequest(
            content="Dr. Wang",
            user_id=1,
            conversation_id=conversation_id
        )
        resp1 = send_message(req1)
        print(f"Response: {resp1.bot_response}")
        print(f"Entities saved: {resp1.entities}")
        print(f"Intent: {resp1.intent}")
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    # Turn 2: User says "Cleaning"
    print("\n[TURN 2] User: 'Cleaning'")
    print("-" * 70)
    
    try:
        req2 = ChatRequest(
            content="Cleaning",
            user_id=1,
            conversation_id=conversation_id  # SAME conversation_id
        )
        resp2 = send_message(req2)
        print(f"Response: {resp2.bot_response}")
        print(f"Entities saved: {resp2.entities}")
        print(f"Intent: {resp2.intent}")
        
        # Check if Dr. Wang is retained
        entities_dict = resp2.entities.dict() if hasattr(resp2.entities, 'dict') else resp2.entities
        if entities_dict.get("doctor") == "Dr. Wang":
            print(f"\n✅ GOOD: Dr. Wang retained")
        else:
            print(f"\n❌ BAD: Dr. Wang NOT retained! Current entities: {resp2.entities}")
            
        # Check if we're asking "What service" or the default greeting
        if "service" in resp2.bot_response.lower() or "date" in resp2.bot_response.lower():
            print(f"GOOD: Asking for next field (not default greeting)")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_full_conversation()
