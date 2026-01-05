# End-to-End Testing Guide - AI Customer Service System

## System Architecture Overview

```
User Input (Natural Language)
    ↓
[Step 1] Llama3.2:3b NLU (LlamaService)
    → Parse intent + extract entities
    → Return: AIResponse(intent, confidence, entities)
    ↓
[Step 2] Business Logic Router (_execute_business_logic)
    → Route to appropriate handler based on intent
    ↓
[Step 3] Business Logic Execution (AppointmentService)
    → Find doctor, service, customer
    → Validate availability
    → Execute database operations
    → Return: success/failure result
    ↓
[Step 4] Response Generation (_generate_response)
    → Create natural language response
    ↓
ChatResponse (JSON with action_result field)
```

---

## Prerequisites

1. **Backend Running:**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```
   Expected: ✅ Backend listening on http://127.0.0.1:8000

2. **Ollama Running:**
   ```bash
   ollama serve
   ```
   Expected: ✅ Ollama listening on http://127.0.0.1:11434

3. **Llama Model Loaded:**
   ```bash
   ollama list
   ```
   Expected: ✅ `llama3.2:3b` in the list

4. **Database Initialized:**
   - clinic.db should exist in project root
   - Tables: customers, doctors, services, appointments, time_slots
   - Sample data pre-populated

---

## Test Case 1: Simple Query (No Action Required)

**Purpose:** Test NLU parsing and query handling (no business logic execution)

**Request:**
```json
POST /chat/message
{
  "content": "What dental services do you offer?",
  "user_id": 1,
  "conversation_id": "test_conv_001"
}
```

**Expected Response:**
```json
{
  "message_id": "msg_...",
  "user_message": "What dental services do you offer?",
  "bot_response": "I'd be happy to help answer your question.",
  "timestamp": "2025-01-04T...",
  "conversation_id": "test_conv_001",
  "intent": "query",
  "confidence": 0.85,
  "entities": {
    "service": null,
    "doctor": null,
    "date": null,
    "time": null,
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  },
  "action_result": null
}
```

**Validation Points:**
- ✅ Intent correctly identified as "query"
- ✅ Confidence score between 0-1
- ✅ action_result is null (no booking)
- ✅ bot_response is natural language

---

## Test Case 2: Complete Appointment Booking

**Purpose:** Test full end-to-end flow with successful appointment booking

**Request:**
```json
POST /chat/message
{
  "content": "I'd like to book a teeth cleaning appointment with Dr. Wang tomorrow at 2 PM",
  "user_id": 1,
  "conversation_id": "test_conv_002"
}
```

**Expected Response:**
```json
{
  "message_id": "msg_...",
  "user_message": "I'd like to book a teeth cleaning appointment with Dr. Wang tomorrow at 2 PM",
  "bot_response": "✅ Great! I've booked your appointment for teeth cleaning with Dr. Wang on 2025-01-05 at 14:00.",
  "timestamp": "2025-01-04T...",
  "conversation_id": "test_conv_002",
  "intent": "appointment",
  "confidence": 0.92,
  "entities": {
    "service": "teeth cleaning",
    "doctor": "Dr. Wang",
    "date": "2025-01-05",
    "time": "14:00",
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  },
  "action_result": {
    "action": "appointment_booking",
    "success": true,
    "message": "Appointment booked successfully",
    "details": {
      "doctor": {"id": 1, "name": "Dr. Wang"},
      "service": {"id": 1, "name": "Teeth Cleaning"},
      "customer": {"id": 1},
      "booking": {
        "success": true,
        "message": "Appointment booked successfully",
        "appointment_id": 5
      }
    }
  }
}
```

**Validation Points:**
- ✅ Intent correctly identified as "appointment"
- ✅ Entities extracted: doctor, service, date, time
- ✅ action_result.success = true
- ✅ appointment_id returned in details
- ✅ bot_response shows confirmation with all details
- ✅ Database should have new appointment record

**Database Verification:**
```sql
-- Check that appointment was created
SELECT * FROM appointments 
WHERE id = <appointment_id_from_response>
ORDER BY created_at DESC LIMIT 1;

