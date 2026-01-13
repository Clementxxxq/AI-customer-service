"""
Planner AI Service - Slot Filling and Dialogue Planning

This layer sits between NLU and Business Logic:
[NLU Output] → [Planner] → [Business Logic]

Planner responsibilities:
✅ Decide next question based on collected slots
✅ Generate natural language responses (NOT bot response - just question templates)
✅ Determine if all required slots are filled
✅ Handle dialogue flow (ask about doctor, service, date, time in order)

This is NOT the NLU layer - the NLU only extracts what user said.
Planner decides what to do next.

Prompt engineering for slot-filling decisions is here, not in NLU.
"""

import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel


class PlannerDecision(BaseModel):
    """Planner's decision about next action"""
    action: str  # "ask_for_slot" | "execute_booking" | "provide_info" | "clarify"
    slot_to_fill: Optional[str] = None  # "doctor", "service", "date", "time", "customer_name"
    message: str  # Natural language prompt or action description
    reasoning: Optional[str] = None  # Why this decision was made


class PlannerService:
    """Service to plan dialogue flow and determine next actions"""
    
    # Required slots for appointment booking (in order of asking)
    APPOINTMENT_SLOTS = ["doctor", "service", "date", "time"]
    OPTIONAL_SLOTS = ["customer_name", "customer_phone", "customer_email"]
    
    @staticmethod
    def plan_next_action(
        intent: str,
        collected_entities: Dict[str, Any],
        conversation_history: Optional[List[Dict]] = None
    ) -> PlannerDecision:
        """
        Decide the next action based on intent and collected entities
        
        Args:
            intent: User's intent (appointment|query|cancel|modify|other)
            collected_entities: Already collected entities from previous turns
            conversation_history: Past messages for context
            
        Returns:
            PlannerDecision with action and message
        """
        
        if intent == "appointment":
            return PlannerService._plan_appointment_booking(collected_entities)
        elif intent == "cancel":
            return PlannerService._plan_appointment_cancellation(collected_entities)
        elif intent == "modify":
            return PlannerService._plan_appointment_modification(collected_entities)
        elif intent == "query":
            return PlannerService._plan_info_query(collected_entities)
        else:
            return PlannerDecision(
                action="clarify",
                message="I'm not sure how to help with that. Are you looking to book an appointment, cancel, or need information about our services?"
            )
    
    @staticmethod
    def _plan_appointment_booking(entities: Dict[str, Any]) -> PlannerDecision:
        """Plan appointment booking flow - ask for missing slots in order"""
        
        # Check which required slots are missing
        missing_slots = []
        for slot in PlannerService.APPOINTMENT_SLOTS:
            if not entities.get(slot):
                missing_slots.append(slot)
        
        if not missing_slots:
            # All slots filled - ready to execute
            return PlannerDecision(
                action="execute_booking",
                message="Ready to book the appointment",
                reasoning="All required slots collected"
            )
        
        # Ask for the first missing slot
        next_slot = missing_slots[0]
        return PlannerService._generate_slot_question(next_slot, entities)
    
    @staticmethod
    def _plan_appointment_cancellation(entities: Dict[str, Any]) -> PlannerDecision:
        """Plan appointment cancellation flow"""
        
        # For cancellation, we need to identify which appointment
        # Either by date+time or by appointment ID
        has_identifier = entities.get("date") or entities.get("appointment_id")
        
        if not has_identifier:
            return PlannerDecision(
                action="ask_for_slot",
                slot_to_fill="date",
                message="Which appointment would you like to cancel? Please provide the date and time (e.g., 'January 15 at 2 PM')"
            )
        
        return PlannerDecision(
            action="execute_booking",
            message="Ready to cancel the appointment",
            reasoning="Have appointment identifier"
        )
    
    @staticmethod
    def _plan_appointment_modification(entities: Dict[str, Any]) -> PlannerDecision:
        """Plan appointment modification flow"""
        
        # First identify which appointment, then ask what to change
        has_identifier = entities.get("date") or entities.get("appointment_id")
        
        if not has_identifier:
            return PlannerDecision(
                action="ask_for_slot",
                slot_to_fill="date",
                message="Which appointment would you like to reschedule? Please provide the original date and time"
            )
        
        # Now ask what to change it to
        return PlannerDecision(
            action="ask_for_slot",
            slot_to_fill="date",
            message="What date and time would work better for you?"
        )
    
    @staticmethod
    def _plan_info_query(entities: Dict[str, Any]) -> PlannerDecision:
        """Plan information query response"""
        
        doctor = entities.get("doctor")
        service = entities.get("service")
        
        if doctor:
            return PlannerDecision(
                action="provide_info",
                message=f"I'll provide information about {doctor}",
                reasoning="User asked about specific doctor"
            )
        elif service:
            return PlannerDecision(
                action="provide_info",
                message=f"I'll provide information about {service}",
                reasoning="User asked about specific service"
            )
        else:
            return PlannerDecision(
                action="provide_info",
                message="I'll provide general information about our services and doctors",
                reasoning="General information query"
            )
    
    @staticmethod
    def _generate_slot_question(slot: str, context: Dict[str, Any]) -> PlannerDecision:
        """Generate natural language question for a specific slot"""
        
        # Professional, customer-friendly questions
        questions = {
            "doctor": "Which doctor would you prefer to see? We have Dr. Wang, Dr. Chen, and Dr. Li available.",
            "service": "What service are you interested in? We offer Cleaning, Extraction, and Checkup.",
            "date": "What date would work best for you?",
            "time": "What time would you prefer?",
            "customer_name": "Could I have your name, please?",
            "customer_phone": "What's the best phone number to reach you?",
            "customer_email": "What's your email address?"
        }
        
        message = questions.get(
            slot,
            f"Could you provide {slot} for us?"
        )
        
        return PlannerDecision(
            action="ask_for_slot",
            slot_to_fill=slot,
            message=message
        )
    
    @staticmethod
    def is_appointment_completable(entities: Dict[str, Any]) -> bool:
        """Check if we have all required info to book appointment"""
        required = ["doctor", "service", "date", "time"]
        return all(entities.get(slot) for slot in required)
    
    @staticmethod
    def get_collected_status(entities: Dict[str, Any]) -> Dict[str, bool]:
        """Get status of all slots"""
        return {
            "doctor": bool(entities.get("doctor")),
            "service": bool(entities.get("service")),
            "date": bool(entities.get("date")),
            "time": bool(entities.get("time")),
            "customer_name": bool(entities.get("customer_name")),
            "customer_phone": bool(entities.get("customer_phone")),
            "customer_email": bool(entities.get("customer_email"))
        }
