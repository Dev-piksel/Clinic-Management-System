import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3

from .database import get_db, get_user_by_id
from .models import UserResponse

SECRET_KEY = os.environ.get(
    "JWT_SECRET",
    "clinic_management_system_super_secret_jwt_key_2026_secured"
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))  # 24 hours

security = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire, "iat": datetime.now(timezone.utc)})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None


def row_to_user_response(row: sqlite3.Row) -> UserResponse:
    return UserResponse(
        id=row["id"],
        studentId=row["student_id"],
        email=row["email"],
        name=row["name"],
        firstName=row["first_name"],
        role=row["role"],
        category=row["category"],
        isCrrmuMember=bool(row["is_crrmu_member"]),
        initials=row["initials"],
        programStrand=row["program_strand"] or "",
        yearSection=row["year_section"] or "",
        contactNumber=row["contact_number"] or "",
        address=row["address"] or "",
        avatarBg=row["avatar_bg"] or "#8fd3a2",
        avatarColor=row["avatar_color"] or "#1b522f",
        emergencyPerson=row["emergency_person"] or "",
        emergencyRelationship=row["emergency_relationship"] or "",
        emergencyContact=row["emergency_contact"] or "",
        preferredContactMethod=row["preferred_contact_method"] or "Phone call",
        status=row["status"] if "status" in row.keys() else "approved",
        termsAccepted=bool(row["terms_accepted"]) if "terms_accepted" in row.keys() else True,
        termsAcceptedAt=row["terms_accepted_at"] if "terms_accepted_at" in row.keys() and row["terms_accepted_at"] else row["created_at"],
        createdAt=row["created_at"],
    )


def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: sqlite3.Connection = Depends(get_db)
) -> UserResponse:
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload["sub"]
    user_row = get_user_by_id(db, user_id)
    if not user_row:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return row_to_user_response(user_row)
