#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
from services.appointment_service import AppointmentService

# Test find_or_create_customer
customer_id = AppointmentService.find_or_create_customer(
    name="John Smith",
    phone="555-1234",
    email=None
)
print(f"Created/found customer ID: {customer_id}")

# Call again with same phone
customer_id2 = AppointmentService.find_or_create_customer(
    name="Jane Doe",
    phone="555-1234",
    email=None
)
print(f"Second call returned customer ID: {customer_id2}")
