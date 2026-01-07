#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('clinic.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check time slots for 2026-01-07 at 14:00
res = cur.execute('SELECT * FROM time_slots WHERE doctor_id=1 AND date="2026-01-07" AND time="14:00"').fetchall()
print(f'Found {len(res)} time slots for 2026-01-07 at 14:00 for Dr. Wang')
for row in res:
    print(f'  {dict(row)}')

# Check all time slots
res2 = cur.execute('SELECT COUNT(*) as count FROM time_slots').fetchone()
print(f'\nTotal time slots in database: {res2["count"]}')

# Check appointments
res3 = cur.execute('SELECT * FROM appointments WHERE doctor_id=1 AND date="2026-01-07" AND time="14:00"').fetchall()
print(f'Found {len(res3)} existing appointments for 2026-01-07 at 14:00 for Dr. Wang')
for row in res3:
    print(f'  {dict(row)}')

conn.close()
