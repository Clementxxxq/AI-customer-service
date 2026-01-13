"""
Dialogue State Management Service
Handles conversation context and multi-turn dialogue flow

ARCHITECTURE:
✅ DialogueState: Pure data storage (NO business logic)
✅ State persistence: Abstracted via StateStore (Redis/SQLite ready)
✅ Merging: Properly saves back to state
✅ Intent: Always persisted for multi-turn context
❌ NO AI decisions here (moved to Planner)
❌ NO business validation here (moved to separate layer)

State Storage Options:
- InMemoryStateStore: Development (default)
- RedisStateStore: Production (multi-process)
- SQLiteStateStore: Alternative persistent

Switch stores by calling:
    from services.state_store import set_state_store, RedisStateStore
    set_state_store(RedisStateStore(redis_client))
"""
from typing import Dict, Any, Optional
from datetime import datetime
from services.state_store import get_state_store


class DialogueState:
    """
    Represents the state of a conversation
    
    ✅ RESPONSIBILITIES:
    - Store conversation ID
    - Store detected intent (NOT decide intent)
    - Store collected entities (merged from multiple NLU turns)
    - Track message count (user turns only)
    - Provide serialization
    
    ❌ NOT RESPONSIBILITIES:
    - Validate entities (done in validation layer)
    - Decide next questions (done by Planner AI)
    - Generate responses (done by response generator)
    """
    
    def __init__(self, conversation_id: str):
        self.conversation_id = conversation_id
        self.intent = None  # Set by NLU, NOT by dialogue logic
        self.collected_entities = {}  # Merged from all NLU calls
        self.user_message_count = 0  # ✅ ONLY incremented on user input
        self.created_at = datetime.now()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for storage"""
        return {
            "conversation_id": self.conversation_id,
            "intent": self.intent,
            "collected_entities": self.collected_entities,
            "user_message_count": self.user_message_count,
            "created_at": self.created_at.isoformat()
        }
    
    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "DialogueState":
        """Create from dictionary"""
        state = DialogueState(data["conversation_id"])
        state.intent = data.get("intent")
        state.collected_entities = data.get("collected_entities", {})
        state.user_message_count = data.get("user_message_count", 0)
        if isinstance(data.get("created_at"), str):
            state.created_at = datetime.fromisoformat(data["created_at"])
        return state


def get_or_create_dialogue_state(conversation_id: str) -> DialogueState:
    """
    Get existing dialogue state or create new one
    
    Uses configured StateStore (in-memory by default, Redis/SQLite in production)
    """
    store = get_state_store()
    state_dict = store.get(conversation_id)
    
    if state_dict:
        return DialogueState.from_dict(state_dict)
    else:
        return DialogueState(conversation_id)


def save_dialogue_state(state: DialogueState) -> None:
    """
    Save dialogue state
    
    ✅ ONLY increments message_count on explicit save
    (chat.py is responsible for calling this only on user input)
    
    Stores to configured StateStore (in-memory by default, Redis/SQLite in production)
    """
    store = get_state_store()
    store.save(state.conversation_id, state.to_dict())



def merge_entities_with_state(
    new_entities: Dict[str, Any],
    conversation_id: str
) -> Dict[str, Any]:
    """
    ✅ FIXED: Merge newly parsed entities with existing dialogue state
    AND save back to state
    
    This is CRITICAL:
    - New entities override old ones
    - But only if non-None (preserves context)
    - SAVES the merged result immediately
    
    Args:
        new_entities: Fresh NLU extraction
        conversation_id: Which conversation
        
    Returns:
        Merged entities (saved to state)
        
    Example:
        Turn 1: User says "Dr. Wang"
          - new_entities = {doctor: "Dr. Wang"}
          - merged = {doctor: "Dr. Wang"}
          - SAVED to state
        
        Turn 2: User says "Cleaning"
          - new_entities = {service: "Cleaning"}
          - merged = {doctor: "Dr. Wang", service: "Cleaning"} ✅
          - SAVED to state
    """
    state = get_or_create_dialogue_state(conversation_id)
    
    # Merge: new overrides old, None is skipped
    merged = {**state.collected_entities}
    for key, value in new_entities.items():
        if value is not None:
            merged[key] = value
    
    # ✅ CRITICAL: Save merged state back
    state.collected_entities = merged
    save_dialogue_state(state)
    
    return merged


def reset_dialogue_state(conversation_id: str) -> None:
    """
    Reset dialogue state for a conversation
    
    Useful for:
    - End of session cleanup
    - Error recovery
    - Explicit user reset
    """
    store = get_state_store()
    store.delete(conversation_id)


def get_dialogue_history(conversation_id: str) -> Optional[Dict[str, Any]]:
    """
    Get complete dialogue state for a conversation
    
    Returns serialized state or None if not found
    """
    store = get_state_store()
    return store.get(conversation_id)


