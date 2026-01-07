"""
Dialogue State Management Service
Handles conversation context and multi-turn dialogue flow
"""
from typing import Dict, Any, Optional
from datetime import datetime
from utils.doctor_validator import normalize_and_validate_doctor, get_doctor_selection_prompt

# Global dialogue states - keyed by conversation_id
# In production, use a proper database or cache
DIALOGUE_STATES: Dict[str, Dict[str, Any]] = {}


class DialogueState:
    """Represents the state of a conversation"""
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.intent = None  # What the user wants to do (e.g., "appointment")
        self.collected_entities = {}  # {doctor, service, date, time, customer_name, customer_phone, customer_email}
        self.current_question = None  # What question to ask next
        self.message_count = 0  # How many messages in this conversation
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "conversation_id": self.conversation_id,
            "intent": self.intent,
            "collected_entities": self.collected_entities,
            "current_question": self.current_question,
            "message_count": self.message_count,
            "created_at": self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DialogueState":
        """Create from dictionary"""
        state = DialogueState(data["conversation_id"])
        state.intent = data.get("intent")
        state.collected_entities = data.get("collected_entities", {})
        state.current_question = data.get("current_question")
        state.message_count = data.get("message_count", 0)
        if isinstance(data.get("created_at"), str):
            state.created_at = datetime.fromisoformat(data["created_at"])
        return state


def get_or_create_dialogue_state(conversation_id: str) -> DialogueState:
    """Get existing dialogue state or create new one"""
    if conversation_id not in DIALOGUE_STATES:
        DIALOGUE_STATES[conversation_id] = DialogueState(conversation_id).to_dict()
    
    return DialogueState.from_dict(DIALOGUE_STATES[conversation_id])


def save_dialogue_state(state: DialogueState) -> None:
    """Save dialogue state"""
    state.message_count += 1
    DIALOGUE_STATES[state.conversation_id] = state.to_dict()


def merge_entities_with_state(
    new_entities: Dict[str, Any],
    conversation_id: str
) -> Dict[str, Any]:
    """
    Merge newly parsed entities with existing dialogue state
    Keeps previously collected information
    """
    state = get_or_create_dialogue_state(conversation_id)
    
    # Merge: new entities override old ones, but keep old if new is None
    merged = {**state.collected_entities}
    for key, value in new_entities.items():
        if value is not None:
            merged[key] = value
    
    return merged


def determine_next_question(
    intent: str,
    collected_entities: Dict[str, Any]
) -> Optional[str]:
    """
    Determine what question to ask next based on what info is missing
    For appointment intent, required fields: doctor, service, date, time
    
    ✅ Doctor question now shows available options
    """
    if intent != "appointment":
        return None
    
    # Check what's missing for appointment booking
    required = ["doctor", "service", "date", "time"]
    
    for field in required:
        if not collected_entities.get(field):
            # Ask for this field
            if field == "doctor":
                # Use product-level doctor selection prompt
                return get_doctor_selection_prompt()
            
            questions = {
                "service": "What service do you need?",
                "date": "What date would you like?",
                "time": "What time works for you?"
            }
            return questions.get(field)
    
    # All required fields collected
    return None


def is_appointment_ready(entities: Dict[str, Any]) -> bool:
    """Check if we have all required info to book an appointment"""
    required = ["doctor", "service", "date", "time"]
    return all(entities.get(field) for field in required)


def reset_dialogue_state(conversation_id: str) -> None:
    """Reset dialogue state for a conversation"""
    if conversation_id in DIALOGUE_STATES:
        del DIALOGUE_STATES[conversation_id]
