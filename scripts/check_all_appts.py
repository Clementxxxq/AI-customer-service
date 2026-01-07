#!/usr/bin/env python3
import sys
sys.path.insert(0, 'backend')
from utils.db_utils import execute_query

# Check all appointments
results = execute_query("SELECT * FROM appointments")
print(f"Total appointments: {len(results) if results else 0}")
if results:
    for row in results:
        print(f"  {row}")
