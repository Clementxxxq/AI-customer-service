# 🎯 Multi-Turn Dialogue with Context Memory

**New Feature**: The AI system can now remember conversation context and ask follow-up questions to collect required information step-by-step.

---

## 🌟 What's New

The system now implements a **dialogue state management system** that allows for multi-turn conversations where the AI:
- ✅ Remembers previously collected information
- ✅ Asks targeted follow-up questions
- ✅ Collects missing information step-by-step
- ✅ Executes booking only when all info is available

---

## 📊 Example Dialogue Flow

### User: "I want to book an appointment"
**AI**: "Which doctor would you like to see?"
- Collected: intent=appointment

### User: "Dr. Wang"
**AI**: "What service do you need?"
- Collected: doctor=Dr. Wang

### User: "Cleaning"
**AI**: "What date would you like?"
- Collected: service=Cleaning

### User: "Tomorrow"
**AI**: "What time works for you?"
- Collected: date=2026-01-07

### User: "2 PM"
**AI**: "✅ Your appointment is booked for cleaning with Dr. Wang on 2026-01-07 at 14:00!"
- Collected: time=14:00
- **Booking executed!**

---

## 🔧 Technical Implementation

### 1. Dialogue State Structure
Each conversation maintains state with:
- **conversation_id**: Unique identifier for the conversation
- **intent**: What the user wants (e.g., "appointment")
- **collected_entities**: Dictionary of collected information (doctor, service, date, time)
- **current_question**: The next question to ask
- **message_count**: How many messages in this conversation

### 2. Key Components

#### `dialogue_service.py` (New)
```python
DialogueState              # Represents conversation state
get_or_create_dialogue_state()  # Get/create state for conversation
merge_entities_with_state()     # Combine new + old entity info
determine_next_question()       # Decide what to ask next
is_appointment_ready()          # Check if ready to book
```

#### `routes/chat.py` (Updated)
```python
# Now includes:
1. Get dialogue state from conversation_id
2. Parse user message with NLU
3. Merge new entities with previous state
4. Determine if we need more info or can execute
5. Ask next question OR execute booking
6. Save updated dialogue state
```

### 3. Flow Diagram
```
User Message (with conversation_id)
    ↓
Load Dialogue State (remember context)
    ↓
Parse with NLU (extract intent/entities)
    ↓
Merge with Dialogue State (keep previous info)
    ↓
Check: Do we have all required info?
    ├─ NO → Ask next question (skip business logic)
    └─ YES → Execute booking + save clean state
    ↓
Return Response (question or booking confirmation)
```

---

## 🧪 Testing the Dialogue System

### Using the Test Script

```bash
# Make sure services are running:
# Terminal 1: ollama serve
# Terminal 2: cd backend && uvicorn main:app --reload

# Terminal 3: Run the dialogue test
.env\Scripts\python.exe test_dialogue_flow.py
```

This will simulate a complete multi-turn conversation with context memory.

### Manual Testing with curl

```bash
# Turn 1: Start booking
curl -X POST http://127.0.0.1:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I want to book an appointment",
    "conversation_id": "conv_1",
    "user_id": 1
  }'

# Expected AI response: "Which doctor would you like to see?"

# Turn 2: Provide doctor
curl -X POST http://127.0.0.1:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Dr. Wang",
    "conversation_id": "conv_1",
    "user_id": 1
  }'

# Expected AI response: "What service do you need?"

# ... continue with service, date, time ...
```

**Key**: Use the **same conversation_id** to maintain dialogue state!

---

## 🎯 Required Information

For appointment booking, the system needs:
1. **Doctor** - Which doctor?
2. **Service** - What procedure?
3. **Date** - What date?
4. **Time** - What time?

The AI will ask for each field one at a time until all are provided.

---

## 💾 Dialogue State Storage

Currently using **in-memory dictionary**:
```python
DIALOGUE_STATES = {}  # keyed by conversation_id
```

For production, this should be replaced with:
- Redis (distributed, high-performance)
- PostgreSQL (persistent)
- MongoDB (flexible schema)

---

## 🔄 State Lifecycle

1. **Create**: New conversation_id → creates empty state
2. **Collect**: Each message → merges new entities, determines next question
3. **Execute**: All info collected → executes booking
4. **Reset**: After booking → clears state for next booking

---

## 🚀 New Response Format

The bot_response now varies:

**While collecting info:**
```json
{
  "bot_response": "Which doctor would you like to see?",
  "action_result": null
}
```

**When ready to book:**
```json
{
  "bot_response": "✅ Your appointment is booked for cleaning with Dr. Wang on 2026-01-07 at 14:00!",
  "action_result": {
    "success": true,
    "appointment_id": 5,
    "appointment_date": "2026-01-07",
    "appointment_time": "14:00"
  }
}
```

---

## 📝 Example Dialogue State Evolution

