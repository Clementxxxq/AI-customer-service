"""
Chat API routes - Real Llama AI implementation
Uses Llama3.2:3b for NLU (Natural Language Understanding)
Converts user messages to structured JSON intent+entities
"""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from services.llama_service import LlamaService

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatMessage(BaseModel):
    """Chat message model"""
    content: str
    user_id: Optional[int] = None
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Chat response model"""
    message_id: str
    user_message: str
    bot_response: str
    timestamp: str
    conversation_id: str
    intent: Optional[str] = None
    confidence: Optional[float] = None
    entities: Optional[Dict[str, Any]] = None


@router.post("/message", response_model=ChatResponse)
def send_message(message: ChatMessage):
    """
    Send a chat message to Llama AI
    
    Args:
        message: User message containing content and optional user_id
    
    Returns:
        ChatResponse with AI response based on NLU parsing
    
    Example:
        {
            "content": "I want to book an appointment with Dr. Wang tomorrow at 2 PM",
            "user_id": 1,
            "conversation_id": "conv_123"
        }
    """
    if not message.content or not message.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty"
        )
    
    try:
        # Parse user message using Llama NLU
        llama_response = LlamaService.parse_user_input(message.content)
        
        # Generate bot response based on parsed intent
        bot_response = LlamaService.generate_bot_response(
            llama_response.intent,
            llama_response.entities
        )
        
        # Generate message ID and conversation ID
        conversation_id = message.conversation_id or f"conv_{datetime.now().timestamp()}"
        message_id = f"msg_{datetime.now().timestamp()}"
        
        return ChatResponse(
            message_id=message_id,
            user_message=message.content,
            bot_response=bot_response,
            timestamp=datetime.now().isoformat(),
            conversation_id=conversation_id,
            intent=llama_response.intent,
            confidence=llama_response.confidence,
            entities=llama_response.entities
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(e)}"
        )
    except RuntimeError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"AI service error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server error: {str(e)}"
        )


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    """
    Get conversation history (Mock implementation)
    
    Args:
        conversation_id: The ID of the conversation
    
    Returns:
        Mock conversation history
    """
    return {
        "conversation_id": conversation_id,
        "messages": [
            {
                "role": "user",
                "content": "Hello, I'd like to know more about your services",
                "timestamp": "2026-01-04T10:00:00"
            },
            {
                "role": "assistant",
                "content": "That's a great question! Our clinic offers comprehensive dental services including cleaning, extractions, and orthodontics.",
                "timestamp": "2026-01-04T10:00:05"
            },
            {
                "role": "user",
                "content": "How much does a cleaning cost?",
                "timestamp": "2026-01-04T10:01:00"
            },
            {
                "role": "assistant",
                "content": "Our cleaning service costs $200 and takes about 30 minutes. Would you like to schedule one?",
                "timestamp": "2026-01-04T10:01:05"
            }
        ]
    }


@router.post("/conversations")
def create_conversation():
    """
    Create a new conversation session
    
    Returns:
        New conversation ID
    """
    conversation_id = f"conv_{datetime.now().timestamp()}"
    return {
        "conversation_id": conversation_id,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }


@router.get("/conversations/{conversation_id}/history")
def get_chat_history(conversation_id: str, limit: int = 10):
    """
    Get chat history with optional limit
    
    Args:
        conversation_id: The ID of the conversation
        limit: Maximum number of messages to return (default: 10)
    
    Returns:
        List of messages in the conversation
    """
    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Limit must be between 1 and 100"
        )
    
    # Mock history data
    mock_messages = [
        {"role": "user", "content": "Hello", "timestamp": "2026-01-04T10:00:00"},
        {"role": "assistant", "content": "Hi! How can I help you today?", "timestamp": "2026-01-04T10:00:05"},
        {"role": "user", "content": "I want to book an appointment", "timestamp": "2026-01-04T10:01:00"},
        {"role": "assistant", "content": "Great! What service are you interested in?", "timestamp": "2026-01-04T10:01:05"},
        {"role": "user", "content": "Teeth cleaning", "timestamp": "2026-01-04T10:02:00"},
        {"role": "assistant", "content": "Perfect! Our cleaning service is $200 and takes 30 minutes.", "timestamp": "2026-01-04T10:02:05"},
    ]
    
    return {
        "conversation_id": conversation_id,
        "total_messages": len(mock_messages),
        "messages": mock_messages[-limit:]
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    """
    Delete a conversation (Mock implementation)
    
    Args:
        conversation_id: The ID of the conversation to delete
    
    Returns:
        Confirmation message
    """
    return {
        "message": "Conversation deleted successfully",
        "conversation_id": conversation_id,
        "deleted_at": datetime.now().isoformat()
    }


@router.get("/health")
def chat_health():
    """
    Check chat service health
    
    Returns:
        Service status
    """
    return {
        "service": "chat",
        "status": "operational",
        "type": "mock",
        "version": "1.0.0"
    }
