# AI Customer Service System for Dental Clinic - Implementation Steps

## Project Overview
Build an AI-powered appointment scheduling system for a dental clinic with:
- **Frontend**: Chat UI dialog box
- **Backend**: Python
- **LLM**: Llama 3.2:3b
- **Database**: SQLite (appointment calendar)
- **Knowledge Source**: Dental clinic service document

---

## Phase 1: Environment Setup

### Step 1.1: Install Required Tools
- [x] ~~Python 3.8+ (verify with `python --version`)~~
- [x] ~~pip package manager~~
- [x] ~~SQLite (usually included with Python)~~
- [x] ~~Ollama (for running Llama 3.2:3b locally)~~
  - Download from: https://ollama.ai
  - `ollama run llama3.2`

### Step 1.2: Create Project Directory Structure
```
AI-customer-service/
├── backend/
│   ├── app.py                  # Main Flask/FastAPI app
│   ├── models.py               # Database models
│   ├── config.py               # Configuration settings
│   ├── requirements.txt         # Python dependencies
│   └── utils/
│       ├── llm_handler.py       # LLM integration
│       ├── db_handler.py        # Database operations
│       └── prompt_generator.py  # Prompt generation logic
├── frontend/
│   ├── index.html              # Chat UI
│   ├── styles.css              # Styling
│   └── script.js               # Frontend logic
├── data/
│   ├── appointments.db         # SQLite database
│   └── services.txt            # Dental clinic services document
├── docs/
│   └── steps.md                # This file
└── README.md
```

### Step 1.3: Set Up Virtual Environment
```bash
cd e:\Learning\AI-customer-service\backend
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

---

## Phase 2: Database Design & Setup

### Step 2.1: Define SQLite Schema
Create `backend/models.py` with the following tables:

**Tables needed:**
1. **appointments** - Store appointment bookings
   - `id` (PRIMARY KEY)
   - `service_type` (TEXT)
   - `date` (DATE)
   - `time` (TIME)
   - `customer_name` (TEXT)
   - `customer_phone` (TEXT)
   - `status` (TEXT: 'confirmed', 'pending', 'cancelled')
   - `created_at` (TIMESTAMP)

2. **services** - Available dental services
   - `id` (PRIMARY KEY)
   - `name` (TEXT)
   - `description` (TEXT)
   - `duration_minutes` (INTEGER)
   - `price` (REAL)

3. **time_slots** - Available time slots per day
   - `id` (PRIMARY KEY)
   - `date` (DATE)
   - `time` (TIME)
   - `is_available` (BOOLEAN)

### Step 2.2: Initialize Database
- [ ] Create `backend/db_handler.py` with SQLite connection logic
- [ ] Implement functions:
  - `initialize_db()` - Create tables if not exist
  - `add_appointment()`
  - `get_available_slots(date)`
  - `get_services()`
  - `check_slot_availability(date, time)`

---

## Phase 3: Dental Clinic Service Document

### Step 3.1: Create Service Document
Create `data/services.txt` with format:

```
DENTAL CLINIC SERVICES
======================

1. Tooth Extraction
   - Description: Professional tooth extraction for damaged or diseased teeth
   - Duration: 30 minutes
   - Price: $200

2. Cleaning & Scaling
   - Description: Professional teeth cleaning and tartar removal
   - Duration: 45 minutes
   - Price: $150

3. Dental Checkup
   - Description: Comprehensive oral examination and diagnosis
   - Duration: 30 minutes
   - Price: $100

4. Cavity Filling
   - Description: Restoration of cavities with composite filling
   - Duration: 30 minutes
   - Price: $180

5. Root Canal Treatment
   - Description: Endodontic treatment for infected or damaged tooth
   - Duration: 60 minutes
   - Price: $500

6. Teeth Whitening
   - Description: Professional teeth whitening treatment
   - Duration: 60 minutes
   - Price: $300

[Add more services as needed]
```

### Step 3.2: Load Service Document into LLM Context
- [ ] Create `backend/utils/prompt_generator.py`
- [ ] Function to read services document
- [ ] Embed services info in system prompt for LLM

---

## Phase 4: LLM Integration with Ollama

### Step 4.1: Install & Run Ollama
- [ ] Start Ollama locally: `ollama serve`
- [ ] Pull Llama model: `ollama pull llama2:3b`
- [ ] Verify API endpoint: `http://localhost:11434`

### Step 4.2: Create LLM Handler
Create `backend/utils/llm_handler.py`:
- [ ] Function to connect to Ollama API
- [ ] System prompt that includes:
  - Dental clinic services
  - Appointment scheduling rules
  - Response guidelines
