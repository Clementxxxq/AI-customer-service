"""
Chat API routes - Real AI with Business Logic + Dialogue State Management
Uses Llama3.2:3b for NLU + AppointmentService for actions
Full integration: NLU → Dialogue State → Business Logic → Response
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional, Dict, Any
from datetime import datetime
from services.llama_service import LlamaService
from services.appointment_service import AppointmentService
from services.dialogue_service import (
    get_or_create_dialogue_state, save_dialogue_state, 
    merge_entities_with_state, determine_next_question, 
    is_appointment_ready
)
from schemas.chat import ChatRequest, ChatResponse, AIEntity

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/message", response_model=ChatResponse)
def send_message(message: ChatRequest):
    """
    Send a chat message with dialogue state management
    
    Flow:
    1. Get or create dialogue state for this conversation
    2. Parse user input with Llama NLU
    3. Merge entities with dialogue state (remember context)
    4. Determine next action (ask for info or execute booking)
    5. Generate contextual response
    6. Save dialogue state for next turn
    7. Return response
    """
    if not message.content or not message.content.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message content cannot be empty"
        )
    
    try:
        # Step 0: Get conversation context
        conversation_id = message.conversation_id or f"conv_{datetime.now().timestamp()}"
        dialogue_state = get_or_create_dialogue_state(conversation_id)
        
        # Step 1: Parse user message using Llama NLU
        llama_response = LlamaService.parse_user_input(message.content)
        
        # Step 2: Merge new entities with dialogue state (remember context)
        merged_entities = merge_entities_with_state(
            llama_response.entities.dict() if hasattr(llama_response.entities, 'dict') else llama_response.entities,
            conversation_id
        )
        
        # Update dialogue state with merged entities
        dialogue_state.intent = llama_response.intent
        dialogue_state.collected_entities = merged_entities
        
        # Step 3: Determine if we need more info or can execute
        next_question = determine_next_question(llama_response.intent, merged_entities)
        
        # Step 4: Execute business logic if we have all info, or just ask the next question
        action_result = None
        if next_question:
            # Still collecting information - don't execute business logic yet
            dialogue_state.current_question = next_question
            bot_response = next_question
        else:
            # We have all required info - execute business logic
            action_result = _execute_business_logic(
                intent=llama_response.intent,
                entities=merged_entities,
                user_id=message.user_id
            )
            
            # Generate final response
            bot_response = _generate_response(
                intent=llama_response.intent,
                entities=merged_entities,
                action_result=action_result
            )
            
            # Clear state after booking
            if llama_response.intent == "appointment" and action_result.get("success"):
                dialogue_state.collected_entities = {}
        
        # Step 5: Save dialogue state
        save_dialogue_state(dialogue_state)
        
        # Step 6: Return structured response
        message_id = f"msg_{datetime.now().timestamp()}"
        
        return ChatResponse(
            message_id=message_id,
            user_message=message.content,
            bot_response=bot_response,
            timestamp=datetime.now().isoformat(),
            conversation_id=conversation_id,
            intent=llama_response.intent,
            confidence=llama_response.confidence,
            entities=merged_entities,
            action_result=action_result
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


def _execute_business_logic(
    intent: str,
    entities: Dict[str, Any],
    user_id: Optional[int] = None
) -> Optional[Dict[str, Any]]:
    """Execute business logic based on parsed intent"""
    if intent == "appointment":
        return _handle_appointment_booking(entities, user_id)
    elif intent == "cancel":
        return _handle_cancellation(entities)
    elif intent == "modify":
        return _handle_modification(entities)
    elif intent == "query":
        return _handle_query(entities)
    else:
        return None


def _handle_appointment_booking(
    entities: Dict[str, Any],
    user_id: Optional[int] = None
) -> Dict[str, Any]:
    """Handle appointment booking"""
    result = {
        "action": "appointment_booking",
        "success": False,
        "message": "",
        "details": {}
    }
    
    doctor_name = entities.get("doctor")
    service_name = entities.get("service")
    appointment_date = entities.get("date")
    appointment_time = entities.get("time")
    customer_name = entities.get("customer_name")
    customer_phone = entities.get("customer_phone")
    customer_email = entities.get("customer_email")
    
    if not all([doctor_name, service_name, appointment_date, appointment_time]):
        result["message"] = "Missing required information (doctor, service, date, time)"
        return result
    
    # Find doctor
    doctor = AppointmentService.find_doctor_by_name(doctor_name)
    if not doctor:
        result["message"] = f"Doctor '{doctor_name}' not found"
        return result
    
    doctor_id = doctor.get('id')
    result["details"]["doctor"] = {"id": doctor_id, "name": doctor.get('name')}
    
    # Find service
    service = AppointmentService.find_service_by_name(service_name)
    if not service:
        result["message"] = f"Service '{service_name}' not found"
        return result
    
    service_id = service.get('id')
    result["details"]["service"] = {"id": service_id, "name": service.get('name')}
    
    # Find or create customer
    customer_id = AppointmentService.find_or_create_customer(
        name=customer_name,
        phone=customer_phone,
        email=customer_email
    )
    
    if not customer_id:
        result["message"] = "Unable to identify or create customer record"
        return result
    
    result["details"]["customer"] = {"id": customer_id}
    
    # Book appointment
    booking_result = AppointmentService.book_appointment(
        service_id=service_id,
        customer_id=customer_id,
        doctor_id=doctor_id,
        appointment_date=appointment_date,
        appointment_time=appointment_time
    )
    
    result["success"] = booking_result.get("success", False)
    result["message"] = booking_result.get("message", "")
    result["details"]["booking"] = booking_result
    
    return result


def _handle_cancellation(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Handle appointment cancellation"""
    return {
        "action": "cancellation",
        "success": False,
        "message": "Cancellation requested but appointment ID not found"
    }


