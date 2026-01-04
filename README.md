# AI Customer Service System for Dental Clinic

## Project Goals

Build an AI-driven appointment scheduling system for a dental clinic with the following features:
- 🤖 **AI Chat Assistant**: Natural language interaction using locally-hosted Llama 3.2 model
- 📅 **Smart Appointment System**: Automated appointment handling, time slot management, and patient information collection
- 💬 **User-Friendly Chat Interface**: Frontend chatbox UI with excellent user experience
- 📊 **Data Management**: SQLite database for storing appointments, services, and time slots
- 🏥 **Dental Clinic Service Management**: Support for defining and managing multiple dental services

---

## Tech Stack

| Technology | Description |
|------|------|
| **Backend** | Python FastAPI 0.127.0+ |
| **Frontend** | HTML5 + CSS3 + JavaScript |
| **Database** | SQLite 3 |
| **AI Model** | Llama 3.2:3b (run via Ollama) |
| **API** | RESTful API with Pydantic validation |
| **Code Quality** | Type hints, validation, error handling |

---

## Project Structure

```
AI-customer-service/
├── backend/                    # Backend services (production-ready)
│   ├── config/                 # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py         # Central configuration
│   ├── routes/                 # API route handlers (modular)
│   │   ├── __init__.py
│   │   ├── services.py         # Services API (CRUD)
│   │   ├── doctors.py          # Doctors API (CRUD)
│   │   └── customers.py        # Customers API (CRUD)
│   ├── schemas/                # Data validation models
│   │   └── __init__.py         # Pydantic models with validation
│   ├── utils/                  # Utility functions
│   │   ├── __init__.py
│   │   ├── db_utils.py         # Database operations
│   │   └── exceptions.py       # Error handling
│   ├── main.py                 # FastAPI application entry point
│   ├── database.py             # ⚠️ Deprecated (use utils/db_utils.py)
│   ├── models.py               # ⚠️ Deprecated (use schemas/)
│   ├── services_api.py         # ⚠️ Deprecated (use routes/services.py)
│   ├── doctors_api.py          # ⚠️ Deprecated (use routes/doctors.py)
│   ├── customers_api.py        # ⚠️ Deprecated (use routes/customers.py)
│   ├── requirements.txt        # Python dependencies
│   ├── IMPROVEMENTS.md         # Detailed improvement notes
│   ├── MIGRATION.md            # Migration guide
│   ├── QUICK_REFERENCE.md      # Quick reference guide
│   └── __pycache__/
├── frontend/                   # Frontend application (to be implemented)
│   ├── index.html              # Chat UI
│   ├── styles.css              # Styles
│   └── script.js               # Frontend logic
├── db/                         # Data storage
│   ├── clinic.db               # SQLite database
│   ├── create_tables.sql       # Database schema
│   └── init_db.py              # Database initialization script
├── docs/
│   └── steps.md                # Implementation steps documentation
├── .gitignore                  # Git ignore file
├── IMPROVEMENT_SUMMARY.md      # Improvement summary
├── IMPROVEMENT_REPORT.md       # Detailed improvement report
└── README.md                   # This file
```

---

## ✅ Recent Updates (Phase 1: Code Refactoring)

### Code Quality Improvements
- ✅ **Modular Architecture** - Organized code into `config/`, `routes/`, `schemas/`, `utils/`
- ✅ **Configuration Management** - Centralized settings with absolute paths
- ✅ **Data Validation** - Pydantic models with field validation
- ✅ **Database Operations** - Context managers, connection pooling, error handling
- ✅ **Error Handling** - Unified exception handling with proper HTTP status codes
- ✅ **API Endpoints** - Complete CRUD operations for services, doctors, customers
- ✅ **Type Annotations** - Full type hints for better code quality
- ✅ **Documentation** - Added comprehensive guides and references

### API Implementation
- ✅ `GET /api/services` - List all services
- ✅ `GET /api/services/{id}` - Get specific service
- ✅ `POST /api/services` - Create new service
- ✅ `PUT /api/services/{id}` - Update service
- ✅ `DELETE /api/services/{id}` - Delete service
- ✅ Same for `/api/doctors` and `/api/customers`
- ✅ `GET /health` - Health check endpoint

### Pydantic Models
- ✅ `ServiceSchema` - Service data model with validation
- ✅ `DoctorSchema` - Doctor data model with phone/email validation
- ✅ `CustomerSchema` - Customer data model with phone/email validation
- ✅ `AppointmentSchema` - Appointment data model with date/time validation

---

## ❌ Pending Tasks

