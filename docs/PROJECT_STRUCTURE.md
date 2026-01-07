# Project File Organization & Structure

## 📁 Complete Project Directory Map

```
AI-customer-service/
│
├── 📂 backend/                    # Backend API & Core Logic
│   ├── main.py                    # FastAPI application entry point
│   ├── database.py                # Database connection setup
│   ├── models.py                  # Pydantic data models
│   │
│   ├── 📂 config/                 # Configuration
│   │   ├── settings.py            # App settings & constants
│   │   └── ...
│   │
│   ├── 📂 routes/                 # API endpoints
│   │   ├── chat.py                # Chat/conversation API
│   │   ├── doctors.py             # Doctor management API
│   │   ├── customers.py           # Customer management API
│   │   ├── services_api.py        # Service management API
│   │   └── ...
│   │
│   ├── 📂 services/               # Business logic & AI
│   │   ├── llama_service.py       # LLM NLU service
│   │   ├── appointment_service.py # Appointment booking logic
│   │   ├── dialogue_service.py    # Multi-turn dialogue state
│   │   └── ...
│   │
│   ├── 📂 schemas/                # Data validation schemas
│   │   └── ...
│   │
│   ├── 📂 utils/                  # Utilities
│   │   ├── doctor_validator.py    # Doctor validation & aliases
│   │   ├── db_utils.py            # Database utilities
│   │   └── ...
│   │
│   └── 📂 test files (backend)
│       ├── test_json_cleaning.py
│       ├── test_llama.py
│       └── ...
│
├── 📂 frontend/                   # React/Next.js Frontend
│   ├── package.json               # npm dependencies
│   ├── next.config.js             # Next.js configuration
│   ├── tsconfig.json              # TypeScript config
│   │
│   ├── 📂 app/                    # Next.js app directory
│   │   └── ...
│   │
│   ├── 📂 components/             # React components
│   │   ├── DentalChat.tsx         # Main chat component
│   │   ├── MessageList.tsx        # Message display
│   │   ├── InputBox.tsx           # User input component
│   │   └── ...
│   │
│   └── README.md                  # Frontend setup guide
│
├── 📂 db/                         # Database files
│   └── clinic.db                  # SQLite database
│
├── 📂 docs/                       # Documentation
│   ├── DIALOGUE_SYSTEM.md         # Dialogue flow docs
│   ├── DOCTOR_SELECTION_IMPLEMENTATION.md
│   ├── CUSTOMER_SERVICE_STYLE_GUIDE.md
│   ├── 5-SLOTS/                   # 5-slot architecture docs
│   └── ... (50+ documentation files)
│
├── 📂 tests/                      # Test suite
│   ├── test_dialogue_flow.py
│   ├── test_dialogue_state_machine.py
│   ├── test_e2e.py                # End-to-end tests
│   ├── test_comprehensive_flow.py
│   ├── test_doctor_fix.py
│   ├── test_full_api_flow.py
│   ├── test_slot_driven.py
│   └── ... (18+ test files)
│
├── 📂 scripts/                    # Utility scripts
│   ├── demo_dialogue_improvement.py
│   ├── check_appointments.py
│   ├── check_schema.py
│   ├── debug_tests.py
│   ├── init_db.py
│   ├── verify_setup.py
│   └── ... (9 scripts)
│
├── 📂 config_root/                # Root config
│   ├── create_tables.sql          # Database schema
│   └── llama_prompt.txt           # LLM prompt template
│
├── 🔧 Root Configuration Files
│   ├── .env                       # Environment variables
│   ├── .env/Scripts/python.exe    # Virtual environment
│   ├── .gitignore                 # Git ignore rules
│   ├── requirements.txt           # Python dependencies
│   └── .pytest_cache/             # Pytest cache
│
├── 📄 Root Project Files
│   ├── README.md                  # Project overview
│   ├── DELIVERABLES.md            # Deliverables checklist
│   ├── FINAL_CHECKLIST.md         # Final checklist
│   ├── ENGLISH_CONVERSION_COMPLETE.md
│   │
│   ├── 🚀 Run Scripts (root)
│   │   ├── run_backend.py         # Start backend
│   │   ├── run_server.py          # Start server
│   │   └── init_db.py             # Initialize database
│   │
│   ├── 🧪 Test Files (root)
│   │   ├── test_doctor_selection.py
│   │   ├── test_doctor_flow_integration.py
│   │   ├── test_app_import.py
│   │   ├── test_debug.py
│   │   ├── test_e2e.py
│   │   ├── test_entities.py
│   │   ├── simple_test.py
│   │   └── check_chinese.py
│   │
│   ├── 📊 Output Files
│   │   ├── test_output.txt
│   │   └── test_results.txt
│   │
│   ├── 📋 SQL Schema
│   │   └── create_tables.sql
│   │
│   └── 🗄️ Database
│       ├── clinic.db              # Main database
│       └── (backup in db/ folder)
│
└── .git/                          # Git repository
```

---

## 📂 File Organization by Category

### 1. **Backend API Layer** 🔧
| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI app initialization |
| `backend/database.py` | SQLite connection |
| `backend/models.py` | Pydantic models |
| `backend/routes/*.py` | API endpoints (chat, doctors, customers, services) |

