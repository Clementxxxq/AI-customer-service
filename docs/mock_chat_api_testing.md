# Mock Chat API Testing with Thunder Client

## Overview
This guide demonstrates how to test the Mock Chat API endpoints using Thunder Client.

**Base URL:** `http://127.0.0.1:8000/api`

---

## Endpoints

### 1. Check Chat Service Health
**Request:**
```
GET http://127.0.0.1:8000/api/chat/health
```

**Response (200 OK):**
```json
{
  "service": "chat",
  "status": "operational",
  "type": "mock",
  "version": "1.0.0"
}
```

---

### 2. Create New Conversation
**Request:**
```
POST http://127.0.0.1:8000/api/chat/conversations
```

**Response (200 OK):**
```json
{
  "conversation_id": "conv_1704368400.123456",
  "created_at": "2026-01-04T10:20:00.123456",
  "status": "active"
}
```

---

### 3. Send Chat Message
**Request:**
```
POST http://127.0.0.1:8000/api/chat/message
Content-Type: application/json

{
  "content": "What services do you offer?",
  "user_id": 1,
  "conversation_id": "conv_1704368400.123456"
}
```

**Response (200 OK):**
```json
{
  "message_id": "msg_1704368400.654321",
  "user_message": "What services do you offer?",
  "bot_response": "That's a great question! Our clinic offers comprehensive dental services including cleaning, extractions, and orthodontics.",
  "timestamp": "2026-01-04T10:21:00.654321",
  "conversation_id": "conv_1704368400.123456"
}
```

---

### 4. Get Conversation History
**Request:**
```
GET http://127.0.0.1:8000/api/chat/conversations/{conversation_id}
```

**Example:**
```
GET http://127.0.0.1:8000/api/chat/conversations/conv_1704368400.123456
```

**Response (200 OK):**
```json
{
  "conversation_id": "conv_1704368400.123456",
  "messages": [
    {
      "role": "user",
      "content": "Hello, I'd like to know more about your services",
      "timestamp": "2026-01-04T10:00:00"
    },
    {
      "role": "assistant",
      "content": "That's a great question! Our clinic offers comprehensive dental services including cleaning, extractions, and orthodontics.",
      "timestamp": "2026-01-04T10:00:05"
    },
    {
      "role": "user",
      "content": "How much does a cleaning cost?",
      "timestamp": "2026-01-04T10:01:00"
    },
    {
      "role": "assistant",
      "content": "Our cleaning service costs $200 and takes about 30 minutes. Would you like to schedule one?",
      "timestamp": "2026-01-04T10:01:05"
    }
  ]
}
```

---

### 5. Get Chat History with Limit
**Request:**
```
GET http://127.0.0.1:8000/api/chat/conversations/{conversation_id}/history?limit=5
```

**Example:**
```
GET http://127.0.0.1:8000/api/chat/conversations/conv_1704368400.123456/history?limit=5
```

**Response (200 OK):**
```json
{
  "conversation_id": "conv_1704368400.123456",
  "total_messages": 6,
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "timestamp": "2026-01-04T10:00:00"
    },
    {
      "role": "assistant",
      "content": "Hi! How can I help you today?",
      "timestamp": "2026-01-04T10:00:05"
    },
    {
      "role": "user",
      "content": "I want to book an appointment",
      "timestamp": "2026-01-04T10:01:00"
    },
    {
      "role": "assistant",
      "content": "Great! What service are you interested in?",
      "timestamp": "2026-01-04T10:01:05"
    },
    {
      "role": "user",
      "content": "Teeth cleaning",
      "timestamp": "2026-01-04T10:02:00"
    }
  ]
}
```

---

### 6. Delete Conversation
**Request:**
```
DELETE http://127.0.0.1:8000/api/chat/conversations/conv_1704368400.123456
```

**Response (200 OK):**
```json
{
  "message": "Conversation deleted successfully",
  "conversation_id": "conv_1704368400.123456",
  "deleted_at": "2026-01-04T10:22:00.123456"
}
```

---

## Testing Workflow

