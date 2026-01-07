#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('clinic.db')
c = conn.cursor()

# Check time slots for 2026-01-07
slots = c.execute('SELECT * FROM time_slots WHERE date = "2026-01-07" LIMIT 5').fetchall()
print(f"Time slots for 2026-01-07 (first 5):")
for slot in slots:
    print(f"  {slot}")

# Check appointments table schema
print("\nAppointments table schema:")
c.execute("PRAGMA table_info(appointments)")
for row in c.fetchall():
    print(f"  {row}")

# Check time_slots table schema
print("\nTime_slots table schema:")
c.execute("PRAGMA table_info(time_slots)")
for row in c.fetchall():
    print(f"  {row}")

conn.close()
