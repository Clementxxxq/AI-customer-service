# Step-by-Step: Running the Complete End-to-End Tests

## 📋 System Overview

Your AI Customer Service System is now complete with full integration:

```
User Message (Natural Language)
    ↓
Step 1: NLU Parsing → LlamaService.parse_user_input()
    ↓ Returns: intent + entities
Step 2: Business Logic → _execute_business_logic()
    ↓ Routes to: _handle_appointment_booking() etc.
Step 3: Service Execution → AppointmentService methods
    ↓ Database operations: find doctor, book appointment
Step 4: Response Generation → _generate_response()
    ↓ Returns natural language + action_result
Result: ChatResponse with structured data
```

---

## 🚀 Prerequisites Checklist

Before running tests, ensure all dependencies are in place:

### 1. Python Environment
```bash
# Check Python version (should be 3.9+)
python --version

# Create virtual environment (if not already done)
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 2. Install Python Dependencies
```bash
# In project root directory
pip install -r requirements.txt
```

Should include: `fastapi`, `uvicorn`, `pydantic`, `sqlite3`, `requests`

### 3. Check/Create Database
```bash
# Initialize database with sample data
python init_db.py

# Expected output:
# clinic.db created with sample data successfully!
```

Verify doctors exist:
```bash
# Check what doctors are in database
sqlite3 clinic.db "SELECT id, name FROM doctors;"
# Expected: Dr. Wang, Dr. Linda, etc.
```

### 4. Install Ollama and Llama Model
```bash
# Download from https://ollama.ai
# After installation:

# Verify Ollama is installed
ollama --version

# Pull the model (one-time)
ollama pull llama3.2:3b

# Expected output:
# pulling bb7e48c0be3f...
# pulling...
# success!
```

### 5. Start Ollama Service
```bash
# In a new terminal, keep running while testing
ollama serve

# Expected output:
# time=2025-01-04T10:00:00.000Z level=INFO msg="Llama Server is listening on [::]:11434"
```

---

## 🏃 Running the Tests

### Method 1: Automated Test Suite (Recommended)

#### Step 1: Start Backend
```bash
# Terminal 1
cd backend
uvicorn main:app --reload

# Expected output:
# INFO:     Started server process [PID]
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

#### Step 2: Verify Ollama is Running
```bash
# Terminal 2 (keep running in background)
ollama serve

# Expected output:
# Llama Server is listening on [::]:11434
```

#### Step 3: Run Test Suite
```bash
# Terminal 3 (in project root)
python test_e2e.py

# Output will show:
# ✅ PASSED | Test 1: Simple Query
# ✅ PASSED | Test 2: Complete Booking
# ✅ PASSED | Test 3: Invalid Doctor Error Handling
# ✅ PASSED | Test 4: Missing Information Error
# ✅ PASSED | Test 5: Empty Message Validation
# ✅ PASSED | Test 6: Health Check
#
# TEST SUMMARY
# Total Tests:    6
# Passed:         6
# Failed:         0
# Pass Rate:      100.0%
#
# 🎉 ALL TESTS PASSED! 🎉
```

### Method 2: Manual Testing with Thunder Client

#### Step 1: Start Backend (Same as Method 1)
```bash
cd backend
uvicorn main:app --reload
```

#### Step 2: Download and Open Thunder Client
- Download from: https://www.thunderclient.com/ (VS Code extension recommended)
- Or use: Postman, Insomnia, or curl

#### Step 3: Test Health Endpoint
```
GET http://127.0.0.1:8000/chat/health

Expected Response:
{
  "service": "chat",
  "status": "operational",
  "features": ["nlu", "appointment_booking", "business_logic"],
  "version": "2.0.0"
}
```

#### Step 4: Test Query
```
POST http://127.0.0.1:8000/chat/message
Content-Type: application/json

{
  "content": "What services do you offer?",
  "user_id": 1,
  "conversation_id": "manual_test_1"
}

Expected Response:
{
  "message_id": "msg_1704351600.123",
  "user_message": "What services do you offer?",
  "bot_response": "I'd be happy to help answer your question.",
  "timestamp": "2025-01-04T10:00:00.123456",
  "conversation_id": "manual_test_1",
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

#### Step 5: Test Complete Booking
```
POST http://127.0.0.1:8000/chat/message
Content-Type: application/json

{
  "content": "I'd like to book a teeth cleaning with Dr. Wang tomorrow at 2 PM",
  "user_id": 1,
  "conversation_id": "manual_test_2"
}

