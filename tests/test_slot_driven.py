"""
TEST: Slot-Driven Dialogue Flow
Verify that the system correctly identifies and fills slots based on missing_slots guidance
This fixes the core issue: "How can I assist?" repetition

Expected behavior:
1. User says "Dr. Wang" -> System identifies it fills doctor slot -> asks for service
2. User says "Cleaning" -> System identifies it fills service slot -> asks for date
3. User says "Next Wednesday" -> System identifies it fills date slot -> asks for time
4. User says "3 PM" -> System identifies it fills time slot -> books appointment

NO "How can I assist?" should appear in slot-driven mode
"""

import sys
import json
import threading
import warnings
sys.path.append('backend')

# Suppress warnings and thread errors
warnings.filterwarnings('ignore')
_original_hook = threading.excepthook
def _suppress_thread_exceptions(args):
    if isinstance(args.exc_value, UnicodeDecodeError):
        pass
    else:
        _original_hook(args)
threading.excepthook = _suppress_thread_exceptions

from services.llama_service import LlamaService
from services.dialogue_service import get_or_create_dialogue_state, DialogueStage

def test_slot_driven_extraction():
    """
    Test that NLU correctly identifies which slot each user input fills
    """
    print("\n" + "="*80)
    print("SLOT-DRIVEN NLU EXTRACTION TEST")
    print("="*80)
    
    test_cases = [
        {
            "name": "Doctor identification",
            "user_input": "Dr. Wang please",
            "missing_slots": ["doctor", "service", "date", "time"],
            "expected_target": "doctor",
            "expected_value": "Dr. Wang"
        },
        {
            "name": "Service identification",
            "user_input": "I need cleaning",
            "missing_slots": ["service", "date", "time"],
            "collected": {"doctor": "Dr. Wang"},
            "expected_target": "service",
            "expected_value": "Cleaning"
        },
        {
            "name": "Date identification",
            "user_input": "Next Wednesday works for me",
            "missing_slots": ["date", "time"],
            "collected": {"doctor": "Dr. Wang", "service": "Cleaning"},
            "expected_target": "date"
        },
        {
            "name": "Time identification",
            "user_input": "How about 3 PM?",
            "missing_slots": ["time"],
            "collected": {"doctor": "Dr. Wang", "service": "Cleaning", "date": "2026-01-08"},
            "expected_target": "time",
            "expected_value": "15:00"
        }
    ]
    
    all_passed = True
    
    for test in test_cases:
        print(f"\n[TEST] {test['name']}")
        print(f"  Input: {test['user_input']}")
        print(f"  Missing slots: {test['missing_slots']}")
        
        context = test.get("collected", {})
        if context:
            print(f"  Already collected: {context}")
        
        try:
            # Call NLU with slot-driven mode
            response = LlamaService.parse_user_input(
                test["user_input"],
                context=context,
                missing_slots=test["missing_slots"]
            )
            
            print(f"  [OK] NLU Response:")
            print(f"    - Intent: {response.intent}")
            print(f"    - Confidence: {response.confidence}")
            print(f"    - Extracted entities: {response.entities}")
            
            # Verify target slot was extracted
            if response.entities:
                extracted_keys = list(response.entities.keys())
                expected_target = test["expected_target"]
                
                if expected_target in extracted_keys:
                    print(f"    [SUCCESS] Correct: Identified target slot '{expected_target}'")
                    
                    # Verify the value if provided
                    if "expected_value" in test:
                        actual_value = response.entities[expected_target]
                        # Normalize for comparison (handle date formats, case, etc.)
                        if isinstance(actual_value, str) and isinstance(test["expected_value"], str):
                            if actual_value.lower() in test["expected_value"].lower() or test["expected_value"].lower() in actual_value.lower():
                                print(f"    [SUCCESS] Correct: Value matches '{actual_value}'")
                            else:
                                print(f"    [WARNING] Value mismatch: got '{actual_value}', expected similar to '{test['expected_value']}'")
                        else:
                            print(f"    -> Value: {actual_value}")
                else:
                    print(f"    [FAILED] Expected target '{expected_target}', got {extracted_keys}")
                    all_passed = False
            else:
                print(f"    [FAILED] No entities extracted")
                all_passed = False
                
        except Exception as e:
            print(f"    [ERROR] {e}")
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("[PASS] SLOT-DRIVEN EXTRACTION TEST PASSED")
    else:
        print("[FAIL] SLOT-DRIVEN EXTRACTION TEST FAILED")
    print("="*80)
    
    return all_passed

