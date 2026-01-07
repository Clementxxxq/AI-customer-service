"""
TEST: Session Memory Persistence Diagnosis
Verify whether conversation_id properly persists state across turns
"""

import sys
sys.path.append('backend')

from services.dialogue_service import (
    get_or_create_dialogue_state,
    save_dialogue_state,
    merge_entities_with_state,
    determine_next_question_and_stage,
    DIALOGUE_STATES
)

def test_session_persistence():
    """Test if state persists across multiple turns"""
    
    print("\n" + "="*60)
    print("TEST 1: Session Memory Persistence")
    print("="*60)
    
    conversation_id = "test_conv_123"
    
    # Turn 1: User says "Dr. Wang"
    print("\n[TURN 1] User: 'Dr. Wang'")
    state1 = get_or_create_dialogue_state(conversation_id)
    print(f"  Before: stage={state1.stage}, entities={state1.collected_entities}")
    
    new_entities_1 = {"doctor": "Dr. Wang", "service": None, "date": None, "time": None}
    merged_1 = merge_entities_with_state(new_entities_1, conversation_id, "appointment")
    state1.collected_entities = merged_1
    
    next_q, next_stage = determine_next_question_and_stage(state1.stage, merged_1, new_entities_1)
    state1.stage = next_stage
    save_dialogue_state(state1)
    
    print(f"  After:  stage={state1.stage}, entities={state1.collected_entities}")
    print(f"  Saved to DIALOGUE_STATES: {DIALOGUE_STATES[conversation_id]}")
    
    # Turn 2: User says "Cleaning"
    print("\n[TURN 2] User: 'Cleaning'")
    state2 = get_or_create_dialogue_state(conversation_id)
    print(f"  Retrieved: stage={state2.stage}, entities={state2.collected_entities}")
    
    # Key check: Did we retain Dr. Wang?
    if state2.collected_entities.get("doctor") == "Dr. Wang":
        print(f"  ✅ GOOD: Dr. Wang retained from previous turn")
    else:
        print(f"  ❌ BAD: Dr. Wang NOT retained!")
        
    new_entities_2 = {"doctor": None, "service": "Cleaning", "date": None, "time": None}
    merged_2 = merge_entities_with_state(new_entities_2, conversation_id, "appointment")
    state2.collected_entities = merged_2
    
    next_q, next_stage = determine_next_question_and_stage(state2.stage, merged_2, new_entities_2)
    state2.stage = next_stage
    save_dialogue_state(state2)
    
    print(f"  After merge: {state2.collected_entities}")
    print(f"  Next stage: {next_stage}")
    print(f"  Next question: {next_q}")
    
    # Turn 3: User says "Next Wednesday"
    print("\n[TURN 3] User: 'Next Wednesday'")
    state3 = get_or_create_dialogue_state(conversation_id)
    print(f"  Retrieved: stage={state3.stage}, entities={state3.collected_entities}")
    
    if (state3.collected_entities.get("doctor") == "Dr. Wang" and 
        state3.collected_entities.get("service") == "Cleaning"):
        print(f"  ✅ GOOD: Both Dr. Wang and Cleaning retained")
    else:
        print(f"  ❌ BAD: Lost some data")
        
    print("\n" + "="*60)
    print("RESULT: Session memory", 
          "✅ WORKING" if state3.collected_entities.get("doctor") else "❌ BROKEN")
    print("="*60)


if __name__ == "__main__":
    test_session_persistence()
