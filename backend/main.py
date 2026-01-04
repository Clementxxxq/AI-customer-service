from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
from typing import List, Optional

DB_PATH = "../clinic.db"  

app = FastAPI(title="Dental Clinic AI Appointment API")

# ----------------------------
# Pydantic Data Model
# ----------------------------
class Customer(BaseModel):
    id: Optional[int]
    name: str
    phone: str
    email: Optional[str]

class Doctor(BaseModel):
    id: Optional[int]
    name: str
    specialization: Optional[str]
    phone: Optional[str]
    email: Optional[str]

class Service(BaseModel):
    id: Optional[int]
    name: str
    description: Optional[str]
    duration_minutes: int
    price: float
    doctor_id: Optional[int]

class Appointment(BaseModel):
    id: Optional[int]
    service_id: int
    customer_id: int
    doctor_id: Optional[int]
    date: str
    time: str
    status: str

# ----------------------------
# Utility functions: Connecting to the database
# ----------------------------
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------
# API: Query all services
# ----------------------------
@app.get("/services", response_model=List[Service])
def get_services():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM services")
    rows = cur.fetchall()
    conn.close()
    return [Service(**dict(row)) for row in rows]

# ----------------------------
# API: Query all doctors
# ----------------------------
@app.get("/doctors", response_model=List[Doctor])
def get_doctors():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors")
    rows = cur.fetchall()
    conn.close()
    return [Doctor(**dict(row)) for row in rows]

# ----------------------------
# API: Query all customers
# ----------------------------
@app.get("/customers", response_model=List[Customer])
def get_customers():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    rows = cur.fetchall()
    conn.close()
    return [Customer(**dict(row)) for row in rows]

# ----------------------------
# API: Query time period
# ----------------------------
@app.get("/time_slots")
def get_time_slots(doctor_id: Optional[int] = None, date: Optional[str] = None):
    conn = get_db_connection()
    cur = conn.cursor()
    query = "SELECT * FROM time_slots WHERE 1=1"
    params = []
    if doctor_id:
        query += " AND doctor_id=?"
        params.append(doctor_id)
    if date:
        query += " AND date=?"
        params.append(date)
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# ----------------------------
# API: Create Appointment
# ----------------------------
@app.post("/appointments", response_model=Appointment)
def create_appointment(appointment: Appointment):
    conn = get_db_connection()
    cur = conn.cursor()

    # Check if the service exists
    cur.execute("SELECT * FROM services WHERE id=?", (appointment.service_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Service not found")

    # Check if the customer is present
    cur.execute("SELECT * FROM customers WHERE id=?", (appointment.customer_id,))
    if not cur.fetchone():
        raise HTTPException(status_code=404, detail="Customer not found")

    # Insert appointment
    cur.execute(
        "INSERT INTO appointments (service_id, customer_id, doctor_id, date, time, status) VALUES (?, ?, ?, ?, ?, ?)",
        (appointment.service_id, appointment.customer_id, appointment.doctor_id, appointment.date, appointment.time, appointment.status)
    )
    conn.commit()
    appointment.id = cur.lastrowid
    conn.close()
    return appointment

# ----------------------------
# API: Query all appointments
# ----------------------------
@app.get("/appointments", response_model=List[Appointment])
def get_appointments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM appointments")
    rows = cur.fetchall()
    conn.close()
    return [Appointment(**dict(row)) for row in rows]
