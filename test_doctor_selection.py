"""
Test script for doctor validation and selection flow
"""
import sys
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

from utils.doctor_validator import (
    normalize_and_validate_doctor,
    get_doctor_selection_prompt,
    get_available_doctors,
    VALID_DOCTORS
)


def test_doctor_validation():
    """Test doctor validation with various inputs"""
    print("=" * 60)
    print("🧪 Testing Doctor Validation")
    print("=" * 60)
    
    test_cases = [
        ("wang_doctor", True, "Dr. Wang"),
        ("Wang", True, "Dr. Wang"),
        ("dr. wang", True, "Dr. Wang"),
        ("Chen", True, "Dr. Chen"),
        ("chen_doctor", True, "Dr. Chen"),
        ("li", True, "Dr. Li"),
        ("Dr. Li", True, "Dr. Li"),
        ("zhao_doctor", False, None),  # Invalid - Zhao is not available
        ("Zhang", False, None),  # Invalid
        ("", False, None),  # Empty
        (None, False, None),  # None
    ]
    
    for user_input, should_be_valid, expected_doctor in test_cases:
        result = normalize_and_validate_doctor(user_input)
        status = "✅" if result.valid == should_be_valid else "❌"
        
        print(f"\n{status} Input: '{user_input}'")
        print(f"   Valid: {result.valid} (expected: {should_be_valid})")
        if result.valid:
            print(f"   Doctor: {result.doctor}")
            if expected_doctor:
                assert result.doctor == expected_doctor, f"Expected {expected_doctor}, got {result.doctor}"
        else:
            print(f"   Message: {result.message}")


def test_doctor_selection_prompt():
    """Test doctor selection prompt generation"""
    print("\n" + "=" * 60)
    print("🎯 Testing Doctor Selection Prompt")
    print("=" * 60)
    
    doctors = get_available_doctors()
    prompt = get_doctor_selection_prompt()
    
    print(f"\n📋 Available doctors: {doctors}")
    print(f"\n💬 Selection prompt:\n{prompt}")
    
    # Verify all doctors are in the prompt
    for doctor in doctors:
        assert doctor in prompt, f"Doctor '{doctor}' not in prompt"
    
    print("\n✅ All doctors are in the prompt")


def test_invalid_doctor_handling():
    """Test handling of invalid doctor selection"""
    print("\n" + "=" * 60)
    print("⚠️  Testing Invalid Doctor Handling")
    print("=" * 60)
    
    invalid_inputs = ["zhao_doctor", "Zhang", "Dr. Smith", "unknown"]  # zhao_doctor is not a valid doctor
    
    for invalid in invalid_inputs:
        result = normalize_and_validate_doctor(invalid)
        print(f"\n❌ Invalid: '{invalid}'")
        print(f"   Message: {result.message}")
        assert not result.valid, f"Expected invalid for '{invalid}'"
        assert "available" in result.message.lower(), "Error message should mention available options"


if __name__ == "__main__":
    try:
        test_doctor_validation()
        test_doctor_selection_prompt()
        test_invalid_doctor_handling()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
