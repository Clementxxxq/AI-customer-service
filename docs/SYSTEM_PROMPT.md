# System Prompt for Llama NLU Parser

This is the exact system prompt used to control Llama3.2:3b behavior.

## Core Philosophy

**One job only:** Convert natural language → JSON (intent + entities)

## The Prompt

```
You are a strict NLU (Natural Language Understanding) parser.
Your ONLY job is to convert user natural language into JSON format.

Rules (MUST FOLLOW):
- Extract user intent: appointment, query, cancel, modify, other
- Extract entities: doctor name, service name, date, time, phone, email
- ALWAYS output ONLY valid JSON
- Do NOT query databases, make decisions, or provide advice
- Set fields to null if not mentioned in user input
- Set confidence between 0.0 and 1.0
- Do NOT add any text before or after the JSON

Output JSON schema (EXACT FORMAT):
{
  "intent": "appointment|query|cancel|modify|other",
  "confidence": 0.95,
  "entities": {
    "service": "string or null",
    "doctor": "string or null",
    "date": "YYYY-MM-DD or null",
    "time": "HH:MM or null",
    "customer_name": "string or null",
    "customer_phone": "string or null",
    "customer_email": "string or null"
  }
}

CRITICAL: Output ONLY JSON, nothing else.
```

## Implementation in Python

See: `backend/services/llama_service.py`

```python
SYSTEM_PROMPT = """You are a strict NLU (Natural Language Understanding) parser.
Your ONLY job is to convert user natural language into JSON format.

Rules (MUST FOLLOW):
- Extract user intent: appointment, query, cancel, modify, other
- Extract entities: doctor name, service name, date, time, phone, email
- ALWAYS output ONLY valid JSON
- Do NOT query databases, make decisions, or provide advice
- Set fields to null if not mentioned in user input
- Set confidence between 0.0 and 1.0
- Do NOT add any text before or after the JSON

Output JSON schema (EXACT FORMAT):
{
  "intent": "appointment|query|cancel|modify|other",
  "confidence": 0.95,
  "entities": {
    "service": "string or null",
    "doctor": "string or null",
    "date": "YYYY-MM-DD or null",
    "time": "HH:MM or null",
    "customer_name": "string or null",
    "customer_phone": "string or null",
    "customer_email": "string or null"
  }
}

CRITICAL: Output ONLY JSON, nothing else."""
```

## Tested Examples

### Example 1: Appointment
**Input:**
```
I want to book an appointment with Dr. Wang for teeth cleaning tomorrow at 2 PM
```

**Output:**
```json
{
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

### Example 2: Cancellation
**Input:**
```
Cancel my 10 AM appointment today
```

**Output:**
```json
{
  "intent": "cancel",
  "confidence": 0.97,
  "entities": {
    "service": null,
    "doctor": null,
    "date": "2026-01-04",
    "time": "10:00",
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  }
}
```

### Example 3: Query
**Input:**
```
What is Dr. Li's medical license?
```

**Output:**
```json
{
  "intent": "query",
  "confidence": 0.95,
  "entities": {
    "service": null,
    "doctor": "Dr. Li",
    "date": null,
    "time": null,
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  }
}
```

### Example 4: Modification
**Input:**
```
I need to move my Thursday appointment to Friday afternoon
```

**Output:**
```json
{
  "intent": "modify",
  "confidence": 0.92,
  "entities": {
    "service": null,
    "doctor": null,
    "date": "2026-01-10",
    "time": null,
    "customer_name": null,
    "customer_phone": null,
    "customer_email": null
  }
}
```

## Key Design Decisions

### ✅ Simple, Strict Format
- Only JSON output, no exceptions
- Clear field definitions
- Type safety (string or null)

### ❌ No Free-Form Responses
- No "Let me check the database"
- No "I recommend..."
- No conversational filler
- No hallucinated information

### 🎯 Confidence Score
- 0.0 = Very uncertain
- 0.5 = Moderate confidence
- 1.0 = Very certain
- Helps frontend decide whether to proceed

### 📅 Date Normalization
- Prompt specifies YYYY-MM-DD format
- Backend normalizes "today"/"tomorrow" separately
- Allows intelligent date handling

### 🔤 Entity Extraction
- Service: What procedure/service mentioned
- Doctor: Which doctor requested
- Date: When the appointment
- Time: What time in HH:MM
- Customer info: Name, phone, email if mentioned

## Why This Works

1. **Constraints**: Strict rules prevent hallucination
2. **Format**: JSON only = easy parsing
3. **Simplicity**: Single responsibility (NLU only)
4. **Clarity**: No ambiguity in expected output
5. **Safety**: No database access, no decisions made

## Model Used

- **Model**: Llama3.2:3b (3 billion parameters)
- **Size**: 2.0 GB
- **Speed**: 2-5 seconds per request
- **Accuracy**: High confidence on clear inputs

## Prompt Engineering Principles Applied

1. **Be explicit** - Exact output format specified
2. **Use lists** - Rules in bullet points
3. **Use CAPS** - For critical instructions (MUST FOLLOW)
4. **Show examples** - In actual implementation
5. **Set constraints** - What NOT to do (❌)
6. **State roles** - "You are a strict NLU parser"

## Iterating the Prompt

To improve accuracy:

1. **Add examples** - Few-shot prompting
   ```
   Example 1:
   User: "Book with Dr. Wang tomorrow"
   Output: {"intent": "appointment", ...}
   ```

2. **Add negative examples**
   ```
   NOT allowed:
   - "I'll check the database"
   - "I recommend Dr. Wang"
   ```

3. **Clarify edge cases**
   ```
   - If time is ambiguous, set to null
   - If doctor name misspelled, extract as-is
   ```

4. **Add domain knowledge**
   ```
   Known doctors: Dr. Wang, Dr. Li, ...
   Known services: Cleaning, Extraction, ...
   ```

## Testing the Prompt

```bash
# Method 1: Direct Ollama CLI
ollama run llama3.2:3b "Your system prompt here... User: test message"

# Method 2: Python LlamaService
from services.llama_service import LlamaService
response = LlamaService.parse_user_input("test message")

# Method 3: Thunder Client API
POST http://127.0.0.1:8000/api/chat/message
{"content": "test message"}
```

## Monitoring Confidence Scores

- **0.9+**: High confidence, safe to proceed
- **0.7-0.9**: Moderate confidence, may need clarification
- **<0.7**: Low confidence, should ask user to clarify

Example logging:
```python
response = LlamaService.parse_user_input(user_input)
if response.confidence < 0.7:
    log_warning(f"Low confidence: {response.confidence}")
    suggest_clarification()
```

---

**Version**: 1.0  
**Last Updated**: 2026-01-04  
**Status**: Production Ready
