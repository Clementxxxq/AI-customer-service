# Dialogue State Machine Improvement - Quick Reference

## Problem

System keeps asking "How can I assist?" instead of remembering the conversation stage.

## Solution

Added **DialogueStage** state machine to track conversation progress.

## Three Key Improvements

### 1. Dialogue Stages (DialogueStage)

```python
# Conversation now has explicit stages
INITIAL 
  → DOCTOR_SELECTED    # User has chosen a doctor
    → SERVICE_SELECTED  # User has chosen a service  
      → DATETIME_PENDING # Waiting for date/time
        → BOOKING_COMPLETE # Ready to book
```

### 2. Stay in Booking Mode

```python
# Once in booking flow, all input is treated as appointment data
User says "Cleaning" in DOCTOR_SELECTED stage
  ✅ Understood as: service selection
  ❌ No longer: "How can I assist?" (ignoring user)
```

### 3. Stage-Aware Next Step Decision

```python
# System decides next step based on current stage
Current stage: SERVICE_SELECTED (has doctor + service)
User says: "Next Wednesday"
System:
  ✅ Recognizes as date
  ✅ Stores as date
  ✅ Asks next required field: "What time?"
```

## Conversation Example

```
User: "I'd like to see Dr. Wang"
Bot: "What service do you need?"
State: DOCTOR_SELECTED ← Remembered doctor

User: "Cleaning"
Bot: "What date would you like?"
State: SERVICE_SELECTED ← Remembered doctor + service

User: "Next Wednesday"
Bot: "What time works for you?"
State: DATETIME_PENDING ← Remembered doctor + service + date

User: "3 PM"
Bot: "✅ Booking confirmed!"
State: BOOKING_COMPLETE ← Ready to execute
```

## Code Changes

### dialogue_service.py

```python
# New class
class DialogueStage(str, Enum):
    INITIAL = "initial"
    DOCTOR_SELECTED = "doctor_selected"
    SERVICE_SELECTED = "service_selected"
    DATETIME_PENDING = "datetime_pending"
    BOOKING_COMPLETE = "booking_complete"

# New field (in DialogueState class)
self.stage = DialogueStage.INITIAL  # Track current stage

# New functions
def determine_next_question_and_stage(stage, collected_entities, new_entities):
    """Returns (next_question, next_stage)"""
    # Returns appropriate question and new stage based on current stage

def should_stay_in_appointment_mode(stage, llm_intent, user_message):
    """Returns True if we should stay in appointment booking flow"""
    if stage != DialogueStage.INITIAL:
        return True  # Stay in appointment mode
    return False
```

### chat.py

```python
# Improved message processing flow

# 1. Check if we should stay in appointment mode
should_stay = should_stay_in_appointment_mode(
    dialogue_state.stage,
    llama_response.intent,
    message.content
)

if should_stay:
    # 2. Force appointment intent (override LLM if needed)
    llama_response.intent = "appointment"

# 3. Determine next question based on stage
next_question, next_stage = determine_next_question_and_stage(
    dialogue_state.stage,
    dialogue_state.collected_entities,
    new_entities
)

dialogue_state.stage = next_stage  # 4. Update stage
```
    llama_response.intent,
    message.content
)

if should_stay:
    # 2. 强制为预约意图 (忽略 LLM 可能说的其他意图)
    llama_response.intent = "appointment"

# 3. 根据新阶段进行状态转移
next_question, next_stage = determine_next_question_and_stage(
    dialogue_state.stage,
    dialogue_state.collected_entities,
    new_entities
)

dialogue_state.stage = next_stage  # 4. 更新阶段
```

## 测试

```bash
cd e:\Learning\AI-customer-service
python tests/test_dialogue_state_machine.py
```

输出将显示状态转移和改进:
```
📨 Turn 2: User says: 'Cleaning'
   Should stay in appointment mode? True
   ✅ FORCED to appointment mode (not asking 'How can I assist?')
   Next stage: service_selected
   🤖 Bot asks: 'What date would you like?'
```

## 关键要点

| 概念 | 说明 |
|------|------|
| **DialogueStage** | 对话现在处于的阶段 (INITIAL, DOCTOR_SELECTED 等) |
| **状态转移** | 根据输入和当前阶段自动进展到下一阶段 |
| **保持模式** | 一旦用户开始预约，所有输入都被视为预约信息 |
| **意图调整** | LLM 意图可被忽略，以支持当前阶段流程 |

## 这是如何解决原始问题的

### 原始问题流程

```
用户: "Cleaning"
LLM: intent="query"
系统: "How can I assist?" ❌
原因: 系统接受 LLM 的查询意图，忽略对话上下文
```

### 改进后流程

## Testing

```bash
cd e:\Learning\AI-customer-service
python tests/test_dialogue_state_machine.py
```

Output will show state transitions and improvements:
```
Turn 2: User says: 'Cleaning'
   Should stay in appointment mode? True
   [OK] FORCED to appointment mode (not asking 'How can I assist?')
   Next stage: service_selected
   Bot asks: 'What date would you like?'
```

## Key Concepts

| Concept | Description |
|---------|-------------|
| **DialogueStage** | Current conversation stage (INITIAL, DOCTOR_SELECTED, etc.) |
| **State Transition** | Automatically progresses to next stage based on input and current stage |
| **Stay in Mode** | Once user starts booking, all input is treated as appointment data |
| **Intent Override** | LLM intent can be ignored to support current stage flow |

## How This Fixes the Original Problem

### Original Problem Flow

```
User: "Cleaning"
LLM: intent="query"
System: "How can I assist?" ❌
Reason: System accepts LLM's query intent, ignoring conversation context
```

### Improved Flow

```
User: "Cleaning"
LLM: intent="query"
System: Check stage → DOCTOR_SELECTED
System: Should stay in appointment mode? → YES
System: Force intent="appointment"
System: Extract service = "Cleaning"
System: Transition stage to SERVICE_SELECTED
System: "What date would you like?" ✅
Reason: System remembers stage, ignores LLM's incorrect intent
```

---

Resources:
- Full docs: [DIALOGUE_STATE_MACHINE_IMPROVEMENT.md](DIALOGUE_STATE_MACHINE_IMPROVEMENT.md)
- Integration guide: [DIALOGUE_IMPROVEMENT_INTEGRATION.md](DIALOGUE_IMPROVEMENT_INTEGRATION.md)
