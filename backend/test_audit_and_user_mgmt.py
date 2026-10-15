import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_user_management_and_audit_logs():
    print("--- 1. Login as Clinic Administrator (ADMIN-001) ---")
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "ADMIN-001", "password": "admin2026"})
    assert r.status_code == 200, f"Admin login failed: {r.text}"
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("Admin login successful.")

    # Unique test IDs
    uid_suffix = uuid.uuid4().hex[:6]
    test_nurse_id = f"NURSE-{uid_suffix}"
    test_nurse_email = f"nurse_{uid_suffix}@celtech.edu.ph"

    print("\n--- 2. Admin creates a new Nurse account ---")
    create_payload = {
        "student_id": test_nurse_id,
        "name": f"Nurse Joyce {uid_suffix}",
        "email": test_nurse_email,
        "password": "tempPassword123",
        "role": "Clinic Staff",
        "category": "staff",
        "program_strand": "School Clinic Operations",
        "year_section": "Nursing Unit",
        "contact_number": "0917-111-2222",
        "status": "approved"
    }
    r = requests.post(f"{BASE_URL}/api/admin/users", headers=admin_headers, json=create_payload)
    assert r.status_code == 201, f"Failed to create user: {r.text}"
    created_nurse = r.json()
    nurse_user_id = created_nurse["id"]
    print(f"Created Nurse account: {created_nurse['name']} ({created_nurse['studentId']}, Role: {created_nurse['role']}, Category: {created_nurse['category']})")

    print("\n--- 3. Verify Audit Log for ADMIN_CREATED_USER ---")
    r = requests.get(f"{BASE_URL}/api/admin/audit-logs", headers=admin_headers, params={"action": "ADMIN_CREATED_USER"})
    assert r.status_code == 200, f"Failed to fetch audit logs: {r.text}"
    logs = r.json()
    assert len(logs) > 0, "No audit logs found for ADMIN_CREATED_USER"
    matching = [l for l in logs if l["targetUserId"] == nurse_user_id]
    assert len(matching) > 0, "Audit log did not record the nurse creation event"
    print(f"Audit log found: {matching[0]['action']} - {matching[0]['details']}")

    print("\n--- 4. Admin updates user role (e.g. changing role to Head Nurse / Clinic Administrator) ---")
    update_payload = {
        "role": "Clinic Administrator",
        "program_strand": "Chief Healthcare Administration"
    }
    r = requests.put(f"{BASE_URL}/api/admin/users/{nurse_user_id}", headers=admin_headers, json=update_payload)
    assert r.status_code == 200, f"Failed to update user role: {r.text}"
    updated_nurse = r.json()
    assert updated_nurse["role"] == "Clinic Administrator"
    print(f"Role updated successfully to '{updated_nurse['role']}'")

    print("\n--- 5. Verify Audit Log for ROLE_UPDATED ---")
    r = requests.get(f"{BASE_URL}/api/admin/audit-logs", headers=admin_headers, params={"action": "ROLE_UPDATED"})
    assert r.status_code == 200
    matching_role = [l for l in r.json() if l["targetUserId"] == nurse_user_id]
    assert len(matching_role) > 0, "Audit log did not record ROLE_UPDATED event"
    print(f"Audit log found: {matching_role[0]['action']} - {matching_role[0]['details']}")

    print("\n--- 6. Admin resets password for user ---")
    new_pw = "newNursePass2026"
    r = requests.post(
        f"{BASE_URL}/api/admin/users/{nurse_user_id}/reset-password",
        headers=admin_headers,
        json={"new_password": new_pw}
    )
    assert r.status_code == 200, f"Failed to reset password: {r.text}"
    print(f"Password reset response: {r.json()['message']}")

    print("\n--- 7. Verify Audit Log for PASSWORD_RESET ---")
    r = requests.get(f"{BASE_URL}/api/admin/audit-logs", headers=admin_headers, params={"action": "PASSWORD_RESET"})
    assert r.status_code == 200
    matching_pw = [l for l in r.json() if l["targetUserId"] == nurse_user_id]
    assert len(matching_pw) > 0, "Audit log did not record PASSWORD_RESET event"
    print(f"Audit log found: {matching_pw[0]['action']} - {matching_pw[0]['details']}")

    print("\n--- 8. User logs in with newly reset password ---")
    r_login = requests.post(f"{BASE_URL}/api/auth/login", json={"username": test_nurse_id, "password": new_pw})
    assert r_login.status_code == 200, f"Login with reset password failed: {r_login.text}"
    print("User successfully logged in with new password!")

    print("\n--- 9. Admin deletes the test user ---")
    r_del = requests.delete(f"{BASE_URL}/api/admin/users/{nurse_user_id}", headers=admin_headers)
    assert r_del.status_code == 200, f"Delete user failed: {r_del.text}"
    print(f"Deleted user response: {r_del.json()['message']}")

    print("\n--- 10. Verify Audit Log for USER_DELETED ---")
    r = requests.get(f"{BASE_URL}/api/admin/audit-logs", headers=admin_headers, params={"action": "USER_DELETED"})
    assert r.status_code == 200
    matching_del = [l for l in r.json() if l["targetUserId"] == nurse_user_id]
    assert len(matching_del) > 0, "Audit log did not record USER_DELETED event"
    print(f"Audit log found: {matching_del[0]['action']} - {matching_del[0]['details']}")

    print("\n==================================================================")
    print("🎉 ALL USER MANAGEMENT AND AUDIT LOG TESTS PASSED SUCCESSFULLY! 🎉")
    print("==================================================================")

if __name__ == "__main__":
    test_user_management_and_audit_logs()
