"""
State Store Abstraction Layer

Decouples dialogue_service.py from storage implementation.

This allows seamless switching:
  🔄 Development: In-memory dict
  📦 Production: Redis
  💾 Alternative: SQLite

Interface:
  - get(conversation_id) → DialogueState dict
  - save(conversation_id, state_dict) → None
  - delete(conversation_id) → None
  - exists(conversation_id) → bool
"""

from typing import Dict, Any, Optional, Protocol
from abc import ABC, abstractmethod
import json


class StateStore(ABC):
    """Abstract state store interface"""
    
    @abstractmethod
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get dialogue state by ID"""
        pass
    
    @abstractmethod
    def save(self, conversation_id: str, state: Dict[str, Any]) -> None:
        """Save dialogue state"""
        pass
    
    @abstractmethod
    def delete(self, conversation_id: str) -> None:
        """Delete dialogue state"""
        pass
    
    @abstractmethod
    def exists(self, conversation_id: str) -> bool:
        """Check if conversation exists"""
        pass
    
    @abstractmethod
    def clear_all(self) -> None:
        """Clear all states (testing only)"""
        pass


class InMemoryStateStore(StateStore):
    """
    Simple in-memory store for development
    
    ⚠️ NOT suitable for production:
    - Lost on service restart
    - No multi-process support
    - No concurrent safety
    """
    
    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}
    
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        return self._store.get(conversation_id)
    
    def save(self, conversation_id: str, state: Dict[str, Any]) -> None:
        self._store[conversation_id] = state
    
    def delete(self, conversation_id: str) -> None:
        if conversation_id in self._store:
            del self._store[conversation_id]
    
    def exists(self, conversation_id: str) -> bool:
        return conversation_id in self._store
    
    def clear_all(self) -> None:
        self._store.clear()
    
    def get_all(self) -> Dict[str, Dict[str, Any]]:
        """Debugging: get all states"""
        return self._store.copy()


# Global store instance (configurable)
_state_store: StateStore = InMemoryStateStore()


def set_state_store(store: StateStore) -> None:
    """
    Set the state store implementation
    
    Usage (in app startup):
        from backend.services.state_store import set_state_store, RedisStateStore
        set_state_store(RedisStateStore(redis_client))
    """
    global _state_store
    _state_store = store


def get_state_store() -> StateStore:
    """Get current state store"""
    return _state_store


# ═══════════════════════════════════════════════════════
# FUTURE IMPLEMENTATIONS (stub)
# ═══════════════════════════════════════════════════════

class RedisStateStore(StateStore):
    """
    Production Redis-backed state store
    
    Features:
    ✅ Multi-process safe
    ✅ Distributed ready
    ✅ TTL support (auto-expiry)
    ✅ Atomic operations
    
    TODO: Implement when Redis added to stack
    """
    
    def __init__(self, redis_client):
        self.redis = redis_client
        self.prefix = "dialogue:"
    
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        key = f"{self.prefix}{conversation_id}"
        data = self.redis.get(key)
        if data:
            return json.loads(data)
        return None
    
    def save(self, conversation_id: str, state: Dict[str, Any]) -> None:
        key = f"{self.prefix}{conversation_id}"
        # TTL: 24 hours
        self.redis.setex(key, 86400, json.dumps(state))
    
    def delete(self, conversation_id: str) -> None:
        key = f"{self.prefix}{conversation_id}"
        self.redis.delete(key)
    
    def exists(self, conversation_id: str) -> bool:
        key = f"{self.prefix}{conversation_id}"
        return self.redis.exists(key) > 0
    
    def clear_all(self) -> None:
        # Only for testing
        keys = self.redis.keys(f"{self.prefix}*")
        if keys:
            self.redis.delete(*keys)


class SQLiteStateStore(StateStore):
    """
    SQLite-backed state store
    
    Features:
    ✅ Persistent storage
    ✅ Simple setup
    ✅ Suitable for MVP/small deployments
    
    TODO: Implement when needed
    """
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Initialize table on first use
    
    def get(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        pass
    
    def save(self, conversation_id: str, state: Dict[str, Any]) -> None:
        pass
    
    def delete(self, conversation_id: str) -> None:
        pass
    
    def exists(self, conversation_id: str) -> bool:
        pass
    
    def clear_all(self) -> None:
        pass
