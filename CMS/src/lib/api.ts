import type { DemoAccount } from './types';

const API_BASE = 'http://localhost:8000';

export interface AuthResponse {
	access_token: string;
	token_type: string;
	user: DemoAccount;
}

export interface RegisterPayload {
	student_id: string;
	email: string;
	password: string;
	name: string;
	first_name?: string;
	role?: string;
	category?: 'student' | 'staff';
	is_crrmu_member?: boolean;
	program_strand?: string;
	year_section?: string;
	contact_number?: string;
	address?: string;
	emergency_person?: string;
	emergency_relationship?: string;
	emergency_contact?: string;
	preferred_contact_method?: string;
	terms_accepted?: boolean;
}

export function getStoredToken(): string | null {
	if (typeof window === 'undefined') return null;
	return localStorage.getItem('cshms_token');
}

export function setStoredToken(token: string | null) {
	if (typeof window === 'undefined') return;
	if (token) {
		localStorage.setItem('cshms_token', token);
	} else {
		localStorage.removeItem('cshms_token');
	}
}

export async function loginWithApi(username: string, password: string): Promise<AuthResponse> {
	const res = await fetch(`${API_BASE}/api/auth/login`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify({ username, password })
	});

	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Authentication failed' }));
		throw new Error(err.detail || 'Failed to sign in');
	}

	const data: AuthResponse = await res.json();
	setStoredToken(data.access_token);
	return data;
}

export async function registerWithApi(payload: RegisterPayload): Promise<AuthResponse> {
	const res = await fetch(`${API_BASE}/api/auth/register`, {
		method: 'POST',
		headers: { 'Content-Type': 'application/json' },
		body: JSON.stringify(payload)
	});

	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Registration failed' }));
		throw new Error(err.detail || 'Failed to register');
	}

	const data: AuthResponse = await res.json();
	setStoredToken(data.access_token);
	return data;
}

export async function fetchCurrentUser(): Promise<DemoAccount | null> {
	const token = getStoredToken();
	if (!token) return null;

	const res = await fetch(`${API_BASE}/api/auth/me`, {
		headers: { Authorization: `Bearer ${token}` }
	});

	if (!res.ok) {
		setStoredToken(null);
		return null;
	}

	return await res.json();
}

export async function checkBackendHealth(): Promise<{ status: string; database: string } | null> {
	try {
		const res = await fetch(`${API_BASE}/api/health`, { signal: AbortSignal.timeout(1500) });
		if (!res.ok) return null;
		return await res.json();
	} catch {
		return null;
	}
}

export function logoutApi() {
	setStoredToken(null);
}

// =========================================================================
// ADMIN API CLIENT FUNCTIONS
// =========================================================================

export async function fetchAdminUsers(statusFilter: string = 'all'): Promise<DemoAccount[]> {
	const token = getStoredToken();
	const headers: Record<string, string> = {};
	if (token) headers['Authorization'] = `Bearer ${token}`;

	const url = statusFilter && statusFilter !== 'all' 
		? `${API_BASE}/api/admin/users?status=${encodeURIComponent(statusFilter)}`
		: `${API_BASE}/api/admin/users`;

	const res = await fetch(url, { headers });
	if (!res.ok) {
		throw new Error('Failed to load registered users');
	}
	return await res.json();
}

export async function updateUserStatus(userId: string, status: 'pending' | 'approved' | 'rejected'): Promise<DemoAccount> {
	const token = getStoredToken();
	const headers: Record<string, string> = { 'Content-Type': 'application/json' };
	if (token) headers['Authorization'] = `Bearer ${token}`;

	const res = await fetch(`${API_BASE}/api/admin/users/${encodeURIComponent(userId)}/status`, {
		method: 'PATCH',
		headers,
		body: JSON.stringify({ status })
	});

	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Failed to update status' }));
		throw new Error(err.detail || 'Failed to update status');
	}
	return await res.json();
}

export async function deleteUser(userId: string): Promise<void> {
	const token = getStoredToken();
	const headers: Record<string, string> = {};
	if (token) headers['Authorization'] = `Bearer ${token}`;

	const res = await fetch(`${API_BASE}/api/admin/users/${encodeURIComponent(userId)}`, {
		method: 'DELETE',
		headers
	});

	if (!res.ok) {
		const err = await res.json().catch(() => ({ detail: 'Failed to delete user' }));
		throw new Error(err.detail || 'Failed to delete user');
	}
}

export async function fetchAdminStats(): Promise<{ total: number; pending: number; approved: number; rejected: number }> {
	const res = await fetch(`${API_BASE}/api/admin/stats`);
	if (!res.ok) {
		throw new Error('Failed to fetch admin stats');
	}
	return await res.json();
}
