#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')

from services.appointment_service import AppointmentService

# Test is_slot_available
result = AppointmentService.is_slot_available(
    doctor_id=1,
    appointment_date="2026-01-07",
    appointment_time="14:00"
)

print(f"is_slot_available(doctor_id=1, date='2026-01-07', time='14:00'): {result}")
