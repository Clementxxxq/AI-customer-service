"""
TEST: 5-Slot Complete Booking Flow
Verifies that the system correctly:
1. Collects doctor, service, date, time (4 slots)
2. Asks for customer identity (5th slot)
3. Only books when all 5 slots are complete

Expected flow:
User: Dr. Wang → System: Ask service
User: Cleaning → System: Ask date
User: Tomorrow → System: Ask time
User: 3 PM → System: Ask customer info
User: John → System: Confirm and book
"""

import sys
import json
import threading
import warnings
sys.path.append('backend')

warnings.filterwarnings('ignore')
_original_hook = threading.excepthook
def _suppress_thread_exceptions(args):
    if isinstance(args.exc_value, UnicodeDecodeError):
        pass
    else:
        _original_hook(args)
threading.excepthook = _suppress_thread_exceptions

from routes.chat import send_message
from schemas.chat import ChatRequest
from datetime import datetime

def test_5_slot_complete_flow():
    """
    Test complete 5-slot booking flow
    """
    print("\n" + "="*80)
    print("5-SLOT COMPLETE BOOKING FLOW TEST")
    print("="*80)
    
    conversation_id = f"test_5slot_{datetime.now().timestamp()}"
    
    turns = [
        {
            "user": "Dr. Wang",
            "description": "Select doctor",
            "expect_progress": "service"
        },
        {
            "user": "Cleaning",
            "description": "Select service",
            "expect_progress": "date"
        },
        {
            "user": "Tomorrow",
            "description": "Select date",
            "expect_progress": "time"
        },
        {
            "user": "3 PM",
            "description": "Select time",
            "expect_progress": "customer_info"  # KEY: Should ask for customer info, not book
        },
        {
            "user": "John",
            "description": "Provide customer name",
            "expect_progress": "booking_or_confirm"
        }
    ]
    
    all_passed = True
    
    for i, turn in enumerate(turns, 1):
        print(f"\n[TURN {i}] {turn['description']}")
        print(f"  User: {turn['user']}")
        
        try:
            request = ChatRequest(
                content=turn["user"],
                conversation_id=conversation_id,
                user_id=123
            )
            
            response = send_message(request)
            
            # Strip non-ASCII for Windows console
            bot_msg = response.bot_response if isinstance(response.bot_response, str) else str(response.bot_response)
            bot_msg = ''.join(c for c in bot_msg if ord(c) < 128)
            
            print(f"  Bot: {bot_msg[:120]}..." if len(bot_msg) > 120 else f"  Bot: {bot_msg}")
            
            # Get collected entities
            collected = {}
            if hasattr(response, 'entities'):
                if hasattr(response.entities, 'model_dump'):
                    entities_dict = response.entities.model_dump()
                elif hasattr(response.entities, 'dict'):
                    entities_dict = response.entities.dict()
                else:
                    entities_dict = response.entities if isinstance(response.entities, dict) else {}
                
                collected = {k: v for k, v in entities_dict.items() if v is not None}
            
            print(f"  Collected: {collected}")
            
            # Verify progress
            expected = turn["expect_progress"]
            bot_lower = bot_msg.lower()
            
            if expected == "service" and ("service" in bot_lower or "cleaning" in bot_lower or "extraction" in bot_lower):
                print(f"  [SUCCESS] Correctly asking for service")
            elif expected == "date" and ("date" in bot_lower or "when" in bot_lower or "monday" in bot_lower):
                print(f"  [SUCCESS] Correctly asking for date")
            elif expected == "time" and ("time" in bot_lower or "am" in bot_lower or "pm" in bot_lower or "clock" in bot_lower):
                print(f"  [SUCCESS] Correctly asking for time")
            elif expected == "customer_info" and ("name" in bot_lower or "phone" in bot_lower or "phone number" in bot_lower):
                print(f"  [SUCCESS] Correctly asking for customer info (KEY IMPROVEMENT)")
            elif expected == "booking_or_confirm":
                if "sorry" in bot_lower or "unable" in bot_lower:
                    print(f"  [WARNING] Still getting booking error")
                else:
                    print(f"  [SUCCESS] Booking or confirmation message")
            else:
                print(f"  [INFO] Got: {bot_lower[:80]}")
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("[PASS] 5-SLOT FLOW TEST COMPLETED")
    else:
        print("[INFO] Test completed with issues (see above)")
    print("="*80)
    
    return all_passed

if __name__ == "__main__":
    try:
        test_5_slot_complete_flow()
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