### Phase 2: LLM Integration
- ⏳ Create `backend/utils/llm_handler.py`
- ⏳ Implement Ollama API connection
- ⏳ Design system prompts
- ⏳ Implement intent detection and parameter extraction
- ⏳ Create `/api/chat` endpoint

### Phase 3: Frontend Development
- ⏳ Create `frontend/index.html` - Chat UI
- ⏳ Create `frontend/styles.css` - UI styling
- ⏳ Create `frontend/script.js` - Frontend logic

### Phase 4: Testing & Deployment
- ⏳ Unit tests with pytest
- ⏳ Integration tests
- ⏳ End-to-end testing
- ⏳ Docker containerization
- ⏳ CI/CD pipeline

---

## Getting Started

### Prerequisites
- Python 3.10+
- Ollama (optional for chat features)
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd AI-customer-service
```

2. **Setup Python environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r backend/requirements.txt
```

4. **Run the backend server**
```bash
cd backend
python main.py
```

The server will start at `http://localhost:8000`

### Accessing the API

**Swagger UI (Interactive API documentation)**
```
http://localhost:8000/docs
```

**ReDoc (Alternative API documentation)**
```
http://localhost:8000/redoc
```

**Health Check**
```bash
curl http://localhost:8000/health
```

### Testing APIs

**Get all services**
```bash
curl http://localhost:8000/api/services
```

**Create a new service**
```bash
curl -X POST http://localhost:8000/api/services \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Teeth Cleaning",
    "description": "Professional teeth cleaning",
    "duration_minutes": 30,
    "price": 50.0
  }'
```

**Get all doctors**
```bash
curl http://localhost:8000/api/doctors
```

**Create a new doctor**
```bash
curl -X POST http://localhost:8000/api/doctors \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Dr. John Smith",
    "specialization": "General Dentistry",
    "phone": "1234567890",
    "email": "john@clinic.com"
  }'
```

---

## Database Information

### Tables
1. **services** - Clinic services information
2. **doctors** - Doctor information
3. **customers** - Patient/customer information
4. **appointments** - Appointment records

### Initialize Database
```bash
cd db
python init_db.py
cd ..
```

---

## API Response Format

### Success Response (200 OK)
```json
{
  "id": 1,
  "name": "Teeth Cleaning",
  "description": "Professional teeth cleaning",
  "duration_minutes": 30,
  "price": 50.0,
  "doctor_id": null
}
```

### Error Response (4xx/5xx)
```json
{
  "detail": "Service not found"
}
```

---

## Cleanup Notes

The following old files are deprecated and can be safely deleted:
- `backend/database.py` → Use `backend/utils/db_utils.py`
- `backend/models.py` → Use `backend/schemas/__init__.py`
- `backend/services_api.py` → Use `backend/routes/services.py`
- `backend/doctors_api.py` → Use `backend/routes/doctors.py`
- `backend/customers_api.py` → Use `backend/routes/customers.py`

---

## Documentation

- **[IMPROVEMENTS.md](backend/IMPROVEMENTS.md)** - Detailed improvement documentation
- **[MIGRATION.md](backend/MIGRATION.md)** - Migration guide from old code
- **[QUICK_REFERENCE.md](backend/QUICK_REFERENCE.md)** - Quick reference for developers
- **[IMPROVEMENT_REPORT.md](IMPROVEMENT_REPORT.md)** - Comprehensive improvement report

---

## Common Issues & Troubleshooting

| Issue | Solution |
|------|----------|
| `ImportError: email-validator not installed` | Removed EmailStr dependency - use regex validation instead |
| `ModuleNotFoundError` | Ensure virtual environment is activated and dependencies are installed |
| `Cannot connect to database` | Verify `clinic.db` exists in `db/` directory, run `python db/init_db.py` |
| `CORS errors from frontend` | Update `CORS_ORIGINS` in `config/settings.py` |
| `Pydantic validation errors` | Check API request format against Swagger docs at `/docs` |

---

## Best Practices

✨ **Type Safety** - All functions use type hints  
✨ **Data Validation** - Pydantic models validate all inputs  
✨ **Error Handling** - Proper HTTP status codes and error messages  
✨ **Code Organization** - Clear separation of concerns  
✨ **Documentation** - Docstrings and API docs  
✨ **Configuration** - Environment-based settings  

---

## Next Steps

1. 🧪 Add comprehensive API tests with pytest
2. 🤖 Implement LLM chat integration
3. 🎨 Develop frontend chat interface
4. 🔐 Add authentication and authorization
5. 📊 Add logging and monitoring
6. 🚀 Deploy with Docker

---

## License

MIT License

---

## Contact

For issues or suggestions, please submit an Issue or Pull Request.

---

**Last Updated**: 2026-01-04  
**Version**: 1.1.0
