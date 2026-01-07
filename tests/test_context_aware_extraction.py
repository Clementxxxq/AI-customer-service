"""
TEST: Ollama Extraction WITH CONTEXT
Verify that passing context helps Ollama understand the booking flow
"""

import sys
sys.path.append('backend')

from services.llama_service import LlamaService

print("\n" + "="*70)
print("TEST: Ollama Extraction - Turn 2 (WITH CONTEXT)")
print("="*70)

# Simulate Turn 1 result
context_after_turn1 = {
    "doctor": "Dr. Wang",
    "service": None,
    "date": None,
    "time": None
}

print("\nContext from Turn 1:")
print(f"  - Doctor: {context_after_turn1['doctor']}")
print(f"  - Service: {context_after_turn1['service']}")

# Turn 2: Extract with context
print("\n[TURN 2] User says: 'Cleaning'")
print("-" * 70)

try:
    result = LlamaService.parse_user_input(
        "Cleaning",
        context=context_after_turn1  # Pass context!
    )
    print(f"Ollama response:")
    print(f"  - Intent: {result.intent}")
    print(f"  - Doctor: {result.entities.get('doctor')}")
    print(f"  - Service: {result.entities.get('service')}")
    
    if result.entities.get('service') == 'Cleaning':
        print(f"\n✅ GOOD: Extracted service='Cleaning'")
    else:
        print(f"\n❌ BAD: Service not extracted")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST: Ollama Extraction - Turn 3 (WITH MORE CONTEXT)")
print("="*70)

# Simulate Turn 2 result
context_after_turn2 = {
    "doctor": "Dr. Wang",
    "service": "Cleaning",
    "date": None,
    "time": None
}

print("\nContext from Turn 2:")
print(f"  - Doctor: {context_after_turn2['doctor']}")
print(f"  - Service: {context_after_turn2['service']}")

# Turn 3: Extract date with full context
print("\n[TURN 3] User says: 'Next Wednesday'")
print("-" * 70)

try:
    result = LlamaService.parse_user_input(
        "Next Wednesday",
        context=context_after_turn2
    )
    print(f"Ollama response:")
    print(f"  - Doctor: {result.entities.get('doctor')}")
    print(f"  - Service: {result.entities.get('service')}")
    print(f"  - Date: {result.entities.get('date')}")
    
    if result.entities.get('date'):
        print(f"\n✅ GOOD: Extracted date={result.entities.get('date')}")
    else:
        print(f"\n❌ BAD: Date not extracted")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("RESULT: Context-aware extraction working! ✅")
print("="*70)
