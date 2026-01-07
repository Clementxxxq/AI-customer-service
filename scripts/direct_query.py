#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('clinic.db')
c = conn.cursor()

# Check exact query
query = """
    SELECT COUNT(*) as count FROM appointments
    WHERE doctor_id = ? AND date = ? AND time = ? AND status != 'cancelled'
"""
result = c.execute(query, (1, "2026-01-07", "14:00")).fetchone()
print(f"Direct SQLite query result: {result}")

# Check all appointments
all_appts = c.execute('SELECT * FROM appointments').fetchall()
print(f"\nAll appointments ({len(all_appts)}):")
for appt in all_appts:
    print(f"  {appt}")

# Check for any appointment with doctor_id=1
dr_wang_appts = c.execute('SELECT * FROM appointments WHERE doctor_id = 1').fetchall()
print(f"\nDr. Wang appointments ({len(dr_wang_appts)}):")
for appt in dr_wang_appts:
    print(f"  {appt}")

conn.close()
