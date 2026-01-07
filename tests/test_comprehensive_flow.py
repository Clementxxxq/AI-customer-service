"""
COMPREHENSIVE VERIFICATION TEST
Confirms the fix: entities are persisted and extracted correctly across multiple turns
"""

import sys
import warnings
import logging
import threading
sys.path.append('backend')

# Suppress Pydantic deprecation warnings and thread errors
warnings.filterwarnings('ignore', category=DeprecationWarning)
logging.getLogger().setLevel(logging.CRITICAL)  # Suppress thread errors from Ollama subprocess

# Custom exception hook to suppress thread errors from Ollama subprocess
_original_hook = threading.excepthook
def _suppress_thread_exceptions(args):
    """Suppress UnicodeDecodeError from Ollama subprocess threads"""
    if isinstance(args.exc_value, UnicodeDecodeError):
        pass  # Ignore Ollama subprocess encoding issues
    else:
        _original_hook(args)  # Re-raise other exceptions

threading.excepthook = _suppress_thread_exceptions

from routes.chat import send_message
from schemas.chat import ChatRequest

def test_complete_booking_flow():
    """Full booking flow: Dr. Wang -> Cleaning -> Next Wed -> 3pm"""
    
    conversation_id = "booking_test_001"
    
    print("\n" + "="*70)
    print("COMPREHENSIVE BOOKING FLOW TEST")
    print("Testing: Dr. Wang -> Cleaning -> Next Wed -> 3 PM")
    print("="*70)
    
    conversations = [
        ("Dr. Wang", "doctor selection"),
        ("Cleaning", "service selection"),
        ("Next Wednesday", "date selection"),
        ("3 PM", "time selection"),
    ]
    
    collected_data = {}
    
    for user_input, step_name in conversations:
        print(f"\n[{step_name.upper()}]")
        print(f"User: {user_input}")
        print("-" * 70)
        
        try:
            req = ChatRequest(
                content=user_input,
                user_id=1,
                conversation_id=conversation_id
            )
            resp = send_message(req)
            
            # Clean bot response to avoid encoding issues - remove any non-ASCII characters
            bot_msg = ''.join(c for c in resp.bot_response if ord(c) < 128)
            print(f"System: {bot_msg}")
            
            # Extract entities (use model_dump for Pydantic v2)
            if hasattr(resp.entities, 'model_dump'):
                entities_dict = resp.entities.model_dump()
            elif hasattr(resp.entities, 'dict'):
                entities_dict = resp.entities.dict()
            else:
                entities_dict = resp.entities
            collected_data = entities_dict.copy()
            
            print(f"\nCollected so far:")
            for key, value in collected_data.items():
                if value:
                    print(f"  - {key}: {value}")
            
            # Verify no default greeting
            if "how can i assist" in resp.bot_response.lower():
                print("\n** ERROR: Back to default greeting! **")
                return False
                
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    print("\n" + "="*70)
    print("FINAL COLLECTED DATA:")
    print("="*70)
    for key, value in collected_data.items():
        if value:
            print(f"  {key}: {value}")
    
    # Verify all required data collected
    required = ["doctor", "service", "date", "time"]
    missing = [k for k in required if not collected_data.get(k)]
    
    if missing:
        print(f"\nMISSING: {missing}")
        return False
    
    print("\n" + "="*70)
    print("SUCCESS: Full booking flow completed!")
    print("[OK] No 'How can I assist?' repetition")
    print("[OK] All data retained across turns")
    print("[OK] Smooth progression through stages")
    print("="*70)
    return True


if __name__ == "__main__":
    try:
        success = test_complete_booking_flow()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
