#!/usr/bin/env python3
"""Quick test to verify doctor name normalization works"""
import sys
sys.path.insert(0, 'backend')

from backend.services.appointment_service import AppointmentService

# Test 1: Verify doctors exist in DB
print("=" * 70)
print("TEST 1: Check available doctors")
print("=" * 70)
doctors = AppointmentService.get_all_doctors()
print(f"Doctors in database: {[d.get('name') for d in doctors]}")

# Test 2: Test doctor finding with different name formats
print("\n" + "=" * 70)
print("TEST 2: Doctor name matching")
print("=" * 70)

test_names = [
    "Dr. Wang",
    "Dr.wang", 
    "Dr wang",
    "Wang",
    "Dr.Li",
    "Dr li",
    "Li"
]

for name in test_names:
    doc = AppointmentService.find_doctor_by_name(name)
    if doc:
        print(f"✅ '{name}' → Found: {doc.get('name')}")
    else:
        print(f"❌ '{name}' → NOT FOUND")

# Test 3: Test services
print("\n" + "=" * 70)
print("TEST 3: Service matching")
print("=" * 70)

service_names = ["Cleaning", "cleaning", "Extraction"]
for name in service_names:
    svc = AppointmentService.find_service_by_name(name)
    if svc:
        print(f"✅ '{name}' → Found: {svc.get('name')}")
    else:
        print(f"❌ '{name}' → NOT FOUND")

print("\n" + "=" * 70)
print("✅ ALL TESTS COMPLETE")
print("=" * 70)
