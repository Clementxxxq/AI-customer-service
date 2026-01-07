#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
from utils.db_utils import execute_query

# Test the actual function
query = """
    SELECT COUNT(*) as count FROM appointments
    WHERE doctor_id = ? AND date = ? AND time = ? AND status != 'cancelled'
"""
results = execute_query(query, (1, "2026-01-07", "14:00"))
print(f"execute_query result: {results}")
if results:
    count = results[0].get('count', 'NOT FOUND')
    print(f"Count value: {count}")
    print(f"Type of count: {type(count)}")
