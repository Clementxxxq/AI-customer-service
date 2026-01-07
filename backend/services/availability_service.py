"""
Availability management service
Generates available dates and time slots for doctors
"""
from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from utils.db_utils import execute_query


class AvailabilityService:
    """Service for managing appointment availability"""
    
    # Default business hours (9 AM to 6 PM)
    BUSINESS_HOURS_START = 9
    BUSINESS_HOURS_END = 18
    SLOT_DURATION_MINUTES = 30  # 30-minute slots
    
    @staticmethod
    def get_available_dates(
        doctor_id: Optional[int] = None,
        days_ahead: int = 14
    ) -> List[Dict[str, Any]]:
        """
        Get available dates for appointment booking
        
        Args:
            doctor_id: Doctor ID (optional). If provided, check doctor's specific availability
            days_ahead: Number of days to look ahead (default 14 days)
            
        Returns:
            List of dates with available time slots
            Example:
            [
                {
                    "date": "2026-01-10",
                    "slots": ["09:00", "09:30", "10:00", ...]
                },
                ...
            ]
        """
        available_dates = []
        today = date.today()
        
        # Generate slots for next N days (skip weekends)
        for i in range(1, days_ahead + 1):
            check_date = today + timedelta(days=i)
            
            # Skip weekends (Monday=0, Sunday=6)
            if check_date.weekday() >= 5:  # Saturday=5, Sunday=6
                continue
            
            # Generate time slots for this date
            slots = AvailabilityService._generate_time_slots(check_date, doctor_id)
            
            if slots:  # Only include dates with available slots
                available_dates.append({
                    "date": check_date.strftime("%Y-%m-%d"),
                    "day_of_week": check_date.strftime("%A"),
                    "slots": slots
                })
        
        return available_dates
    
    @staticmethod
    def _generate_time_slots(
        check_date: date,
        doctor_id: Optional[int] = None
    ) -> List[str]:
        """
        Generate available time slots for a specific date
        
        Args:
            check_date: Date to check
            doctor_id: Doctor ID (optional)
            
        Returns:
            List of available time slots in HH:MM format
        """
        slots = []
        
        # Generate slots from business start to end
        current_time = datetime.combine(check_date, datetime.min.time()).replace(
            hour=AvailabilityService.BUSINESS_HOURS_START,
            minute=0
        )
        end_time = current_time.replace(
            hour=AvailabilityService.BUSINESS_HOURS_END,
            minute=0
        )
        
        # Generate 30-minute slots
        while current_time < end_time:
            time_str = current_time.strftime("%H:%M")
            
            # Check if this slot is available (not booked)
            if AvailabilityService._is_slot_available(
                doctor_id,
                check_date,
                time_str
            ):
                slots.append(time_str)
            
            current_time += timedelta(minutes=AvailabilityService.SLOT_DURATION_MINUTES)
        
        return slots
    
    @staticmethod
    def _is_slot_available(
        doctor_id: Optional[int],
        check_date: date,
        time_str: str
    ) -> bool:
        """
        Check if a specific time slot is available
        
        Args:
            doctor_id: Doctor ID (optional)
            check_date: Date to check
            time_str: Time in HH:MM format
            
        Returns:
            True if slot is available, False otherwise
        """
        try:
            # Convert date and time to comparable format
            date_str = check_date.strftime("%Y-%m-%d")
            
            # Query for existing appointments at this time
            if doctor_id:
                query = """
                    SELECT COUNT(*) as count FROM appointments
                    WHERE doctor_id = ?
                    AND appointment_date = ?
                    AND appointment_time = ?
                    AND status != 'cancelled'
                """
                result = execute_query(query, (doctor_id, date_str, time_str))
            else:
                query = """
                    SELECT COUNT(*) as count FROM appointments
                    WHERE appointment_date = ?
                    AND appointment_time = ?
                    AND status != 'cancelled'
                """
                result = execute_query(query, (date_str, time_str))
            
            # Slot is available if no appointment exists
            count = result[0]['count'] if result else 0
            return count == 0
            
        except Exception as e:
            # If database error, assume slot is available
            print(f"Error checking slot availability: {e}")
            return True
    
    @staticmethod
    def get_doctor_availability(doctor_id: int, days_ahead: int = 14) -> List[Dict[str, Any]]:
        """
        Get availability specifically for a doctor
        
        Args:
            doctor_id: Doctor ID
            days_ahead: Number of days to look ahead
            
        Returns:
            List of available dates with time slots for this doctor
        """
        return AvailabilityService.get_available_dates(
            doctor_id=doctor_id,
            days_ahead=days_ahead
        )
    
    @staticmethod
    def get_suggested_appointment(
        available_dates: List[Dict[str, Any]]
    ) -> Optional[Dict[str, str]]:
        """
        Get a suggested appointment time from available dates
        
        Args:
            available_dates: List of available dates with slots
            
        Returns:
            Suggested appointment as {"date": "2026-01-10", "time": "10:00"}
            or None if no slots available
        """
        if not available_dates or len(available_dates) == 0:
            return None
        
        # Suggest the earliest available date with morning slot (10:00)
        for date_info in available_dates:
            slots = date_info.get("slots", [])
            
            # Try to find 10:00 slot (popular time)
            if "10:00" in slots:
                return {
                    "date": date_info["date"],
                    "time": "10:00"
                }
            
            # If 10:00 not available, take first available slot
            if slots:
                return {
                    "date": date_info["date"],
                    "time": slots[0]
                }
        
        return None
