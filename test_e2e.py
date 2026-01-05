#!/usr/bin/env python3
"""
End-to-End Testing Script for AI Customer Service System
Tests all major flows: NLU → Business Logic → Response Generation
"""
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configuration
BASE_URL = "http://127.0.0.1:8000"
CHAT_ENDPOINT = f"{BASE_URL}/api/chat/message"
HEALTH_ENDPOINT = f"{BASE_URL}/api/chat/health"

# Test counters
PASSED = 0
FAILED = 0
ERRORS = []

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"


def print_header(title: str):
    """Print formatted header"""
    print(f"\n{BOLD}{BLUE}{'='*70}{RESET}")
    print(f"{BOLD}{BLUE}{title:^70}{RESET}")
    print(f"{BOLD}{BLUE}{'='*70}{RESET}\n")


def print_test_result(test_name: str, passed: bool, details: str = ""):
    """Print formatted test result"""
    global PASSED, FAILED
    
    if passed:
        PASSED += 1
        status = f"{GREEN}✅ PASSED{RESET}"
    else:
        FAILED += 1
        status = f"{RED}❌ FAILED{RESET}"
    
    print(f"{status} | {test_name}")
    if details:
        print(f"       → {details}")


def print_request(method: str, endpoint: str, data: Dict[str, Any]):
    """Print formatted request"""
    print(f"\n{YELLOW}Request:{RESET}")
    print(f"  {method} {endpoint}")
    print(f"  Body: {json.dumps(data, indent=2)}")


def print_response(response: Dict[str, Any]):
    """Print formatted response"""
    print(f"\n{YELLOW}Response:{RESET}")
    print(f"  Status: {response.get('status_code', 'N/A')}")
    if response.get('data'):
        print(f"  Body: {json.dumps(response['data'], indent=2)}")
    if response.get('error'):
        print(f"  Error: {response['error']}")


def send_chat_message(content: str, user_id: int = 1, conversation_id: str = None) -> Dict[str, Any]:
    """Send chat message and return response"""
    if not conversation_id:
        conversation_id = f"test_{datetime.now().timestamp()}"
    
    payload = {
        "content": content,
        "user_id": user_id,
        "conversation_id": conversation_id
    }
    
    try:
        response = requests.post(CHAT_ENDPOINT, json=payload, timeout=30)
        return {
            "status_code": response.status_code,
            "data": response.json() if response.status_code < 400 else None,
            "error": response.text if response.status_code >= 400 else None,
            "ok": response.status_code < 400
        }
    except Exception as e:
        return {
            "status_code": 0,
            "data": None,
            "error": str(e),
            "ok": False
        }


def check_health() -> bool:
    """Check if backend is running"""
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        return response.status_code == 200
    except:
        return False


def validate_chat_response(response_data: Dict[str, Any], expected_intent: str) -> tuple[bool, str]:
    """Validate response structure and content"""
    errors = []
    
    # Check required fields
    required_fields = [
        "message_id", "user_message", "bot_response", "timestamp",
        "conversation_id", "intent", "confidence", "entities"
    ]
    for field in required_fields:
        if field not in response_data:
            errors.append(f"Missing field: {field}")
    
    # Check intent
    if response_data.get("intent") != expected_intent:
        errors.append(f"Intent mismatch: expected '{expected_intent}', got '{response_data.get('intent')}'")
    
    # Check confidence score
    confidence = response_data.get("confidence")
    if not isinstance(confidence, (int, float)) or confidence < 0 or confidence > 1:
        errors.append(f"Invalid confidence score: {confidence}")
    
    # Check entities structure
    entities = response_data.get("entities", {})
    if not isinstance(entities, dict):
        errors.append("Entities should be a dict")
    
    # Check bot_response is non-empty string
    bot_response = response_data.get("bot_response")
    if not isinstance(bot_response, str) or not bot_response.strip():
        errors.append("bot_response should be non-empty string")
    
    return len(errors) == 0, "; ".join(errors)


