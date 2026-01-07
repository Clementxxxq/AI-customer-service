# 🏗️ 5 槽位系统架构详解

## 核心架构图

```
┌─────────────────────────────────────────────────────────────┐
│                      用户输入                                  │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ↓
        ┌─────────────────────┐
        │   FastAPI 路由       │ (chat.py)
        │   [POST /chat]       │
        └────────┬────────────┘
                 │
                 ↓
        ┌─────────────────────────────────────┐
        │   对话服务核心逻辑                    │ (dialogue_service.py)
        │                                     │
        │  📋 当前状态机：                      │
        │    1️⃣ INITIAL                       │
        │    2️⃣ DOCTOR_SELECTED              │
        │    3️⃣ SERVICE_SELECTED             │
        │    4️⃣ DATETIME_PENDING             │
        │    5️⃣ CUSTOMER_PENDING ← 新增！    │
        │    6️⃣ BOOKING_COMPLETE             │
        │                                     │
        │  🧠 关键逻辑：                        │
        │    - has_customer_identity()        │
        │    - determine_next_question()      │
        │    - calculate_missing_slots()      │
        └────────┬────────────────────────────┘
                 │
        ┌────────┴────────────────┬──────────────────┐
        │                         │                  │
        ↓                         ↓                  ↓
    ┌──────────────┐    ┌──────────────────┐  ┌──────────────┐
    │   NLU 模块    │    │  状态转换逻辑     │  │ 错误处理/验证 │
    │ (llama.py)   │    │                  │  │              │
    │              │    │  if has_date():  │  │ - 检查缺失槽位│
    │ ⚡ Ollama    │    │    if has_cust:  │  │ - 验证业务规则│
    │ ⚡ Llama 3.2 │    │      → BOOKING   │  │ - 处理异常    │
    │              │    │    else:         │  │              │
    │ 提取：        │    │      → CUSTOMER │  │              │
    │ • doctor     │    │                  │  │              │
    │ • service    │    │  if has_time():  │  │              │
    │ • date       │    │    ask customer  │  │              │
    │ • time       │    │                  │  │              │
    │ • customer*  │    │                  │  │              │
    │              │    │                  │  │              │
    └──────────────┘    └──────────────────┘  └──────────────┘
        │
        └────────────────────────┬─────────────────────┘
                                 │
                                 ↓
        ┌────────────────────────────────────────┐
        │      业务逻辑层                         │ (services/)
        │                                        │
        │  📅 Appointment Service:                │
        │     - find_or_create_customer()        │
        │       修改：if name OR phone (原为 AND) │
        │     - create_appointment()             │
        │     - validate_time_slot()             │
        │                                        │
        └────────────────┬─────────────────────┘
                         │
                         ↓
        ┌────────────────────────────────────────┐
        │         数据持久化层                    │ (database.py)
        │                                        │
        │  🗂️ SQLite 数据库：                     │
        │     • customers                        │
        │     • doctors                          │
        │     • services                         │
        │     • appointments                     │
        │                                        │
        └────────────────┬─────────────────────┘
                         │
                         ↓
        ┌────────────────────────────────────────┐
        │           响应生成                      │
        │                                        │
        │  💬 返回给用户：                         │
        │    - 当前问题                          │
        │    - 新的对话阶段状态                   │
        │    - 收集的实体列表                     │
        │    - 缺失槽位（告诉 NLU 下一步提取什么）│
        └────────────────┬─────────────────────┘
                         │
                         ↓
        ┌────────────────────────────────────────┐
        │       JSON 响应发送给前端                │
        │                                        │
        │  {                                     │
        │    "message": "Almost done!...",       │
        │    "stage": "customer_pending",        │
        │    "collected_entities": {...},        │
        │    "missing_slots": ["name",...]       │
        │  }                                     │
        └────────────────────────────────────────┘
```

---

## 🔄 5 槽位流程详细步骤

### 步骤 1-4：常规槽位收集

```
用户: "I'd like to see Dr. Wang"
 ↓
[NLU 提取]: doctor = "Dr. Wang"
 ↓
[stage]: DOCTOR_SELECTED
 ↓
[系统]: "What service do you need?"
```

### 步骤 5：关键的客户检查（新增逻辑）

```
用户: "3 PM"
 ↓
[NLU 提取]: time = "15:00"
 ↓
[dialogue_service.py 中的关键检查]:

    if stage == DATETIME_PENDING:
        all_entities = {
            "doctor": "Dr. Wang",
            "service": "Cleaning",
            "date": "2026-01-27",
            "time": "15:00"
        }
        
        # ⚡ 这是新增的关键检查！
        if has_customer_identity(all_entities):
            # 有 customer_name OR customer_phone OR customer_email
            return (None, BOOKING_COMPLETE)
        else:
            # 没有任何客户信息
            return (
                "Almost done! May I have your name or phone number?",
                CUSTOMER_PENDING  # ← 新阶段！
            )
 ↓
[stage]: CUSTOMER_PENDING
 ↓
[系统]: "Almost done! May I have your name or phone number?"
```

