#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
from utils.db_utils import execute_query

# Run the exact query from is_slot_available
query = """
    SELECT COUNT(*) as count FROM appointments
    WHERE doctor_id = ? AND date = ? AND time = ? AND status != 'cancelled'
"""
results = execute_query(query, (1, "2026-01-07", "14:00"))
print(f"Query results: {results}")
if results:
    count = results[0].get('count', 0)
    print(f"Count: {count}")
    print(f"is_slot_available would return: {count == 0}")
