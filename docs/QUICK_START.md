# Quick Start - Llama AI Chat API

## Prerequisites
- Ollama installed and running: `ollama serve`
- Python 3.10+ with dependencies installed
- Backend running: `uvicorn main:app --reload`

## In 30 Seconds

### 1. Ollama Running?
```powershell
ollama serve
```

### 2. Start Backend
```powershell
cd backend
uvicorn main:app --reload
```

### 3. Open Thunder Client & Test

**Method:** POST  
**URL:** `http://127.0.0.1:8000/api/chat/message`

**Body:**
```json
{
  "content": "I want to book with Dr. Wang tomorrow at 2 PM",
  "user_id": 1
}
```

**Expected Response:**
```json
{
  "intent": "appointment",
  "confidence": 0.99,
  "entities": {
    "doctor": "Dr. Wang",
    "date": "2026-01-05",
    "time": "14:00"
  },
  "bot_response": "I understand you want to book with Dr. Wang on 2026-01-05. Let me connect you...",
  ...
}
```

## What It Does

| Step | What Happens |
|------|--------------|
| 1. User sends message | "I want to book with Dr. Wang tomorrow at 2 PM" |
| 2. Llama parses NLU | Extracts intent=appointment, entities={doctor, date, time} |
| 3. Backend processes | Generates contextual response |
| 4. Returns full response | intent, confidence, entities, bot_response |

## Key Features

✅ **Only Extracts** Intent + Entities  
✅ **No Database** Access  
✅ **No Business** Logic  
✅ **No** Hallucination  
✅ **Always** Valid JSON  

## Intents Recognized

- `appointment` - Book an appointment
- `cancel` - Cancel an appointment  
- `modify` - Reschedule appointment
- `query` - Ask questions (non-appointment)
- `other` - Unknown/small talk

## Test Cases

```
1. "Book with Dr. Wang tomorrow at 2 PM" 
   → intent: appointment

2. "Cancel my 10 AM appointment today"
   → intent: cancel

3. "What is Dr. Li's specialization?"
   → intent: query

4. "Move my Thursday appointment to Friday"
   → intent: modify
```

## Entities Extracted

```json
{
  "service": "teeth cleaning",
  "doctor": "Dr. Wang", 
  "date": "2026-01-05",
  "time": "14:00",
  "customer_name": null,
  "customer_phone": null,
  "customer_email": null
}
```

## Performance

- First call: 5-15 seconds (model loading)
- Subsequent: 2-5 seconds
- Average: ~3 seconds

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Service error 503 | Ollama not running. Run `ollama serve` |
| Timeout | First call slow. Wait 10 seconds |
| Empty entities | Try more specific prompt |
| Low confidence | Normal for ambiguous input |

## File Structure

```
backend/
├── services/
│   ├── llama_service.py      # NLU Parser
│   └── __init__.py
├── routes/
│   └── chat.py               # Chat API (real AI)
└── main.py
```

## API Endpoint

```
POST /api/chat/message

Request:
{
  "content": "string",           # Required
  "user_id": int,               # Optional
  "conversation_id": string     # Optional
}

Response:
{
  "message_id": "string",
  "user_message": "string",
  "bot_response": "string",
  "timestamp": "string",
  "conversation_id": "string",
  "intent": "string",
  "confidence": float,
  "entities": {
    "service": string,
    "doctor": string,
    "date": string,
    "time": string,
    "customer_name": string,
    "customer_phone": string,
    "customer_email": string
  }
}
```

## Documentation

📖 [Full Implementation Summary](IMPLEMENTATION_SUMMARY.md)  
📖 [AI Chat Testing Guide](ai_chat_testing.md)  
📖 [Thunder Client Guide](thunder_client_guide.md)

## Next Steps

1. Integration with frontend
2. Save conversations to database
3. Add appointment validation
4. Multi-language support

---

**Status:** ✅ Ready to test
