#!/usr/bin/env python3
"""
Demo Script: How to use the improved dialogue state machine

This script demonstrates how to use the new API to implement natural, 
fluent multi-turn conversations for a dental appointment chatbot.
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from services.dialogue_service import (
    DialogueState, DialogueStage, get_or_create_dialogue_state,
    determine_next_question_and_stage, merge_entities_with_state,
    should_stay_in_appointment_mode, save_dialogue_state
)


class DemoDentistChatbot:
    """Demo dental appointment chatbot"""
    
    def __init__(self, conversation_id="demo"):
        self.conversation_id = conversation_id
        self.state = get_or_create_dialogue_state(conversation_id)
        
    def process_message(self, user_input, llm_intent, llm_entities):
        """
        Process user message (simulates LLM output)
        
        Args:
            user_input: Text input from user
            llm_intent: Intent recognized by LLM
            llm_entities: Entities extracted by LLM
        """
        print(f"\n{'─'*60}")
        print(f"👤 User: {user_input}")
        print(f"Current stage: {self.state.stage.value}")
        
        # Key decision: whether to stay in appointment mode
        should_stay = should_stay_in_appointment_mode(
            self.state.stage,
            llm_intent,
            user_input
        )
        
        if should_stay:
            print(f"✅ Stay in appointment mode (ignore LLM's '{llm_intent}' intent)")
            llm_intent = "appointment"
        else:
            print(f"→ Use LLM intent: {llm_intent}")
        
        # Merge entities
        merged_entities = merge_entities_with_state(
            llm_entities,
            self.conversation_id,
            current_intent=llm_intent
        )
        
        # Update state
        self.state.intent = llm_intent
        self.state.collected_entities = merged_entities
        
        # State transition
        next_question, next_stage = determine_next_question_and_stage(
            self.state.stage,
            self.state.collected_entities,
            llm_entities
        )
        
        # Update stage
        self.state.stage = next_stage
        
        # Show progress
        print(f"Collected: {json.dumps({k:v for k,v in merged_entities.items() if v}, indent=11)}")
        print(f"New stage: {next_stage.value}")
        
        # Generate response
        if next_question:
            bot_response = next_question
            print(f"🤖 Bot: {bot_response}")
        else:
            bot_response = f"✅ Booking Confirmed!\nDoctor: {merged_entities.get('doctor')}\nService: {merged_entities.get('service')}\nDate: {merged_entities.get('date')}\nTime: {merged_entities.get('time')}"
            print(f"🤖 Bot: {bot_response}")
        
        # Save state
        save_dialogue_state(self.state)
        
        return bot_response


def demo_normal_flow():
    """Demo: Normal appointment booking flow"""
    print("\n" + "="*60)
    print("📋 Demo 1: Normal Appointment Flow")
    print("="*60)
    
    bot = DemoDentistChatbot("demo_normal")
    
    # Conversation flow
    conversation = [
        ("I want to see Dr. Wang", "appointment", {"doctor": "Dr. Wang"}),
        ("I need a cleaning", "query", {"service": "cleaning"}),  # LLM says query, but we stay in appointment mode
        ("Next Monday", "other", {"date": "2026-01-13"}),
        ("10 AM", "query", {"time": "10:00"}),
    ]
    
    for user_msg, llm_intent, llm_entities in conversation:
        bot.process_message(user_msg, llm_intent, llm_entities)


def demo_conflicting_intents():
    """Demo: Handling conflicting intents"""
    print("\n" + "="*60)
    print("📋 Demo 2: Handling Conflicting Intents")
    print("="*60)
    
    bot = DemoDentistChatbot("demo_conflict")
    
    # In the middle of appointment, user says things that could be misunderstood
    conversation = [
        ("Doctor Wang", "appointment", {"doctor": "Wang"}),
        ("Extraction", "appointment", {"service": "extraction"}),  # LLM correctly identified
        ("Can you do emergency?", "query", {"service": "emergency"}),  # LLM says query, but we stay in appointment
        ("Friday", "other", {"date": "2026-01-17"}),
        ("2 PM", "query", {"time": "14:00"}),  # LLM says query again, but it doesn't matter
    ]
    
    for user_msg, llm_intent, llm_entities in conversation:
        bot.process_message(user_msg, llm_intent, llm_entities)


def demo_stage_progression():
    """Demo: Stage progression"""
    print("\n" + "="*60)
    print("📋 Demo 3: Detailed Stage Progression")
    print("="*60)
    
    bot = DemoDentistChatbot("demo_stages")
    
    print("\nStage progression:")
    print(f"  INITIAL (needs doctor)")
    print(f"    ↓")
    print(f"  DOCTOR_SELECTED (needs service)")
    print(f"    ↓")
    print(f"  SERVICE_SELECTED (needs date)")
    print(f"    ↓")
    print(f"  DATETIME_PENDING (needs time)")
    print(f"    ↓")
    print(f"  BOOKING_COMPLETE (ready for booking)")
    
    print("\n\nActual conversation:")
    
    steps = [
        ("Dr. Smith", "appointment", {"doctor": "Smith"}),
        ("Filling", "appointment", {"service": "filling"}),
        ("Tomorrow", "appointment", {"date": "2026-01-07"}),
        ("3:30 PM", "appointment", {"time": "15:30"}),
    ]
    
    for user_msg, llm_intent, llm_entities in steps:
        bot.process_message(user_msg, llm_intent, llm_entities)


def demo_key_improvement():
    """Demo: Key improvement"""
    print("\n" + "="*60)
    print("🎯 Key Improvement: 'Cleaning' is correctly handled in appointment flow")
    print("="*60)
    
    print("\nComparison:")
    print("\n❌ Before improvement:")
    print("  User: 'Cleaning'")
    print("  LLM: intent='query'")
    print("  System: intent != appointment → default response 'How can I assist?'")
    print("  Result: User input is ignored ❌")
    
    print("\n✅ After improvement:")
    print("  User: 'Cleaning'")
    print("  LLM: intent='query'")
    print("  System: stage=DOCTOR_SELECTED → should_stay_in_appointment_mode=True")
    print("  System: Force intent='appointment'")
    print("  System: Extract service='Cleaning'")
    print("  System: Transition stage to SERVICE_SELECTED")
    print("  System: Ask next: 'What date would you like?'")
    print("  Result: Conversation flows naturally ✅")


def main():
    print("\n" + "="*60)
    print("🦷 Dental Appointment Chatbot - Dialogue State Machine Improvement Demo")
    print("="*60)
    
    print("\nThis demo shows how the improved multi-turn conversation system works:")
    print("  • Remember conversation stage")
    print("  • Understand user input based on stage")
    print("  • Natural and fluent conversation progression")
    print("  • Handle LLM's incorrect intents")
    
    # Run all demos
    demo_normal_flow()
    demo_conflicting_intents()
    demo_stage_progression()
    demo_key_improvement()
    
    # Summary
    print("\n" + "="*60)
    print("✅ Demo Complete!")
    print("="*60)
    
    print("\n📚 Core Concepts:")
    print("  1. DialogueStage tracks the current conversation stage")
    print("  2. Once in appointment flow, all input is treated as appointment data")
    print("  3. State machine automatically advances to next stage")
    print("  4. System never loses context or repeats questions")
    
    print("\n📖 Learn More:")
    print("  • Detailed docs: docs/DIALOGUE_STATE_MACHINE_IMPROVEMENT.md")
    print("  • Quick reference: docs/DIALOGUE_STATE_MACHINE_QUICK_REFERENCE.md")
    print("  • Test file: tests/test_dialogue_state_machine.py")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()
