import os
import sqlite3
import uuid
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
    conn.execute("PRAGMA journal_mode = WAL")
    conn.execute("PRAGMA synchronous = NORMAL")
    return conn


def get_db() -> Generator[sqlite3.Connection, None, None]:
    ensure_tables()
    conn = get_db_connection()
    try:
        yield conn
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

    # 1. Users table
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
            terms_accepted INTEGER NOT NULL DEFAULT 1,
            terms_accepted_at TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_student_id ON users(student_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_email ON users(email)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_users_category ON users(category)")

    # 2. Active sessions
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

    # 3. Audit logs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audit_logs (
            id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            actor_id TEXT NOT NULL,
            actor_name TEXT NOT NULL,
            actor_role TEXT NOT NULL,
            action TEXT NOT NULL,
            category TEXT NOT NULL,
            target_user_id TEXT,
            target_user_name TEXT,
            target_user_role TEXT,
            details TEXT NOT NULL,
            metadata_json TEXT DEFAULT '{}'
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action)")

    # 4. Appointments table (Synced between student, CRRMU, nurse, and admin)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            student_initials TEXT NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL,
            date TEXT NOT NULL,
            day TEXT NOT NULL,
            month TEXT NOT NULL,
            time TEXT NOT NULL,
            location TEXT NOT NULL DEFAULT 'School Clinic',
            reason TEXT NOT NULL,
            additional_notes TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Confirmed',
            attended_by TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(date)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_student ON appointments(student_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_appointments_status ON appointments(status)")

    # 5. Patient Queue table (Live clinic triage)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patient_queue (
            id TEXT PRIMARY KEY,
            queue_number TEXT NOT NULL,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            student_initials TEXT NOT NULL,
            complaint TEXT NOT NULL,
            time_in_clinic TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Waiting',
            action_text TEXT NOT NULL DEFAULT 'Start visit',
            attended_by TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_queue_status ON patient_queue(status)")

    # 6. Clinic Visits table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clinic_visits (
            id TEXT PRIMARY KEY,
            student_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            date TEXT NOT NULL,
            month_year TEXT NOT NULL,
            title TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'consultation',
            time TEXT NOT NULL,
            assessment TEXT NOT NULL,
            intervention TEXT NOT NULL,
            disposition TEXT NOT NULL,
            clinic_note TEXT DEFAULT '',
            status TEXT NOT NULL DEFAULT 'Completed',
            attended_by TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_visits_student ON clinic_visits(student_id)")

    # 7. First Aid Reports table (CRRMU module)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS first_aid_reports (
            id TEXT PRIMARY KEY,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            patient_name TEXT NOT NULL,
            patient_role TEXT NOT NULL,
            location TEXT NOT NULL,
            incident_type TEXT NOT NULL,
            treatment TEXT NOT NULL,
            responder TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Submitted',
            reviewed_by TEXT DEFAULT '',
            reviewed_at TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_first_aid_status ON first_aid_reports(status)")

    # 8. Notifications table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            time TEXT NOT NULL,
            type TEXT NOT NULL DEFAULT 'confirmation',
            category TEXT NOT NULL DEFAULT 'appointment',
            read INTEGER NOT NULL DEFAULT 0,
            action_text TEXT DEFAULT '',
            action_href TEXT DEFAULT '',
            created_at TEXT NOT NULL
        )
    """)
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_notifications_user ON notifications(user_id)")

    conn.commit()
    conn.close()


def ensure_tables():
    init_db()


# =========================================================================
# USER CRUD FUNCTIONS
# =========================================================================

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


def update_user_profile(conn: sqlite3.Connection, user_id: str, data: dict) -> Optional[sqlite3.Row]:
    allowed_fields = {
        "name", "first_name", "email", "student_id", "role", "category",
        "is_crrmu_member", "program_strand", "year_section", "contact_number",
        "address", "emergency_person", "emergency_relationship", "emergency_contact",
        "preferred_contact_method", "status"
    }
    updates = []
    values = []
    for k, v in data.items():
        if k in allowed_fields and v is not None:
            updates.append(f"{k} = ?")
            values.append(int(v) if k == "is_crrmu_member" and isinstance(v, bool) else v)

    if not updates:
        return get_user_by_id(conn, user_id)

    updates.append("updated_at = ?")
    now = datetime.now(timezone.utc).isoformat()
    values.append(now)
    values.append(user_id)

    query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
    cursor = conn.cursor()
    cursor.execute(query, tuple(values))
    conn.commit()
    return get_user_by_id(conn, user_id)


def reset_user_password(conn: sqlite3.Connection, user_id: str, new_password: str) -> bool:
    pw_hash = hash_password(new_password)
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET password_hash = ?, updated_at = ? WHERE id = ?
    """, (pw_hash, now, user_id))
    conn.commit()
    return cursor.rowcount > 0