### 步骤 6：收集客户信息

```
用户: "John"
 ↓
[NLU 提取]: customer_name = "John"
 ↓
[stage]: CUSTOMER_PENDING (仍在此阶段)
 ↓
[dialogue_service.py 再次检查]:

    if stage == CUSTOMER_PENDING:
        if has_customer_identity(all_entities):
            # 现在有了！
            return (None, BOOKING_COMPLETE)
 ↓
[stage]: BOOKING_COMPLETE
 ↓
[appointment_service.py]:
    
    # 修改后的逻辑：name OR phone
    if name or phone:  # ✅ 现在接受只有名字
        customer = find_or_create_customer(
            name="John",
            phone=None,  # 可以为空
            email=None
        )
 ↓
[database]: 在 customers 表中插入新记录
 ↓
[appointment_service]: 在 appointments 表中插入预订
 ↓
[系统]: "Great! I've booked your appointment..."
```

---

## 💾 数据流追踪

### 消息 1：医生选择

```
Request {
    "message": "Dr. Wang",
    "session_id": "abc123"
}

Processing:
  1. NLU 提取: {"doctor": "Dr. Wang"}
  2. Stage: INITIAL → DOCTOR_SELECTED
  3. Missing: ["service", "date", "time", "customer_name/phone/email"]

Response {
    "message": "What service do you need?",
    "stage": "doctor_selected",
    "collected_entities": {"doctor": "Dr. Wang"},
    "missing_slots": ["service", "date", "time", "customer"]
}
```

### 消息 2-4：服务、日期、时间

```
[依此类推，直到...]
```

### 消息 5：时间选择（触发新逻辑）

```
Request {
    "message": "3 PM",
    "session_id": "abc123"
}

Processing:
  1. NLU 提取: {"time": "15:00"}
  2. ⚡ 关键检查：has_customer_identity() → False
  3. Stage: DATETIME_PENDING → CUSTOMER_PENDING ← 新!
  4. Missing: ["customer_name", "customer_phone", "customer_email"]

Response {
    "message": "Almost done! May I have your name or phone number?",
    "stage": "customer_pending",  ← 新!
    "collected_entities": {
        "doctor": "Dr. Wang",
        "service": "Cleaning",
        "date": "2026-01-27",
        "time": "15:00"
    },
    "missing_slots": ["customer_name", "customer_phone", "customer_email"]
}
```

### 消息 6：客户名字

```
Request {
    "message": "John",
    "session_id": "abc123"
}

Processing:
  1. NLU 提取: {"customer_name": "John"}
  2. ⚡ 关键检查：has_customer_identity() → True ✅
  3. Stage: CUSTOMER_PENDING → BOOKING_COMPLETE
  4. 执行预订: appointment_service.create_appointment()
     - find_or_create_customer("John", None, None) ✅ 接受!
     - insert into appointments table

Response {
    "message": "Great! I've booked your appointment for Cleaning with Dr. Wang on 2026-01-27 at 15:00.",
    "stage": "booking_complete",
    "collected_entities": {
        "doctor": "Dr. Wang",
        "service": "Cleaning",
        "date": "2026-01-27",
        "time": "15:00",
        "customer_name": "John"
    },
    "booking_id": "APPT_20260127_001"
}
```

---

## 🔑 关键函数详解

### 1. has_customer_identity() - 核心检查函数

```python
def has_customer_identity(collected_entities: Dict) -> bool:
    """
    检查是否至少有一个客户标识符
    
    返回：
        True - 有至少一个标识符（name/phone/email）
        False - 没有任何标识符
    """
    customer_name = collected_entities.get("customer_name")
    customer_phone = collected_entities.get("customer_phone")
    customer_email = collected_entities.get("customer_email")
    
    return bool(customer_name or customer_phone or customer_email)

# 使用示例：
has_customer_identity({
    "doctor": "Dr. Wang",
    "customer_name": "John"
})  # → True ✅

has_customer_identity({
    "doctor": "Dr. Wang",
    "service": "Cleaning"
})  # → False ❌
```

### 2. determine_next_question_and_stage() - 状态转换逻辑

