<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import {
		fetchAdminUsers,
		updateUserStatus,
		deleteUser,
		fetchAdminStats,
		checkBackendHealth,
		createUserByAdmin,
		updateUserByAdmin,
		resetUserPasswordByAdmin,
		fetchAuditLogs
	} from '#lib/api';
	import type { DemoAccount, AuditLogItem } from '#lib/types';

	// Main tab
	let activeTab = $state<'users' | 'audit'>('users');

	// Users state
	let users = $state<DemoAccount[]>([]);
	let isLoading = $state(true);
	let isBackendOnline = $state<boolean | null>(null);
	let errorMessage = $state('');
	let toastMessage = $state('');
	let toastType = $state<'success' | 'error'>('success');

	// Filters & Search
	let statusFilter = $state<'all' | 'pending' | 'approved' | 'rejected'>('all');
	let searchQuery = $state('');
	let roleFilter = $state<'all' | 'admin' | 'staff' | 'crrmu' | 'student'>('all');

	// Audit Logs state
	let auditLogs = $state<AuditLogItem[]>([]);
	let isLoadingAudit = $state(false);
	let auditCategoryFilter = $state<string>('all');
	let auditSearchQuery = $state('');

	// Action in-flight states
	let updatingUserId = $state<string | null>(null);
	let deletingUserId = $state<string | null>(null);
	let isSubmittingModal = $state(false);

	// Modals
	let selectedUser = $state<DemoAccount | null>(null);
	let showDetailModal = $state(false);

	let showCreateModal = $state(false);
	let createUserData = $state({
		student_id: '',
		name: '',
		email: '',
		password: '',
		role: 'Student',
		program_strand: 'BSIT',
		year_section: '1A',
		contact_number: '',
		emergency_person: '',
		emergency_relationship: 'Parent',
		emergency_contact: '',
		status: 'approved' as 'approved' | 'pending'
	});

	let showEditModal = $state(false);
	let editingUser = $state<DemoAccount | null>(null);
	let editUserData = $state({
		name: '',
		student_id: '',
		email: '',
		role: 'Student',
		program_strand: '',
		year_section: '',
		contact_number: '',
		status: 'approved' as 'approved' | 'pending' | 'rejected',
		emergency_person: '',
		emergency_contact: ''
	});

	let showResetModal = $state(false);
	let resettingUser = $state<DemoAccount | null>(null);
	let newPasswordInput = $state('');

	// Stats
	let stats = $state({
		total: 0,
		pending: 0,
		approved: 0,
		rejected: 0
	});

	function showToast(msg: string, type: 'success' | 'error' = 'success') {
		toastMessage = msg;
		toastType = type;
		setTimeout(() => {
			toastMessage = '';
		}, 3500);
	}

	async function loadData() {
		isLoading = true;
		errorMessage = '';
		try {
			const health = await checkBackendHealth();
			isBackendOnline = health !== null;

			if (isBackendOnline) {
				const [fetchedUsers, fetchedStats] = await Promise.all([
					fetchAdminUsers('all'),
					fetchAdminStats()
				]);
				users = fetchedUsers;
				stats = fetchedStats;
				clinicStore.setPendingUsersCount(fetchedStats.pending);
			} else {
				users = [];
				recalcLocalStats();
			}
		} catch (err: any) {
			console.warn('Admin load error', err);
			users = [];
			recalcLocalStats();
		} finally {
			isLoading = false;
		}
	}

	async function loadAuditLogsData() {
		isLoadingAudit = true;
		try {
			if (isBackendOnline) {
				auditLogs = await fetchAuditLogs({
					category: auditCategoryFilter !== 'all' ? auditCategoryFilter : undefined,
					search: auditSearchQuery
				});
			}
		} catch (err) {
			console.warn('Audit logs load error', err);
		} finally {
			isLoadingAudit = false;
		}
	}

	function recalcLocalStats() {
		const total = users.length;
		const pending = users.filter((u) => u.status === 'pending').length;
		const approved = users.filter((u) => u.status === 'approved').length;
		const rejected = users.filter((u) => u.status === 'rejected').length;
		stats = { total, pending, approved, rejected };
		clinicStore.setPendingUsersCount(pending);
	}

	onMount(() => {
		if (clinicStore.isLoggedIn && clinicStore.currentUser.category !== 'staff') {
			goto('/dashboard');
			return;
		}
		loadData();
	});

	// Quick status change
	async function handleStatusChange(userId: string, newStatus: 'approved' | 'rejected') {
		updatingUserId = userId;
		try {
			if (isBackendOnline) {
				const updated = await updateUserStatus(userId, newStatus);
				users = users.map((u) => (u.id === userId ? { ...u, status: updated.status } : u));
				const newStats = await fetchAdminStats();
				stats = newStats;
				clinicStore.setPendingUsersCount(newStats.pending);
			} else {
				users = users.map((u) => (u.id === userId ? { ...u, status: newStatus } : u));
				recalcLocalStats();
			}

			if (selectedUser && selectedUser.id === userId) {
				selectedUser = { ...selectedUser, status: newStatus };
			}

			showToast(
				newStatus === 'approved'
					? `Account for ${selectedUser?.name || 'user'} approved! They can now log in.`
					: `Account for ${selectedUser?.name || 'user'} was rejected.`,
				'success'
			);
		} catch (err: any) {
			showToast(err.message || 'Failed to update user status.', 'error');
		} finally {
			updatingUserId = null;
		}
	}

	// Delete user
	async function handleDeleteUser(userId: string, userName: string) {
		if (clinicStore.currentUser.id === userId) {
			showToast('Cannot delete your own logged-in administrator account.', 'error');
			return;
		}

		if (!confirm(`Are you sure you want to permanently delete user "${userName}"? This cannot be undone.`)) {
			return;
		}

		deletingUserId = userId;
		try {
			if (isBackendOnline) {
				await deleteUser(userId);
			}
			users = users.filter((u) => u.id !== userId);
			if (isBackendOnline) {
				const newStats = await fetchAdminStats();
				stats = newStats;
				clinicStore.setPendingUsersCount(newStats.pending);
			} else {
				recalcLocalStats();
			}

			if (selectedUser?.id === userId) {
				showDetailModal = false;
				selectedUser = null;
			}

			showToast(`User "${userName}" was permanently removed.`, 'success');
		} catch (err: any) {
			showToast(err.message || 'Failed to delete user.', 'error');
		} finally {
			deletingUserId = null;
		}
	}

	// Open Edit Modal
	function openEditModal(user: DemoAccount) {
		editingUser = user;
		editUserData = {
			name: user.name,
			student_id: user.studentId,
			email: user.email,
			role: user.role,
			program_strand: user.programStrand || '',
			year_section: user.yearSection || '',
			contact_number: user.contactNumber || '',
			status: user.status || 'approved',
			emergency_person: user.emergencyPerson || '',
			emergency_contact: user.emergencyContact || ''
		};
		showEditModal = true;
	}

	// Save Edit User
	async function handleSaveEditUser(e: SubmitEvent) {
		e.preventDefault();
		if (!editingUser) return;
		isSubmittingModal = true;
		try {
			const updated = await updateUserByAdmin(editingUser.id, editUserData);
			users = users.map((u) => (u.id === editingUser!.id ? updated : u));
			if (selectedUser?.id === editingUser.id) {
				selectedUser = updated;
			}
			showEditModal = false;
			showToast(`Account & role for ${updated.name} updated successfully!`, 'success');
		} catch (err: any) {
			showToast(err.message || 'Failed to update user account.', 'error');
		} finally {
			isSubmittingModal = false;
		}
	}

	// Open Reset Password Modal
	function openResetModal(user: DemoAccount) {
		resettingUser = user;
		newPasswordInput = '';
		showResetModal = true;
	}

	// Save Reset Password
	async function handleResetPassword(e: SubmitEvent) {
		e.preventDefault();
		if (!resettingUser) return;
		if (newPasswordInput.length < 6) {
			showToast('Password must be at least 6 characters.', 'error');
			return;
		}

		isSubmittingModal = true;
		try {
			await resetUserPasswordByAdmin(resettingUser.id, newPasswordInput);
			showResetModal = false;
			showToast(`Password for ${resettingUser.name} reset successfully!`, 'success');
		} catch (err: any) {
			showToast(err.message || 'Failed to reset password.', 'error');
		} finally {
			isSubmittingModal = false;
		}
	}

	// Create New User
	async function handleCreateUser(e: SubmitEvent) {
		e.preventDefault();
		isSubmittingModal = true;
		try {
			const created = await createUserByAdmin(createUserData);
			users = [created, ...users];
			const newStats = await fetchAdminStats();
			stats = newStats;
			clinicStore.setPendingUsersCount(newStats.pending);
			showCreateModal = false;
			showToast(`New ${created.role} account created for ${created.name}!`, 'success');
			// Reset form
			createUserData = {
				student_id: '',
				name: '',
				email: '',
				password: '',
				role: 'Student',
				program_strand: 'BSIT',
				year_section: '1A',
				contact_number: '',
				emergency_person: '',
				emergency_relationship: 'Parent',
				emergency_contact: '',
				status: 'approved'
			};
		} catch (err: any) {
			showToast(err.message || 'Failed to create user.', 'error');
		} finally {
			isSubmittingModal = false;
		}
	}

	function openDetails(user: DemoAccount) {
		selectedUser = user;
		showDetailModal = true;
	}

	function getRoleBadge(user: DemoAccount) {
		const r = user.role.toLowerCase();
		if (r.includes('admin')) {
			return { label: user.role || 'Clinic Administrator', bg: 'bg-purple-100 text-purple-900 border-purple-200' };
		}
		if (user.category === 'staff' || r.includes('staff') || r.includes('nurse') || r.includes('doctor')) {
			return { label: user.role || 'Clinic Staff', bg: 'bg-emerald-100 text-emerald-900 border-emerald-200' };
		}
		if (user.isCrrmuMember || r.includes('crrmu')) {
			return { label: 'CRRMU Responder', bg: 'bg-blue-100 text-blue-900 border-blue-200' };
		}
		return { label: 'Student', bg: 'bg-gray-100 text-gray-800 border-gray-200' };
	}

	// Derived user list with filtering
	let filteredUsers = $derived.by(() => {
		let list = users;

		// Status filter
		if (statusFilter !== 'all') {
			list = list.filter((u) => (u.status || 'approved') === statusFilter);
		}

		// Role filter
		if (roleFilter === 'admin') {
			list = list.filter((u) => u.role.toLowerCase().includes('admin'));
		} else if (roleFilter === 'staff') {
			list = list.filter((u) => u.category === 'staff' && !u.role.toLowerCase().includes('admin'));
		} else if (roleFilter === 'crrmu') {
			list = list.filter((u) => u.isCrrmuMember || u.role.toLowerCase().includes('crrmu'));
		} else if (roleFilter === 'student') {
			list = list.filter((u) => u.category === 'student' && !u.isCrrmuMember);
		}

		// Search filter
		if (searchQuery.trim()) {
			const q = searchQuery.toLowerCase().trim();
			list = list.filter(
				(u) =>
					u.name.toLowerCase().includes(q) ||
					u.studentId.toLowerCase().includes(q) ||
					u.email.toLowerCase().includes(q) ||
					(u.programStrand && u.programStrand.toLowerCase().includes(q)) ||
					(u.role && u.role.toLowerCase().includes(q)) ||
					(u.emergencyPerson && u.emergencyPerson.toLowerCase().includes(q))
			);
		}

		return list;
	});

	let filteredAuditLogs = $derived.by(() => {
		let list = auditLogs;
		if (auditCategoryFilter !== 'all') {
			list = list.filter((l) => l.category === auditCategoryFilter);
		}
		if (auditSearchQuery.trim()) {
			const q = auditSearchQuery.toLowerCase().trim();
			list = list.filter(
				(l) =>
					l.details.toLowerCase().includes(q) ||
					l.actorName.toLowerCase().includes(q) ||
					(l.targetUserName && l.targetUserName.toLowerCase().includes(q)) ||
					l.action.toLowerCase().includes(q)
			);
		}
		return list;
	});
