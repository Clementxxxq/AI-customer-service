"""
Appointment business logic
Handles booking, cancellation, and modification without touching AI
"""
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from utils.db_utils import execute_query, execute_update, get_by_id, DatabaseError


class AppointmentService:
    """Business logic for appointment management"""
    
    @staticmethod
    def find_doctor_by_name(doctor_name: str) -> Optional[Dict[str, Any]]:
        """
        Find doctor by name
        
        Args:
            doctor_name: Doctor name (partial or full)
            
        Returns:
            Doctor record or None
        """
        if not doctor_name:
            return None
        
        try:
            # Search for doctor by name (case-insensitive)
            query = "SELECT * FROM doctors WHERE LOWER(name) LIKE LOWER(?)"
            results = execute_query(query, (f"%{doctor_name}%",))
            return results[0] if results else None
        except Exception as e:
            return None
    
    @staticmethod
    def find_service_by_name(service_name: str) -> Optional[Dict[str, Any]]:
        """
        Find service by name
        
        Args:
            service_name: Service name (partial or full)
            
        Returns:
            Service record or None
        """
        if not service_name:
            return None
        
        try:
            query = "SELECT * FROM services WHERE LOWER(name) LIKE LOWER(?)"
            results = execute_query(query, (f"%{service_name}%",))
            return results[0] if results else None
        except Exception as e:
            return None
    
    @staticmethod
    def find_customer_by_phone(phone: str) -> Optional[Dict[str, Any]]:
        """
        Find customer by phone
        
        Args:
            phone: Phone number
            
        Returns:
            Customer record or None
        """
        if not phone:
            return None
        
        try:
            query = "SELECT * FROM customers WHERE phone = ?"
            results = execute_query(query, (phone,))
            return results[0] if results else None
        except Exception:
            return None
    
    @staticmethod
    def find_or_create_customer(
        name: Optional[str] = None,
        phone: Optional[str] = None,
        email: Optional[str] = None
    ) -> Optional[int]:
        """
        Find existing customer or create new one
        
        Args:
            name: Customer name
            phone: Phone number
            email: Email address
            
        Returns:
            Customer ID or None
        """
        # Try to find by phone if provided
        if phone:
            customer = AppointmentService.find_customer_by_phone(phone)
            if customer:
                return customer.get('id')
        
        # Create new customer if we have required info
        if name and phone:
            try:
                query = """
                    INSERT INTO customers (name, phone, email)
                    VALUES (?, ?, ?)
                """
                execute_update(query, (name, phone, email or ""))
                
                # Get the new customer ID
                customer = AppointmentService.find_customer_by_phone(phone)
                return customer.get('id') if customer else None
            except DatabaseError:
                return None
        
        return None
    
    @staticmethod
    def is_slot_available(
        doctor_id: int,
        appointment_date: str,
        appointment_time: str
    ) -> bool:
        """
        Check if time slot is available
        
        Args:
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD
            appointment_time: Time in HH:MM
            
        Returns:
            True if slot is available
        """
        try:
            # Check for existing appointments at same time
            query = """
                SELECT COUNT(*) as count FROM appointments
                WHERE doctor_id = ? AND date = ? AND time = ? AND status != 'cancelled'
            """
            results = execute_query(query, (doctor_id, appointment_date, appointment_time))
            count = results[0].get('count', 0) if results else 0
            return count == 0
        except Exception:
            return False
    
    @staticmethod
    def book_appointment(
        service_id: int,
        customer_id: int,
        doctor_id: int,
        appointment_date: str,
        appointment_time: str,
        status: str = "confirmed"
    ) -> Dict[str, Any]:
        """
        Book an appointment
        
        Args:
            service_id: Service ID
            customer_id: Customer ID
            doctor_id: Doctor ID
            appointment_date: Date in YYYY-MM-DD
            appointment_time: Time in HH:MM
            status: Appointment status (confirmed/pending)
            
        Returns:
            Dict with success, message, appointment_id
        """
        # Validate inputs
        if not all([service_id, customer_id, doctor_id, appointment_date, appointment_time]):
            return {
                "success": False,
                "message": "Missing required information for booking",
                "errors": ["service_id", "customer_id", "doctor_id", "date", "time"]
            }
        
        # Check if slot is available
        if not AppointmentService.is_slot_available(doctor_id, appointment_date, appointment_time):
            return {
                "success": False,
                "message": f"Time slot not available for {appointment_date} at {appointment_time}",
                "errors": ["slot_unavailable"]
            }
        
        # Verify doctor and service exist
        doctor = get_by_id("doctors", doctor_id)
        service = get_by_id("services", service_id)
        
        if not doctor or not service:
            return {
                "success": False,
                "message": "Invalid doctor or service",
                "errors": ["invalid_doctor_or_service"]
            }
        
        try:
            # Insert appointment
            query = """
                INSERT INTO appointments (service_id, customer_id, doctor_id, date, time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            execute_update(query, (service_id, customer_id, doctor_id, appointment_date, appointment_time, status))
            
            # Get the appointment ID (last inserted)
            query = """
                SELECT id FROM appointments
                WHERE customer_id = ? AND doctor_id = ? AND date = ? AND time = ?
                ORDER BY id DESC LIMIT 1
            """
            result = execute_query(query, (customer_id, doctor_id, appointment_date, appointment_time))
            appointment_id = result[0].get('id') if result else None
            
            return {
                "success": True,
                "message": f"Appointment booked successfully with Dr. {doctor.get('name')} for {service.get('name')} on {appointment_date} at {appointment_time}",
                "appointment_id": appointment_id,
                "appointment_date": appointment_date,
                "appointment_time": appointment_time
            }
        except DatabaseError as e:
            return {
                "success": False,
                "message": f"Failed to book appointment: {str(e)}",
                "errors": [str(e)]
            }
    
    @staticmethod
    def cancel_appointment(appointment_id: int) -> Dict[str, Any]:
        """
        Cancel an appointment
        
        Args:
            appointment_id: Appointment ID
            
        Returns:
            Dict with success, message
        """
        if not appointment_id:
            return {
                "success": False,
                "message": "Appointment ID required",
                "errors": ["appointment_id_required"]
            }
        
        # Check if appointment exists
        appointment = get_by_id("appointments", appointment_id)
        if not appointment:
            return {
                "success": False,
                "message": f"Appointment {appointment_id} not found",
                "errors": ["appointment_not_found"]
            }
        
        # Check if already cancelled
        if appointment.get('status') == 'cancelled':
            return {
                "success": False,
                "message": "Appointment already cancelled",
                "errors": ["already_cancelled"]
            }
        
        try:
            # Update status to cancelled
            query = "UPDATE appointments SET status = ? WHERE id = ?"
            execute_update(query, ("cancelled", appointment_id))
            
            return {
                "success": True,
                "message": f"Appointment {appointment_id} cancelled successfully",
                "cancelled_appointment_id": appointment_id
            }
        except DatabaseError as e:
            return {
                "success": False,
                "message": f"Failed to cancel appointment: {str(e)}",
                "errors": [str(e)]
            }
    
    @staticmethod
    def modify_appointment(
        appointment_id: int,
        new_date: Optional[str] = None,
        new_time: Optional[str] = None,
        new_doctor_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Modify an appointment
        
        Args:
            appointment_id: Appointment ID
            new_date: New date in YYYY-MM-DD
            new_time: New time in HH:MM
            new_doctor_id: New doctor ID
            
        Returns:
            Dict with success, message
        """
        if not appointment_id:
            return {
                "success": False,
                "message": "Appointment ID required",
                "errors": ["appointment_id_required"]
            }
        
        # Get existing appointment
        appointment = get_by_id("appointments", appointment_id)
        if not appointment:
            return {
                "success": False,
                "message": f"Appointment {appointment_id} not found",
                "errors": ["appointment_not_found"]
            }
        
        # Use existing values if not provided
        date_to_use = new_date or appointment.get('date')
        time_to_use = new_time or appointment.get('time')
        doctor_to_use = new_doctor_id or appointment.get('doctor_id')
        
        # Check if new slot is available
        if not AppointmentService.is_slot_available(doctor_to_use, date_to_use, time_to_use):
            return {
                "success": False,
                "message": f"New time slot not available",
                "errors": ["slot_unavailable"]
            }
        
        try:
            # Update appointment
            query = """
                UPDATE appointments
                SET date = ?, time = ?, doctor_id = ?
                WHERE id = ?
            """
            execute_update(query, (date_to_use, time_to_use, doctor_to_use, appointment_id))
            
            return {
                "success": True,
                "message": f"Appointment {appointment_id} modified successfully",
                "appointment_id": appointment_id,
                "new_date": date_to_use,
                "new_time": time_to_use
            }
        except DatabaseError as e:
            return {
                "success": False,
                "message": f"Failed to modify appointment: {str(e)}",
                "errors": [str(e)]
            }
