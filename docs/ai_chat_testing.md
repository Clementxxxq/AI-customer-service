# Testing Real Llama AI Chat with Thunder Client

## Overview

The Chat API now uses Llama3.2:3b for real NLU (Natural Language Understanding) parsing.

**Base URL:** `http://127.0.0.1:8000/api`

---

## How It Works

1. User sends a natural language message
2. Llama NLU parser extracts **intent** and **entities** as JSON
3. Backend generates a contextual bot response
4. Response includes parsed data for frontend integration

---

## Key Difference from Mock

### Before (Mock)
```json
{
  "message_id": "msg_xxx",
  "user_message": "...",
  "bot_response": "Random predefined response",
  "timestamp": "...",
  "conversation_id": "..."
}
```

### Now (Real AI)
```json
{
  "message_id": "msg_xxx",
  "user_message": "I want to book with Dr. Wang tomorrow at 2 PM",
  "bot_response": "I understand you want to book teeth cleaning with Dr. Wang on 2026-01-05. Let me connect you with our scheduling system.",
  "timestamp": "...",
  "conversation_id": "...",
  "intent": "appointment",
  "confidence": 0.99,
  "entities": {
    "service": "teeth cleaning",
    "doctor": "Dr. Wang",
    "date": "2026-01-05",
    "time": "14:00",
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  }
}
```

---

## Testing Steps

### 1. Start Backend with Llama
```powershell
cd backend
uvicorn main:app --reload
```

Wait for the server to start, then proceed to Thunder Client.

### 2. Create Request in Thunder Client

**URL:** `http://127.0.0.1:8000/api/chat/message`

**Method:** POST

**Headers:**
```
Content-Type: application/json
```

**Body (JSON):**
```json
{
  "content": "I want to book an appointment with Dr. Wang for teeth cleaning tomorrow at 2 PM",
  "user_id": 1,
  "conversation_id": "conv_test_001"
}
```

**Send and observe response**

---

## Test Cases

### Test 1: Appointment Request
**Request:**
```json
{
  "content": "I want to book an appointment with Dr. Wang for teeth cleaning tomorrow at 2 PM",
  "user_id": 1
}
```

**Expected Response:**
- `intent`: "appointment"
- `confidence`: high (0.95+)
- `entities.doctor`: "Dr. Wang"
- `entities.service`: "teeth cleaning"
- `entities.date`: "2026-01-05" (tomorrow)
- `entities.time`: "14:00"
- `bot_response`: Contextual response about booking

---

### Test 2: Cancellation Request
**Request:**
```json
{
  "content": "Cancel my 10 AM appointment today",
  "user_id": 2
}
```

**Expected Response:**
- `intent`: "cancel"
- `confidence`: high
- `entities.date`: "2026-01-04" (today)
- `entities.time`: "10:00"
- `bot_response`: Confirmation message about cancellation

---

### Test 3: Query (Non-Appointment)
**Request:**
```json
{
  "content": "What is Dr. Li's specialization?"
}
```

**Expected Response:**
- `intent`: "query"
- `confidence`: moderate to high
- `entities.doctor`: "Dr. Li"
- Other entities: null
- `bot_response`: Generic query response

---

### Test 4: Reschedule Request
**Request:**
```json
{
  "content": "I need to move my Thursday appointment to Friday afternoon"
}
```

**Expected Response:**
- `intent`: "modify"
- `confidence`: high
- `bot_response`: Confirmation about rescheduling

---

### Test 5: Complex Multi-Intent
**Request:**
```json
{
  "content": "Can Dr. Wang do teeth whitening? I'm free next Monday at 3 PM",
  "user_id": 1
}
```

**Expected Response:**
- `intent`: "query" or "appointment" (depends on Llama's parsing)
- Multiple entities extracted
- `bot_response`: Contextual response

---

## Response Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `message_id` | string | Unique ID for this message |
| `user_message` | string | Original user input |
| `bot_response` | string | AI-generated contextual response |
| `timestamp` | string | ISO 8601 timestamp |
| `conversation_id` | string | Conversation session ID |
| `intent` | string | Parsed intent: appointment, query, cancel, modify, other |
| `confidence` | float | 0.0-1.0 confidence score |
| `entities.service` | string/null | Extracted service name |
| `entities.doctor` | string/null | Extracted doctor name |
| `entities.date` | string/null | Extracted date (YYYY-MM-DD) |
| `entities.time` | string/null | Extracted time (HH:MM) |
| `entities.customer_name` | string/null | Customer name if mentioned |
| `entities.customer_phone` | string/null | Phone number if mentioned |
| `entities.customer_email` | string/null | Email if mentioned |

---

## Performance Notes

⏱️ **First Call:** 5-15 seconds (Llama loads into memory)
⏱️ **Subsequent Calls:** 2-5 seconds (Llama already loaded)

If taking longer, check:
1. Ollama service is running: `ollama serve`
2. Model is downloaded: `ollama list | grep llama3.2`
3. Network connectivity (if running remotely)

---

## Common Responses by Intent

### Appointment Intent
```
"I understand you want to book [SERVICE] with [DOCTOR] on [DATE]. Let me connect you with our scheduling system."
```

### Cancel Intent
```
"I see you want to cancel your appointment on [DATE] at [TIME]. I'll process the cancellation."
```

### Query Intent
```
"You're asking about [DOCTOR/SERVICE]. Let me fetch that information for you."
```

### Modify Intent
```
"I see you want to modify your appointment. Let me help you reschedule."
```

### Other Intent
```
"I understood your message. How can I assist you with our dental services?"
```

---

## Error Handling

### Empty Message
**Request:**
```json
{
  "content": ""
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Message content cannot be empty"
}
```

### Llama Service Down
**Response (503 Service Unavailable):**
```json
{
  "detail": "AI service error: Ollama request timed out"
}
```

Make sure Ollama is running:
```bash
ollama serve
```

### Invalid JSON Input
**Response (422 Unprocessable Entity):**
```json
{
  "detail": [
    {
      "loc": ["body", "field"],
      "msg": "error message",
      "type": "value_error"
    }
  ]
}
```

---

## Advanced Testing

### Test with Real Conversation
1. Create a new request
2. POST message 1
3. Copy `conversation_id` from response
4. Use same `conversation_id` for message 2
5. Verify conversation flow

**Example Flow:**
```
User: "I need to book an appointment"
Response: intent=appointment, confidence=0.9

User: "With Dr. Wang please"  
Response: intent=appointment, entities.doctor="Dr. Wang"

User: "Tomorrow at 2 PM"
Response: intent=appointment, entities.date="2026-01-05", entities.time="14:00"
```

### Test Edge Cases
- Typos: "Dr Whang" vs "Dr. Wang"
- Relative dates: "tomorrow", "next Monday", "in 3 days"
- Time variations: "2 PM", "14:00", "2 o'clock"
- Multiple services: "cleaning and extraction"
- Implicit info: "Cancel my appointment" (no time/date)

---

## Next Steps

After testing:

1. **Save requests** in Thunder Client Collections
2. **Add more test cases** for different languages/intents
3. **Monitor confidence scores** to improve prompts
4. **Integrate with frontend** to use real API
5. **Add conversation history** storage in database
6. **Implement appointment validation** against actual schedule

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Response takes >15 seconds | Ollama model not loaded. First request is slower |
| Invalid JSON in response | Llama hallinating. May need prompt refinement |
| Lowercase doctor names | Normalize in backend or improve Llama prompt |
| Missing entities | Improve entity extraction in LlamaService |
| Wrong intent classification | Refine system prompt or check confidence threshold |

