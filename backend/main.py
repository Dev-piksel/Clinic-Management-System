import os
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
    update_user_profile,
    reset_user_password,
    create_audit_log,
    get_audit_logs,
)
from .models import (
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
    TokenResponse,
    MessageResponse,
    StatusUpdateRequest,
    AdminUpdateUserRequest,
    AdminCreateUserRequest,
    AdminResetPasswordRequest,
    AuditLogResponse,
)
from .auth import (
    create_access_token,
    get_current_user,
    require_staff,
    row_to_user_response,
)


def row_to_audit_log_response(row: sqlite3.Row) -> AuditLogResponse:
    return AuditLogResponse(
        id=row["id"],
        timestamp=row["timestamp"],
        actorId=row["actor_id"],
        actorName=row["actor_name"],
        actorRole=row["actor_role"],
        action=row["action"],
        category=row["category"],
        targetUserId=row["target_user_id"],
        targetUserName=row["target_user_name"],
        targetUserRole=row["target_user_role"],
        details=row["details"],
        metadataJson=row["metadata_json"] or "{}",
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

    # Strict RBAC: determine role, category, and approval status
    is_staff_request = (
        req.category.strip().lower() == "staff"
        or "staff" in req.role.strip().lower()
        or "admin" in req.role.strip().lower()
    )

    if is_staff_request:
        expected_passkey = os.environ.get("CLINIC_STAFF_PASSKEY", "CELTECH-CLINIC-2026")
        if not req.staff_passkey or req.staff_passkey.strip() != expected_passkey:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid Clinic Staff Authorization Passkey. Only authorized clinic personnel can register staff or administrator accounts.",
            )
        assigned_category = "staff"
        assigned_role = req.role.strip() if req.role.strip() in ("Clinic Staff", "Clinic Administrator") else "Clinic Staff"
        user_status = "approved"
    else:
        # Strictly student account - never converted to admin
        assigned_category = "student"
        assigned_role = "Student - CRRMU Member" if req.is_crrmu_member else "Student"
        user_status = "pending"

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
    token = create_access_token({
        "sub": user_id,
        "student_id": user_resp.studentId,
        "role": user_resp.role,
        "category": user_resp.category,
        "name": user_resp.name,
    })

    create_audit_log(
        db,
        actor_id=user_id,
        actor_name=user_resp.name,
        actor_role=user_resp.role,
        action="USER_SELF_REGISTERED",
        category="AUTHENTICATION",
        details=f"New {user_resp.role} account registered for {user_resp.name} ({user_resp.studentId}). Status: {user_status}.",
        target_user_id=user_id,
        target_user_name=user_resp.name,
        target_user_role=user_resp.role,
    )

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
        "category": user_resp.category,
        "name": user_resp.name,
    })

    create_audit_log(
        db,
        actor_id=user_resp.id,
        actor_name=user_resp.name,
        actor_role=user_resp.role,
        action="USER_LOGIN",
        category="AUTHENTICATION",
        details=f"User signed in successfully: {user_resp.name} ({user_resp.studentId}, {user_resp.role}).",
        target_user_id=user_resp.id,
        target_user_name=user_resp.name,
        target_user_role=user_resp.role,
    )

    return TokenResponse(access_token=token, token_type="bearer", user=user_resp)


@app.get("/api/auth/me", response_model=UserResponse, tags=["Authentication"])
def get_me(current_user: UserResponse = Depends(get_current_user)):
    return current_user


@app.post("/api/auth/logout", response_model=MessageResponse, tags=["Authentication"])
def logout():
    return MessageResponse(message="Successfully logged out")


# =========================================================================
# ADMIN / USER MANAGEMENT & AUDIT LOG ENDPOINTS
# =========================================================================