- [ ] Function to send messages to LLM
- [ ] Function to parse LLM responses for:
  - Intent detection (book appointment, check availability, ask info, etc.)
  - Extracted parameters (service type, date, time, customer info)

**Sample System Prompt Structure:**
```
You are a helpful AI assistant for [Clinic Name] dental clinic.
Your role is to help customers schedule appointments for dental services.

Available services:
[Services from document]

Rules:
1. Only offer services listed above. For unlisted services, respond: "I'm sorry, we don't offer that service."
2. Confirm appointment details before booking
3. Be friendly and professional
4. Ask for customer name and phone number

When booking, extract:
- Service type
- Preferred date
- Preferred time
- Customer name
- Customer phone
```

---

## Phase 5: Backend API Development

### Step 5.1: Set Up Flask or FastAPI
Create `backend/app.py`:
- [ ] Install dependencies: `pip install flask flask-cors` or `pip install fastapi uvicorn`
- [ ] Create API endpoints:

**Required Endpoints:**
1. `POST /api/chat` - Send message and get LLM response
   - Input: `{ "message": "user message" }`
   - Output: `{ "response": "AI response", "intent": "...", "appointment_data": {...} }`

2. `POST /api/book-appointment` - Confirm and save appointment
   - Input: `{ "service": "...", "date": "...", "time": "...", "name": "...", "phone": "..." }`
   - Output: `{ "success": true, "booking_id": "..." }`

3. `GET /api/available-slots` - Get available time slots
   - Query: `?date=YYYY-MM-DD`
   - Output: `{ "slots": ["09:00", "10:30", "14:00", ...] }`

4. `GET /api/services` - Get list of available services
   - Output: `{ "services": [...] }`

### Step 5.2: Implement Conversation Flow Logic
- [ ] Track conversation context
- [ ] Implement state machine for appointment booking process
- [ ] Handle conversation turns and clarifications

### Step 5.3: Error Handling
- [ ] Invalid service requests → "not offered" response
- [ ] Unavailable time slots → suggest alternatives
- [ ] Missing customer info → request information

---

## Phase 6: Frontend Development

### Step 6.1: Create HTML Chat UI
Create `frontend/index.html`:
- [ ] Chat container with message display area
- [ ] Input field for user messages
- [ ] Send button
- [ ] Message styling (different for user vs AI)
- [ ] Timestamp for messages

### Step 6.2: Add Styling
Create `frontend/styles.css`:
- [ ] Chat bubble styling
- [ ] Responsive design
- [ ] Input field styling
- [ ] Color scheme for user (blue) and AI (green) messages

### Step 6.3: Implement Frontend Logic
Create `frontend/script.js`:
- [ ] Connect to backend API
- [ ] Handle message sending
- [ ] Display messages in chat
- [ ] Handle API responses
- [ ] Auto-scroll to latest message
- [ ] Show loading indicator while waiting for LLM response

**Key Functions:**
```javascript
- sendMessage(userInput)
- displayMessage(text, sender)
- fetchAIResponse(message)
- updateChatUI()
```

---

## Phase 7: Integration & Testing

### Step 7.1: End-to-End Testing
- [ ] Test complete appointment booking flow
- [ ] Test service availability inquiries
- [ ] Test invalid service requests (should show "not offered")
- [ ] Test time slot conflicts
- [ ] Test customer info collection

### Step 7.2: Error Cases Testing
- [ ] User asks for unlisted service
- [ ] No available slots on requested date
- [ ] Incomplete customer information
- [ ] Malformed requests

### Step 7.3: Performance Testing
- [ ] Response time for LLM
- [ ] Database query performance
- [ ] UI responsiveness

---

## Phase 8: Deployment Considerations

### Step 8.1: Configuration
- [ ] Create `backend/config.py` for:
  - Database path
  - Ollama API endpoint
  - Flask/FastAPI settings
  - CORS settings

### Step 8.2: Logging
- [ ] Add logging for:
  - API requests
  - Database operations
  - LLM responses
  - Errors

### Step 8.3: Documentation
- [ ] API documentation (Swagger/OpenAPI)
- [ ] Setup instructions in README.md
- [ ] User guide for dental clinic staff

---

## Quick Start Commands

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start Ollama (in separate terminal)
ollama serve

# 3. Run backend server
python app.py

# 4. Open frontend
# Open frontend/index.html in browser
```

---

## Technology Stack Summary

| Component | Technology |
|-----------|-----------|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python (Flask/FastAPI) |
| Database | SQLite |
| LLM | Llama 3.2:3b via Ollama |
| API Communication | RESTful HTTP |

---

## Notes
- Ensure Ollama is running before starting the backend
- SQLite database file will be auto-created in `data/` folder
- Services document should be easily updatable for clinic staff
- System prompt should be regularly updated to match clinic policies
