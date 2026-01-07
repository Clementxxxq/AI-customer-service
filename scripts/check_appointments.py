#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('clinic.db')
conn.row_factory = sqlite3.Row
cur = conn.cursor()

# Check all appointments
res = cur.execute('SELECT * FROM appointments').fetchall()
print(f'Total appointments: {len(res)}')
for row in res:
    print(f'  {dict(row)}')

conn.close()