-- Should return:
-- id | customer_id | doctor_id | service_id | appointment_date | appointment_time | ...
```

---

## Test Case 3: Booking with Invalid Doctor

**Purpose:** Test error handling when requested doctor doesn't exist

**Request:**
```json
POST /chat/message
{
  "content": "I want to see Dr. Smith for a cleaning",
  "user_id": 1,
  "conversation_id": "test_conv_003"
}
```

**Expected Response:**
```json
{
  "message_id": "msg_...",
  "user_message": "I want to see Dr. Smith for a cleaning",
  "bot_response": "❌ Sorry: Doctor 'Dr. Smith' not found",
  "timestamp": "2025-01-04T...",
  "conversation_id": "test_conv_003",
  "intent": "appointment",
  "confidence": 0.88,
  "entities": {
    "service": "cleaning",
    "doctor": "Dr. Smith",
    "date": null,
    "time": null,
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  },
  "action_result": {
    "action": "appointment_booking",
    "success": false,
    "message": "Doctor 'Dr. Smith' not found",
    "details": {}
  }
}
```

**Validation Points:**
- ✅ Intent correctly identified as "appointment"
- ✅ action_result.success = false
- ✅ Error message clearly states why booking failed
- ✅ bot_response shows error with ❌ prefix
- ✅ No appointment created in database

---

## Test Case 4: Booking with Missing Information

**Purpose:** Test handling of incomplete booking requests

**Request:**
```json
POST /chat/message
{
  "content": "Book an appointment",
  "user_id": 1,
  "conversation_id": "test_conv_004"
}
```

**Expected Response:**
```json
{
  "message_id": "msg_...",
  "user_message": "Book an appointment",
  "bot_response": "❌ Sorry: Missing required information (doctor, service, date, time)",
  "timestamp": "2025-01-04T...",
  "conversation_id": "test_conv_004",
  "intent": "appointment",
  "confidence": 0.65,
  "entities": {
    "service": null,
    "doctor": null,
    "date": null,
    "time": null,
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  },
  "action_result": {
    "action": "appointment_booking",
    "success": false,
    "message": "Missing required information (doctor, service, date, time)",
    "details": {}
  }
}
```

**Validation Points:**
- ✅ Intent identified as "appointment"
- ✅ action_result.success = false
- ✅ Clear error message about missing fields
- ✅ No database modification

---

## Test Case 5: Empty Message (Error Handling)

**Purpose:** Test input validation

**Request:**
```json
POST /chat/message
{
  "content": "",
  "user_id": 1,
  "conversation_id": "test_conv_005"
}
```

**Expected Response:**
```json
{
  "detail": "Message content cannot be empty"
}
```

**Status:** 400 Bad Request

**Validation Points:**
- ✅ HTTP 400 status code
- ✅ Clear error message in detail field

---

## Test Case 6: Multi-entity Booking with Customer Info

**Purpose:** Test booking with customer information included

**Request:**
```json
POST /chat/message
{
  "content": "Hi, I'm John Smith, my phone is 555-1234. I'd like to book a root canal with Dr. Linda on January 10th at 10:00 AM",
  "user_id": 1,
  "conversation_id": "test_conv_006"
}
```

**Expected Response:**
```json
{
  "message_id": "msg_...",
  "user_message": "Hi, I'm John Smith, my phone is 555-1234...",
  "bot_response": "✅ Great! I've booked your appointment for root canal with Dr. Linda on 2025-01-10 at 10:00.",
  "timestamp": "2025-01-04T...",
  "conversation_id": "test_conv_006",
  "intent": "appointment",
  "confidence": 0.94,
  "entities": {
    "service": "root canal",
    "doctor": "Dr. Linda",
    "date": "2025-01-10",
    "time": "10:00",
    "customer_name": "John Smith",
    "customer_phone": "555-1234",
    "customer_email": null
  },
  "action_result": {
    "action": "appointment_booking",
    "success": true,
    "message": "Appointment booked successfully",
    "details": {
      "doctor": {"id": 2, "name": "Dr. Linda"},
      "service": {"id": 3, "name": "Root Canal"},
      "customer": {"id": 2},
      "booking": {
        "success": true,
        "message": "Appointment booked successfully",
        "appointment_id": 6
      }
    }
  }
}
```

**Validation Points:**
- ✅ Customer information extracted (name, phone)
- ✅ All entities populated
- ✅ Customer record created or retrieved
- ✅ Appointment successfully booked
- ✅ appointment_id in response

---

## Test Case 7: Health Check Endpoint

**Purpose:** Verify service status and capabilities

**Request:**
```json
GET /chat/health
```

**Expected Response:**
```json
{
  "service": "chat",
  "status": "operational",
  "features": ["nlu", "appointment_booking", "business_logic"],
  "version": "2.0.0"
}
```

**Validation Points:**
- ✅ Service status is "operational"
- ✅ All features listed
- ✅ Version is 2.0.0 (indicating new business logic integration)

---

## Testing Checklist

### Before Testing:
- [ ] Backend running on http://127.0.0.1:8000
- [ ] Ollama running on http://127.0.0.1:11434
- [ ] Llama3.2:3b model available
- [ ] clinic.db exists with sample data
- [ ] Thunder Client installed and configured
- [ ] All Python dependencies installed

### During Testing:
- [ ] Test Case 1: Query handling ✅
- [ ] Test Case 2: Complete booking ✅
- [ ] Test Case 3: Invalid doctor error ✅
- [ ] Test Case 4: Missing information error ✅
- [ ] Test Case 5: Empty message validation ✅
- [ ] Test Case 6: Multi-entity booking ✅
- [ ] Test Case 7: Health check ✅

### After Each Successful Test:
- [ ] Response has correct HTTP status code
- [ ] All required fields present in response
- [ ] Confidence score between 0-1
- [ ] action_result matches expected structure
- [ ] bot_response is user-friendly natural language
- [ ] Database state updated correctly (for booking tests)

### Success Criteria:
- ✅ NLU correctly parses all test inputs
- ✅ Business logic executes for appointment intents
- ✅ Errors are handled gracefully with clear messages
- ✅ Database transactions are atomic (all or nothing)
- ✅ Response format consistent and well-structured
- ✅ No unhandled exceptions or 500 errors

---

## Sample Thunder Client Collection

### Test 1: Query
```
POST http://127.0.0.1:8000/chat/message
Content-Type: application/json

