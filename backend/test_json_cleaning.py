#!/usr/bin/env python
"""Verify JSON cleaning works correctly"""

from services.llama_service import LlamaService

def test_json_cleaning():
    """Test the _clean_json method"""
    
    test_cases = [
        # Case 1: Comment after value
        (
            '{\n  "intent": "appointment",\n  "confidence": 0.95, // comment\n  "entities": {}\n}',
            {"intent": "appointment", "confidence": 0.95}
        ),
        # Case 2: Block comment
        (
            '{ /* comment */ "intent": "appointment", "confidence": 0.95 }',
            {"intent": "appointment", "confidence": 0.95}
        ),
        # Case 3: Trailing comma
        (
            '{"intent": "appointment", "confidence": 0.95,}',
            {"intent": "appointment", "confidence": 0.95}
        ),
        # Case 4: Mixed issues
        (
            '''{ 
  "intent": "appointment", // this is the intent
  "confidence": 0.95, /* confidence score */
  "entities": { "doctor": "Dr. Wang", } // entities,
}''',
            {"intent": "appointment"}
        ),
    ]
    
    print("Testing JSON Cleaning\n" + "="*60)
    
    for i, (dirty_json, expected_keys) in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input: {dirty_json[:50]}...")
        
        try:
            cleaned = LlamaService._clean_json(dirty_json)
            import json
            parsed = json.loads(cleaned)
            
            # Check if expected keys exist
            all_match = all(k in parsed for k in expected_keys)
            if all_match:
                print(f"✓ PASS - JSON cleaned and parsed successfully")
                print(f"  Parsed: {parsed}")
            else:
                print(f"✗ FAIL - Missing expected keys")
                print(f"  Got: {parsed}")
                print(f"  Expected keys: {expected_keys}")
        except Exception as e:
            print(f"✗ FAIL - {e}")
            print(f"  Cleaned: {LlamaService._clean_json(dirty_json)}")
    
    print("\n" + "="*60)
    print("All tests completed!")

if __name__ == "__main__":
    test_json_cleaning()