# =========================================================================
# AUDIT LOGS FUNCTIONS
# =========================================================================

def create_audit_log(
    conn: sqlite3.Connection,
    actor_id: str,
    actor_name: str,
    actor_role: str,
    action: str,
    category: str,
    details: str,
    target_user_id: Optional[str] = None,
    target_user_name: Optional[str] = None,
    target_user_role: Optional[str] = None,
    metadata_json: str = "{}"
) -> str:
    log_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO audit_logs (
            id, timestamp, actor_id, actor_name, actor_role, action,
            category, target_user_id, target_user_name, target_user_role,
            details, metadata_json
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        log_id, now, actor_id, actor_name, actor_role, action,
        category, target_user_id, target_user_name, target_user_role,
        details, metadata_json
    ))
    conn.commit()
    return log_id


def get_audit_logs(
    conn: sqlite3.Connection,
    limit: int = 100,
    offset: int = 0,
    action_filter: Optional[str] = None,
    category_filter: Optional[str] = None,
    search: Optional[str] = None
) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    query = "SELECT * FROM audit_logs WHERE 1=1"
    params = []

    if action_filter and action_filter.lower() != "all":
        query += " AND LOWER(action) = LOWER(?)"
        params.append(action_filter)

    if category_filter and category_filter.lower() != "all":
        query += " AND LOWER(category) = LOWER(?)"
        params.append(category_filter)

    if search and search.strip():
        q = f"%{search.strip().lower()}%"
        query += " AND (LOWER(details) LIKE ? OR LOWER(actor_name) LIKE ? OR LOWER(target_user_name) LIKE ? OR LOWER(action) LIKE ?)"
        params.extend([q, q, q, q])

    query += " ORDER BY timestamp DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])

    cursor.execute(query, tuple(params))
    return cursor.fetchall()


# =========================================================================
# APPOINTMENTS CRUD FUNCTIONS
# =========================================================================

def create_appointment(conn: sqlite3.Connection, data: dict) -> sqlite3.Row:
    app_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (
            id, student_id, student_name, student_initials, title, type,
            date, day, month, time, location, reason, additional_notes,
            status, attended_by, created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?
        )
    """, (
        app_id,
        data["student_id"],
        data["student_name"],
        data["student_initials"],
        data["title"],
        data.get("type", data["title"]),
        data["date"],
        data["day"],
        data["month"],
        data["time"],
        data.get("location", "School Clinic"),
        data["reason"],
        data.get("additional_notes", ""),
        data.get("status", "Confirmed"),
        data.get("attended_by", ""),
        now,
        now,
    ))
    conn.commit()
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (app_id,))
    return cursor.fetchone()


def get_appointments(
    conn: sqlite3.Connection,
    student_id: Optional[str] = None,
    status_filter: Optional[str] = None,
    date_filter: Optional[str] = None
) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    query = "SELECT * FROM appointments WHERE 1=1"
    params = []

    if student_id:
        query += " AND LOWER(student_id) = LOWER(?)"
        params.append(student_id)

    if status_filter and status_filter.lower() != "all":
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status_filter)

    if date_filter:
        query += " AND date = ?"
        params.append(date_filter)

    query += " ORDER BY date DESC, time ASC"
    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def get_appointment_by_id(conn: sqlite3.Connection, app_id: str) -> Optional[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM appointments WHERE id = ?", (app_id,))
    return cursor.fetchone()


def update_appointment_status(
    conn: sqlite3.Connection,
    app_id: str,
    new_status: str,
    attended_by: Optional[str] = None
) -> Optional[sqlite3.Row]:
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    if attended_by:
        cursor.execute("""
            UPDATE appointments
            SET status = ?, attended_by = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, attended_by, now, app_id))
    else:
        cursor.execute("""
            UPDATE appointments
            SET status = ?, updated_at = ?
            WHERE id = ?
        """, (new_status, now, app_id))
    conn.commit()
    return get_appointment_by_id(conn, app_id)