def _handle_modification(entities: Dict[str, Any]) -> Dict[str, Any]:
    """Handle appointment modification"""
    return {
        "action": "modification",
        "success": False,
        "message": "Modification requested but appointment ID not found"
    }


def _handle_query(entities: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Handle information query"""
    return None


def _generate_response(
    intent: str,
    entities: Dict[str, Any],
    action_result: Optional[Dict[str, Any]]
) -> str:
    """Generate contextual bot response"""
    if not action_result:
        if intent == "query":
            doctor = entities.get("doctor")
            if doctor:
                return f"You're asking about {doctor}. I'd be happy to help!"
            return "I'd be happy to help answer your question."
        return "How can I assist you with our dental services?"
    
    if action_result.get("action") == "appointment_booking":
        if action_result.get("success"):
            doctor = entities.get("doctor")
            service = entities.get("service")
            date = entities.get("date")
            time = entities.get("time")
            return (
                f"✅ Great! I've booked your appointment for {service} "
                f"with {doctor} on {date} at {time}."
            )
        else:
            return f"❌ Sorry: {action_result.get('message', 'Unable to complete booking')}"
    
    return "Your request has been processed."


@router.get("/conversations/{conversation_id}")
def get_conversation(conversation_id: str):
    """Get conversation history"""
    return {
        "conversation_id": conversation_id,
        "messages": []
    }


@router.post("/conversations")
def create_conversation():
    """Create a new conversation session"""
    conversation_id = f"conv_{datetime.now().timestamp()}"
    return {
        "conversation_id": conversation_id,
        "created_at": datetime.now().isoformat(),
        "status": "active"
    }


@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    return {
        "message": "Conversation deleted successfully",
        "conversation_id": conversation_id,
        "deleted_at": datetime.now().isoformat()
    }


@router.get("/health")
def chat_health():
    """Check chat service health"""
    return {
        "service": "chat",
        "status": "operational",
        "features": ["nlu", "appointment_booking", "business_logic"],
        "version": "2.0.0"
    }
