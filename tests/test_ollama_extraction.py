"""
TEST OLLAMA DIRECTLY
See what Ollama actually returns for "Cleaning"
"""

import sys
sys.path.append('backend')

from services.llama_service import LlamaService

print("\n" + "="*70)
print("TEST: What does Ollama extract from 'Cleaning'?")
print("="*70)

try:
    result = LlamaService.parse_user_input("Cleaning")
    print(f"\nRaw result: {result}")
    print(f"\nIntent: {result.intent}")
    print(f"Confidence: {result.confidence}")
    print(f"Entities: {result.entities}")
    print(f"  - Doctor: {result.entities.get('doctor')}")
    print(f"  - Service: {result.entities.get('service')}")
    print(f"  - Date: {result.entities.get('date')}")
    print(f"  - Time: {result.entities.get('time')}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TEST: What does Ollama extract from 'Dr. Wang'?")
print("="*70)

try:
    result = LlamaService.parse_user_input("Dr. Wang")
    print(f"\nIntent: {result.intent}")
    print(f"Entities: {result.entities}")
    print(f"  - Doctor: {result.entities.get('doctor')}")
    print(f"  - Service: {result.entities.get('service')}")
    
except Exception as e:
    print(f"Error: {e}")