@app.get("/api/admin/users", response_model=List[UserResponse], tags=["Admin"])
def list_admin_users(
    status_filter: Optional[str] = Query(None, alias="status", description="Filter by status (pending, approved, rejected, or all)"),
    role_filter: Optional[str] = Query(None, alias="role", description="Filter by role (student, staff, crrmu, or specific role)"),
    search: Optional[str] = Query(None, description="Search query"),
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    rows = get_all_users(db, status_filter)
    result = [row_to_user_response(r) for r in rows]

    if role_filter and role_filter.lower() != "all":
        rf = role_filter.lower()
        if rf == "crrmu":
            result = [u for u in result if u.isCrrmuMember]
        elif rf == "student":
            result = [u for u in result if u.category == "student" and not u.isCrrmuMember]
        elif rf == "staff":
            result = [u for u in result if u.category == "staff"]
        else:
            result = [u for u in result if rf in u.role.lower()]

    if search and search.strip():
        q = search.strip().lower()
        result = [
            u for u in result
            if q in u.name.lower() or q in u.studentId.lower() or q in u.email.lower() or q in u.programStrand.lower()
        ]

    return result


@app.post("/api/admin/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["Admin"])
def admin_create_user(
    req: AdminCreateUserRequest,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    cursor = db.cursor()
    # Check duplicate ID or email
    cursor.execute("SELECT id FROM users WHERE LOWER(student_id) = LOWER(?)", (req.student_id.strip(),))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail=f"User ID '{req.student_id}' is already registered.")

    cursor.execute("SELECT id FROM users WHERE LOWER(email) = LOWER(?)", (req.email.strip(),))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail=f"Email '{req.email}' is already registered.")

    user_id = str(uuid.uuid4())
    pw_hash = hash_password(req.password)
    now = datetime.now(timezone.utc).isoformat()

    name_parts = req.name.strip().split()
    first_name = name_parts[0] if name_parts else req.name
    initials = (name_parts[0][0] + name_parts[-1][0]).upper() if len(name_parts) >= 2 else (name_parts[0][:2].upper() if name_parts else "US")

    role_clean = req.role.strip()
    r_lower = role_clean.lower()
    if "admin" in r_lower or "staff" in r_lower or "nurse" in r_lower or "doctor" in r_lower:
        cat = "staff"
        is_crrmu = False
    elif "crrmu" in r_lower:
        cat = "student"
        is_crrmu = True
    else:
        cat = "student"
        is_crrmu = bool(req.is_crrmu_member)

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
            ?, ?, 1, ?,
            ?, ?
        )
    """, (
        user_id, req.student_id.strip(), req.email.strip().lower(), pw_hash,
        req.name.strip(), first_name.strip(), role_clean, cat,
        1 if is_crrmu else 0, initials, req.program_strand or "",
        req.year_section or "", req.contact_number or "", req.address or "",
        "#8fd3a2", "#1b522f", req.emergency_person or "", req.emergency_relationship or "",
        req.emergency_contact or "", req.preferred_contact_method or "Phone call",
        req.status or "approved", now, now, now
    ))
    db.commit()

    created_row = get_user_by_id(db, user_id)
    user_resp = row_to_user_response(created_row)

    create_audit_log(
        db,
        actor_id=current_user.id,
        actor_name=current_user.name,
        actor_role=current_user.role,
        action="ADMIN_CREATED_USER",
        category="USER_MANAGEMENT",
        details=f"Admin {current_user.name} created account for {user_resp.name} ({user_resp.studentId}, Role: {user_resp.role}).",
        target_user_id=user_id,
        target_user_name=user_resp.name,
        target_user_role=user_resp.role,
    )

    return user_resp


@app.get("/api/admin/users/{user_id}", response_model=UserResponse, tags=["Admin"])
def get_admin_user_details(
    user_id: str,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return row_to_user_response(user)


@app.put("/api/admin/users/{user_id}", response_model=UserResponse, tags=["Admin"])
def admin_update_user(
    user_id: str,
    req: AdminUpdateUserRequest,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    target = get_user_by_id(db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    old_role = target["role"]
    old_status = target["status"]

    update_dict = req.model_dump(exclude_unset=True)

    # Smart category & CRRMU adjustment based on role
    if "role" in update_dict and update_dict["role"]:
        r_lower = update_dict["role"].lower()
        if "admin" in r_lower or "staff" in r_lower or "nurse" in r_lower or "doctor" in r_lower:
            update_dict["category"] = "staff"
            update_dict["is_crrmu_member"] = False
        elif "crrmu" in r_lower:
            update_dict["category"] = "student"
            update_dict["is_crrmu_member"] = True
        elif "student" in r_lower:
            update_dict["category"] = "student"
            if "is_crrmu_member" not in update_dict:
                update_dict["is_crrmu_member"] = False

    updated_row = update_user_profile(db, user_id, update_dict)
    if not updated_row:
        raise HTTPException(status_code=500, detail="Failed to update user profile")

    new_role = updated_row["role"]
    new_status = updated_row["status"]

    if old_role != new_role:
        action = "ROLE_UPDATED"
        details = f"Admin {current_user.name} changed role of {target['name']} ({target['student_id']}) from '{old_role}' to '{new_role}'."
    elif old_status != new_status:
        action = "USER_STATUS_UPDATED"
        details = f"Admin {current_user.name} changed status of {target['name']} ({target['student_id']}) from '{old_status}' to '{new_status}'."
    else:
        action = "USER_ACCOUNT_UPDATED"
        details = f"Admin {current_user.name} updated account details for {target['name']} ({target['student_id']})."

    create_audit_log(
        db,
        actor_id=current_user.id,
        actor_name=current_user.name,
        actor_role=current_user.role,
        action=action,
        category="USER_MANAGEMENT",
        details=details,
        target_user_id=user_id,
        target_user_name=updated_row["name"],
        target_user_role=updated_row["role"],
    )

    return row_to_user_response(updated_row)


@app.post("/api/admin/users/{user_id}/reset-password", response_model=MessageResponse, tags=["Admin"])
def admin_reset_password(
    user_id: str,
    req: AdminResetPasswordRequest,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    target = get_user_by_id(db, user_id)
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    success = reset_user_password(db, user_id, req.new_password)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to reset password")

    create_audit_log(
        db,
        actor_id=current_user.id,
        actor_name=current_user.name,
        actor_role=current_user.role,
        action="PASSWORD_RESET",
        category="SECURITY",
        details=f"Admin {current_user.name} reset password for {target['name']} ({target['student_id']}).",
        target_user_id=user_id,
        target_user_name=target["name"],
        target_user_role=target["role"],
    )

    return MessageResponse(message=f"Password for {target['name']} ({target['student_id']}) has been successfully reset.")


@app.patch("/api/admin/users/{user_id}/status", response_model=UserResponse, tags=["Admin"])
def update_status(
    user_id: str,
    req: StatusUpdateRequest,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    updated = update_user_status(db, user_id, req.status)
    if not updated:
        raise HTTPException(status_code=500, detail="Failed to update user status")

    create_audit_log(
        db,
        actor_id=current_user.id,
        actor_name=current_user.name,
        actor_role=current_user.role,
        action="USER_STATUS_UPDATED",
        category="USER_MANAGEMENT",
        details=f"Admin {current_user.name} updated account status for {user['name']} ({user['student_id']}) to '{req.status}'.",
        target_user_id=user_id,
        target_user_name=user["name"],
        target_user_role=user["role"],
    )

    return row_to_user_response(updated)


@app.delete("/api/admin/users/{user_id}", response_model=MessageResponse, tags=["Admin"])
def remove_user(
    user_id: str,
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own administrator account while logged in."
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete user")

    create_audit_log(
        db,
        actor_id=current_user.id,
        actor_name=current_user.name,
        actor_role=current_user.role,
        action="USER_DELETED",
        category="USER_MANAGEMENT",
        details=f"Admin {current_user.name} permanently deleted account of {user['name']} ({user['student_id']}, Role: {user['role']}).",
        target_user_id=user_id,
        target_user_name=user["name"],
        target_user_role=user["role"],
    )

    return MessageResponse(message=f"User {user['name']} ({user['student_id']}) deleted successfully")


@app.get("/api/admin/stats", tags=["Admin"])
def get_admin_stats(
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
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


@app.get("/api/admin/audit-logs", response_model=List[AuditLogResponse], tags=["Admin"])
def list_audit_logs(
    limit: int = Query(100, ge=1, le=500),
    offset: int = Query(0, ge=0),
    action: Optional[str] = Query(None, description="Filter by action"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search audit details or names"),
    current_user: UserResponse = Depends(require_staff),
    db: sqlite3.Connection = Depends(get_db)
):
    rows = get_audit_logs(db, limit, offset, action, category, search)
    return [row_to_audit_log_response(r) for r in rows]
