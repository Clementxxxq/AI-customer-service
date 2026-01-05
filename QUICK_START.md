# 🚀 Quick Start Guide - AI Customer Service System

## TL;DR - Run Tests in 3 Steps

```bash
# Step 1: Start Backend (Terminal 1)
cd backend && uvicorn main:app --reload

# Step 2: Start Ollama (Terminal 2)
ollama serve

# Step 3: Run Tests (Terminal 3)
python test_e2e.py
```

Expected output: **✅ ALL TESTS PASSED! 100% Pass Rate**

---

## What Was Built

A complete AI customer service chatbot with **4-step architecture**:

```
User Message (Natural Language)
       ↓
[Step 1] NLU: Parse intent + extract entities (Llama3.2:3b)
       ↓
[Step 2] Business Logic: Execute appointment operations
       ↓
[Step 3] Database: Store appointment in clinic.db
       ↓
[Step 4] Response: Return confirmation + action details
```

---

## Prerequisites

### 1. Python Environment (One-time)
```bash
# Navigate to project
cd e:\Learning\AI-customer-service

# Create virtual environment (if needed)
python -m venv venv

# Activate
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Ollama (One-time)
```bash
# Download from: https://ollama.ai

# After installation, pull the model
ollama pull llama3.2:3b

# This takes ~2 GB space, one-time download
```

### 3. Database (One-time)
```bash
# Initialize database with sample data
python init_db.py

# Verify success:
# "clinic.db created with sample data successfully!"
```

---

## Running the Tests

### Setup (Each Test Session)

**Terminal 1 - Start Backend:**
```bash
cd backend
uvicorn main:app --reload

# Should show:
# INFO:     Uvicorn running on http://127.0.0.1:8000
# INFO:     Application startup complete
```

**Terminal 2 - Start Ollama (keep running):**
```bash
ollama serve

# Should show:
# time=... level=INFO msg="Llama Server is listening on [::]:11434"
```

**Terminal 3 - Run Tests:**
```bash
python test_e2e.py

# Watch as tests execute:
# ✅ PASSED | Test 1: Simple Query
# ✅ PASSED | Test 2: Complete Booking
# ✅ PASSED | Test 3: Invalid Doctor Error Handling
# ✅ PASSED | Test 4: Missing Information Error
# ✅ PASSED | Test 5: Empty Message Validation
# ✅ PASSED | Test 6: Health Check
#
# 🎉 ALL TESTS PASSED! 🎉
```

---

## Test Cases Explained

### Test 1: Query Handling
- **Request:** "What dental services do you offer?"
- **Result:** intent=query, action_result=null (no booking)
- **Validates:** NLU correctly identifies queries

### Test 2: Complete Booking
- **Request:** "Book cleaning with Dr. Wang tomorrow at 2 PM"
- **Result:** Appointment created in database, appointment_id returned
- **Validates:** Full end-to-end flow works

### Test 3: Error Handling
- **Request:** "Book with Dr. NonExistent"
- **Result:** action_result.success=false, clear error message
- **Validates:** Graceful error handling

### Test 4: Validation
- **Request:** "Book an appointment" (missing details)
- **Result:** Error about missing information
- **Validates:** Input validation works

### Test 5: Input Validation
- **Request:** Empty message ""
- **Result:** HTTP 400 with "cannot be empty" error
- **Validates:** API-level validation

### Test 6: Health Check
- **Request:** GET /chat/health
- **Result:** {"status": "operational", "version": "2.0.0", ...}
- **Validates:** Service is running and reports capabilities

---

## What Each Test Verifies

| Test | What It Checks |
|------|-----------------|
| 1. Query | NLU parsing works for non-booking requests |
| 2. Booking | Complete end-to-end flow: NLU → Business Logic → DB |
| 3. Error | Invalid doctor is caught and reported |
| 4. Validation | Missing fields are rejected before DB |
| 5. Input | Empty input is rejected by FastAPI |
| 6. Health | Backend is responsive and features are enabled |

---

## Expected Test Times

- **Test 1 (Query):** 500-1500ms (Ollama inference)
- **Test 2 (Booking):** 800-2000ms (NLU + database)
- **Test 3-4 (Error cases):** 600-1500ms (similar to booking)
- **Test 5 (Empty):** <50ms (no inference)
- **Test 6 (Health):** <10ms (simple JSON)

**Total Suite Time:** ~5-10 seconds

---

## Verify Success

After tests pass, verify database was updated:

```bash
# Check appointments were created
sqlite3 clinic.db "SELECT COUNT(*) FROM appointments;"

