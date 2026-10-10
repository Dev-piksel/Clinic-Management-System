import re
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

from .database import (
    init_db,
    get_db,
    get_user_by_identifier,
    get_user_by_id,
    get_all_users,
    update_user_status,
    delete_user,
    hash_password,
    verify_password,
)
from .models import (
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    TokenResponse,
    MessageResponse,
    StatusUpdateRequest,
)
from .auth import (
    create_access_token,
    get_current_user,
    row_to_user_response,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize SQLite database schema and seed demo accounts
    init_db()
    yield


app = FastAPI(
    title="Clinic Management System (CSHMS) Auth & Admin API",
    description="Authentication and User Management backend with SQLite database for CELTECH School Clinic",
    version="1.1.0",
    lifespan=lifespan,
)

# Enable CORS for frontend applications (SvelteKit / Vite)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
        "http://localhost:8443",
        "http://localhost:3000",
        "*",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["General"])
def root():
    return {
        "message": "CSHMS Clinic Management System Authentication Backend",
        "status": "online",
        "database": "SQLite",
        "docs_url": "/docs",
    }


@app.get("/api/health", tags=["General"])
def health(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) as count FROM users")
    row = cursor.fetchone()
    count = row["count"] if row else 0
    return {
        "status": "healthy",
        "database": "sqlite",
        "registered_users": count,
    }


@app.post("/api/auth/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def register(req: UserRegisterRequest, db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()

    # Student ID validation: students must have numeric IDs only
    is_student = req.category.strip().lower() == "student" or "student" in req.role.strip().lower()
    if is_student and not req.student_id.strip().isdigit():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Student ID must contain numbers only.",
        )

    # Check for existing student_id
    cursor.execute("SELECT id FROM users WHERE LOWER(student_id) = LOWER(?)", (req.student_id.strip(),))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Student ID '{req.student_id}' is already registered.",
        )

    # Check for existing email
    cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (req.email.strip(),))
    if cursor.fetchone():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Email '{req.email}' is already registered.",
        )

    # Compute initials
    name_parts = req.name.strip().split()
    if len(name_parts) >= 2:
        initials = (name_parts[0][0] + name_parts[-1][0]).upper()
    elif len(name_parts) == 1 and name_parts[0]:
        initials = name_parts[0][:2].upper()
    else:
        initials = "ST"

    first_name = req.first_name or (name_parts[0] if name_parts else req.name)
    user_id = str(uuid.uuid4())
    pw_hash = hash_password(req.password)
    now = datetime.now(timezone.utc).isoformat()

    # Check existing user count
    cursor.execute("SELECT COUNT(*) as count FROM users")
    total_users_count = cursor.fetchone()["count"]

    # First user registered in the system is automatically approved as Clinic Administrator
    if total_users_count == 0:
        user_status = "approved"
        assigned_role = "Clinic Administrator"
        assigned_category = "staff"
    else:
        user_status = "pending"
        assigned_role = req.role.strip()
        assigned_category = req.category.strip().lower()

    cursor.execute("""
        INSERT INTO users (
            id, student_id, email, password_hash, name, first_name,
            role, category, is_crrmu_member, initials, program_strand,
            year_section, contact_number, address, avatar_bg, avatar_color,
            emergency_person, emergency_relationship, emergency_contact,
            preferred_contact_method, status, terms_accepted, terms_accepted_at,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?
        )
    """, (
        user_id,
        req.student_id.strip(),
        req.email.strip().lower(),
        pw_hash,
        req.name.strip(),
        first_name.strip(),
        assigned_role,
        assigned_category,
        1 if req.is_crrmu_member else 0,
        initials,
        req.program_strand or "",
        req.year_section or "",
        req.contact_number or "",
        req.address or "",
        "#8fd3a2",
        "#1b522f",
        req.emergency_person or "",
        req.emergency_relationship or "",
        req.emergency_contact or "",
        req.preferred_contact_method or "Phone call",
        user_status,
        1 if req.terms_accepted else 0,
        now if req.terms_accepted else "",
        now,
        now,
    ))
    db.commit()

    created_row = get_user_by_id(db, user_id)
    if not created_row:
        raise HTTPException(status_code=500, detail="Failed to retrieve created user")

    user_resp = row_to_user_response(created_row)
    token = create_access_token({"sub": user_id, "student_id": user_resp.studentId, "role": user_resp.role})

    return TokenResponse(access_token=token, token_type="bearer", user=user_resp)


@app.post("/api/auth/login", response_model=TokenResponse, tags=["Authentication"])
def login(req: UserLoginRequest, db: sqlite3.Connection = Depends(get_db)):
    identifier = req.username.strip()
    user_row = get_user_by_identifier(db, identifier)

    if not user_row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Student ID/Email or password",
        )

    if not verify_password(req.password, user_row["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Student ID/Email or password",
        )

    # Check approval status
    user_status = user_row["status"] if "status" in user_row.keys() else "approved"

    if user_status == "pending":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your account is pending administrator approval before you can access the clinic portal. Please contact clinic staff or check back shortly.",
        )
    elif user_status == "rejected":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Your registration request was rejected by the administrator. Please contact the school clinic for assistance.",
        )

    user_resp = row_to_user_response(user_row)
    token = create_access_token({
        "sub": user_resp.id,
        "student_id": user_resp.studentId,
        "role": user_resp.role,
        "name": user_resp.name,
    })

    return TokenResponse(access_token=token, token_type="bearer", user=user_resp)


@app.get("/api/auth/me", response_model=UserResponse, tags=["Authentication"])
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@app.post("/api/auth/logout", response_model=MessageResponse, tags=["Authentication"])
def logout():
    return MessageResponse(message="Successfully logged out")


# =========================================================================
# ADMIN / USER MANAGEMENT ENDPOINTS
# =========================================================================

@app.get("/api/admin/users", response_model=List[UserResponse], tags=["Admin"])
def list_admin_users(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (pending, approved, rejected, or all)"),
    db: sqlite3.Connection = Depends(get_db)
):
    rows = get_all_users(db, status_filter)
    return [row_to_user_response(r) for r in rows]


@app.patch("/api/admin/users/{user_id}/status", response_model=UserResponse, tags=["Admin"])
def update_status(
    user_id: str,
    req: StatusUpdateRequest,
    db: sqlite3.Connection = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = update_user_status(db, user_id, req.status)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update user status")

    return row_to_user_response(updated)


@app.delete("/api/admin/users/{user_id}", response_model=MessageResponse, tags=["Admin"])
def remove_user(
    user_id: str,
    db: sqlite3.Connection = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    return MessageResponse(message=f"User {user['name']} ({user['student_id']}) deleted successfully")


@app.get("/api/admin/stats", tags=["Admin"])
def get_admin_stats(db: sqlite3.Connection = Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT status, COUNT(*) as count FROM users GROUP BY status")
    rows = cursor.fetchall()

    stats = {"total": 0, "pending": 0, "approved": 0, "rejected": 0}
    for row in rows:
        st = row["status"]
        cnt = row["count"]
        stats["total"] += cnt
        if st in stats:
            stats[st] = cnt

    return stats