def test_1_query():
    """Test Case 1: Simple Query (No Action Required)"""
    print_header("TEST CASE 1: Simple Query")
    
    request_data = {
        "content": "What dental services do you offer?",
        "user_id": 1,
        "conversation_id": "test_case_1"
    }
    
    print_request("POST", CHAT_ENDPOINT, request_data)
    response = send_chat_message(request_data["content"], request_data["user_id"], request_data["conversation_id"])
    print_response(response)
    
    # Validate
    passed = True
    details = ""
    
    if response["status_code"] != 200:
        passed = False
        details = f"Expected status 200, got {response['status_code']}"
    else:
        is_valid, error_msg = validate_chat_response(response["data"], "query")
        if not is_valid:
            passed = False
            details = error_msg
        elif response["data"].get("action_result") is not None:
            passed = False
            details = "Query should have action_result=null"
        elif response["data"].get("confidence") < 0.7:
            passed = False
            details = f"Confidence too low: {response['data'].get('confidence')}"
    
    print_test_result("Test 1: Simple Query", passed, details)
    return passed


def test_2_complete_booking():
    """Test Case 2: Complete Appointment Booking"""
    print_header("TEST CASE 2: Complete Appointment Booking")
    
    # Get tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    request_data = {
        "content": f"I'd like to book a cleaning with Dr. Wang on {tomorrow} at 2 PM. My name is John Smith and my phone is 555-1234",
        "user_id": 1,
        "conversation_id": "test_case_2"
    }
    
    print_request("POST", CHAT_ENDPOINT, request_data)
    response = send_chat_message(request_data["content"], request_data["user_id"], request_data["conversation_id"])
    print_response(response)
    
    # Validate
    passed = True
    details = ""
    
    if response["status_code"] != 200:
        passed = False
        details = f"Expected status 200, got {response['status_code']}"
    else:
        is_valid, error_msg = validate_chat_response(response["data"], "appointment")
        if not is_valid:
            passed = False
            details = error_msg
        else:
            action_result = response["data"].get("action_result")
            if not action_result:
                passed = False
                details = "action_result should not be null for appointment"
            elif not action_result.get("success"):
                passed = False
                details = f"Booking failed: {action_result.get('message')}"
            elif "appointment_id" not in str(action_result):
                passed = False
                details = "No appointment_id in action_result"
            elif "✅" not in response["data"].get("bot_response", ""):
                passed = False
                details = "Bot response should contain ✅ confirmation"
    
    print_test_result("Test 2: Complete Booking", passed, details)
    return passed


def test_3_invalid_doctor():
    """Test Case 3: Booking with Invalid Doctor"""
    print_header("TEST CASE 3: Booking with Invalid Doctor")
    
    request_data = {
        "content": "I want to see Dr. NonExistent for a cleaning",
        "user_id": 1,
        "conversation_id": "test_case_3"
    }
    
    print_request("POST", CHAT_ENDPOINT, request_data)
    response = send_chat_message(request_data["content"], request_data["user_id"], request_data["conversation_id"])
    print_response(response)
    
    # Validate
    passed = True
    details = ""
    
    if response["status_code"] != 200:
        passed = False
        details = f"Expected status 200, got {response['status_code']}"
    else:
        is_valid, error_msg = validate_chat_response(response["data"], "appointment")
        if not is_valid:
            passed = False
            details = error_msg
        else:
            action_result = response["data"].get("action_result")
            if not action_result:
                passed = False
                details = "action_result should not be null for appointment"
            elif action_result.get("success"):
                passed = False
                details = "Booking should have failed for invalid doctor"
            elif "❌" not in response["data"].get("bot_response", ""):
                passed = False
                details = "Bot response should contain ❌ error indicator"
    
    print_test_result("Test 3: Invalid Doctor Error Handling", passed, details)
    return passed


def test_4_missing_info():
    """Test Case 4: Booking with Missing Information"""
    print_header("TEST CASE 4: Booking with Missing Information")
    
    request_data = {
        "content": "Book an appointment",
        "user_id": 1,
        "conversation_id": "test_case_4"
    }
    
    print_request("POST", CHAT_ENDPOINT, request_data)
    response = send_chat_message(request_data["content"], request_data["user_id"], request_data["conversation_id"])
    print_response(response)
    
    # Validate
    passed = True
    details = ""
    
    if response["status_code"] != 200:
        passed = False
        details = f"Expected status 200, got {response['status_code']}"
    else:
        is_valid, error_msg = validate_chat_response(response["data"], "appointment")
        if not is_valid:
            passed = False
            details = error_msg
        else:
            action_result = response["data"].get("action_result")
            if not action_result:
                passed = False
                details = "action_result should not be null for appointment"
            elif action_result.get("success"):
                passed = False
                details = "Booking should have failed due to missing info"
            elif "Missing required information" not in action_result.get("message", ""):
                passed = False
                details = f"Error message should mention missing info, got: {action_result.get('message')}"
    
    print_test_result("Test 4: Missing Information Error", passed, details)
    return passed