def delete_appointment(conn: sqlite3.Connection, app_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM appointments WHERE id = ?", (app_id,))
    conn.commit()
    return cursor.rowcount > 0


# =========================================================================
# PATIENT QUEUE CRUD FUNCTIONS
# =========================================================================

def add_queue_item(conn: sqlite3.Connection, data: dict) -> sqlite3.Row:
    q_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()

    # Generate queue number (e.g. Q-01)
    cursor.execute("SELECT COUNT(*) as count FROM patient_queue WHERE date(created_at) = date(?)", (now,))
    count = cursor.fetchone()["count"] + 1
    queue_num = data.get("queue_number") or f"Q-{count:02d}"

    cursor.execute("""
        INSERT INTO patient_queue (
            id, queue_number, student_id, student_name, student_initials,
            complaint, time_in_clinic, status, action_text, attended_by,
            created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?
        )
    """, (
        q_id,
        queue_num,
        data["student_id"],
        data["student_name"],
        data["student_initials"],
        data["complaint"],
        data.get("time_in_clinic", "Just arrived"),
        data.get("status", "Waiting"),
        data.get("action_text", "Start visit"),
        data.get("attended_by", ""),
        now,
        now,
    ))
    conn.commit()
    cursor.execute("SELECT * FROM patient_queue WHERE id = ?", (q_id,))
    return cursor.fetchone()


def get_queue_items(conn: sqlite3.Connection, status_filter: Optional[str] = None) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    query = "SELECT * FROM patient_queue WHERE 1=1"
    params = []
    if status_filter and status_filter.lower() != "all":
        query += " AND LOWER(status) = LOWER(?)"
        params.append(status_filter)
    query += " ORDER BY created_at ASC"
    cursor.execute(query, tuple(params))
    return cursor.fetchall()


def update_queue_item_status(
    conn: sqlite3.Connection,
    queue_id: str,
    new_status: str,
    attended_by: Optional[str] = None
) -> Optional[sqlite3.Row]:
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE patient_queue
        SET status = ?, attended_by = COALESCE(?, attended_by), updated_at = ?
        WHERE id = ?
    """, (new_status, attended_by, now, queue_id))
    conn.commit()
    cursor.execute("SELECT * FROM patient_queue WHERE id = ?", (queue_id,))
    return cursor.fetchone()


def delete_queue_item(conn: sqlite3.Connection, queue_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patient_queue WHERE id = ?", (queue_id,))
    conn.commit()
    return cursor.rowcount > 0


# =========================================================================
# CLINIC VISITS CRUD FUNCTIONS
# =========================================================================

def create_clinic_visit(conn: sqlite3.Connection, data: dict) -> sqlite3.Row:
    visit_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clinic_visits (
            id, student_id, student_name, date, month_year, title,
            type, time, assessment, intervention, disposition,
            clinic_note, status, attended_by, created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?,
            ?, ?, ?, ?, ?
        )
    """, (
        visit_id,
        data["student_id"],
        data["student_name"],
        data["date"],
        data["month_year"],
        data["title"],
        data.get("type", "consultation"),
        data["time"],
        data["assessment"],
        data["intervention"],
        data["disposition"],
        data.get("clinic_note", ""),
        data.get("status", "Completed"),
        data.get("attended_by", ""),
        now,
        now,
    ))
    conn.commit()
    cursor.execute("SELECT * FROM clinic_visits WHERE id = ?", (visit_id,))
    return cursor.fetchone()


def get_clinic_visits(conn: sqlite3.Connection, student_id: Optional[str] = None) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    if student_id:
        cursor.execute("SELECT * FROM clinic_visits WHERE LOWER(student_id) = LOWER(?) ORDER BY created_at DESC", (student_id,))
    else:
        cursor.execute("SELECT * FROM clinic_visits ORDER BY created_at DESC")
    return cursor.fetchall()


# =========================================================================
# FIRST AID REPORTS (CRRMU) CRUD FUNCTIONS
# =========================================================================