Expected Response:
{
  "message_id": "msg_1704351620.456",
  "user_message": "I'd like to book a teeth cleaning with Dr. Wang tomorrow at 2 PM",
  "bot_response": "✅ Great! I've booked your appointment for teeth cleaning with Dr. Wang on 2025-01-05 at 14:00.",
  "timestamp": "2025-01-04T10:00:20.456789",
  "conversation_id": "manual_test_2",
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
      "doctor": {
        "id": 1,
        "name": "Dr. Wang"
      },
      "service": {
        "id": 1,
        "name": "Teeth Cleaning"
      },
      "customer": {
        "id": 1
      },
      "booking": {
        "success": true,
        "message": "Appointment booked successfully",
        "appointment_id": 5
      }
    }
  }
}
```

#### Step 6: Verify in Database
```bash
# Check that appointment was created
sqlite3 clinic.db "SELECT * FROM appointments ORDER BY created_at DESC LIMIT 1;"

# Should show the newly created appointment with:
# - customer_id from entities
# - doctor_id matching Dr. Wang
# - appointment_date: 2025-01-05
# - appointment_time: 14:00
```

---

## 📊 Understanding Test Output

### Successful Query Response
```json
{
  "intent": "query",
  "confidence": 0.85,
  "action_result": null,
  "bot_response": "I'd be happy to help answer your question."
}
```
✅ Indicates: NLU correctly identified non-transactional request, no database changes

### Successful Booking Response
```json
{
  "intent": "appointment",
  "confidence": 0.92,
  "action_result": {
    "success": true,
    "message": "Appointment booked successfully",
    "details": {
      "booking": {"appointment_id": 5}
    }
  },
  "bot_response": "✅ Great! I've booked your appointment..."
}
```
✅ Indicates: Full end-to-end flow successful - NLU → business logic → database ✓

### Error Booking Response (Invalid Doctor)
```json
{
  "intent": "appointment",
  "confidence": 0.88,
  "action_result": {
    "success": false,
    "message": "Doctor 'Dr. Unknown' not found",
    "details": {}
  },
  "bot_response": "❌ Sorry: Doctor 'Dr. Unknown' not found"
}
```
✅ Indicates: Error handling working correctly, no database modification attempted

### Missing Information Response
```json
{
  "intent": "appointment",
  "confidence": 0.65,
  "action_result": {
    "success": false,
    "message": "Missing required information (doctor, service, date, time)",
    "details": {}
  },
  "bot_response": "❌ Sorry: Missing required information (doctor, service, date, time)"
}
```
✅ Indicates: Validation working correctly before attempting database operations

---

## 🔍 Troubleshooting

### Issue: "Connection refused on port 8000"
```
Error: ConnectionRefusedError: [Errno 111] Connection refused
```
**Solution:**
1. Ensure backend is running: `cd backend && uvicorn main:app --reload`
2. Check if port 8000 is available: `netstat -ano | findstr 8000` (Windows)
3. Wait 2-3 seconds for backend to fully start

### Issue: "Failed to connect to Ollama"
```
Error: "AI service error: Unable to connect to Ollama on localhost:11434"
```
**Solution:**
1. Start Ollama: `ollama serve` in separate terminal
2. Verify model exists: `ollama list`
3. If missing: `ollama pull llama3.2:3b`
4. Check Ollama port: http://127.0.0.1:11434 should respond

### Issue: "Doctor not found" even though doctor exists
```
Response: "Doctor 'Dr. Wang' not found"
```
**Solution:**
1. Check doctor name in database: `sqlite3 clinic.db "SELECT name FROM doctors;"`
2. Verify exact spelling matches (case-sensitive in some configurations)
3. Try different doctor name or check if database was initialized
4. Run: `python init_db.py` to re-initialize if needed

### Issue: "All tests fail with validation errors"
```
Error: "Invalid input: validation error"
```
**Solution:**
1. Verify Pydantic models are loaded: Check `backend/schemas/chat.py` exists
2. Check imports in `backend/routes/chat.py` are correct
3. Reinstall requirements: `pip install -r requirements.txt`
4. Restart backend

### Issue: "Empty appointment_id in response"
```
Response: appointment_id is null or missing
```
**Solution:**
1. Check database schema: `sqlite3 clinic.db ".schema appointments"`
2. Verify id column exists and is PRIMARY KEY
3. Check no constraints preventing inserts
4. Review appointment_service.py book_appointment() method

---

## 📈 Performance Metrics

### Expected Response Times

| Test Case | Expected Time | Notes |
|-----------|---------------|-------|
| Query | 500-1500ms | Ollama inference (LLM) takes most time |
| Booking | 800-2000ms | NLU + database operations |
| Invalid Doctor | 600-1500ms | NLU + quick database lookup |
| Missing Info | 600-1500ms | NLU + validation |
| Empty Message | <50ms | FastAPI validation (no inference) |
| Health Check | <10ms | Simple JSON response |

**Note:** First request after backend start will be slower (~3-5s) due to model loading.

---

## ✅ Success Checklist

After running all tests, verify:

- [ ] All 6 tests show ✅ PASSED
- [ ] Pass rate is 100%
- [ ] No unhandled exceptions in backend logs
- [ ] Database shows new appointment records for booking tests
- [ ] Ollama logs show successful inference
- [ ] Response times are within expected range
- [ ] action_result structure matches expected format

---

## 🎯 What Each Component Does

### 1. NLU Parsing (`LlamaService.parse_user_input`)
- Takes: Natural language user message
- Does: Sends to Llama3.2:3b via Ollama
- Returns: Structured intent + entities (JSON)
- Key feature: _clean_json() removes Llama comments

### 2. Business Logic Router (`_execute_business_logic`)
- Takes: Intent and entities from NLU
- Does: Routes to appropriate handler function
- Returns: Action result dict or None

### 3. Appointment Service (`AppointmentService`)
- Provides: Pure business logic methods
- Methods:
  - `find_doctor_by_name()`
  - `find_service_by_name()`
  - `find_or_create_customer()`
  - `book_appointment()`
  - `cancel_appointment()`
  - `modify_appointment()`
  - `is_slot_available()`

### 4. Response Generation (`_generate_response`)
- Takes: Intent + entities + action result
- Does: Generates contextual bot response
- Returns: Natural language response string

### 5. Chat Endpoint (`/chat/message`)
- Orchestrates: Steps 1-4 above
- Validates: ChatRequest Pydantic schema
- Returns: ChatResponse with full details

---

## 📝 Database Verification

After successful booking test, verify in database:

```bash
# Check new appointment
sqlite3 clinic.db "SELECT * FROM appointments WHERE id = (SELECT MAX(id) FROM appointments);"