{
  "content": "What services do you offer?",
  "user_id": 1,
  "conversation_id": "test_001"
}
```

### Test 2: Full Booking
```
POST http://127.0.0.1:8000/chat/message
Content-Type: application/json

{
  "content": "I'd like to book a cleaning with Dr. Wang tomorrow at 2 PM",
  "user_id": 1,
  "conversation_id": "test_002"
}
```

### Test 3: Health Check
```
GET http://127.0.0.1:8000/chat/health
```

---

## Debugging Guide

### Issue: Ollama Connection Error
```
Error: "AI service error: Unable to connect to Ollama"
```
**Solution:**
1. Verify Ollama is running: `ollama serve` in separate terminal
2. Check Ollama port: http://127.0.0.1:11434
3. Ensure model exists: `ollama list`
4. If missing: `ollama pull llama3.2:3b`

### Issue: Doctor Not Found
```
Error: "Doctor 'Dr. Wang' not found"
```
**Solution:**
1. Verify doctors in database: `SELECT * FROM doctors;`
2. Check spelling in request matches database exactly
3. Verify database is initialized: `python init_db.py`

### Issue: Appointment Date Parsing Error
```
Error: "Invalid appointment date format"
```
**Solution:**
1. Ensure date format is YYYY-MM-DD
2. Check Llama prompt is formatting dates correctly
3. Test with explicit date: "January 5, 2025" → should parse to "2025-01-05"

### Issue: Empty action_result for Appointment
```
"action_result": null  // Expected: booking details
```
**Solution:**
1. Verify intent was correctly identified as "appointment"
2. Check all required entities (doctor, service, date, time) are present
3. Review Llama NLU output for parsing accuracy
4. Enable debug logging in _execute_business_logic()

### Issue: Database Transaction Failed
```
"success": false, "message": "Database error"
```
**Solution:**
1. Check clinic.db file exists and is accessible
2. Verify tables are created: `python init_db.py`
3. Check time slots exist for requested date/time
4. Review database constraints (e.g., duplicate appointments)

---

## Success Metrics

After completing all 7 test cases, your system is production-ready if:

1. **100% Success Rate:** All test cases pass without modification
2. **Sub-100ms Response Time:** Each request completes in < 100ms (excluding Ollama inference)
3. **Accurate NLU:** Intent confidence > 0.8 for well-formed requests
4. **Data Integrity:** All bookings create correct database records
5. **Error Resilience:** All error cases handled gracefully
6. **Clear Communication:** All error messages are user-friendly

---

## Next Steps

After successful end-to-end testing:

1. **Implement Cancellation Logic:**
   - Add `_handle_cancellation()` implementation
   - Get appointment ID from entities
   - Call `AppointmentService.cancel_appointment()`

2. **Implement Modification Logic:**
   - Add `_handle_modification()` implementation
   - Support date/time changes
   - Ensure no double-booking

3. **Add Conversation History:**
   - Implement database storage for conversations
   - Add multi-turn context awareness
   - Support follow-up messages

4. **Production Deployment:**
   - Add authentication/authorization
   - Implement rate limiting
   - Set up monitoring and logging
   - Configure Ollama for production performance

---

**Last Updated:** January 4, 2025
**System Version:** 2.0.0 (NLU + Business Logic Integration)