# Should show: 3 or more (tests created appointments)

# View the appointments
sqlite3 clinic.db "SELECT * FROM appointments ORDER BY created_at DESC LIMIT 3;"

# Should show booking details with dates/times from tests
```

---

## Troubleshooting

### Backend Won't Start
```bash
Error: Connection refused
```
**Fix:**
```bash
# Make sure you're in backend directory
cd backend
uvicorn main:app --reload
```

### Ollama Connection Error
```bash
Error: Unable to connect to Ollama
```
**Fix:**
```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Test Ollama is running
curl http://127.0.0.1:11434/api/tags
```

### Tests Fail with "Doctor not found"
```bash
Error: Doctor 'Dr. Wang' not found
```
**Fix:**
```bash
# Reinitialize database
python init_db.py

# Verify doctor exists
sqlite3 clinic.db "SELECT * FROM doctors WHERE name LIKE '%Wang%';"
```

### First Test Takes Too Long
```bash
Test taking 30+ seconds
```
**Fix:** This is normal on first run (Ollama is loading model). Subsequent tests are faster.

---

## Manual Testing with Thunder Client

### Option: Test with GUI instead of CLI

**Import this into Thunder Client:**

```json
{
  "clientName": "AI Customer Service",
  "dateExported": "2025-01-04",
  "version": "1.1",
  "folders": [],
  "requests": [
    {
      "name": "Health Check",
      "method": "GET",
      "url": "http://127.0.0.1:8000/chat/health",
      "tests": "if (response.status === 200) { tests['✅ Health'] = true; }"
    },
    {
      "name": "Query",
      "method": "POST",
      "url": "http://127.0.0.1:8000/chat/message",
      "body": {
        "content": "What services do you offer?",
        "user_id": 1,
        "conversation_id": "test_1"
      }
    },
    {
      "name": "Book Appointment",
      "method": "POST",
      "url": "http://127.0.0.1:8000/chat/message",
      "body": {
        "content": "I'd like to book a cleaning with Dr. Wang tomorrow at 2 PM",
        "user_id": 1,
        "conversation_id": "test_2"
      }
    }
  ]
}
```

---

## System Architecture

The system has 4 layers:

```
┌─────────────────────┐
│  FastAPI Routes     │  ← Receives requests, validates, orchestrates
├─────────────────────┤
│  NLU Service        │  ← Parses natural language using Llama
│  (LlamaService)     │
├─────────────────────┤
│  Business Logic     │  ← Performs operations (books, cancels, modifies)
│  (AppointmentSvc)   │
├─────────────────────┤
│  SQLite Database    │  ← Stores all data persistently
│  (clinic.db)        │
└─────────────────────┘
```

Each layer is independent and can be tested separately.

---

## Key Files

| File | Purpose |
|------|---------|
| `backend/routes/chat.py` | Orchestrates the 4-step flow |
| `backend/services/llama_service.py` | NLU parsing with Ollama |
| `backend/services/appointment_service.py` | Business logic (8 methods) |
| `backend/schemas/chat.py` | Pydantic models for validation |
| `test_e2e.py` | Automated test suite |
| `clinic.db` | SQLite database with sample data |

---

## Next Steps After Tests Pass

1. **Try more bookings manually:**
   - Use Thunder Client
   - Try different doctors/services/dates
   - Watch database update in real-time

2. **Check logs:**
   - Monitor backend terminal for parsing
   - Watch Ollama terminal for inference
   - Verify no errors occur

3. **Explore responses:**
   - Notice how bot responses are contextual
   - See how errors are handled gracefully
   - Check appointment_id is always returned for bookings

4. **Extend functionality:**
   - Implement cancellation handling
   - Implement modification handling
   - Add conversation history

---

## Production Deployment

When ready for production:

1. **Environment Setup:**
   ```bash
   # Create .env file
   DATABASE_URL=postgresql://...
   OLLAMA_URL=http://ollama-server:11434
   ```

2. **Deployment:**
   ```bash
   # Use Gunicorn for production
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.main:app
   ```

3. **Monitoring:**
   - Set up logging to centralized service
   - Monitor Ollama inference times
   - Alert on database errors

---

## Support

If tests fail, check:
1. ✅ Backend is running on port 8000
2. ✅ Ollama is running on port 11434
3. ✅ Database is initialized (clinic.db exists)
4. ✅ All Python dependencies installed
5. ✅ Llama model downloaded locally

---

**Status:** ✅ System Complete - Ready to Test
**Last Updated:** January 4, 2025
**System Version:** 2.0.0