def test_5_empty_message():
    """Test Case 5: Empty Message Validation"""
    print_header("TEST CASE 5: Empty Message Validation")
    
    request_data = {
        "content": "",
        "user_id": 1,
        "conversation_id": "test_case_5"
    }
    
    print_request("POST", CHAT_ENDPOINT, request_data)
    response = send_chat_message(request_data["content"], request_data["user_id"], request_data["conversation_id"])
    print_response(response)
    
    # Validate
    passed = True
    details = ""
    
    if response["status_code"] != 400:
        passed = False
        details = f"Expected status 400, got {response['status_code']}"
    elif "cannot be empty" not in response["error"].lower():
        passed = False
        details = "Error message should mention empty message"
    
    print_test_result("Test 5: Empty Message Validation", passed, details)
    return passed


def test_6_health_check():
    """Test Case 6: Health Check Endpoint"""
    print_header("TEST CASE 6: Health Check Endpoint")
    
    print_request("GET", HEALTH_ENDPOINT, {})
    
    try:
        response = requests.get(HEALTH_ENDPOINT, timeout=5)
        data = response.json()
        print_response({
            "status_code": response.status_code,
            "data": data,
            "error": None
        })
        
        passed = True
        details = ""
        
        if response.status_code != 200:
            passed = False
            details = f"Expected status 200, got {response.status_code}"
        elif data.get("service") != "chat":
            passed = False
            details = f"Expected service='chat', got '{data.get('service')}'"
        elif data.get("status") != "operational":
            passed = False
            details = f"Expected status='operational', got '{data.get('status')}'"
        elif "appointment_booking" not in data.get("features", []):
            passed = False
            details = "features should include 'appointment_booking'"
        
        print_test_result("Test 6: Health Check", passed, details)
        return passed
    except Exception as e:
        print_test_result("Test 6: Health Check", False, str(e))
        return False


def main():
    """Run all tests"""
    print(f"\n{BOLD}{BLUE}{'*'*70}{RESET}")
    print(f"{BOLD}{BLUE}{'AI CUSTOMER SERVICE - END-TO-END TEST SUITE':^70}{RESET}")
    print(f"{BOLD}{BLUE}{'*'*70}{RESET}")
    print(f"\nStarting tests at {datetime.now().isoformat()}")
    print(f"Backend URL: {BASE_URL}")
    
    # Check backend health
    print(f"\n{YELLOW}Checking backend connectivity...{RESET}")
    if not check_health():
        print(f"{RED}❌ Backend is not responding on {BASE_URL}{RESET}")
        print(f"   Please start backend: cd backend && uvicorn main:app --reload")
        return
    print(f"{GREEN}✅ Backend is running{RESET}")
    
    # Run all tests
    time.sleep(1)  # Brief pause before tests
    test_1_query()
    time.sleep(1)
    test_2_complete_booking()
    time.sleep(1)
    test_3_invalid_doctor()
    time.sleep(1)
    test_4_missing_info()
    time.sleep(1)
    test_5_empty_message()
    time.sleep(1)
    test_6_health_check()
    
    # Print summary
    print_header("TEST SUMMARY")
    total_tests = PASSED + FAILED
    pass_rate = (PASSED / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests:    {total_tests}")
    print(f"Passed:         {GREEN}{PASSED}{RESET}")
    print(f"Failed:         {RED}{FAILED}{RESET}")
    print(f"Pass Rate:      {BOLD}{pass_rate:.1f}%{RESET}")
    print(f"Completed at:   {datetime.now().isoformat()}")
    
    if FAILED == 0:
        print(f"\n{BOLD}{GREEN}🎉 ALL TESTS PASSED! 🎉{RESET}")
        print(f"{GREEN}System is ready for production deployment{RESET}\n")
    else:
        print(f"\n{BOLD}{RED}⚠️  {FAILED} TEST(S) FAILED{RESET}")
        print(f"{YELLOW}Please review the failures above and fix the issues{RESET}\n")


if __name__ == "__main__":
    main()