### Step 1: Start Backend Server
```powershell
cd backend
uvicorn main:app --reload
```

### Step 2: Create New Conversation
1. Open Thunder Client
2. Click "New Request"
3. Select **POST**
4. Enter URL: `http://127.0.0.1:8000/api/chat/conversations`
5. Click "Send"
6. Copy the `conversation_id` from response

### Step 3: Send First Message
1. Create new request in Thunder Client
2. Select **POST**
3. Enter URL: `http://127.0.0.1:8000/api/chat/message`
4. Set Headers tab → Add `Content-Type: application/json`
5. Go to Body tab → Set to JSON
6. Enter:
```json
{
  "content": "Hello, what services do you offer?",
  "user_id": 1,
  "conversation_id": "your_conversation_id_here"
}
```
7. Click "Send"

### Step 4: Send More Messages
Repeat Step 3 with different questions:

**Example Messages to Try:**
- "How much does a cleaning cost?"
- "When are you open?"
- "Who is the best doctor for orthodontics?"
- "Can I book an appointment online?"
- "Do you accept insurance?"

### Step 5: Get Conversation History
1. Create new request
2. Select **GET**
3. Enter URL: `http://127.0.0.1:8000/api/chat/conversations/{conversation_id}`
4. Replace `{conversation_id}` with your actual ID
5. Click "Send"

### Step 6: Get Limited History
1. Create new request
2. Select **GET**
3. Enter URL: `http://127.0.0.1:8000/api/chat/conversations/{conversation_id}/history?limit=3`
4. Click "Send"

### Step 7: Delete Conversation
1. Create new request
2. Select **DELETE**
3. Enter URL: `http://127.0.0.1:8000/api/chat/conversations/{conversation_id}`
4. Click "Send"

---

## Request Body Schema

### Send Message Request
```json
{
  "content": "string (required) - User message text",
  "user_id": "integer (optional) - ID of the user sending message",
  "conversation_id": "string (optional) - ID of the conversation"
}
```

---

## Response Status Codes

| Status | Meaning |
|--------|---------|
| 200 | Success |
| 400 | Bad Request (e.g., empty message) |
| 404 | Not Found |
| 500 | Server Error |

---

## Error Examples

### Empty Message Error
**Request:**
```json
{
  "content": "",
  "user_id": 1
}
```

**Response (400 Bad Request):**
```json
{
  "detail": "Message content cannot be empty"
}
```

### Invalid Limit Parameter
**Request:**
```
GET http://127.0.0.1:8000/api/chat/conversations/conv_123/history?limit=150
```

**Response (400 Bad Request):**
```json
{
  "detail": "Limit must be between 1 and 100"
}
```

---

## Mock Bot Responses

The chatbot randomly selects from these predefined responses:

1. "That's a great question! Our clinic offers comprehensive dental services including cleaning, extractions, and orthodontics."
2. "I'd recommend booking an appointment with Dr. Wang or Dr. Li. Both are highly experienced professionals."
3. "We're open Monday to Friday from 9:00 AM to 6:00 PM. What time works best for you?"
4. "Our cleaning service costs $200 and takes about 30 minutes. Would you like to schedule one?"
5. "I'm here to help! Feel free to ask about our services, doctors, or appointment availability."
6. "For urgent dental issues, please call us directly at our clinic. We can usually fit emergency cases within an hour."
7. "All our dentists are board-certified with years of experience in their respective specializations."
8. "We accept most insurance plans. I can help verify your coverage if you provide your insurance details."

---

## Tips

✅ **Use Thunder Client Collections** to organize chat endpoints:
- Create a "Chat" folder
- Save each endpoint request for quick reuse

✅ **Copy Conversation ID** from the create conversation response for subsequent requests

✅ **Check Timestamps** to verify response timing

✅ **View API Documentation** at `http://127.0.0.1:8000/docs` (Swagger UI)

---

## Next Steps

Once you're familiar with the mock API:
1. Integrate actual AI service (e.g., OpenAI API)
2. Replace mock responses with real AI responses
3. Add database storage for conversations
4. Implement authentication
5. Add conversation analytics