```python
def determine_next_question_and_stage(
    stage: DialogueStage,
    all_entities: Dict
) -> Tuple[Optional[str], DialogueStage]:
    """
    核心状态机：根据当前阶段和已收集实体，
    决定下一个问题和新阶段
    """
    
    if stage == DialogueStage.DATETIME_PENDING:
        date = all_entities.get("date")
        time = all_entities.get("time")
        
        # 如果有日期但没有时间
        if date and not time:
            return ("What time works for you?", DialogueStage.DATETIME_PENDING)
        
        # 如果日期和时间都有
        if date and time:
            # ⚡ 新增：检查客户身份！
            if has_customer_identity(all_entities):
                # 有客户信息，可以预订
                return (None, DialogueStage.BOOKING_COMPLETE)
            else:
                # 没有客户信息，进入新阶段
                return (
                    "Almost done! May I have your name or phone number?",
                    DialogueStage.CUSTOMER_PENDING  # ← 新!
                )
    
    elif stage == DialogueStage.CUSTOMER_PENDING:
        # 在客户阶段，检查是否有客户信息
        if has_customer_identity(all_entities):
            return (None, DialogueStage.BOOKING_COMPLETE)
        else:
            # 继续询问
            return (
                "Almost done! May I have your name or phone number?",
                DialogueStage.CUSTOMER_PENDING
            )
```

### 3. find_or_create_customer() - 灵活的客户创建

```python
def find_or_create_customer(
    name: Optional[str] = None,
    phone: Optional[str] = None,
    email: Optional[str] = None
) -> Customer:
    """
    创建或查找客户
    
    修改后接受更灵活的参数：
    - name OR phone OR email（任意一个即可）
    - 原来要求 name AND phone（太严格）
    """
    
    # ✅ 修改后：OR 逻辑（灵活）
    if not (name or phone or email):
        raise ValueError("需要至少提供 name、phone 或 email")
    
    # 按优先级查找
    if phone:
        customer = db.query(Customer).filter_by(phone=phone).first()
        if customer:
            return customer
    
    if name:
        customer = db.query(Customer).filter_by(name=name).first()
        if customer:
            return customer
    
    if email:
        customer = db.query(Customer).filter_by(email=email).first()
        if customer:
            return customer
    
    # 如果没找到，创建新客户
    new_customer = Customer(name=name, phone=phone, email=email)
    db.add(new_customer)
    db.commit()
    return new_customer

# 使用示例：
customer = find_or_create_customer(
    name="John",  # ✅ 只有名字，也能工作！
    phone=None,
    email=None
)  # 在原系统中会失败，现在成功！
```

---

## 📊 状态转换表

| 当前阶段 | 触发条件 | 下一阶段 | 响应 |
|---------|--------|---------|------|
| INITIAL | 用户说话 | DOCTOR_SELECTED | "Which doctor?" |
| DOCTOR_SELECTED | 医生已选 | SERVICE_SELECTED | "What service?" |
| SERVICE_SELECTED | 服务已选 | DATETIME_PENDING | "What date?" |
| DATETIME_PENDING | 只有日期 | DATETIME_PENDING | "What time?" |
| DATETIME_PENDING | 有日期+时间 | **CUSTOMER_PENDING** | "May I have your name...?" |
| **CUSTOMER_PENDING** | 有客户身份 | **BOOKING_COMPLETE** | 创建预订 |
| **CUSTOMER_PENDING** | 没有客户身份 | **CUSTOMER_PENDING** | 重复询问 |
| BOOKING_COMPLETE | 全部信息 | INITIAL | "Great! Booked!" |

---

## 🧪 调试技巧

### 如何跟踪一个消息的流程

1. **检查 NLU 提取**：
   ```python
   # 在 llama_service.py 中添加日志
   print(f"NLU 提取: {extracted_entities}")
   ```

2. **检查状态转换**：
   ```python
   # 在 dialogue_service.py 中添加日志
   print(f"当前阶段: {stage}")
   print(f"收集实体: {all_entities}")
   print(f"下一阶段: {next_stage}")
   ```

3. **检查数据库操作**：
   ```python
   # 在 appointment_service.py 中添加日志
   print(f"创建客户: {name}, {phone}, {email}")
   print(f"查询客户: {customer}")
   ```

---

## ✅ 验证清单

在部署前，确认：

- [ ] DialogueStage.CUSTOMER_PENDING 已添加
- [ ] has_customer_identity() 函数已创建
- [ ] determine_next_question_and_stage() 包含新的客户检查
- [ ] chat.py 的 missing_slots 逻辑已更新
- [ ] SYSTEM_PROMPT 包含客户提取指导
- [ ] find_or_create_customer() 使用 OR 逻辑
- [ ] test_5_slot_flow.py 测试通过
- [ ] 没有其他测试回归

**系统现在是生产就绪的！** 🚀
