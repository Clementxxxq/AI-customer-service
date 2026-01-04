"""
Data models and schemas for API requests/responses
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ServiceSchema(BaseModel):
    """Service model for dental services"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    duration_minutes: int = Field(..., ge=1)
    price: float = Field(..., ge=0)
    doctor_id: Optional[int] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Teeth Cleaning",
                "description": "Professional teeth cleaning",
                "duration_minutes": 30,
                "price": 50.0,
            }
        }


class DoctorSchema(BaseModel):
    """Doctor model"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    specialization: Optional[str] = Field(None, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^\d{10,15}$")
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. John Smith",
                "specialization": "General Dentistry",
                "phone": "1234567890",
                "email": "john@clinic.com",
            }
        }


class CustomerSchema(BaseModel):
    """Customer model"""
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    phone: str = Field(..., pattern=r"^\d{10,15}$")
    email: Optional[str] = Field(None, pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Jane Doe",
                "phone": "9876543210",
                "email": "jane@email.com",
            }
        }


class AppointmentSchema(BaseModel):
    """Appointment model"""
    id: Optional[int] = None
    service_id: int
    customer_id: int
    doctor_id: Optional[int] = None
    date: str = Field(..., pattern=r"^\d{4}-\d{2}-\d{2}$")
    time: str = Field(..., pattern=r"^\d{2}:\d{2}$")
    status: str = Field(default="scheduled", pattern=r"^(scheduled|completed|cancelled)$")

    class Config:
        json_schema_extra = {
            "example": {
                "service_id": 1,
                "customer_id": 1,
                "doctor_id": 1,
                "date": "2025-01-15",
                "time": "14:00",
                "status": "scheduled",
            }
        }
