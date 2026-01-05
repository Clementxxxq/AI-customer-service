# Thunder Client API Testing Guide

## Table of Contents
1. [Installation & Setup](#installation--setup)
2. [Base Configuration](#base-configuration)
3. [API Endpoints](#api-endpoints)
4. [Testing Examples](#testing-examples)
5. [Request Headers](#request-headers)

---

## Installation & Setup

### Step 1: Install Thunder Client Extension
- Open VS Code Extensions (Ctrl+Shift+X)
- Search for "Thunder Client"
- Click Install (official extension by Rangav)

### Step 2: Open Thunder Client
- Click the Thunder icon in VS Code left sidebar
- Or press Ctrl+Shift+P and type "Thunder Client"

### Step 3: Create New Request
- Click "New Request" or press Ctrl+K

---

## Base Configuration

**Base URL:** `http://127.0.0.1:8000`

**API Documentation:** `http://127.0.0.1:8000/docs` (Swagger UI)

### Default Headers
```
Content-Type: application/json
Accept: application/json
```

---

## API Endpoints

### 1. Health Check
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Check API health status |

### 2. Customers Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/customers` | Get all customers |
| GET | `/customers/{id}` | Get customer by ID |
| POST | `/customers` | Create new customer |
| PUT | `/customers/{id}` | Update customer |
| DELETE | `/customers/{id}` | Delete customer |

### 3. Doctors Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/doctors` | Get all doctors |
| GET | `/doctors/{id}` | Get doctor by ID |
| POST | `/doctors` | Create new doctor |
| PUT | `/doctors/{id}` | Update doctor |
| DELETE | `/doctors/{id}` | Delete doctor |

### 4. Services Management
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/services` | Get all services |
| GET | `/services/{id}` | Get service by ID |
| POST | `/services` | Create new service |
| PUT | `/services/{id}` | Update service |
| DELETE | `/services/{id}` | Delete service |

---

## Testing Examples

### 1. Health Check
**Request:**
```
GET http://127.0.0.1:8000/health
```

**Expected Response (200 OK):**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

---

### 2. Get All Customers
**Request:**
```
GET http://127.0.0.1:8000/customers
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Alice Zhang",
    "phone": "1234567890",
    "email": "alice@example.com",
    "created_at": "2026-01-04T10:44:00"
  },
  {
    "id": 2,
    "name": "Bob Li",
    "phone": "0987654321",
    "email": "bob@example.com",
    "created_at": "2026-01-04T10:44:00"
  }
]
```

---

### 3. Get Single Customer by ID
**Request:**
```
GET http://127.0.0.1:8000/customers/1
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "name": "Alice Zhang",
  "phone": "1234567890",
  "email": "alice@example.com",
  "created_at": "2026-01-04T10:44:00"
}
```

---

### 4. Create New Customer
**Request:**
```
POST http://127.0.0.1:8000/customers
Content-Type: application/json

{
  "name": "Charlie Chen",
  "phone": "5555555555",
  "email": "charlie@example.com"
}
```

**Expected Response (201 Created):**
```json
{
  "name": "Charlie Chen",
  "phone": "5555555555",
  "email": "charlie@example.com"
}
```

---

### 5. Update Customer
**Request:**
```
PUT http://127.0.0.1:8000/customers/1
Content-Type: application/json

{
  "name": "Alice Zhang Updated",
  "phone": "1111111111",
  "email": "alice.updated@example.com"
}
```

**Expected Response (200 OK):**
```json
{
  "name": "Alice Zhang Updated",
  "phone": "1111111111",
  "email": "alice.updated@example.com"
}
```

---

### 6. Delete Customer
**Request:**
```
DELETE http://127.0.0.1:8000/customers/1
```

**Expected Response (200 OK):**
```json
{
  "message": "Customer deleted successfully"
}
```

---

### 7. Get All Doctors
**Request:**
```
GET http://127.0.0.1:8000/doctors
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Dr. Wang",
    "specialization": "Orthodontics",
    "phone": "1112223333",
    "email": "wang@example.com",
    "created_at": "2026-01-04T10:44:00"
  },
  {
    "id": 2,
    "name": "Dr. Li",
    "specialization": "General Dentistry",
    "phone": "4445556666",
    "email": "li@example.com",
    "created_at": "2026-01-04T10:44:00"
  }
]
```

---

### 8. Create New Doctor
**Request:**
```
POST http://127.0.0.1:8000/doctors
Content-Type: application/json

