from typing import Optional
from pydantic import BaseModel, Field, field_validator
import re


class UserLoginRequest(BaseModel):
    # Can be student_id (e.g., 202611399), email, or user id
    username: str = Field(..., description="Student ID, Email, or Account ID", min_length=1)
    password: str = Field(..., description="Account password", min_length=1)


class UserRegisterRequest(BaseModel):
    student_id: str = Field(..., min_length=3, max_length=50, description="Student ID or Staff ID")
    email: str = Field(..., min_length=3, max_length=100, description="Email address")
    password: str = Field(..., min_length=6, description="Password (at least 6 characters)")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
        if not re.match(pattern, v):
            raise ValueError("Invalid email format")
        return v.strip().lower()

    name: str = Field(..., min_length=2, description="Full name")
    first_name: Optional[str] = None
    role: str = Field(default="Student")
    category: str = Field(default="student")
    is_crrmu_member: bool = Field(default=False)
    program_strand: Optional[str] = "BSIT"
    year_section: Optional[str] = "1A"
    contact_number: Optional[str] = ""
    address: Optional[str] = ""
    # Emergency Contact Details
    emergency_person: Optional[str] = ""
    emergency_relationship: Optional[str] = ""
    emergency_contact: Optional[str] = ""
    preferred_contact_method: Optional[str] = "Phone call"
    terms_accepted: bool = Field(default=True, description="Accepted Terms & Conditions")


class StatusUpdateRequest(BaseModel):
    status: str = Field(..., description="Status must be pending, approved, or rejected")

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        cleaned = v.strip().lower()
        if cleaned not in ("pending", "approved", "rejected"):
            raise ValueError("Status must be 'pending', 'approved', or 'rejected'")
        return cleaned


class UserResponse(BaseModel):
    id: str
    studentId: str
    email: str
    name: str
    firstName: str
    role: str
    category: str
    isCrrmuMember: bool
    initials: str
    programStrand: str
    yearSection: str
    contactNumber: str
    address: str
    avatarBg: str
    avatarColor: str
    emergencyPerson: str
    emergencyRelationship: str
    emergencyContact: str
    preferredContactMethod: str
    status: str = "pending"
    termsAccepted: bool = True
    termsAcceptedAt: Optional[str] = None
    createdAt: Optional[str] = None

    class Config:
        populate_by_name = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class MessageResponse(BaseModel):
    message: str
    success: bool = True
