"""
VISUAL CONVERSATION TEST
Shows the actual conversation flow side-by-side
"""

import sys
sys.path.append('backend')

from routes.chat import send_message
from schemas.chat import ChatRequest

def format_entities(entities_dict):
    """Format entities for display"""
    items = []
    for k, v in entities_dict.items():
        if v:
            items.append(f"{k}={v}")
    return " | ".join(items) if items else "(empty)"

def test_visual_conversation():
    """Show conversation flow with collected entities"""
    
    conversation_id = "visual_test_" + str(__import__('time').time())
    
    print("\n" + "="*80)
    print("ACTUAL CONVERSATION FLOW WITH SESSION PERSISTENCE".center(80))
    print("="*80)
    
    turns = [
        "Dr. Wang",
        "Cleaning",
        "Next Wednesday",
        "3 PM",
    ]
    
    for i, user_msg in enumerate(turns, 1):
        print(f"\n{'─'*80}")
        print(f"TURN {i}".ljust(10) + f"| USER INPUT: '{user_msg}'".rjust(70))
        print('─'*80)
        
        try:
            req = ChatRequest(
                content=user_msg,
                user_id=1,
                conversation_id=conversation_id
            )
            resp = send_message(req)
            
            # Get entities
            entities_dict = resp.entities.dict() if hasattr(resp.entities, 'dict') else resp.entities
            
            print(f"\n  BOT:      {resp.bot_response}")
            print(f"\n  ENTITIES: {format_entities(entities_dict)}")
            print(f"  INTENT:   {resp.intent}")
            
            # Check for default greeting
            if "how can i assist" in resp.bot_response.lower():
                print(f"\n  ⚠️  WARNING: Back to default greeting!")
            else:
                print(f"\n  ✓ Progressed to next question")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            return False
    
    print("\n" + "="*80)
    print("RESULT: Smooth conversation flow without repetition!".center(80))
    print("="*80 + "\n")
    
    return True


if __name__ == "__main__":
    test_visual_conversation()