### 2. **Business Logic & Services** 🧠
| File | Purpose |
|------|---------|
| `backend/services/llama_service.py` | NLU extraction using Llama |
| `backend/services/appointment_service.py` | Appointment booking logic |
| `backend/services/dialogue_service.py` | Multi-turn dialogue state mgmt |

### 3. **Configuration & Utilities** ⚙️
| File | Purpose |
|------|---------|
| `backend/config/settings.py` | Environment & settings |
| `backend/utils/doctor_validator.py` | Doctor validation & aliases |
| `backend/utils/db_utils.py` | Database helpers |
| `backend/schemas/*.py` | Input validation schemas |

### 4. **Frontend** 🎨
| File | Purpose |
|------|---------|
| `frontend/components/DentalChat.tsx` | Main chat UI |
| `frontend/components/MessageList.tsx` | Message display |
| `frontend/components/InputBox.tsx` | User input |

### 5. **Database** 🗄️
| File | Purpose |
|------|---------|
| `db/clinic.db` | SQLite database |
| `create_tables.sql` | Database schema |
| `reset_db_with_test_data.py` | DB initialization script |

### 6. **Testing** 🧪

#### Root Level Tests (Quick tests)
- `test_doctor_selection.py` - Doctor validation tests
- `test_doctor_flow_integration.py` - Integration tests
- `simple_test.py` - Basic functionality tests

#### tests/ Directory (Comprehensive)
- `test_dialogue_flow.py` - Dialogue flow tests
- `test_e2e.py` - End-to-end tests
- `test_comprehensive_flow.py` - Full system flow
- `test_dialogue_state_machine.py` - State machine tests
- `test_slot_driven.py` - 5-slot architecture tests
- ... and 12+ more

### 7. **Scripts & Utilities** 🛠️
| File | Purpose |
|------|---------|
| `scripts/demo_dialogue_improvement.py` | Demo script |
| `scripts/check_appointments.py` | Query appointments |
| `scripts/debug_tests.py` | Debug utilities |
| `scripts/verify_setup.py` | Setup verification |

### 8. **Documentation** 📚
| Category | Files |
|----------|-------|
| Architecture | `5_SLOT_ARCHITECTURE.md`, `DIALOGUE_SYSTEM.md` |
| Implementation | `DOCTOR_SELECTION_IMPLEMENTATION.md`, `DIALOGUE_STATE_MACHINE_IMPROVEMENT.md` |
| Style Guides | `CUSTOMER_SERVICE_STYLE_GUIDE.md` |
| Reports | `COMPLETION_REPORT.md`, `PROJECT_SUMMARY.md` |
| Quick Start | `START_HERE.md`, `QUICK_REFERENCE.md` |

### 9. **Root Configuration** ⚙️
| File | Purpose |
|------|---------|
| `.env` | Environment variables |
| `requirements.txt` | Python dependencies |
| `.gitignore` | Git ignore rules |
| `README.md` | Project overview |

---

## 🎯 Quick Access Guide

### To Run the Project
```bash
# 1. Backend
python run_backend.py
# or
python -m uvicorn backend.main:app --reload

# 2. Frontend
cd frontend && npm run dev

# 3. Database
python reset_db_with_test_data.py
```

### To Run Tests
```bash
# Quick tests (root level)
python test_doctor_selection.py
python test_doctor_flow_integration.py

# Full test suite
pytest tests/
```

### To Check Setup
```bash
python scripts/verify_setup.py
python scripts/check_schema.py
```

---

## 📊 File Statistics

| Category | Count | Location |
|----------|-------|----------|
| Python Files (backend) | 40+ | `backend/` |
| Python Files (tests) | 25+ | `tests/` + root |
| Python Scripts | 9 | `scripts/` |
| Documentation Files | 50+ | `docs/` |
| Frontend Components | 10+ | `frontend/components/` |
| Database Tables | 5 | SQLite |
| **Total Files** | **150+** | Across all folders |

---

## 🏗️ Architecture Layers

```
┌─────────────────────────────────────┐
│         Frontend (Next.js/React)    │  ← User Interface
├─────────────────────────────────────┤
│         API Layer (FastAPI)         │  ← HTTP endpoints
├─────────────────────────────────────┤
│    Routes (chat, doctors, etc)      │  ← URL routing
├─────────────────────────────────────┤
│   Services (LLM, Dialogue, etc)     │  ← Business Logic
├─────────────────────────────────────┤
│  Database (SQLite) & Utils          │  ← Data & Helpers
└─────────────────────────────────────┘
```

---

## ✅ Project Status

- ✅ Backend: Fully implemented
- ✅ Frontend: Fully implemented
- ✅ Database: Set up with test data
- ✅ Tests: Comprehensive coverage
- ✅ Documentation: Extensive
- ✅ Language: 100% English

---

## 🚀 Recommended File Access Order

1. **Start Here**: `README.md`, `docs/START_HERE.md`
2. **Run Backend**: `python run_backend.py`
3. **Run Frontend**: `cd frontend && npm run dev`
4. **Test**: `python test_doctor_selection.py`
5. **Explore**: Check `backend/routes/chat.py` for API logic
6. **Learn**: Read `docs/DIALOGUE_SYSTEM.md` for architecture
