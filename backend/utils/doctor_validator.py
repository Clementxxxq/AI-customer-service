"""
Doctor Validator with Alias Mapping
Ensures doctor selection is deterministic and validated
"""
from typing import Optional, List, Dict, Tuple
from pydantic import BaseModel

# Doctor Alias Mapping - Support various user expressions
DOCTOR_ALIAS_MAP = {
    # Dr. Wang
    "wang": "Dr. Wang",
    "wangs": "Dr. Wang",
    "wang doctor": "Dr. Wang",
    "doctor wang": "Dr. Wang",
    "dr. wang": "Dr. Wang",
    "dr wang": "Dr. Wang",
    
    # Dr. Chen
    "chen": "Dr. Chen",
    "chens": "Dr. Chen",
    "chen doctor": "Dr. Chen",
    "doctor chen": "Dr. Chen",
    "dr. chen": "Dr. Chen",
    "dr chen": "Dr. Chen",
    
    # Dr. Li
    "li": "Dr. Li",
    "lis": "Dr. Li",
    "li doctor": "Dr. Li",
    "doctor li": "Dr. Li",
    "dr. li": "Dr. Li",
    "dr li": "Dr. Li",
}

# Valid doctor names (canonical)
VALID_DOCTORS = ["Dr. Wang", "Dr. Chen", "Dr. Li"]


class DoctorValidationResult(BaseModel):
    """Result of doctor validation"""
    valid: bool
    doctor: Optional[str] = None  # Canonical name if valid
    message: Optional[str] = None
    available_doctors: List[str] = VALID_DOCTORS


def normalize_and_validate_doctor(user_input: Optional[str]) -> DoctorValidationResult:
    """
    Normalize user input and validate against available doctors
    
    Args:
        user_input: Raw user input (e.g., "wang", "Dr. Wang", "wang")
    
    Returns:
        DoctorValidationResult with validation status and canonical name
    """
    if not user_input:
        return DoctorValidationResult(
            valid=False,
            message=f"Please choose one of our available dentists: {', '.join(VALID_DOCTORS)}",
            available_doctors=VALID_DOCTORS
        )
    
    # Normalize: lowercase, strip whitespace
    normalized = user_input.strip().lower()
    
    # Try alias mapping
    if normalized in DOCTOR_ALIAS_MAP:
        canonical_name = DOCTOR_ALIAS_MAP[normalized]
        return DoctorValidationResult(
            valid=True,
            doctor=canonical_name,
            available_doctors=VALID_DOCTORS
        )
    
    # Try direct match (in case LLM already returned canonical name)
    for canonical_name in VALID_DOCTORS:
        if normalized == canonical_name.lower():
            return DoctorValidationResult(
                valid=True,
                doctor=canonical_name,
                available_doctors=VALID_DOCTORS
            )
    
    # Invalid doctor
    return DoctorValidationResult(
        valid=False,
        message=f"Sorry, '{user_input}' is not available. Our available dentists are: {', '.join(VALID_DOCTORS)}",
        available_doctors=VALID_DOCTORS
    )


def get_doctor_selection_prompt() -> str:
    """
    Generate the prompt that shows available doctors
    ✅ Product-level: Show options first, then ask for selection
    """
    doctors_list = ", ".join(VALID_DOCTORS)
    return f"Today, we have {doctors_list} available. Which doctor would you like to see?"


def get_available_doctors() -> List[str]:
    """Get list of available doctors"""
    return VALID_DOCTORS.copy()