{
  "name": "Dr. Zhang",
  "specialization": "Cosmetic Dentistry",
  "phone": "7778889999",
  "email": "zhang@example.com"
}
```

**Expected Response (201 Created):**
```json
{
  "name": "Dr. Zhang",
  "specialization": "Cosmetic Dentistry",
  "phone": "7778889999",
  "email": "zhang@example.com"
}
```

---

### 9. Get All Services
**Request:**
```
GET http://127.0.0.1:8000/services
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Cleaning",
    "description": "Teeth cleaning and polishing",
    "duration_minutes": 30,
    "price": 200.0,
    "doctor_id": 2
  },
  {
    "id": 2,
    "name": "Extraction",
    "description": "Remove damaged tooth",
    "duration_minutes": 60,
    "price": 500.0,
    "doctor_id": 2
  },
  {
    "id": 3,
    "name": "Checkup",
    "description": "Oral health examination",
    "duration_minutes": 20,
    "price": 100.0,
    "doctor_id": 1
  }
]
```

---

### 10. Create New Service
**Request:**
```
POST http://127.0.0.1:8000/services
Content-Type: application/json

{
  "name": "Whitening",
  "description": "Professional teeth whitening",
  "duration_minutes": 45,
  "price": 350.0,
  "doctor_id": 1
}
```

**Expected Response (201 Created):**
```json
{
  "name": "Whitening",
  "description": "Professional teeth whitening",
  "duration_minutes": 45,
  "price": 350.0,
  "doctor_id": 1
}
```

---

## Request Headers

### Common Headers
```
Content-Type: application/json
Accept: application/json
```

### POST/PUT Request Body Format
All POST and PUT requests require JSON body with the appropriate fields:

**Customer Schema:**
```json
{
  "name": "string (required)",
  "phone": "string (unique, optional)",
  "email": "string (optional)"
}
```

**Doctor Schema:**
```json
{
  "name": "string (required)",
  "specialization": "string (optional)",
  "phone": "string (optional)",
  "email": "string (optional)"
}
```

**Service Schema:**
```json
{
  "name": "string (required, unique)",
  "description": "string (optional)",
  "duration_minutes": "integer (required)",
  "price": "float (required)",
  "doctor_id": "integer (optional)"
}
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error message"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "Validation error message",
      "type": "value_error"
    }
  ]
}
```

---

## Tips for Testing

1. **Use Thunder Client Collections**
   - Create a folder for each resource (Customers, Doctors, Services)
   - Organize all endpoints logically

2. **Set Environment Variables**
   - Define `{{base_url}}` as `http://127.0.0.1:8000`
   - Use `{{base_url}}/customers` instead of full URL
   - Makes switching between environments easier

3. **Save Request History**
   - Thunder Client automatically saves requests
   - Access from the History tab on the left

4. **Use Quick Send**
   - Quick action to test changes without saving

5. **Check Response Status**
   - Look for status codes: 200 (OK), 201 (Created), 400 (Bad Request), 404 (Not Found), 500 (Server Error)

---

## Quick Start Checklist

- [ ] Install Thunder Client extension
- [ ] Start backend: `uvicorn main:app --reload`
- [ ] Create new request in Thunder Client
- [ ] Test `/health` endpoint
- [ ] Test GET `/customers`
- [ ] Test POST `/customers` with sample data
- [ ] Test PUT `/customers/{id}`
- [ ] Test DELETE `/customers/{id}`
- [ ] Repeat for `/doctors` and `/services`

---

## Additional Resources

- [Thunder Client Documentation](https://www.thunderclient.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [API Documentation (Swagger UI)](http://127.0.0.1:8000/docs)