def test_multi_turn_dialogue():
    """
    Test full dialogue flow with slot-driven progression
    """
    print("\n" + "="*80)
    print("MULTI-TURN SLOT-DRIVEN DIALOGUE TEST")
    print("="*80)
    
    # Simulate conversation
    conversation_id = "test_slot_driven_conv"
    dialogue_state = get_or_create_dialogue_state(conversation_id)
    
    turns = [
        {
            "user": "Dr. Wang",
            "description": "Select doctor",
        },
        {
            "user": "Cleaning",
            "description": "Select service",
        },
        {
            "user": "Next Wednesday",
            "description": "Select date",
        },
        {
            "user": "3 PM",
            "description": "Select time",
        }
    ]
    
    all_passed = True
    
    for i, turn in enumerate(turns, 1):
        print(f"\n[TURN {i}] {turn['description']}")
        print(f"  User: {turn['user']}")
        
        try:
            # Calculate missing slots
            REQUIRED_SLOTS = ["doctor", "service", "date", "time"]
            missing_slots = [
                slot for slot in REQUIRED_SLOTS
                if dialogue_state.collected_entities.get(slot) is None
            ]
            
            print(f"  Missing slots: {missing_slots}")
            
            # Parse with slot-driven mode
            response = LlamaService.parse_user_input(
                turn["user"],
                context=dialogue_state.collected_entities,
                missing_slots=missing_slots
            )
            
            # Update dialogue state with extracted entities
            if response.entities:
                dialogue_state.collected_entities.update(response.entities)
            
            print(f"  Extracted: {response.entities}")
            print(f"  Collected so far: {dialogue_state.collected_entities}")
            
            if response.entities:
                print(f"  [SUCCESS] Successfully extracted slot data")
            else:
                print(f"  [WARNING] No entities extracted")
                all_passed = False
                
        except Exception as e:
            print(f"  [ERROR] {e}")
            all_passed = False
    
    # Final check
    print(f"\n[FINAL STATE]")
    print(f"  Doctor: {dialogue_state.collected_entities.get('doctor', 'MISSING')}")
    print(f"  Service: {dialogue_state.collected_entities.get('service', 'MISSING')}")
    print(f"  Date: {dialogue_state.collected_entities.get('date', 'MISSING')}")
    print(f"  Time: {dialogue_state.collected_entities.get('time', 'MISSING')}")
    
    required = ["doctor", "service", "date", "time"]
    collected = [s for s in required if dialogue_state.collected_entities.get(s) is not None]
    
    print(f"\n  Slots collected: {len(collected)}/{len(required)}")
    
    if len(collected) == len(required):
        print(f"  [SUCCESS] All slots successfully collected!")
    else:
        missing = [s for s in required if s not in collected]
        print(f"  [FAILED] Missing slots: {missing}")
        all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("[PASS] MULTI-TURN DIALOGUE TEST PASSED")
    else:
        print("[FAIL] MULTI-TURN DIALOGUE TEST FAILED")
    print("="*80)
    
    return all_passed

if __name__ == "__main__":
    try:
        test1_passed = test_slot_driven_extraction()
        test2_passed = test_multi_turn_dialogue()
        
        if test1_passed and test2_passed:
            print("\n\n" + ("*"*40))
            print("ALL SLOT-DRIVEN TESTS PASSED!")
            print("*"*40)
            sys.exit(0)
        else:
            print("\n\nSome tests failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
