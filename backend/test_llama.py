#!/usr/bin/env python
"""Quick test of Llama service"""

from services.llama_service import LlamaService

if __name__ == "__main__":
    test_cases = [
        "Book with Dr. Wang tomorrow at 2 PM",
        "Cancel my 10 AM appointment today",
        "What is Dr. Li's specialization?",
    ]
    
    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"User: {test}")
        print('='*60)
        
        try:
            response = LlamaService.parse_user_input(test)
            print(f"✓ Intent: {response.intent}")
            print(f"✓ Confidence: {response.confidence}")
            print(f"✓ Doctor: {response.entities.get('doctor')}")
            print(f"✓ Date: {response.entities.get('date')}")
            print(f"✓ Time: {response.entities.get('time')}")
        except Exception as e:
            print(f"✗ Error: {e}")