### Turn 1: User says "Book an appointment"
```python
state = {
  "intent": "appointment",
  "collected_entities": {},
  "current_question": "Which doctor would you like to see?"
}
```

### Turn 2: User says "Dr. Wang"
```python
state = {
  "intent": "appointment",
  "collected_entities": {"doctor": "Dr. Wang"},
  "current_question": "What service do you need?"
}
```

### Turn 3: User says "Cleaning"
```python
state = {
  "intent": "appointment",
  "collected_entities": {"doctor": "Dr. Wang", "service": "Cleaning"},
  "current_question": "What date would you like?"
}
```

### Turn 4: User says "Tomorrow"
```python
state = {
  "intent": "appointment",
  "collected_entities": {"doctor": "Dr. Wang", "service": "Cleaning", "date": "2026-01-07"},
  "current_question": "What time works for you?"
}
```

### Turn 5: User says "2 PM"
```python
state = {
  "intent": "appointment",
  "collected_entities": {"doctor": "Dr. Wang", "service": "Cleaning", "date": "2026-01-07", "time": "14:00"},
  "current_question": null  # Ready to book!
  # After booking: state gets reset to {}
}
```

---

## ✨ Key Benefits

- ✅ **Natural Conversation**: AI asks questions naturally
- ✅ **Context Memory**: Previous info is remembered
- ✅ **Error Recovery**: Missing info collected incrementally
- ✅ **User Friendly**: No need to provide everything at once
- ✅ **Scalable**: Works with any number of required fields

---

## 🔌 API Endpoints

### Existing Endpoint (Updated)
```
POST /api/chat/message
```

**New behavior**:
- Same endpoint
- Must provide `conversation_id` to maintain dialogue state
- AI response changes based on dialogue state
- Can be called multiple times with same conversation_id

### Health Check
```
GET /api/chat/health
```

---

## 🛠️ How to Extend

To add more questions to collect:

1. **Edit dialogue_service.py**:
   ```python
   def determine_next_question(intent: str, collected_entities: Dict[str, Any]) -> Optional[str]:
       if intent != "appointment":
           return None
       
       required = ["doctor", "service", "date", "time"]  # Add more fields
       
       for field in required:
           if not collected_entities.get(field):
               questions = {
                   "doctor": "Which doctor?",
                   "service": "What service?",
                   # Add more questions here
               }
               return questions.get(field)
       
       return None
   ```

2. **Update appointment_service.py** to handle new fields if needed

3. **Test with test_dialogue_flow.py**

---

## 📚 Files Modified/Created

### Created
- `backend/services/dialogue_service.py` - Dialogue state management
- `test_dialogue_flow.py` - Multi-turn test script

### Modified
- `backend/routes/chat.py` - Added dialogue state handling
- `backend/schemas/chat.py` - Updated to accept dict or AIEntity

### Unchanged
- `backend/services/llama_service.py` - NLU parsing (still works same)
- `backend/services/appointment_service.py` - Business logic (still works same)
- `test_e2e.py` - Original tests still pass

---

## ✅ Backwards Compatibility

✅ Old single-message requests still work:
```bash
curl -X POST http://127.0.0.1:8000/api/chat/message \
  -d '{"content": "Book cleaning with Dr. Wang tomorrow at 2 PM"}'
```

This will:
1. Parse all info in one message
2. Book immediately
3. No follow-up questions needed

The dialogue state is **optional** - works with or without conversation_id.

---

## 🎓 Testing Scenarios

### Scenario 1: Multi-turn Dialogue
- Sends messages one at a time
- AI asks for missing info
- State persists across messages
- Booking happens on final message

### Scenario 2: Single Message Booking
- All info in one message
- No follow-up questions
- Booking happens immediately

### Scenario 3: Mixed Information
- Some info provided initially
- Some provided in follow-ups
- State merges both
- AI asks only for missing fields

---

## 📊 Architecture Overview

```
Request with conversation_id
    ↓
DialogueService.get_or_create_dialogue_state()
    ↓
Dialogue State Lookup (or create new)
    ↓
LlamaService.parse_user_input()
    ↓
DialogueService.merge_entities_with_state()
    ↓
DialogueService.determine_next_question()
    ├─ Questions to ask? → Send question, NO booking
    └─ All info ready? → Execute booking
    ↓
DialogueService.save_dialogue_state()
    ↓
Return Response (question or confirmation)
```

---

## 🚀 Next Steps

1. ✅ Test multi-turn dialogue with `test_dialogue_flow.py`
2. ✅ Verify existing tests still pass
3. ⏳ Deploy and monitor
4. ⏳ Consider persistent storage for production

---

**Feature Status**: ✅ Ready for Testing

**Test Command**:
```bash
.env\Scripts\python.exe test_dialogue_flow.py
```

Enjoy the new multi-turn dialogue system! 🎉
