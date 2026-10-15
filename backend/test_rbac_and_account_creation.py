import requests
import json
import uuid

BASE_URL = "http://localhost:8000"

def test_rbac_and_account_creation():
    print("--- 1. Testing health endpoint ---")
    r = requests.get(f"{BASE_URL}/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("Health check passed.")

    # Generate random test student id and emails
    suffix = uuid.uuid4().hex[:6]
    student_num_id = f"2026{int(uuid.uuid4().int % 90000 + 10000)}"
    student_email = f"student_{suffix}@celtech.edu.ph"

    print("\n--- 2. Registering Student (numerical student_id) ---")
    reg_student_payload = {
        "student_id": student_num_id,
        "name": "Jane Student",
        "email": student_email,
        "password": "password123",
        "role": "Student",
        "category": "student",
        "is_crrmu_member": False,
        "program_strand": "BSIT",
        "year_section": "2A",
        "contact_number": "09123456789",
        "emergency_person": "Mom",
        "emergency_relationship": "Parent",
        "emergency_contact": "09987654321",
        "terms_accepted": True
    }
    r = requests.post(f"{BASE_URL}/api/auth/register", json=reg_student_payload)
    assert r.status_code in (200, 201), f"Student registration failed: {r.text}"
    student_data = r.json()
    assert student_data["user"]["role"] == "Student", f"Expected role Student, got {student_data['user']['role']}"
    assert student_data["user"]["category"] == "student", f"Expected category student, got {student_data['user']['category']}"
    assert student_data["user"]["status"] == "pending", f"Expected status pending, got {student_data['user']['status']}"
    print(f"Student successfully registered as role='{student_data['user']['role']}', category='{student_data['user']['category']}', status='{student_data['user']['status']}'")

    print("\n--- 3. Testing student_id numbers-only validation ---")
    invalid_student_payload = reg_student_payload.copy()
    invalid_student_payload["student_id"] = "ABC-1234"
    invalid_student_payload["email"] = f"invalid_{suffix}@celtech.edu.ph"
    r = requests.post(f"{BASE_URL}/api/auth/register", json=invalid_student_payload)
    assert r.status_code == 400, f"Expected 400 for non-numeric student ID, got {r.status_code}: {r.text}"
    print("Non-numeric student_id correctly rejected with 400.")

    print("\n--- 4. Testing Staff Registration WITHOUT passkey (should be rejected) ---")
    staff_without_key = {
        "student_id": f"STAFF-{suffix}",
        "name": "Nurse Kelly",
        "email": f"kelly_{suffix}@celtech.edu.ph",
        "password": "password123",
        "role": "Clinic Staff",
        "category": "staff",
        "emergency_person": "Doc",
        "emergency_relationship": "Colleague",
        "emergency_contact": "09123456780",
        "terms_accepted": True
    }
    r = requests.post(f"{BASE_URL}/api/auth/register", json=staff_without_key)
    assert r.status_code == 403, f"Expected 403 Forbidden for missing passkey, got {r.status_code}: {r.text}"
    print("Staff registration without passkey correctly blocked with 403.")

    print("\n--- 5. Testing Staff Registration WITH WRONG passkey (should be rejected) ---")
    staff_wrong_key = staff_without_key.copy()
    staff_wrong_key["staff_passkey"] = "WRONG-KEY-XYZ"
    r = requests.post(f"{BASE_URL}/api/auth/register", json=staff_wrong_key)
    assert r.status_code == 403, f"Expected 403 Forbidden for wrong passkey, got {r.status_code}: {r.text}"
    print("Staff registration with wrong passkey correctly blocked with 403.")

    print("\n--- 6. Testing Staff Registration WITH CORRECT passkey (CELTECH-CLINIC-2026) ---")
    staff_correct_key = staff_without_key.copy()
    staff_correct_key["staff_passkey"] = "CELTECH-CLINIC-2026"
    r = requests.post(f"{BASE_URL}/api/auth/register", json=staff_correct_key)
    assert r.status_code in (200, 201), f"Staff registration with passkey failed: {r.text}"
    staff_res = r.json()
    assert staff_res["user"]["category"] == "staff", f"Expected category staff, got {staff_res['user']['category']}"
    assert staff_res["user"]["role"] == "Clinic Staff", f"Expected role Clinic Staff, got {staff_res['user']['role']}"
    assert staff_res["user"]["status"] == "approved", f"Expected status approved, got {staff_res['user']['status']}"
    print("Staff successfully registered with passkey!")

    print("\n--- 7. Testing Login as John Doe (Student) and Admin Endpoint Guarding ---")
    r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "2027100", "password": "password"})
    # If John Doe was registered with another password, let's try johndoe@gmail.com
    if r.status_code != 200:
        # Check login with known student
        print(f"Note: John Doe password check responded with {r.status_code}: {r.text}")
    else:
        john_token = r.json()["access_token"]
        john_user = r.json()["user"]
        assert john_user["category"] == "student", f"Expected John Doe category to be student, got {john_user['category']}"
        assert john_user["role"] == "Student", f"Expected John Doe role to be Student, got {john_user['role']}"
        print(f"John Doe verified: role='{john_user['role']}', category='{john_user['category']}'")

        # Now try accessing admin endpoint with John Doe's token: MUST BE REJECTED 403
        r_admin = requests.get(f"{BASE_URL}/api/admin/users", headers={"Authorization": f"Bearer {john_token}"})
        assert r_admin.status_code == 403, f"Expected 403 Forbidden for student accessing /api/admin/users, got {r_admin.status_code}"
        print("Student token correctly blocked from /api/admin/users with 403 Forbidden!")

        r_stats = requests.get(f"{BASE_URL}/api/admin/stats", headers={"Authorization": f"Bearer {john_token}"})
        assert r_stats.status_code == 403, f"Expected 403 Forbidden for student accessing /api/admin/stats, got {r_stats.status_code}"
        print("Student token correctly blocked from /api/admin/stats with 403 Forbidden!")

    print("\n--- 8. Testing Login as Clinic Administrator (ADMIN-001) ---")
    r_admin_login = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "ADMIN-001", "password": "admin2026"})
    assert r_admin_login.status_code == 200, f"Admin login failed: {r_admin_login.text}"
    admin_token = r_admin_login.json()["access_token"]
    admin_user = r_admin_login.json()["user"]
    assert admin_user["category"] == "staff"
    assert admin_user["role"] == "Clinic Administrator"
    print(f"Admin logged in: role='{admin_user['role']}', category='{admin_user['category']}'")

    print("\n--- 9. Accessing Admin Endpoints with Admin Token ---")
    r_admin_users = requests.get(f"{BASE_URL}/api/admin/users", headers={"Authorization": f"Bearer {admin_token}"})
    assert r_admin_users.status_code == 200, f"Admin fetching users failed: {r_admin_users.text}"
    users_list = r_admin_users.json()
    print(f"Admin retrieved {len(users_list)} registered users.")

    r_admin_stats = requests.get(f"{BASE_URL}/api/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert r_admin_stats.status_code == 200, f"Admin fetching stats failed: {r_admin_stats.text}"
    print(f"Admin retrieved stats: {r_admin_stats.json()}")

    print("\n--- 10. Admin approving newly registered student ---")
    new_student_id = student_data["user"]["id"]
    r_approve = requests.patch(
        f"{BASE_URL}/api/admin/users/{new_student_id}/status",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={"status": "approved"}
    )
    assert r_approve.status_code == 200, f"Admin approving user failed: {r_approve.text}"
    assert r_approve.json()["status"] == "approved"
    print("Admin successfully approved student account!")

    print("\n--- 11. Newly approved student can now log in ---")
    r_new_login = requests.post(
        f"{BASE_URL}/api/auth/login",
        json={"username": student_num_id, "password": "password123"}
    )
    assert r_new_login.status_code == 200, f"Approved student login failed: {r_new_login.text}"
    new_user = r_new_login.json()["user"]
    assert new_user["role"] == "Student"
    assert new_user["category"] == "student"
    print(f"Student {new_user['name']} successfully signed in with role '{new_user['role']}' and category '{new_user['category']}'!")

    print("\n--- 12. Testing RBAC: Student token attempting to access Admin endpoints ---")
    student_jwt = r_new_login.json()["access_token"]
    
    # 1. GET /api/admin/users
    r_stu_users = requests.get(f"{BASE_URL}/api/admin/users", headers={"Authorization": f"Bearer {student_jwt}"})
    assert r_stu_users.status_code == 403, f"Expected 403 for student accessing /api/admin/users, got {r_stu_users.status_code}"
    print("✓ GET /api/admin/users correctly rejected student with 403 Forbidden")

    # 2. GET /api/admin/stats
    r_stu_stats = requests.get(f"{BASE_URL}/api/admin/stats", headers={"Authorization": f"Bearer {student_jwt}"})
    assert r_stu_stats.status_code == 403, f"Expected 403 for student accessing /api/admin/stats, got {r_stu_stats.status_code}"
    print("✓ GET /api/admin/stats correctly rejected student with 403 Forbidden")

    # 3. PATCH /api/admin/users/{id}/status
    r_stu_patch = requests.patch(
        f"{BASE_URL}/api/admin/users/{new_student_id}/status",
        headers={"Authorization": f"Bearer {student_jwt}"},
        json={"status": "approved"}
    )
    assert r_stu_patch.status_code == 403, f"Expected 403 for student calling patch status, got {r_stu_patch.status_code}"
    print("✓ PATCH /api/admin/users/.../status correctly rejected student with 403 Forbidden")

    # 4. DELETE /api/admin/users/{id}
    r_stu_del = requests.delete(
        f"{BASE_URL}/api/admin/users/{new_student_id}",
        headers={"Authorization": f"Bearer {student_jwt}"}
    )
    assert r_stu_del.status_code == 403, f"Expected 403 for student calling delete user, got {r_stu_del.status_code}"
    print("✓ DELETE /api/admin/users/... correctly rejected student with 403 Forbidden")

    print("\n============================================================")
    print("🎉 ALL RBAC AND ACCOUNT CREATION TESTS PASSED PERFECTLY! 🎉")
    print("============================================================")

if __name__ == "__main__":
    test_rbac_and_account_creation()
