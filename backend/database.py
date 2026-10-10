import os
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Generator, Optional, Dict, Any, List
import bcrypt

# Database file path (located in backend/clinic.db by default)
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = os.environ.get("CLINIC_DB_PATH", str(BASE_DIR / "clinic.db"))


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    # Ensure tables exist
    ensure_tables()
    conn = get_db_connection()
    try:
        yield conn
    finally:
        conn.close()


def ensure_tables():
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            init_db()
        else:
            # Check if status and terms columns exist, if not migrate
            cursor.execute("PRAGMA table_info(users)")
            cols = [row["name"] for row in cursor.fetchall()]
            if "status" not in cols:
                cursor.execute("ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'approved'")
            if "terms_accepted" not in cols:
                cursor.execute("ALTER TABLE users ADD COLUMN terms_accepted INTEGER DEFAULT 1")
            if "terms_accepted_at" not in cols:
                cursor.execute("ALTER TABLE users ADD COLUMN terms_accepted_at TEXT DEFAULT ''")
            conn.commit()
    finally:
        conn.close()


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False


def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            student_id TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            name TEXT NOT NULL,
            first_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Student',
            category TEXT NOT NULL DEFAULT 'student',
            is_crrmu_member INTEGER NOT NULL DEFAULT 0,
            initials TEXT NOT NULL,
            program_strand TEXT DEFAULT '',
            year_section TEXT DEFAULT '',
            contact_number TEXT DEFAULT '',
            address TEXT DEFAULT '',
            avatar_bg TEXT DEFAULT '#8fd3a2',
            avatar_color TEXT DEFAULT '#1b522f',
            emergency_person TEXT DEFAULT '',
            emergency_relationship TEXT DEFAULT '',
            emergency_contact TEXT DEFAULT '',
            preferred_contact_method TEXT DEFAULT 'Phone call',
            status TEXT NOT NULL DEFAULT 'pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    # Active sessions / token revocation table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            token TEXT NOT NULL,
            created_at TEXT NOT NULL,
            expires_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()


def get_user_by_identifier(conn: sqlite3.Connection, identifier: str) -> Optional[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE LOWER(student_id) = LOWER(?) OR LOWER(email) = LOWER(?) OR LOWER(id) = LOWER(?)
    """, (identifier, identifier, identifier))
    return cursor.fetchone()


def get_user_by_id(conn: sqlite3.Connection, user_id: str) -> Optional[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()


def update_user_status(conn: sqlite3.Connection, user_id: str, new_status: str) -> Optional[sqlite3.Row]:
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users
        SET status = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, now, user_id))
    conn.commit()
    return get_user_by_id(conn, user_id)


def get_all_users(conn: sqlite3.Connection, status_filter: Optional[str] = None) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    if status_filter and status_filter.lower() != "all":
        cursor.execute("SELECT * FROM users WHERE LOWER(status) = LOWER(?) ORDER BY created_at DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
    return cursor.fetchall()


def delete_user(conn: sqlite3.Connection, user_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    return cursor.rowcount > 0
