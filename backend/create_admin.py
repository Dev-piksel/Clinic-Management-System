#!/usr/bin/env python3
"""
CSHMS Clinic Management System - Administrator Provisioning Tool
Use this script to securely create or update a Clinic Administrator account.

Usage:
    python3 -m backend.create_admin
    python3 -m backend.create_admin --id ADMIN-001 --email admin@celtech.edu.ph --name "Dr. Angela Reyes" --password SecurePass123
"""

import argparse
import os
import sys
import uuid
from datetime import datetime, timezone

from .database import get_db_connection, init_db, hash_password


def create_or_update_admin(
    staff_id: str,
    email: str,
    name: str,
    password: str,
    role: str = "Clinic Administrator",
    phone: str = "0917-000-0001",
) -> None:
    init_db()
    conn = get_db_connection()
    cursor = conn.cursor()

    email_clean = email.strip().lower()
    staff_id_clean = staff_id.strip()
    name_clean = name.strip()
    password_hash = hash_password(password)
    now = datetime.now(timezone.utc).isoformat()

    # Determine initials
    parts = name_clean.split()
    initials = (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else (parts[0][:2].upper() if parts else "AD")
    first_name = parts[0] if parts else name_clean

    # Check if user with this email or ID already exists
    cursor.execute("SELECT id, email, student_id, role, category FROM users WHERE LOWER(email) = ? OR LOWER(student_id) = ?", (email_clean, staff_id_clean.lower()))
    existing = cursor.fetchone()

    if existing:
        user_id = existing["id"]
        cursor.execute("""
            UPDATE users
            SET student_id = ?,
                email = ?,
                password_hash = ?,
                name = ?,
                first_name = ?,
                role = ?,
                category = 'staff',
                initials = ?,
                program_strand = 'School Clinic Operations',
                year_section = 'Medical & Health Services',
                contact_number = ?,
                status = 'approved',
                updated_at = ?
            WHERE id = ?
        """, (
            staff_id_clean,
            email_clean,
            password_hash,
            name_clean,
            first_name,
            role,
            initials,
            phone,
            now,
            user_id
        ))
        conn.commit()
        conn.close()
        print(f"\n✅ Successfully updated existing account to {role}!")
    else:
        user_id = str(uuid.uuid4())
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
                ?, 'staff', 0, ?, 'School Clinic Operations',
                'Medical & Health Services', ?, 'CELTECH School Clinic', '#225530', '#ffffff',
                'Clinic Operations Desk', 'Workplace', '0917-000-0000',
                'Phone call', 'approved', 1, ?,
                ?, ?
            )
        """, (
            user_id,
            staff_id_clean,
            email_clean,
            password_hash,
            name_clean,
            first_name,
            role,
            initials,
            phone,
            now,
            now,
            now,
        ))
        conn.commit()
        conn.close()
        print(f"\n✅ Successfully created new {role} account!")

    print("=" * 60)
    print("  CLINIC ADMINISTRATOR CREDENTIALS")
    print("=" * 60)
    print(f"  Account ID / Staff ID : {staff_id_clean}")
    print(f"  Email Address         : {email_clean}")
    print(f"  Full Name             : {name_clean}")
    print(f"  Role                  : {role}")
    print(f"  Category              : staff (RBAC Authorized)")
    print(f"  Approval Status       : approved")
    print("=" * 60)
    print("  You can now log in at http://localhost:5173 with these credentials.")
    print("=" * 60 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Provision a Clinic Administrator account for CSHMS.")
    parser.add_argument("--id", default="ADMIN-001", help="Staff/Admin ID (default: ADMIN-001)")
    parser.add_argument("--email", default="admin@celtech.edu.ph", help="Email address (default: admin@celtech.edu.ph)")
    parser.add_argument("--name", default="Clinic Administrator", help="Full name (default: Clinic Administrator)")
    parser.add_argument("--password", default="admin2026", help="Password (default: admin2026)")
    parser.add_argument("--role", default="Clinic Administrator", help="Role (default: Clinic Administrator)")
    parser.add_argument("--phone", default="0917-000-0001", help="Contact phone")

    args = parser.parse_args()

    create_or_update_admin(
        staff_id=args.id,
        email=args.email,
        name=args.name,
        password=args.password,
        role=args.role,
        phone=args.phone,
    )


if __name__ == "__main__":
    main()