def create_first_aid_report(conn: sqlite3.Connection, data: dict) -> sqlite3.Row:
    report_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO first_aid_reports (
            id, date, time, patient_name, patient_role, location,
            incident_type, treatment, responder, status,
            reviewed_by, reviewed_at, created_at, updated_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?,
            ?, ?, ?, ?
        )
    """, (
        report_id,
        data["date"],
        data["time"],
        data["patient_name"],
        data.get("patient_role", "Student"),
        data["location"],
        data["incident_type"],
        data["treatment"],
        data["responder"],
        data.get("status", "Submitted"),
        "",
        "",
        now,
        now,
    ))
    conn.commit()
    cursor.execute("SELECT * FROM first_aid_reports WHERE id = ?", (report_id,))
    return cursor.fetchone()


def get_first_aid_reports(conn: sqlite3.Connection, status_filter: Optional[str] = None) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    if status_filter and status_filter.lower() != "all":
        cursor.execute("SELECT * FROM first_aid_reports WHERE LOWER(status) = LOWER(?) ORDER BY created_at DESC", (status_filter,))
    else:
        cursor.execute("SELECT * FROM first_aid_reports ORDER BY created_at DESC")
    return cursor.fetchall()


def update_first_aid_report_status(
    conn: sqlite3.Connection,
    report_id: str,
    new_status: str,
    reviewed_by: Optional[str] = None
) -> Optional[sqlite3.Row]:
    now = datetime.now(timezone.utc).isoformat()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE first_aid_reports
        SET status = ?, reviewed_by = ?, reviewed_at = ?, updated_at = ?
        WHERE id = ?
    """, (new_status, reviewed_by or "", now, now, report_id))
    conn.commit()
    cursor.execute("SELECT * FROM first_aid_reports WHERE id = ?", (report_id,))
    return cursor.fetchone()


# =========================================================================
# NOTIFICATIONS CRUD FUNCTIONS
# =========================================================================

def create_notification(
    conn: sqlite3.Connection,
    user_id: str,
    title: str,
    message: str,
    notif_type: str = "confirmation",
    category: str = "appointment",
    action_text: str = "",
    action_href: str = ""
) -> sqlite3.Row:
    notif_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).isoformat()
    time_str = "Just now"
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO notifications (
            id, user_id, title, message, time, type,
            category, read, action_text, action_href, created_at
        ) VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, 0, ?, ?, ?
        )
    """, (notif_id, user_id, title, message, time_str, notif_type, category, action_text, action_href, now))
    conn.commit()
    cursor.execute("SELECT * FROM notifications WHERE id = ?", (notif_id,))
    return cursor.fetchone()


def get_notifications(conn: sqlite3.Connection, user_id: str) -> List[sqlite3.Row]:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY created_at DESC LIMIT 50", (user_id,))
    return cursor.fetchall()


def mark_all_notifications_read(conn: sqlite3.Connection, user_id: str) -> bool:
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET read = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    return True


# =========================================================================
# DASHBOARD METRICS QUERY FUNCTION
# =========================================================================

def get_dashboard_metrics(conn: sqlite3.Connection, user_id: str, is_staff: bool) -> dict:
    cursor = conn.cursor()
    now_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    # Appointments count
    cursor.execute("SELECT COUNT(*) as cnt FROM appointments WHERE date = ?", (now_date,))
    today_appointments = cursor.fetchone()["cnt"]

    cursor.execute("SELECT COUNT(*) as cnt FROM appointments WHERE status = 'Confirmed' OR status = 'Pending'")
    active_appointments = cursor.fetchone()["cnt"]

    # Queue count
    cursor.execute("SELECT COUNT(*) as cnt FROM patient_queue WHERE status = 'Waiting'")
    waiting_queue = cursor.fetchone()["cnt"]

    # In consultation
    cursor.execute("SELECT COUNT(*) as cnt FROM patient_queue WHERE status = 'In Consultation' OR status = 'Under Observation'")
    in_consultation = cursor.fetchone()["cnt"]

    # Active clinic visits
    cursor.execute("SELECT COUNT(*) as cnt FROM clinic_visits WHERE status = 'Completed'")
    total_visits = cursor.fetchone()["cnt"]

    # Pending CRRMU reports
    cursor.execute("SELECT COUNT(*) as cnt FROM first_aid_reports WHERE status = 'Submitted'")
    pending_crrmu = cursor.fetchone()["cnt"]

    # Registered students
    cursor.execute("SELECT COUNT(*) as cnt FROM users WHERE category = 'student'")
    total_students = cursor.fetchone()["cnt"]

    return {
        "today_appointments": today_appointments,
        "active_appointments": active_appointments,
        "waiting_queue": waiting_queue,
        "in_consultation": in_consultation,
        "total_visits": total_visits,
        "pending_crrmu": pending_crrmu,
        "total_students": total_students,
    }
