from pydantic import BaseModel
from typing import Optional

class Service(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    duration_minutes: int
    price: float
    doctor_id: Optional[int]

class Doctor(BaseModel):
    id: Optional[int]
    name: str
    specialization: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class Customer(BaseModel):
    id: Optional[int]
    name: str
    phone: str
    email: Optional[str]

class Appointment(BaseModel):
    id: Optional[int]
    service_id: int
    customer_id: int
    doctor_id: Optional[int]
    date: str
    time: str
    status: str
