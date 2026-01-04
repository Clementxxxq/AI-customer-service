"""
Doctors API routes
"""
from fastapi import APIRouter, HTTPException, status
from schemas import DoctorSchema
from utils.db_utils import execute_query, execute_update, get_by_id, DatabaseError
from utils.exceptions import handle_not_found, handle_invalid_input

router = APIRouter(tags=["doctors"])


@router.get("/", response_model=list[DoctorSchema])
def get_doctors():
    """Get all doctors"""
    try:
        results = execute_query("SELECT * FROM doctors")
        return results
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{doctor_id}", response_model=DoctorSchema)
def get_doctor(doctor_id: int):
    """Get a specific doctor by ID"""
    doctor = get_by_id("doctors", doctor_id)
    if not doctor:
        handle_not_found("Doctor")
    return doctor


@router.post("/", response_model=DoctorSchema, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: DoctorSchema):
    """Create a new doctor"""
    try:
        query = """
            INSERT INTO doctors (name, specialization, phone, email)
            VALUES (?, ?, ?, ?)
        """
        execute_update(query, (doctor.name, doctor.specialization, doctor.phone, doctor.email))
        return doctor
    except DatabaseError as e:
        handle_invalid_input(f"Failed to create doctor: {str(e)}")


@router.put("/{doctor_id}", response_model=DoctorSchema)
def update_doctor(doctor_id: int, doctor: DoctorSchema):
    """Update an existing doctor"""
    if not get_by_id("doctors", doctor_id):
        handle_not_found("Doctor")
    
    try:
        query = """
            UPDATE doctors 
            SET name=?, specialization=?, phone=?, email=?
            WHERE id=?
        """
        execute_update(query, (doctor.name, doctor.specialization, doctor.phone, doctor.email, doctor_id))
        return get_by_id("doctors", doctor_id)
    except DatabaseError as e:
        handle_invalid_input(f"Failed to update doctor: {str(e)}")


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int):
    """Delete a doctor"""
    if not get_by_id("doctors", doctor_id):
        handle_not_found("Doctor")
    
    try:
        query = "DELETE FROM doctors WHERE id=?"
        execute_update(query, (doctor_id,))
    except DatabaseError as e:
        handle_invalid_input(f"Failed to delete doctor: {str(e)}")
