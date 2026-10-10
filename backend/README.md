# CSHMS Authentication Backend (FastAPI + SQLite)

A lightweight authentication backend built with **FastAPI** and **SQLite** for the CELTECH School Clinic Management System.

---

## Features

- **SQLite Database**: Stored locally in `backend/clinic.db` (zero configuration, no separate database server needed).
- **Secure Password Hashing**: Uses `bcrypt` with unique salts.
- **JWT Authentication**: Generates Bearer access tokens with configurable expiration.
- **Strict Student Validation**: Student IDs must contain numbers only (digits 0-9).
- **Admin Verification Gate**: Student registrations require clinic administration review before access is granted.
- **CORS Configured**: Allows cross-origin requests from the SvelteKit frontend running on port 5173.
- **Interactive OpenAPI Docs**: Available out-of-the-box at `http://localhost:8000/docs`.

---

## Quick Start

### 1. Run the Backend
From the repository root:
```bash
npm run backend:dev
```
Or directly using Python/Uvicorn:
```bash
uvicorn backend.main:app --reload --port 8000
```

The API will be available at:
- API Base: `http://localhost:8000`
- Interactive Swagger UI: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

---

## Account Registration & Verification

There are zero preset, mock, or hardcoded accounts. All users are registered dynamically:
- **First Account Registration**: When the system is initialized with 0 users, the very first registered user (Staff or Student) is automatically approved as the initial Administrator/User so you can immediately access the portal and review incoming registrations.
- **Student Registrations**: Student IDs must be numbers only (e.g. `202611888`). Newly registered students remain in `pending` status until approved by a clinic administrator.
- **Approval Gate**: Users pending approval cannot log in (`403 Forbidden`). Once approved via `/api/admin/users/{user_id}/status` or the `/admin/users` UI, they gain immediate access.

---

## API Endpoints

### 1. `POST /api/auth/login`
Authenticate using Student ID (or Email) and Password.

**Request Body:**
```json
{
  "username": "202611888",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOi...",
  "token_type": "bearer",
  "user": {
    "id": "faith-manada",
    "studentId": "202611399",
    "email": "faithmanada@gmail.com",
    "name": "Faith Manada",
    "firstName": "Faith",
    "role": "Student",
    "category": "student",
    "isCrrmuMember": false,
    "initials": "FM",
    "programStrand": "BSIT",
    "yearSection": "4A"
  }
}
```

---

### 2. `POST /api/auth/register`
Register a new student or staff account.

**Request Body:**
```json
{
  "student_id": "202688888",
  "email": "student@celtech.edu.ph",
  "password": "securepassword",
  "name": "Maria Santos",
  "role": "Student",
  "category": "student",
  "program_strand": "BSIT",
  "year_section": "1A"
}
```

---

### 3. `GET /api/auth/me`
Retrieve profile of currently authenticated user.

**Headers:**
```http
Authorization: Bearer <access_token>
```

---

### 4. `GET /api/auth/users`
List all registered users in SQLite (passwords omitted).

---

### 5. `POST /api/auth/logout`
Log out current session.
