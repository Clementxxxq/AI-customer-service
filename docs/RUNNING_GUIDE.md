# 🚀 Quick Running Guide - AI Customer Service System

**Status**: ✅ Production Ready | 100% Tests Passing

---

## Quick Start (5 Minutes)

### Step 1: Open 3 Terminal Windows

You need **3 separate terminals** to run the system:

#### Terminal 1: Start Ollama (AI Model Server)
```powershell
# Run this once to start the AI model server
ollama serve
```
✅ You should see: `Listening on 127.0.0.1:11434`

#### Terminal 2: Start FastAPI Backend
```powershell
# Navigate to backend folder
cd e:\Learning\AI-customer-service\backend

# Start the server
uvicorn main:app --reload
```
✅ You should see: `Uvicorn running on http://127.0.0.1:8000`

#### Terminal 3: Run Tests
```powershell
# Run from project root directory
cd e:\Learning\AI-customer-service

# Run tests with virtual environment Python
.env\Scripts\python.exe test_e2e.py
```

✅ **Expected Output**:
```
🎉 ALL TESTS PASSED! 🎉
Total Tests:    6
Passed:         6
Failed:         0
Pass Rate:      100.0%
System is ready for production deployment
```

---

## Full Setup from Scratch

If this is your first time running the system:

### Step 1: Install Dependencies
```powershell
cd e:\Learning\AI-customer-service

# Activate virtual environment
.env\Scripts\activate

# Install Python packages (only once)
pip install -r requirements.txt
```

### Step 2: Initialize Database
```powershell
# Run once to set up database with sample data
python init_db.py
```

### Step 3: Download AI Model (One-Time)
```powershell
# This downloads Llama 3.2:3b model (~3GB)
# Only needed on first run
ollama pull llama3.2:3b
```

### Step 4: Follow "Quick Start" Above

---

## Stopping Services

**Press `Ctrl+C`** in each terminal to stop:
- Terminal 1 (Ollama): `Ctrl+C`
- Terminal 2 (Backend): `Ctrl+C`  
- Terminal 3 (Tests): Already done after tests complete

---

## What Each Test Does

| Test | Purpose | Status |
|------|---------|--------|
| Test 1 | Query for information | ✅ Passing |
| Test 2 | Complete appointment booking | ✅ Passing |
| Test 3 | Handle invalid doctor error | ✅ Passing |
| Test 4 | Handle missing information | ✅ Passing |
| Test 5 | Validate empty messages | ✅ Passing |
| Test 6 | Health check endpoint | ✅ Passing |

---

## Manual API Testing

Once backend is running at `http://127.0.0.1:8000`, you can test manually:

### Test 1: Send Chat Message
```bash
curl -X POST http://127.0.0.1:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I want to book a cleaning with Dr. Wang",
    "user_id": 1,
    "conversation_id": "test_1"
  }'
```

### Test 2: Health Check
```bash
curl http://127.0.0.1:8000/api/chat/health
```

### Test 3: List Services
```bash
curl http://127.0.0.1:8000/api/services
```

### Test 4: Interactive Docs
Open in browser: `http://127.0.0.1:8000/docs`

---

## Troubleshooting

### ❌ "ModuleNotFoundError: requests"
**Cause**: Using wrong Python
**Fix**: Use virtual environment Python:
```powershell
.env\Scripts\python.exe test_e2e.py
```

### ❌ "Backend not responding (400 error)"
**Cause**: Backend not running
**Fix**: Start backend in Terminal 2:
```powershell
cd backend
uvicorn main:app --reload
```

### ❌ "Ollama connection refused"
**Cause**: Ollama server not running
**Fix**: Start Ollama in Terminal 1:
```powershell
ollama serve
```

### ❌ "database is locked"
**Cause**: Multiple processes accessing database
**Fix**: 
```powershell
# Close all terminals
# Delete clinic.db
# Restart services
python init_db.py
```

### ❌ "Llama model not found"
**Cause**: Model not downloaded
**Fix**: Download model (one-time):
```powershell
ollama pull llama3.2:3b
```

---

## Performance Tips

- **First run**: Llama model takes ~10-15 seconds to load
- **Subsequent runs**: Model loads in ~2-3 seconds (cached)
- **Tests**: Should complete in ~10-15 seconds
- **Database**: SQLite works well for 1000+ appointments

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 4GB | 8GB+ |
| **Disk** | 4GB (AI model) | 10GB+ |
| **Python** | 3.9+ | 3.10+ |
| **CPU** | Dual-core | Quad-core+ |

---

## File Organization

```
Key Files:
- test_e2e.py              ← Run this to test everything
- backend/main.py          ← FastAPI application
- clinic.db                ← Database (auto-created)
- init_db.py               ← Initialize database
- requirements.txt         ← Python dependencies
```

---

## Common Commands Cheat Sheet

```powershell
# Activate virtual environment
.env\Scripts\activate

# Run tests
.env\Scripts\python.exe test_e2e.py

# Start backend
cd backend && uvicorn main:app --reload

# Start Ollama
ollama serve

# Initialize database
python init_db.py

# Check database tables
sqlite3 clinic.db ".tables"

# View API docs
# Open browser: http://127.0.0.1:8000/docs
```

---

## Success Indicators

✅ Ollama server: `Listening on 127.0.0.1:11434`
✅ Backend server: `Uvicorn running on http://127.0.0.1:8000`  
✅ Tests: `🎉 ALL TESTS PASSED! 🎉`

---

## Next Steps

After everything is running:

1. **Explore API**: Visit `http://127.0.0.1:8000/docs` for interactive API documentation
2. **Try different queries**: 
   - "Book an appointment"
   - "What services do you offer?"
   - "I want to see Dr. Wang"
3. **Check database**: Query `clinic.db` to see created appointments
4. **Review code**: Check `backend/services/` for business logic

---

## Support

- 📖 Full documentation: [README.md](README.md)
- 🧪 Test details: [docs/steps.md](docs/steps.md)
- 🐛 Issues: Check terminal output for error messages
- 💾 Database: Check `clinic.db` with SQLite viewer

---

**Last Updated**: 2026-01-06  
**System Status**: ✅ Production Ready
