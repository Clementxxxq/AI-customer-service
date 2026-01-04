"""
Services API routes
"""
from fastapi import APIRouter, HTTPException, status
from schemas import ServiceSchema
from utils.db_utils import execute_query, execute_update, get_by_id, DatabaseError
from utils.exceptions import handle_not_found, handle_invalid_input

router = APIRouter(tags=["services"])


@router.get("/", response_model=list[ServiceSchema])
def get_services():
    """Get all services"""
    try:
        results = execute_query("SELECT * FROM services")
        return results
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{service_id}", response_model=ServiceSchema)
def get_service(service_id: int):
    """Get a specific service by ID"""
    service = get_by_id("services", service_id)
    if not service:
        handle_not_found("Service")
    return service


@router.post("/", response_model=ServiceSchema, status_code=status.HTTP_201_CREATED)
def create_service(service: ServiceSchema):
    """Create a new service"""
    try:
        query = """
            INSERT INTO services (name, description, duration_minutes, price, doctor_id)
            VALUES (?, ?, ?, ?, ?)
        """
        execute_update(query, (service.name, service.description, service.duration_minutes, service.price, service.doctor_id))
        return service
    except DatabaseError as e:
        handle_invalid_input(f"Failed to create service: {str(e)}")


@router.put("/{service_id}", response_model=ServiceSchema)
def update_service(service_id: int, service: ServiceSchema):
    """Update an existing service"""
    if not get_by_id("services", service_id):
        handle_not_found("Service")
    
    try:
        query = """
            UPDATE services 
            SET name=?, description=?, duration_minutes=?, price=?, doctor_id=?
            WHERE id=?
        """
        execute_update(query, (service.name, service.description, service.duration_minutes, service.price, service.doctor_id, service_id))
        return get_by_id("services", service_id)
    except DatabaseError as e:
        handle_invalid_input(f"Failed to update service: {str(e)}")


@router.delete("/{service_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service(service_id: int):
    """Delete a service"""
    if not get_by_id("services", service_id):
        handle_not_found("Service")
    
    try:
        query = "DELETE FROM services WHERE id=?"
        execute_update(query, (service_id,))
    except DatabaseError as e:
        handle_invalid_input(f"Failed to delete service: {str(e)}")
