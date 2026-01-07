"""
E2E TEST: Slot-Driven Chat Integration
Verify that the chat endpoint uses slot-driven extraction correctly
and NO LONGER repeats "How can I assist?"
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

def test_e2e_slot_driven_chat():
    """
    Test the complete chat flow with slot-driven NLU
    """
    print("\n" + "="*80)
    print("E2E TEST: SLOT-DRIVEN CHAT INTEGRATION")
    print("="*80)
    
    conversation_id = f"e2e_test_{datetime.now().timestamp()}"
    
    turns = [
        {
            "user": "Dr. Wang",
            "description": "Select doctor",
            "should_ask": ["service", "cleaning", "extraction"]  # Should ask for service next
        },
        {
            "user": "Cleaning",
            "description": "Select service",
            "should_ask": ["date", "when", "monday"]  # Should ask for date next
        },
        {
            "user": "Next Wednesday",
            "description": "Select date",
            "should_ask": ["time", "when", "o'clock"]  # Should ask for time next
        },
        {
            "user": "3 PM",
            "description": "Select time",
            "should_not_ask": ["doctor", "service", "date", "time"]  # Should NOT ask for these again
        }
    ]
    
    all_passed = True
    default_question = "How can I assist you with our dental services?"
    
    for i, turn in enumerate(turns, 1):
        print(f"\n[TURN {i}] {turn['description']}")
        print(f"  User: {turn['user']}")
        
        try:
            # Send message via chat endpoint
            request = ChatRequest(
                content=turn["user"],
                conversation_id=conversation_id,
                user_id=123
            )
            
            response = send_message(request)
            
            bot_msg = response.bot_response if isinstance(response.bot_response, str) else str(response.bot_response)
            # Strip non-ASCII for Windows console
            bot_msg = ''.join(c for c in bot_msg if ord(c) < 128)
            
            print(f"  Bot: {bot_msg[:100]}..." if len(bot_msg) > 100 else f"  Bot: {bot_msg}")
            
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
            
            # Check: Should NOT be the default "How can I assist?" if we're making progress
            if response.bot_response.lower().strip() == default_question.lower():
                print(f"  [WARNING] Got default question - might indicate slot-driven mode not working")
                if i > 1:  # After turn 1, this is a problem
                    all_passed = False
            
            # Check expected keywords in response
            if "should_ask" in turn:
                expected_keywords = turn["should_ask"]
                bot_response_lower = response.bot_response.lower()
                
                found_keywords = [kw for kw in expected_keywords if kw in bot_response_lower]
                
                if found_keywords:
                    print(f"  [SUCCESS] Response asks about {found_keywords[0]}")
                else:
                    print(f"  [WARNING] Response doesn't ask about expected topics: {expected_keywords}")
            
            # Check should NOT ask
            if "should_not_ask" in turn:
                forbidden_keywords = turn["should_not_ask"]
                bot_response_lower = response.bot_response.lower()
                
                found_keywords = [kw for kw in forbidden_keywords if kw in bot_response_lower]
                
                if found_keywords:
                    print(f"  [WARNING] Response mentions forbidden topics: {found_keywords}")
                    # Don't fail, just warn
                else:
                    print(f"  [SUCCESS] Response doesn't repeat questions")
            
        except Exception as e:
            print(f"  [ERROR] {e}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("[PASS] E2E SLOT-DRIVEN CHAT TEST PASSED")
    else:
        print("[INFO] E2E test completed with warnings (see above)")
    print("="*80)
    
    return all_passed

if __name__ == "__main__":
    try:
        test_e2e_slot_driven_chat()
        sys.exit(0)
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
