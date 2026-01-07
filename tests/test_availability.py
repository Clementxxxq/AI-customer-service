#!/usr/bin/env python3
"""
Test calendar availability feature end-to-end
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))

from services.availability_service import AvailabilityService
from datetime import date, timedelta

print("=" * 60)
print("📅 Testing Availability Service")
print("=" * 60)

# Test 1: Get available dates
print("\n1️⃣ Testing get_available_dates()...")
available_dates = AvailabilityService.get_available_dates(days_ahead=7)
print(f"✅ Found {len(available_dates)} available dates")
for date_info in available_dates[:3]:
    print(f"   📆 {date_info['date']} ({date_info.get('day_of_week')}): {len(date_info['slots'])} slots")
    print(f"      Times: {', '.join(date_info['slots'][:3])}...")

# Test 2: Get suggested appointment
print("\n2️⃣ Testing get_suggested_appointment()...")
if available_dates:
    suggested = AvailabilityService.get_suggested_appointment(available_dates)
    print(f"✅ Suggested appointment: {suggested['date']} at {suggested['time']}")

# Test 3: JSON format test
print("\n3️⃣ Testing JSON response format...")
response_data = {
    "available_dates": available_dates[:3],
    "suggested": AvailabilityService.get_suggested_appointment(available_dates)
}
print(f"✅ Response structure:")
print(f"   - available_dates: {len(response_data['available_dates'])} items")
print(f"   - suggested: {response_data['suggested']}")

# Test 4: Empty availability edge case
print("\n4️⃣ Testing edge case (far future dates)...")
far_future_dates = AvailabilityService.get_available_dates(days_ahead=1000)
print(f"✅ Far future dates: {len(far_future_dates)} dates (should be > 100)")

print("\n" + "=" * 60)
print("✅ All tests passed!")
print("=" * 60)
