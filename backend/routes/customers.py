"""
Customers API routes
"""
from fastapi import APIRouter, HTTPException, status
from schemas import CustomerSchema
from utils.db_utils import execute_query, execute_update, get_by_id, DatabaseError
from utils.exceptions import handle_not_found, handle_invalid_input

router = APIRouter(tags=["customers"])


@router.get("/", response_model=list[CustomerSchema])
def get_customers():
    """Get all customers"""
    try:
        results = execute_query("SELECT * FROM customers")
        return results
    except DatabaseError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(customer_id: int):
    """Get a specific customer by ID"""
    customer = get_by_id("customers", customer_id)
    if not customer:
        handle_not_found("Customer")
    return customer


@router.post("/", response_model=CustomerSchema, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerSchema):
    """Create a new customer"""
    try:
        query = """
            INSERT INTO customers (name, phone, email)
            VALUES (?, ?, ?)
        """
        execute_update(query, (customer.name, customer.phone, customer.email))
        return customer
    except DatabaseError as e:
        handle_invalid_input(f"Failed to create customer: {str(e)}")


@router.put("/{customer_id}", response_model=CustomerSchema)
def update_customer(customer_id: int, customer: CustomerSchema):
    """Update an existing customer"""
    if not get_by_id("customers", customer_id):
        handle_not_found("Customer")
    
    try:
        query = """
            UPDATE customers 
            SET name=?, phone=?, email=?
            WHERE id=?
        """
        execute_update(query, (customer.name, customer.phone, customer.email, customer_id))
        return get_by_id("customers", customer_id)
    except DatabaseError as e:
        handle_invalid_input(f"Failed to update customer: {str(e)}")


@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    """Delete a customer"""
    if not get_by_id("customers", customer_id):
        handle_not_found("Customer")
    
    try:
        query = "DELETE FROM customers WHERE id=?"
        execute_update(query, (customer_id,))
    except DatabaseError as e:
        handle_invalid_input(f"Failed to delete customer: {str(e)}")
