"""
Schema definitions for AI output validation
Ensures structured, type-safe data flow from AI to business logic
"""
from pydantic import BaseModel, Field, validator, root_validator, ConfigDict
from typing import Optional, List, Dict, Any, Union
from datetime import datetime, date
from enum import Enum


class IntentType(str, Enum):
    """Valid intent types"""
    APPOINTMENT = "appointment"
    QUERY = "query"
    CANCEL = "cancel"
    MODIFY = "modify"
    OTHER = "other"


class AIEntity(BaseModel):
    """Extracted entities from user input"""
    service: Optional[str] = Field(None, description="Service/procedure name")
    doctor: Optional[str] = Field(None, description="Doctor name")
    date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    time: Optional[str] = Field(None, description="Time in HH:MM format")
    customer_name: Optional[str] = Field(None, description="Customer name")
    customer_phone: Optional[str] = Field(None, description="Phone number")
    customer_email: Optional[str] = Field(None, description="Email address")
    
    @validator('date')
    def validate_date(cls, v):
        """Ensure date is in YYYY-MM-DD format if provided"""
        if v and not isinstance(v, str):
            v = str(v)
        if v and len(v) == 10:  # YYYY-MM-DD
            return v
        return v


class AIResponse(BaseModel):
    """Structured AI response with parsed intent and entities"""
    intent: IntentType = Field(..., description="Parsed user intent")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence 0-1")
    entities: AIEntity = Field(..., description="Extracted entities")
    raw_input: Optional[str] = Field(None, description="Original user input")
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "intent": "appointment",
                "confidence": 0.95,
                "entities": {
                    "service": "teeth cleaning",
                    "doctor": "Dr. Wang",
                    "date": "2026-01-06",
                    "time": "14:00",
                    "customer_name": None,
                    "customer_phone": None,
                    "customer_email": None
                },
                "raw_input": "Book with Dr. Wang tomorrow at 2 PM"
            }
        }
    )


class AppointmentRequest(BaseModel):
    """Request to create an appointment"""
    service_id: int = Field(..., description="Service ID")
    doctor_id: int = Field(..., description="Doctor ID")
    customer_id: int = Field(..., description="Customer ID")
    appointment_date: date = Field(..., description="Appointment date")
    appointment_time: str = Field(..., description="Appointment time HH:MM")
    notes: Optional[str] = Field(None, description="Additional notes")


class AppointmentResponse(BaseModel):
    """Response after creating appointment"""
    success: bool
    message: str
    appointment_id: Optional[int] = None
    appointment_date: Optional[str] = None
    appointment_time: Optional[str] = None
    errors: Optional[List[str]] = None
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Appointment booked successfully",
                "appointment_id": 1,
                "appointment_date": "2026-01-06",
                "appointment_time": "14:00",
                "errors": None
            }
        }
    )


class CancellationRequest(BaseModel):
    """Request to cancel an appointment"""
    appointment_id: int = Field(..., description="Appointment ID to cancel")
    reason: Optional[str] = Field(None, description="Cancellation reason")


class CancellationResponse(BaseModel):
    """Response after cancellation"""
    success: bool
    message: str
    cancelled_appointment_id: Optional[int] = None
    errors: Optional[List[str]] = None


class ModificationRequest(BaseModel):
    """Request to modify an appointment"""
    appointment_id: int = Field(..., description="Appointment ID to modify")
    new_date: Optional[date] = Field(None, description="New appointment date")
    new_time: Optional[str] = Field(None, description="New appointment time HH:MM")
    new_doctor_id: Optional[int] = Field(None, description="New doctor ID")


class ModificationResponse(BaseModel):
    """Response after modification"""
    success: bool
    message: str
    appointment_id: Optional[int] = None
    new_date: Optional[str] = None
    new_time: Optional[str] = None
    errors: Optional[List[str]] = None


class ChatRequest(BaseModel):
    """User message to chat API"""
    content: str = Field(..., description="User message")
    user_id: Optional[int] = Field(None, description="User ID")
    conversation_id: Optional[str] = Field(None, description="Conversation ID")


class TimeSlotInfo(BaseModel):
    """Information about available time slots for a date"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    day_of_week: Optional[str] = Field(None, description="Day of week (e.g., Monday)")
    slots: List[str] = Field(..., description="List of available times in HH:MM format")


class AvailableAppointmentTime(BaseModel):
    """Available appointment time (date + time)"""
    date: str = Field(..., description="Date in YYYY-MM-DD format")
    time: str = Field(..., description="Time in HH:MM format")


class AppointmentAvailability(BaseModel):
    """Appointment availability data for frontend calendar"""
    available_dates: List[TimeSlotInfo] = Field(
        ..., 
        description="List of dates with available time slots"
    )
    suggested: Optional[AvailableAppointmentTime] = Field(
        None,
        description="AI-suggested appointment time"
    )
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "available_dates": [
                    {
                        "date": "2026-01-10",
                        "day_of_week": "Friday",
                        "slots": ["09:00", "09:30", "10:00", "14:00", "14:30"]
                    },
                    {
                        "date": "2026-01-11",
                        "day_of_week": "Saturday",
                        "slots": ["10:00", "11:00", "15:00"]
                    }
                ],
                "suggested": {
                    "date": "2026-01-10",
                    "time": "10:00"
                }
            }
        }
    )


class ChatResponse(BaseModel):
    """Response from chat API"""
    message_id: str
    user_message: str
    bot_response: str
    timestamp: str
    conversation_id: str
    intent: str = Field(..., description="Parsed intent")
    confidence: float = Field(..., description="Confidence score 0-1")
    entities: Union[AIEntity, Dict[str, Any]] = Field(..., description="Extracted entities")
    action_result: Optional[dict] = Field(None, description="Result of business logic execution")
    availability: Optional[AppointmentAvailability] = Field(
        None,
        description="Available appointment times for booking (when intent is appointment)"
    )
    
    @root_validator(pre=True)
    def convert_entities_to_dict(cls, values):
        """Convert AIEntity to dict if needed for dialogue state compatibility"""
        entities = values.get('entities')
        if isinstance(entities, AIEntity):
            values['entities'] = entities.dict()
        return values
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "message_id": "msg_xxx",
                "user_message": "Book with Dr. Wang tomorrow at 2 PM",
                "bot_response": "I can help you book with Dr. Wang. Here are our available dates and times...",
                "timestamp": "2026-01-05T10:30:00",
                "conversation_id": "conv_xxx",
                "intent": "appointment",
                "confidence": 0.95,
                "entities": {
                    "service": "teeth cleaning",
                    "doctor": "Dr. Wang",
                    "date": None,
                    "time": None,
                    "customer_name": None,
                    "customer_phone": None,
                    "customer_email": None
                },
                "action_result": None,
                "availability": {
                    "available_dates": [
                        {
                            "date": "2026-01-10",
                            "day_of_week": "Friday",
                            "slots": ["09:00", "09:30", "10:00", "14:00", "14:30"]
                        }
                    ],
                    "suggested": {
                        "date": "2026-01-10",
                        "time": "10:00"
                    }
                }
            }
        }
    )