</script>

<svelte:head>
	<title>User Management & Audit Logs - Clinic Admin - CSHMS</title>
</svelte:head>

<div class="space-y-8">

	<!-- Toast Notification -->
	{#if toastMessage}
		<div
			class="fixed bottom-6 right-6 z-50 px-5 py-3.5 rounded-2xl shadow-xl flex items-center space-x-3 text-xs font-semibold animate-fade-in transition-all {toastType === 'success' ? 'bg-[#1b522f] text-white' : 'bg-red-600 text-white'}"
		>
			<svg class="w-4 h-4 shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				{#if toastType === 'success'}
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
				{:else}
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
				{/if}
			</svg>
			<span>{toastMessage}</span>
		</div>
	{/if}

	<!-- Top Admin Header -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
		<div>
			<div class="flex items-center space-x-2 mb-1">
				<p class="text-[10px] font-bold tracking-[0.18em] text-[#1b522f] uppercase">
					ADMINISTRATION & USER GOVERNANCE
				</p>
				{#if isBackendOnline === true}
					<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
						<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
						SQLite Live
					</span>
				{:else if isBackendOnline === false}
					<span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">
						<span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
						Offline Prototype
					</span>
				{/if}
			</div>

			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				User Accounts & Audit Logs
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Manage staff, nurses, CRRMU responders, and student accounts. Review activity audit trails and approve access.
			</p>
		</div>

		<!-- Action Buttons -->
		<div class="flex items-center space-x-3 self-start sm:self-auto">
			<button
				type="button"
				onclick={() => { loadData(); if (activeTab === 'audit') loadAuditLogsData(); }}
				disabled={isLoading}
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-2xl bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 text-xs font-semibold shadow-2xs transition-colors cursor-pointer disabled:opacity-50"
			>
				<svg class="w-4 h-4 text-gray-500 {isLoading ? 'animate-spin' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
				</svg>
				<span>Refresh</span>
			</button>

			<button
				type="button"
				onclick={() => (showCreateModal = true)}
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-2xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-2xs transition-colors cursor-pointer"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
				</svg>
				<span>+ Add New User</span>
			</button>
		</div>
	</div>

	<!-- Navigation Tabs: Users Directory vs Security Audit Logs -->
	<div class="flex items-center space-x-1 p-1 bg-gray-100 rounded-2xl w-fit">
		<button
			type="button"
			onclick={() => (activeTab = 'users')}
			class="px-5 py-2.5 text-xs font-semibold rounded-xl transition-all flex items-center space-x-2 cursor-pointer {activeTab === 'users' ? 'bg-white text-[#1b522f] shadow-xs' : 'text-gray-500 hover:text-gray-800'}"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
			</svg>
			<span>User Accounts ({users.length})</span>
		</button>
		<button
			type="button"
			onclick={() => { activeTab = 'audit'; loadAuditLogsData(); }}
			class="px-5 py-2.5 text-xs font-semibold rounded-xl transition-all flex items-center space-x-2 cursor-pointer {activeTab === 'audit' ? 'bg-white text-[#1b522f] shadow-xs' : 'text-gray-500 hover:text-gray-800'}"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
			</svg>
			<span>Security Audit Logs</span>
		</button>
	</div>

	{#if activeTab === 'users'}
		<!-- 4 Stat Metric Cards -->
		<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
			<!-- Card 1: Pending Approvals -->
			<button
				type="button"
				onclick={() => (statusFilter = 'pending')}
				class="p-5 rounded-3xl border transition-all text-left group cursor-pointer {statusFilter === 'pending'
					? 'bg-amber-50/70 border-amber-300 ring-2 ring-amber-400/20'
					: 'bg-white hover:bg-amber-50/30 border-gray-100 shadow-2xs'}"
			>
				<div class="flex items-center justify-between mb-3">
					<div class="w-10 h-10 rounded-2xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold">
						<svg class="w-5 h-5 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
						</svg>
					</div>
					<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-amber-100 text-amber-800">
						Pending
					</span>
				</div>
				<p class="text-3xl font-bold text-gray-900 group-hover:text-amber-800 transition-colors">
					{stats.pending}
				</p>
				<p class="text-xs font-semibold text-gray-700 mt-1">Pending Approvals</p>
				<p class="text-[11px] text-gray-400 mt-0.5">Awaiting clinic review</p>
			</button>

			<!-- Card 2: Approved Accounts -->
			<button
				type="button"
				onclick={() => (statusFilter = 'approved')}
				class="p-5 rounded-3xl border transition-all text-left group cursor-pointer {statusFilter === 'approved'
					? 'bg-[#edf7f0] border-[#1b522f]/30 ring-2 ring-[#1b522f]/20'
					: 'bg-white hover:bg-[#edf7f0]/40 border-gray-100 shadow-2xs'}"
			>
				<div class="flex items-center justify-between mb-3">
					<div class="w-10 h-10 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center font-bold">
						<svg class="w-5 h-5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
						</svg>
					</div>
					<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-[#edf7f0] text-[#1b522f]">
						Active
					</span>
				</div>
				<p class="text-3xl font-bold text-gray-900 group-hover:text-[#1b522f] transition-colors">
					{stats.approved}
				</p>
				<p class="text-xs font-semibold text-gray-700 mt-1">Approved Accounts</p>
				<p class="text-[11px] text-gray-400 mt-0.5">Granted portal access</p>
			</button>

			<!-- Card 3: Rejected Requests -->
			<button
				type="button"
				onclick={() => (statusFilter = 'rejected')}
				class="p-5 rounded-3xl border transition-all text-left group cursor-pointer {statusFilter === 'rejected'
					? 'bg-rose-50 border-rose-300 ring-2 ring-rose-400/20'
					: 'bg-white hover:bg-rose-50/40 border-gray-100 shadow-2xs'}"
			>
				<div class="flex items-center justify-between mb-3">
					<div class="w-10 h-10 rounded-2xl bg-rose-100 text-rose-800 flex items-center justify-center font-bold">
						<svg class="w-5 h-5 text-rose-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
						</svg>
					</div>
					<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-rose-100 text-rose-800">
						Blocked
					</span>
				</div>
				<p class="text-3xl font-bold text-gray-900 group-hover:text-rose-800 transition-colors">
					{stats.rejected}
				</p>
				<p class="text-xs font-semibold text-gray-700 mt-1">Rejected Requests</p>
				<p class="text-[11px] text-gray-400 mt-0.5">Denied authentication</p>
			</button>

			<!-- Card 4: Total Registered Accounts -->
			<button
				type="button"
				onclick={() => (statusFilter = 'all')}
				class="p-5 rounded-3xl border transition-all text-left group cursor-pointer {statusFilter === 'all'
					? 'bg-gray-100 border-gray-300 ring-2 ring-gray-400/20'
					: 'bg-white hover:bg-gray-50 border-gray-100 shadow-2xs'}"
			>
				<div class="flex items-center justify-between mb-3">
					<div class="w-10 h-10 rounded-2xl bg-gray-100 text-gray-700 flex items-center justify-center font-bold">
						<svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
						</svg>
					</div>
					<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600">
						Total
					</span>
				</div>
				<p class="text-3xl font-bold text-gray-900 group-hover:text-gray-700 transition-colors">
					{stats.total}
				</p>
				<p class="text-xs font-semibold text-gray-700 mt-1">Total Users</p>
				<p class="text-[11px] text-gray-400 mt-0.5">Staff, CRRMU & students</p>
			</button>
		</div>

		<!-- Filter Toolbar -->
		<div class="bg-white p-4 sm:p-5 rounded-3xl border border-gray-100 shadow-2xs space-y-4">
			<div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
				<!-- Search -->
				<div class="relative flex-1">
					<svg class="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
					</svg>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search by name, student ID, email, role, or emergency person..."
						class="w-full pl-10 pr-4 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] transition-all"
					/>
				</div>

				<!-- Role Filter Dropdown -->
				<div class="flex items-center space-x-2">
					<select
						bind:value={roleFilter}
						class="px-3.5 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] cursor-pointer"
					>
						<option value="all">All Roles</option>
						<option value="admin">Clinic Administrators</option>
						<option value="staff">Clinic Staff / Nurses</option>
						<option value="crrmu">Student – CRRMU Responders</option>
						<option value="student">Standard Students</option>
					</select>

					<!-- Status Filter Dropdown -->
					<select
						bind:value={statusFilter}
						class="px-3.5 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] cursor-pointer"
					>
						<option value="all">All Statuses</option>
						<option value="pending">Pending Approval</option>
						<option value="approved">Approved</option>
						<option value="rejected">Rejected</option>
					</select>
				</div>
			</div>
		</div>

		<!-- User Table -->
		<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
			{#if isLoading}
				<div class="p-12 text-center text-gray-400 space-y-3">
					<div class="w-8 h-8 border-3 border-[#1b522f] border-t-transparent rounded-full animate-spin mx-auto"></div>
					<p class="text-xs font-medium">Loading user accounts...</p>
				</div>
			{:else if filteredUsers.length === 0}
				<div class="p-14 text-center text-gray-400 space-y-3">
					<div class="w-14 h-14 bg-gray-50 text-gray-300 rounded-3xl mx-auto flex items-center justify-center">
						<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
						</svg>
					</div>
					<h4 class="text-sm font-semibold text-gray-700">No User Accounts Found</h4>
					<p class="text-xs text-gray-400 max-w-sm mx-auto">
						No accounts matched your current filters. Click "Add New User" to register an account directly.
					</p>
				</div>
			{:else}
				<div class="overflow-x-auto">
					<table class="w-full text-left border-collapse">
						<thead>
							<tr class="bg-gray-50/80 border-b border-gray-100 text-[11px] font-bold text-gray-500 uppercase tracking-wider">
								<th class="py-3.5 px-6">User / Account</th>
								<th class="py-3.5 px-4">Role & Permissions</th>
								<th class="py-3.5 px-4">Department / Program</th>
								<th class="py-3.5 px-4">Emergency Contact</th>
								<th class="py-3.5 px-4">Status</th>
								<th class="py-3.5 px-6 text-right">Actions</th>
							</tr>
						</thead>
						<tbody class="divide-y divide-gray-100 text-xs">
							{#each filteredUsers as user (user.id)}
								{@const roleBadge = getRoleBadge(user)}
								{@const isPending = user.status === 'pending'}
								{@const isApproved = user.status === 'approved'}
								{@const isRejected = user.status === 'rejected'}
								<tr class="hover:bg-gray-50/60 transition-colors group {isPending ? 'bg-amber-50/20' : ''}">
									<!-- User / Account -->
									<td class="py-4 px-6">
										<div class="flex items-center space-x-3.5">
											<div
												class="w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs"
												style="background-color: {user.avatarBg || '#edf7f0'}; color: {user.avatarColor || '#1b522f'};"
											>
												{user.initials}
											</div>
											<div class="min-w-0">
												<button
													type="button"
													onclick={() => openDetails(user)}
													class="font-bold text-gray-900 hover:text-[#1b522f] truncate text-left cursor-pointer transition-colors block"
												>
													{user.name}
												</button>
												<div class="flex items-center space-x-2 text-[11px] text-gray-400 mt-0.5">
													<span class="font-mono text-gray-600 bg-gray-100 px-1.5 py-0.5 rounded">ID: {user.studentId}</span>
													<span>·</span>
													<span class="truncate">{user.email}</span>
												</div>
											</div>
										</div>
									</td>

									<!-- Role & Permissions -->
									<td class="py-4 px-4 whitespace-nowrap">
										<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-bold border {roleBadge.bg}">
											{#if user.isCrrmuMember}
												<svg class="w-3 h-3 mr-1 text-blue-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
												</svg>
											{/if}
											{roleBadge.label}
										</span>
									</td>

									<!-- Department / Program -->
									<td class="py-4 px-4">
										<div>
											<p class="font-semibold text-gray-800">{user.programStrand || 'N/A'}</p>
											{#if user.yearSection}
												<p class="text-[11px] text-gray-400">{user.yearSection}</p>
											{/if}
										</div>
									</td>

									<!-- Emergency Contact -->
									<td class="py-4 px-4">
										<div>
											{#if user.emergencyPerson}
												<p class="font-semibold text-gray-800">{user.emergencyPerson}</p>
												<p class="text-[11px] text-gray-500">
													{user.emergencyRelationship || 'Contact'} · <span class="font-medium text-[#1b522f]">{user.emergencyContact || ''}</span>
												</p>
											{:else}
												<span class="text-gray-400 italic text-[11px]">No contact specified</span>
											{/if}
										</div>
									</td>

									<!-- Status -->
									<td class="py-4 px-4 whitespace-nowrap">
										{#if isPending}
											<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200">
												<span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
												Pending Review
											</span>
										{:else if isApproved}
											<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
												<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
												</svg>
												Approved
											</span>
										{:else if isRejected}
											<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-200">
												<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
												</svg>
												Rejected
											</span>
										{/if}
									</td>

									<!-- Actions Column -->
									<td class="py-4 px-6 text-right whitespace-nowrap">
										<div class="flex items-center justify-end space-x-1.5">
											<!-- Edit Role & Account -->
											<button
												type="button"
												onclick={() => openEditModal(user)}
												title="Edit role, permissions, or profile"
												class="p-2 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-700 cursor-pointer transition-colors"
											>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
												</svg>
											</button>

											<!-- Reset Password -->
											<button
												type="button"
												onclick={() => openResetModal(user)}
												title="Reset account password"
												class="p-2 rounded-xl bg-gray-50 hover:bg-gray-100 text-amber-700 cursor-pointer transition-colors"
											>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
												</svg>
											</button>

											<!-- View Details -->
											<button
												type="button"
												onclick={() => openDetails(user)}
												title="View full details"
												class="p-2 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-700 cursor-pointer transition-colors"
											>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
												</svg>
											</button>

											<!-- Approve Button (if pending/rejected) -->
											{#if isPending || isRejected}
												<button
													type="button"
													disabled={updatingUserId === user.id}
													onclick={() => handleStatusChange(user.id, 'approved')}
													title="Approve access"
													class="px-2.5 py-1.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer transition-all shadow-2xs disabled:opacity-50 flex items-center space-x-1"
												>
													<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
														<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
													</svg>
													<span>Approve</span>
												</button>
											{/if}

											<!-- Reject Button -->
											{#if isPending || isApproved}
												<button
													type="button"
													disabled={updatingUserId === user.id}
													onclick={() => handleStatusChange(user.id, 'rejected')}
													title="Reject access"
													class="px-2.5 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-semibold cursor-pointer transition-all border border-rose-200 disabled:opacity-50"
												>
													Reject
												</button>
											{/if}

											<!-- Delete Button -->
											<button
												type="button"
												disabled={deletingUserId === user.id || clinicStore.currentUser.id === user.id}
												onclick={() => handleDeleteUser(user.id, user.name)}
												title="Delete account"
												class="p-2 rounded-xl bg-gray-50 hover:bg-rose-50 text-gray-400 hover:text-rose-600 cursor-pointer transition-colors disabled:opacity-30"
											>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
												</svg>
											</button>
										</div>
									</td>
								</tr>
							{/each}
						</tbody>
					</table>
				</div>
			{/if}
		</div>

	{:else}
		<!-- ================= AUDIT LOGS TAB VIEW ================= -->
		<div class="space-y-4">
			<!-- Audit Controls -->
			<div class="bg-white p-4 sm:p-5 rounded-3xl border border-gray-100 shadow-2xs space-y-4">
				<div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
					<div class="relative flex-1">
						<svg class="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
						</svg>
						<input
							type="text"
							bind:value={auditSearchQuery}
							placeholder="Search audit trail by actor, target user, action, or details..."
							class="w-full pl-10 pr-4 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>

					<div class="flex items-center space-x-2">
						<select
							bind:value={auditCategoryFilter}
							onchange={loadAuditLogsData}
							class="px-3.5 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] cursor-pointer"
						>
							<option value="all">All Categories</option>
							<option value="USER_MANAGEMENT">User Management</option>
							<option value="AUTHENTICATION">Authentication</option>
							<option value="SECURITY">Security</option>
						</select>

						<a
							href="/admin/audit-logs"
							class="px-4 py-2.5 rounded-2xl border border-gray-200 bg-white text-xs font-semibold text-gray-700 hover:bg-gray-50 transition-colors shadow-2xs flex items-center space-x-1.5"
						>
							<span>Full Audit Page</span>
							<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14"></path>
							</svg>
						</a>
					</div>
				</div>
			</div>

			<!-- Audit Log Table -->
			<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
				{#if isLoadingAudit}
					<div class="p-12 text-center text-gray-400 space-y-3">
						<div class="w-8 h-8 border-3 border-[#1b522f] border-t-transparent rounded-full animate-spin mx-auto"></div>
						<p class="text-xs font-medium">Loading audit logs...</p>
					</div>
				{:else if filteredAuditLogs.length === 0}
					<div class="p-14 text-center text-gray-400 space-y-3">
						<div class="w-14 h-14 bg-gray-50 text-gray-300 rounded-3xl mx-auto flex items-center justify-center">
							<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
							</svg>
						</div>
						<h4 class="text-sm font-semibold text-gray-700">No Audit Logs Found</h4>
						<p class="text-xs text-gray-400 max-w-sm mx-auto">All security events, status updates, and role modifications will appear here.</p>
					</div>
				{:else}
					<div class="overflow-x-auto">
						<table class="w-full text-left border-collapse">
							<thead>
								<tr class="bg-gray-50/80 border-b border-gray-100 text-[11px] font-bold text-gray-500 uppercase tracking-wider">
									<th class="py-3.5 px-6">Timestamp</th>
									<th class="py-3.5 px-4">Action</th>
									<th class="py-3.5 px-4">Actor</th>
									<th class="py-3.5 px-4">Target User</th>
									<th class="py-3.5 px-6">Details</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-100 text-xs">
								{#each filteredAuditLogs as log (log.id)}
									<tr class="hover:bg-gray-50/60 transition-colors">
										<td class="py-3.5 px-6 font-mono text-[11px] text-gray-500 whitespace-nowrap">
											{new Date(log.timestamp).toLocaleString()}
										</td>
										<td class="py-3.5 px-4 whitespace-nowrap">
											<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold border bg-gray-100 text-gray-700">
												{log.action.replace(/_/g, ' ')}
											</span>
										</td>
										<td class="py-3.5 px-4 whitespace-nowrap">
											<span class="font-bold text-gray-900">{log.actorName}</span>
											<span class="text-[10px] text-gray-400 block">{log.actorRole}</span>
										</td>
										<td class="py-3.5 px-4 whitespace-nowrap">
											{#if log.targetUserName}
												<span class="font-medium text-gray-800">{log.targetUserName}</span>
												{#if log.targetUserRole}
													<span class="text-[10px] text-gray-400 block">{log.targetUserRole}</span>
												{/if}
											{:else}
												<span class="text-gray-400 italic">Self / System</span>
											{/if}
										</td>
										<td class="py-3.5 px-6 text-gray-600 leading-relaxed min-w-[280px]">
											{log.details}
										</td>
									</tr>
								{/each}
							</tbody>
						</table>
					</div>
				{/if}
			</div>
		</div>
	{/if}

</div>

<!-- ================= CREATE USER MODAL ================= -->
{#if showCreateModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-fade-in">
		<div class="bg-white rounded-3xl max-w-xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden border border-gray-100">
			<div class="p-5 border-b border-gray-100 flex items-center justify-between bg-[#edf7f0]">
				<div>
					<h3 class="text-base font-bold text-gray-900">Create New Account</h3>
					<p class="text-xs text-gray-500">Provision a staff, nurse, CRRMU responder, or student account</p>
				</div>
				<button
					type="button"
					onclick={() => (showCreateModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-white/80 hover:bg-white text-gray-500 hover:text-gray-800 flex items-center justify-center cursor-pointer"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>

			<form onsubmit={handleCreateUser} class="p-6 overflow-y-auto space-y-4 text-xs">
				<!-- Role Selection -->
				<div>
					<label for="create-role" class="block font-semibold text-gray-700 mb-1">Account Role & Access Level *</label>
					<select
						id="create-role"
						bind:value={createUserData.role}
						class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs font-semibold text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
					>
						<option value="Student">Student (Standard Patient)</option>
						<option value="Student - CRRMU Member">Student – CRRMU Member (First Aid Responder)</option>
						<option value="Clinic Staff">Clinic Staff (School Nurse / Healthcare Practitioner)</option>
						<option value="Clinic Administrator">Clinic Administrator (Full System Management)</option>
					</select>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="create-id" class="block font-semibold text-gray-700 mb-1">
							{createUserData.role.includes('Student') ? 'Student ID (Numbers only)' : 'Staff ID'} *
						</label>
						<input
							id="create-id"
							type="text"
							bind:value={createUserData.student_id}
							placeholder={createUserData.role.includes('Student') ? 'e.g. 202611999' : 'e.g. CN-1020'}
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>

					<div>
						<label for="create-name" class="block font-semibold text-gray-700 mb-1">Full Name *</label>
						<input
							id="create-name"
							type="text"
							bind:value={createUserData.name}
							placeholder="e.g. Maria Santos"
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="create-email" class="block font-semibold text-gray-700 mb-1">Email Address *</label>
						<input
							id="create-email"
							type="email"
							bind:value={createUserData.email}
							placeholder="e.g. user@celtech.edu.ph"
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>

					<div>
						<label for="create-password" class="block font-semibold text-gray-700 mb-1">Password *</label>
						<input
							id="create-password"
							type="password"
							bind:value={createUserData.password}
							placeholder="At least 6 characters"
							required
							minlength="6"
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="create-program" class="block font-semibold text-gray-700 mb-1">Department / Academic Program</label>
						<input
							id="create-program"
							type="text"
							bind:value={createUserData.program_strand}
							placeholder="e.g. BS Nursing, BSIT"
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>

					<div>
						<label for="create-phone" class="block font-semibold text-gray-700 mb-1">Contact Phone</label>
						<input
							id="create-phone"
							type="text"
							bind:value={createUserData.contact_number}
							placeholder="09XX XXX XXXX"
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
						/>
					</div>
				</div>

				<div class="p-3 bg-gray-50 rounded-2xl border border-gray-200/80 flex items-center justify-between">
					<div>
						<p class="font-semibold text-gray-800">Initial Account Status</p>
						<p class="text-[11px] text-gray-500">Admins can immediately activate or leave as pending</p>
					</div>
					<select
						bind:value={createUserData.status}
						class="px-3 py-1.5 bg-white border border-gray-300 rounded-xl text-xs font-semibold text-gray-800 cursor-pointer"
					>
						<option value="approved">Approved (Active immediately)</option>
						<option value="pending">Pending Approval</option>
					</select>
				</div>

				<div class="pt-3 border-t border-gray-100 flex items-center justify-end space-x-2">
					<button
						type="button"
						onclick={() => (showCreateModal = false)}
						class="px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold cursor-pointer"
					>
						Cancel
					</button>
					<button
						type="submit"
						disabled={isSubmittingModal}
						class="px-5 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white font-semibold cursor-pointer shadow-xs disabled:opacity-50"
					>
						{isSubmittingModal ? 'Creating...' : 'Create Account'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- ================= EDIT USER MODAL ================= -->
{#if showEditModal && editingUser}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-fade-in">
		<div class="bg-white rounded-3xl max-w-lg w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden border border-gray-100">
			<div class="p-5 border-b border-gray-100 flex items-center justify-between bg-purple-50">
				<div>
					<h3 class="text-base font-bold text-gray-900">Edit User & Role</h3>
					<p class="text-xs text-purple-700">Modify permissions, role tier, and user details</p>
				</div>
				<button
					type="button"
					onclick={() => (showEditModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-white text-gray-500 hover:text-gray-800 flex items-center justify-center cursor-pointer"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>

			<form onsubmit={handleSaveEditUser} class="p-6 overflow-y-auto space-y-4 text-xs">
				<!-- Role Change (Key RBAC feature) -->
				<div class="p-3.5 bg-purple-50/60 border border-purple-200 rounded-2xl">
					<label for="edit-role" class="block font-bold text-purple-900 mb-1">Assigned Role & Permissions *</label>
					<select
						id="edit-role"
						bind:value={editUserData.role}
						class="w-full px-3.5 py-2.5 bg-white border border-purple-300 rounded-xl text-xs font-bold text-gray-900 focus:outline-none focus:ring-2 focus:ring-purple-500/20"
					>
						<option value="Student">Student (Regular Patient Access)</option>
						<option value="Student - CRRMU Member">Student – CRRMU Member (First Aid Responder Module)</option>
						<option value="Clinic Staff">Clinic Staff (Nurse / Healthcare Practitioner)</option>
						<option value="Clinic Administrator">Clinic Administrator (Full Administration)</option>
					</select>
					<p class="text-[10px] text-purple-600 mt-1">
						Changing role automatically adjusts access to admin portals, patient triage, and first-aid reporting.
					</p>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="edit-name" class="block font-semibold text-gray-700 mb-1">Full Name</label>
						<input
							id="edit-name"
							type="text"
							bind:value={editUserData.name}
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						/>
					</div>

					<div>
						<label for="edit-id" class="block font-semibold text-gray-700 mb-1">Student / Staff ID</label>
						<input
							id="edit-id"
							type="text"
							bind:value={editUserData.student_id}
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						/>
					</div>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="edit-email" class="block font-semibold text-gray-700 mb-1">Email</label>
						<input
							id="edit-email"
							type="email"
							bind:value={editUserData.email}
							required
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						/>
					</div>

					<div>
						<label for="edit-status" class="block font-semibold text-gray-700 mb-1">Account Status</label>
						<select
							id="edit-status"
							bind:value={editUserData.status}
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs font-semibold text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						>
							<option value="approved">Approved (Active)</option>
							<option value="pending">Pending Review</option>
							<option value="rejected">Rejected (Blocked)</option>
						</select>
					</div>
				</div>

				<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
					<div>
						<label for="edit-prog" class="block font-semibold text-gray-700 mb-1">Program / Department</label>
						<input
							id="edit-prog"
							type="text"
							bind:value={editUserData.program_strand}
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						/>
					</div>

					<div>
						<label for="edit-phone" class="block font-semibold text-gray-700 mb-1">Contact Number</label>
						<input
							id="edit-phone"
							type="text"
							bind:value={editUserData.contact_number}
							class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
						/>
					</div>
				</div>

				<div class="pt-3 border-t border-gray-100 flex items-center justify-end space-x-2">
					<button
						type="button"
						onclick={() => (showEditModal = false)}
						class="px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold cursor-pointer"
					>
						Cancel
					</button>
					<button
						type="submit"
						disabled={isSubmittingModal}
						class="px-5 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white font-semibold cursor-pointer shadow-xs disabled:opacity-50"
					>
						{isSubmittingModal ? 'Saving...' : 'Save Changes'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- ================= RESET PASSWORD MODAL ================= -->
{#if showResetModal && resettingUser}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-fade-in">
		<div class="bg-white rounded-3xl max-w-md w-full shadow-2xl overflow-hidden border border-gray-100">
			<div class="p-5 border-b border-gray-100 flex items-center justify-between bg-amber-50">
				<div class="flex items-center space-x-2.5">
					<div class="w-9 h-9 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center font-bold">
						<svg class="w-5 h-5 text-amber-700" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z"></path>
						</svg>
					</div>
					<div>
						<h3 class="text-base font-bold text-gray-900">Reset Password</h3>
						<p class="text-xs text-amber-800">For {resettingUser.name} ({resettingUser.studentId})</p>
					</div>
				</div>
				<button
					type="button"
					onclick={() => (showResetModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-white text-gray-500 hover:text-gray-800 flex items-center justify-center cursor-pointer"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>

			<form onsubmit={handleResetPassword} class="p-6 space-y-4 text-xs">
				<p class="text-gray-600 leading-relaxed">
					Enter a new password for <strong>{resettingUser.name}</strong>. An immutable audit log entry will record this security event.
				</p>

				<div>
					<label for="new-pw-input" class="block font-semibold text-gray-700 mb-1">New Temporary Password *</label>
					<input
						id="new-pw-input"
						type="password"
						bind:value={newPasswordInput}
						placeholder="Minimum 6 characters"
						required
						minlength="6"
						class="w-full px-3.5 py-2.5 bg-white border border-gray-300 rounded-xl text-xs text-gray-800 focus:outline-none focus:ring-2 focus:ring-amber-500/20 focus:border-amber-600"
					/>
				</div>

				<div class="pt-3 border-t border-gray-100 flex items-center justify-end space-x-2">
					<button
						type="button"
						onclick={() => (showResetModal = false)}
						class="px-4 py-2 rounded-xl bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold cursor-pointer"
					>
						Cancel
					</button>
					<button
						type="submit"
						disabled={isSubmittingModal}
						class="px-5 py-2 rounded-xl bg-amber-600 hover:bg-amber-700 text-white font-semibold cursor-pointer shadow-xs disabled:opacity-50"
					>
						{isSubmittingModal ? 'Resetting...' : 'Update Password'}
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}

<!-- ================= USER DETAIL MODAL ================= -->
{#if showDetailModal && selectedUser}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-fade-in">
		<div class="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] flex flex-col shadow-2xl overflow-hidden border border-gray-100">
			<!-- Modal Header -->
			<div class="p-6 border-b border-gray-100 flex items-center justify-between bg-[#edf7f0]">
				<div class="flex items-center space-x-3.5">
					<div
						class="w-12 h-12 rounded-2xl flex items-center justify-center font-bold text-base shadow-2xs"
						style="background-color: {selectedUser.avatarBg}; color: {selectedUser.avatarColor};"
					>
						{selectedUser.initials}
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900 leading-tight">{selectedUser.name}</h3>
						<p class="text-xs text-gray-600">ID: {selectedUser.studentId} · {selectedUser.email}</p>
					</div>
				</div>

				<button
					type="button"
					onclick={() => (showDetailModal = false)}
					class="w-8 h-8 rounded-full bg-white/80 hover:bg-white text-gray-500 hover:text-gray-800 flex items-center justify-center cursor-pointer transition-colors"
					aria-label="Close modal"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>

			<!-- Modal Body (Details) -->
			<div class="p-6 overflow-y-auto space-y-6 text-xs text-gray-600">
				<!-- Current Status Banner -->
				<div class="p-4 rounded-2xl flex items-center justify-between {selectedUser.status === 'pending'
					? 'bg-amber-50 border border-amber-200'
					: selectedUser.status === 'approved'
					? 'bg-emerald-50 border border-emerald-200'
					: 'bg-rose-50 border border-rose-200'}">
					<div class="flex items-center space-x-3">
						<div class="w-3 h-3 rounded-full {selectedUser.status === 'pending'
							? 'bg-amber-500 animate-pulse'
							: selectedUser.status === 'approved'
							? 'bg-emerald-500'
							: 'bg-rose-500'}"></div>
						<div>
							<p class="font-bold text-gray-900">
								Account Status: <span class="capitalize">{selectedUser.status || 'Approved'}</span>
							</p>
							<p class="text-[11px] text-gray-500">
								{selectedUser.status === 'pending'
									? 'User cannot log in until approved by clinic administrator.'
									: selectedUser.status === 'approved'
									? 'User has verified access to the clinic web app.'
									: 'Access denied.'}
							</p>
						</div>
					</div>

					<div class="flex items-center space-x-2">
						{#if selectedUser.status !== 'approved'}
							<button
								type="button"
								onclick={() => handleStatusChange(selectedUser!.id, 'approved')}
								class="px-3.5 py-1.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white font-semibold cursor-pointer shadow-xs transition-colors"
							>
								Approve Access
							</button>
						{/if}
						{#if selectedUser.status !== 'rejected'}
							<button
								type="button"
								onclick={() => handleStatusChange(selectedUser!.id, 'rejected')}
								class="px-3.5 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 font-semibold cursor-pointer border border-rose-200 transition-colors"
							>
								Reject
							</button>
						{/if}
					</div>
				</div>

				<!-- Section: Account Information -->
				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-3 flex items-center space-x-2">
						<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
						</svg>
						<span>Account & Role Information</span>
					</h4>
					<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Assigned Role</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.role}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Category</span>
							<span class="text-xs font-bold text-gray-800 capitalize">{selectedUser.category}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Department / Strand</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.programStrand || 'N/A'}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Contact</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.contactNumber || 'N/A'}</span>
						</div>
					</div>
				</div>

				<!-- Section: Emergency Contact Details -->
				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-3 flex items-center space-x-2">
						<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
						</svg>
						<span>Emergency Contact Information</span>
					</h4>
					<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
						<div class="p-3 bg-emerald-50/50 border border-emerald-100 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Responsible Person</span>
							<span class="text-xs font-bold text-gray-900">{selectedUser.emergencyPerson || 'None specified'}</span>
						</div>
						<div class="p-3 bg-emerald-50/50 border border-emerald-100 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Relationship</span>
							<span class="text-xs font-bold text-gray-900">{selectedUser.emergencyRelationship || 'None specified'}</span>
						</div>
						<div class="p-3 bg-emerald-50/50 border border-emerald-100 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Emergency Phone</span>
							<span class="text-xs font-bold text-[#1b522f]">{selectedUser.emergencyContact || 'None specified'}</span>
						</div>
						<div class="p-3 bg-emerald-50/50 border border-emerald-100 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Preferred Method</span>
							<span class="text-xs font-bold text-gray-900">{selectedUser.preferredContactMethod || 'Phone call'}</span>
						</div>
					</div>
				</div>
			</div>

			<!-- Modal Footer -->
			<div class="p-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
				<span class="text-[11px] text-gray-500">ID: {selectedUser.id}</span>
				<div class="flex items-center space-x-2">
					<button
						type="button"
						onclick={() => { showDetailModal = false; openEditModal(selectedUser!); }}
						class="px-4 py-2 rounded-xl bg-purple-50 text-purple-700 hover:bg-purple-100 text-xs font-semibold cursor-pointer transition-colors"
					>
						Edit Role / Info
					</button>
					<button
						type="button"
						onclick={() => (showDetailModal = false)}
						class="px-5 py-2 rounded-xl bg-gray-200 hover:bg-gray-300 text-gray-800 text-xs font-semibold cursor-pointer transition-colors"
					>
						Close
					</button>
				</div>
			</div>
		</div>
	</div>
{/if}
