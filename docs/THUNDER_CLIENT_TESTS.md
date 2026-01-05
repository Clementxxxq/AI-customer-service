# Thunder Client Test Cases - Llama AI Chat

## Test 1: Appointment Booking
**Name:** Book Appointment with Dr. Wang

**Method:** POST  
**URL:** http://127.0.0.1:8000/api/chat/message

**Headers:**
```
Content-Type: application/json
```

**Body:**
```json
{
  "content": "I want to book an appointment with Dr. Wang for teeth cleaning tomorrow at 2 PM",
  "user_id": 1,
  "conversation_id": "test_conv_001"
}
```

**Expected Response (200 OK):**
```json
{
  "intent": "appointment",
  "confidence": 0.9+,
  "entities": {
    "service": "teeth cleaning",
    "doctor": "Dr. Wang",
    "date": "2026-01-06",
    "time": "14:00"
  },
  "bot_response": "I understand you want to book teeth cleaning with Dr. Wang on 2026-01-06..."
}
```

---

## Test 2: Cancel Appointment
**Name:** Cancel Appointment

**Method:** POST  
**URL:** http://127.0.0.1:8000/api/chat/message

**Body:**
```json
{
  "content": "Cancel my 10 AM appointment today",
  "user_id": 1,
  "conversation_id": "test_conv_001"
}
```

**Expected:**
- intent: "cancel"
- date: "2026-01-05" (today)
- time: "10:00"

---

## Test 3: Query Doctor Info
**Name:** Query Doctor

**Method:** POST  
**URL:** http://127.0.0.1:8000/api/chat/message

**Body:**
```json
{
  "content": "What is Dr. Li's specialization?",
  "user_id": 1
}
```

**Expected:**
- intent: "query"
- doctor: "Dr. Li"
- service and date: null

---

## Test 4: Reschedule
**Name:** Modify Appointment

**Method:** POST  
**URL:** http://127.0.0.1:8000/api/chat/message

**Body:**
```json
{
  "content": "I need to move my Thursday appointment to Friday afternoon",
  "user_id": 1
}
```

**Expected:**
- intent: "modify"
- date: Friday's date
- time: afternoon time

---

## Test 5: Complex Request
**Name:** Multiple Entities

**Method:** POST  
**URL:** http://127.0.0.1:8000/api/chat/message

**Body:**
```json
{
  "content": "Can I book with Dr. Wang for extraction next Monday at 10 AM? My phone is 555-1234 and email is test@example.com",
  "user_id": 1
}
```

**Expected:**
- intent: "appointment"
- doctor: "Dr. Wang"
- service: "extraction"
- date: next Monday
- time: "10:00"
- customer_phone: "555-1234"
- customer_email: "test@example.com"

---

## Cleanup: Delete Conversation
**Name:** Delete Conversation

**Method:** DELETE  
**URL:** http://127.0.0.1:8000/api/chat/conversations/test_conv_001

**Expected:**
```json
{
  "message": "Conversation deleted successfully"
}
```