# Check customer created
sqlite3 clinic.db "SELECT * FROM customers ORDER BY created_at DESC LIMIT 1;"

# Count total appointments
sqlite3 clinic.db "SELECT COUNT(*) FROM appointments;"

# View time slots for a doctor
sqlite3 clinic.db "SELECT * FROM time_slots WHERE doctor_id = 1;"
```

---

## 🚀 Next Steps After Successful Testing

1. **Implement Cancellation & Modification:**
   - Complete `_handle_cancellation()` in chat.py
   - Complete `_handle_modification()` in chat.py
   - Add tests for these features

2. **Add Conversation History:**
   - Implement database storage
   - Return conversation history in responses
   - Support multi-turn context

3. **Production Hardening:**
   - Add authentication/authorization
   - Implement rate limiting
   - Add request/response logging
   - Configure error tracking

4. **Deployment:**
   - Deploy backend to cloud (AWS/GCP/Azure)
   - Set up production Ollama instance
   - Configure CI/CD pipeline
   - Add monitoring and alerts

---

## 📚 Key Files Reference

| File | Purpose |
|------|---------|
| [backend/routes/chat.py](backend/routes/chat.py) | Chat API orchestration |
| [backend/services/llama_service.py](backend/services/llama_service.py) | NLU parsing |
| [backend/services/appointment_service.py](backend/services/appointment_service.py) | Business logic |
| [backend/schemas/chat.py](backend/schemas/chat.py) | Request/response validation |
| [test_e2e.py](test_e2e.py) | Automated test suite |
| [docs/E2E_TESTING_GUIDE.md](docs/E2E_TESTING_GUIDE.md) | Detailed test cases |

---

## 💡 Pro Tips

1. **Monitor Ollama in parallel:**
   ```bash
   # Terminal with Ollama to see inference happening
   ollama serve
   ```

2. **Watch backend logs:**
   ```bash
   # Backend logs show parsing steps
   cd backend && uvicorn main:app --reload --log-level debug
   ```

3. **Test with curl:**
   ```bash
   curl -X POST http://127.0.0.1:8000/chat/message \
     -H "Content-Type: application/json" \
     -d '{"content": "What services do you offer?", "user_id": 1}'
   ```

4. **Inspect database:**
   ```bash
   # Use SQLite CLI to debug
   sqlite3 clinic.db
   > .tables
   > SELECT * FROM doctors;
   > .exit
   ```

---

**Last Updated:** January 4, 2025
**System Version:** 2.0.0
**Status:** ✅ Ready for End-to-End Testing
