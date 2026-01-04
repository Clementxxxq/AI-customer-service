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
| **Backend** | Python (Flask/FastAPI) |
| **Frontend** | HTML5 + CSS3 + JavaScript |
| **Database** | SQLite 3 |
| **AI Model** | Llama 3.2:3b (run via Ollama) |
| **API** | RESTful API |

---

## Project Structure

```
AI-customer-service/
├── backend/                    # Backend services
│   ├── app.py                  # Main application
│   ├── models.py               # Database models
│   ├── config.py               # Configuration file
│   ├── requirements.txt         # Python dependencies
│   └── utils/
│       ├── llm_handler.py       # LLM integration
│       ├── db_handler.py        # Database operations
│       └── prompt_generator.py  # Prompt generation
├── frontend/                   # Frontend application
│   ├── index.html              # Chat UI
│   ├── styles.css              # Styles
│   └── script.js               # Frontend logic
├── db/                         # Data storage
│   ├── clinic.db               # SQLite database ✓
│   ├── test.py                 # Database initialization script ✓
│   └── create_tables.sql       # Database schema ✓
├── data/
│   └── services.txt            # Clinic services document
├── docs/
│   └── steps.md                # Implementation steps documentation
├── .gitignore                  # Git ignore file ✓
└── README.md                   # This file
```

---

## ✅ Completed Tasks

### Phase 1: Environment Setup
- ✅ Installed Python 3.8+
- ✅ Installed pip package manager
- ✅ Installed SQLite (built-in with Python)
- ✅ Installed Ollama and configured Llama 3.2:3b

### Phase 2: Database Design and Initialization
- ✅ **Database Creation** - Created `clinic.db` SQLite database
- ✅ **Schema Definition** - Defined 3 tables in `create_tables.sql`:
  - `services` - Clinic service information
  - `appointments` - Appointment records
  - `time_slots` - Available time slots
- ✅ **Database Initialization** - `test.py` script successfully creates and initializes the database
- ✅ **Sample Data** - Added sample services and time slots

### Other Completed Items
- ✅ Created project directory structure
- ✅ Created `.gitignore` file (ignores `*.db`, `venv/`, `.env`, etc.)

---

## ❌ Pending Tasks

### Phase 3: Clinic Service Document
- ⏳ Create `data/services.txt` with complete clinic service list
- ⏳ Define service information format (name, description, duration, price)

### Phase 4: LLM Integration
- ⏳ Create `backend/utils/llm_handler.py`
- ⏳ Implement Ollama API connection
- ⏳ Design system prompts (including clinic rules and service info)
- ⏳ Implement intent detection and parameter extraction

### Phase 5: Backend API Development
- ⏳ Create `backend/app.py` (Flask/FastAPI)
- ⏳ Implement API endpoints:
  - `POST /api/chat` - Chat message handling
  - `POST /api/book-appointment` - Appointment confirmation
  - `GET /api/available-slots` - Get available time slots
  - `GET /api/services` - Get services list
- ⏳ Create `backend/utils/db_handler.py` database operation functions
- ⏳ Implement conversation flow and state machine

### Phase 6: Frontend Development
- ⏳ Create `frontend/index.html` - Chat UI interface
- ⏳ Create `frontend/styles.css` - UI styling
- ⏳ Create `frontend/script.js` - Frontend interaction logic

### Phase 7: Testing
- ⏳ End-to-end functional testing
- ⏳ Error case handling testing
- ⏳ Performance testing

### Phase 8: Deployment and Documentation
- ⏳ Configure environment variables and settings
- ⏳ Add logging system
- ⏳ Improve project documentation

---

## Getting Started

### Prerequisites
- Python 3.8+
- Ollama (already installed)
- Git

### Local Development Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd AI-customer-service
```

2. **Initialize the database**
```bash
cd db
python test.py
# Output: clinic.db created successfully!
cd ..
```

3. **Create virtual environment** (to be implemented)
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

4. **Install dependencies** (to be implemented)
```bash
pip install -r backend/requirements.txt
```

5. **Start Ollama service** (in another terminal)
```bash
ollama serve
ollama pull llama2:3b
```

6. **Run backend** (to be implemented)
```bash
cd backend
python app.py
```

7. **Open frontend** (to be implemented)
```
Open in browser: http://localhost:5000
```

---

## Database Information

### Initialized Tables
1. **services** - Clinic services
2. **appointments** - Patient appointment records
3. **time_slots** - Available time slots

### Sample Data
- 3 sample services: Cleaning, Extraction, Checkup
- 3 sample time slots: 09:00, 10:00, 11:00 on 2026-01-05

---

## Next Steps

1. 📝 Write clinic services document (`data/services.txt`)
2. 🤖 Implement LLM integration and conversation handling
3. 🔧 Develop backend API endpoints
4. 🎨 Design and develop frontend chat interface
5. 🧪 Perform functional and integration testing
6. 🚀 Deploy and launch

---

## Troubleshooting

### clinic.db Issue (Fixed)
- **Original Issue**: `clinic.db` was a SQL script instead of a database file
- **Solution**: Renamed file to `create_tables.sql` and ran `test.py` to generate real database

### Common Errors

| Error | Solution |
|------|----------|
| `FileNotFoundError: create_tables.sql` | Ensure `python test.py` has been executed |
| `sqlite3.DatabaseError: file is not a database` | Delete `clinic.db` and re-run `test.py` |
| Ollama connection failed | Ensure `ollama serve` is running, check `localhost:11434` |

---

## License

MIT License

---

## Contact

For issues or suggestions, please submit an Issue or Pull Request.

---

**Last Updated**: 2026-01-03
