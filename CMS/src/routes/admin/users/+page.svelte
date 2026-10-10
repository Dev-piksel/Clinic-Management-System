<script lang="ts">
	import { onMount } from 'svelte';
	import { clinicStore } from '#lib/state.svelte';
	import { fetchAdminUsers, updateUserStatus, deleteUser, fetchAdminStats, checkBackendHealth } from '#lib/api';
	import type { DemoAccount } from '#lib/types';

	let users = $state<DemoAccount[]>([]);
	let isLoading = $state(true);
	let isBackendOnline = $state<boolean | null>(null);
	let errorMessage = $state('');
	let toastMessage = $state('');
	let toastType = $state<'success' | 'error'>('success');

	// Filters & Search
	let statusFilter = $state<'all' | 'pending' | 'approved' | 'rejected'>('all');
	let searchQuery = $state('');
	let roleFilter = $state<'all' | 'student' | 'staff' | 'crrmu'>('all');

	// Selected user for full details modal
	let selectedUser = $state<DemoAccount | null>(null);
	let showDetailModal = $state(false);

	// Action in-flight states
	let updatingUserId = $state<string | null>(null);
	let deletingUserId = $state<string | null>(null);

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

	function recalcLocalStats() {
		const total = users.length;
		const pending = users.filter((u) => u.status === 'pending').length;
		const approved = users.filter((u) => u.status === 'approved').length;
		const rejected = users.filter((u) => u.status === 'rejected').length;
		stats = { total, pending, approved, rejected };
		clinicStore.setPendingUsersCount(pending);
	}

	onMount(() => {
		loadData();
	});

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
				// Offline optimistic update
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

	async function handleDeleteUser(userId: string, userName: string) {
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

			showToast(`User ${userName} was deleted from the system.`, 'success');
		} catch (err: any) {
			showToast(err.message || 'Failed to delete user.', 'error');
		} finally {
			deletingUserId = null;
		}
	}

	function openDetails(user: DemoAccount) {
		selectedUser = user;
		showDetailModal = true;
	}

	// Filtered users calculation
	let filteredUsers = $derived.by(() => {
		let list = users;

		// Status filter
		if (statusFilter !== 'all') {
			list = list.filter((u) => (u.status || 'approved') === statusFilter);
		}

		// Role filter
		if (roleFilter === 'student') {
			list = list.filter((u) => u.category === 'student' && !u.isCrrmuMember);
		} else if (roleFilter === 'staff') {
			list = list.filter((u) => u.category === 'staff');
		} else if (roleFilter === 'crrmu') {
			list = list.filter((u) => u.isCrrmuMember);
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
					(u.emergencyPerson && u.emergencyPerson.toLowerCase().includes(q))
			);
		}

		return list;
	});
</script>

<svelte:head>
	<title>User Approvals & Management - Clinic Admin - CSHMS</title>
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
					ADMINISTRATION & VERIFICATION GATE
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
				User Approvals & Management
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Review student registrations, verify emergency contacts and Terms & Conditions acceptance before granting clinic portal access.
			</p>
		</div>

		<div class="flex items-center space-x-3 self-start sm:self-auto">
			<button
				type="button"
				onclick={loadData}
				disabled={isLoading}
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-2xl bg-white hover:bg-gray-50 text-gray-700 border border-gray-200 text-xs font-semibold shadow-2xs transition-colors cursor-pointer disabled:opacity-50"
			>
				<svg class="w-4 h-4 text-gray-500 {isLoading ? 'animate-spin' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
				</svg>
				<span>Refresh Data</span>
			</button>

			<a
				href="/register"
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-2xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-2xs transition-colors"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
				</svg>
				<span>New Registration</span>
			</a>
		</div>
	</div>

	<!-- 4 Stat Metric Cards -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
		<!-- Card 1: Pending Approvals (Featured Amber) -->
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
					Requires Action
				</span>
			</div>
			<p class="text-3xl font-bold text-gray-900 group-hover:text-amber-800 transition-colors">
				{stats.pending}
			</p>
			<p class="text-xs font-semibold text-gray-700 mt-1">Pending Approvals</p>
			<p class="text-[11px] text-gray-400 mt-0.5">Awaiting clinic review to log in</p>
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
					<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-800">
					Active
				</span>
			</div>
			<p class="text-3xl font-bold text-gray-900 group-hover:text-[#1b522f] transition-colors">
				{stats.approved}
			</p>
			<p class="text-xs font-semibold text-gray-700 mt-1">Approved Accounts</p>
			<p class="text-[11px] text-gray-400 mt-0.5">Granted full clinic access</p>
		</button>

		<!-- Card 3: Rejected Accounts -->
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
			<p class="text-xs font-semibold text-gray-700 mt-1">Rejected Accounts</p>
			<p class="text-[11px] text-gray-400 mt-0.5">Declined or invalid identities</p>
		</button>

		<!-- Card 4: Total Users -->
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
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z"></path>
					</svg>
				</div>
				<span class="text-[10px] font-bold tracking-wider uppercase px-2.5 py-0.5 rounded-full bg-gray-100 text-gray-600">
					Directory
				</span>
			</div>
			<p class="text-3xl font-bold text-gray-900 group-hover:text-gray-900 transition-colors">
				{stats.total}
			</p>
			<p class="text-xs font-semibold text-gray-700 mt-1">Total Registered</p>
			<p class="text-[11px] text-gray-400 mt-0.5">Students, Staff & Admin</p>
		</button>
	</div>

	<!-- Filter Tabs, Search Bar and Actions Card -->
	<div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs space-y-4">
		<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
			
			<!-- Status Filter Tabs -->
			<div class="flex items-center p-1 bg-gray-100/80 rounded-2xl self-start overflow-x-auto max-w-full">
				<button
					type="button"
					onclick={() => (statusFilter = 'all')}
					class="px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap {statusFilter === 'all'
						? 'bg-white text-gray-900 shadow-xs'
						: 'text-gray-500 hover:text-gray-800'}"
				>
					All Users ({stats.total})
				</button>
				<button
					type="button"
					onclick={() => (statusFilter = 'pending')}
					class="px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer flex items-center space-x-1.5 whitespace-nowrap {statusFilter === 'pending'
						? 'bg-white text-amber-900 shadow-xs'
						: 'text-gray-500 hover:text-amber-700'}"
				>
					<span>Pending Approvals</span>
					{#if stats.pending > 0}
						<span class="w-5 h-5 rounded-full bg-amber-500 text-white text-[10px] font-bold flex items-center justify-center">
							{stats.pending}
						</span>
					{/if}
				</button>
				<button
					type="button"
					onclick={() => (statusFilter = 'approved')}
					class="px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap {statusFilter === 'approved'
						? 'bg-white text-[#1b522f] shadow-xs'
						: 'text-gray-500 hover:text-[#1b522f]'}"
				>
					Approved ({stats.approved})
				</button>
				<button
					type="button"
					onclick={() => (statusFilter = 'rejected')}
					class="px-4 py-2 rounded-xl text-xs font-semibold transition-all cursor-pointer whitespace-nowrap {statusFilter === 'rejected'
						? 'bg-white text-rose-800 shadow-xs'
						: 'text-gray-500 hover:text-rose-700'}"
				>
					Rejected ({stats.rejected})
				</button>
			</div>

			<!-- Search and Role Dropdown -->
			<div class="flex flex-col sm:flex-row items-center gap-3 w-full lg:w-auto">
				<!-- Search Input -->
				<div class="relative w-full sm:w-72">
					<div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-gray-400">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
						</svg>
					</div>
					<input
						type="text"
						bind:value={searchQuery}
						placeholder="Search name, ID, email..."
						class="w-full pl-10 pr-3.5 py-2.5 rounded-xl border border-gray-200 text-xs text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
					/>
				</div>

				<!-- Role Selector -->
				<select
					bind:value={roleFilter}
					class="w-full sm:w-auto px-3.5 py-2.5 rounded-xl border border-gray-200 bg-white text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
				>
					<option value="all">All Roles</option>
					<option value="student">Regular Students</option>
					<option value="crrmu">CRRMU Members</option>
					<option value="staff">Clinic Staff</option>
				</select>
			</div>
		</div>
	</div>

	<!-- Users Table / Card Grid -->
	<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
		<div class="p-6 border-b border-gray-100 flex items-center justify-between">
			<div>
				<h2 class="text-lg font-bold text-gray-900">Registered Users Directory</h2>
				<p class="text-xs text-gray-500 mt-0.5">
					Showing {filteredUsers.length} of {users.length} registered accounts
				</p>
			</div>

			<div class="flex items-center space-x-2 text-xs">
				<a
					href="/terms"
					target="_blank"
					class="text-[#1b522f] hover:underline font-semibold flex items-center gap-1"
				>
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
					</svg>
					<span>View Clinic Terms</span>
				</a>
			</div>
		</div>

		{#if isLoading}
			<div class="p-16 text-center text-gray-400 space-y-3">
				<div class="w-10 h-10 border-3 border-[#1b522f] border-t-transparent rounded-full animate-spin mx-auto"></div>
				<p class="text-xs font-medium">Loading user registrations...</p>
			</div>
		{:else if filteredUsers.length === 0}
			<div class="p-16 text-center text-gray-400 space-y-3">
				<div class="w-14 h-14 rounded-3xl bg-gray-50 mx-auto flex items-center justify-center text-gray-400">
					<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
					</svg>
				</div>
				<p class="text-sm font-semibold text-gray-700">No users found</p>
				<p class="text-xs text-gray-400 max-w-sm mx-auto">
					No accounts match the current filter or search criteria.
				</p>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs border-collapse">
					<thead>
						<tr class="bg-gray-50/70 text-gray-500 font-semibold border-b border-gray-100 uppercase tracking-wider text-[10px]">
							<th class="py-3.5 px-6">User & Identity</th>
							<th class="py-3.5 px-4">Program & Role</th>
							<th class="py-3.5 px-4">Emergency Contact</th>
							<th class="py-3.5 px-4">Terms Acceptance</th>
							<th class="py-3.5 px-4">Access Status</th>
							<th class="py-3.5 px-6 text-right">Approval Actions</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-100">
						{#each filteredUsers as user (user.id)}
							{@const isPending = user.status === 'pending'}
							{@const isApproved = user.status === 'approved' || !user.status}
							{@const isRejected = user.status === 'rejected'}
							<tr class="hover:bg-gray-50/60 transition-colors group {isPending ? 'bg-amber-50/20' : ''}">
								<!-- 1. User & Identity -->
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

								<!-- 2. Program & Role -->
								<td class="py-4 px-4">
									<div>
										<p class="font-semibold text-gray-800">
											{user.programStrand || 'N/A'} {user.yearSection || ''}
										</p>
										<div class="flex items-center gap-1.5 mt-1">
											{#if user.category === 'staff'}
												<span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold bg-purple-50 text-purple-700 border border-purple-200">
													Staff / Nurse
												</span>
											{:else if user.isCrrmuMember}
												<span class="inline-block px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-50 text-emerald-800 border border-emerald-200">
													CRRMU First Responder
												</span>
											{:else}
												<span class="inline-block px-2 py-0.5 rounded text-[10px] font-medium bg-gray-100 text-gray-600">
													Student
												</span>
											{/if}
										</div>
									</div>
								</td>

								<!-- 3. Emergency Contact (Student side requirement) -->
								<td class="py-4 px-4">
									<div>
										{#if user.emergencyPerson}
											<p class="font-semibold text-gray-800">{user.emergencyPerson}</p>
											<p class="text-[11px] text-gray-500">
												{user.emergencyRelationship || 'Contact'} · <span class="font-medium text-[#1b522f]">{user.emergencyContact || 'No number'}</span>
											</p>
										{:else}
											<span class="text-gray-400 italic text-[11px]">No contact specified</span>
										{/if}
									</div>
								</td>

								<!-- 4. Terms Acceptance -->
								<td class="py-4 px-4">
									<div class="space-y-1">
										<span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-semibold bg-emerald-50 text-[#1b522f] border border-emerald-200">
											<svg class="w-3 h-3 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
											</svg>
											<span>Accepted</span>
										</span>
										<p class="text-[10px] text-gray-400">RA 10173 Privacy Consent</p>
									</div>
								</td>

								<!-- 5. Access Status -->
								<td class="py-4 px-4">
									{#if isPending}
										<span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200 shadow-2xs">
											<span class="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></span>
											Pending Approval
										</span>
									{:else if isApproved}
										<span class="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
											<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
											</svg>
											Approved (Active)
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

								<!-- 6. Actions -->
								<td class="py-4 px-6 text-right">
									<div class="flex items-center justify-end space-x-1.5">
										<!-- Inspect Button -->
										<button
											type="button"
											onclick={() => openDetails(user)}
											title="View complete registration details"
											class="p-2 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-600 cursor-pointer transition-colors"
										>
											<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
											</svg>
										</button>

										<!-- Approve Button -->
										{#if isPending || isRejected}
											<button
												type="button"
												disabled={updatingUserId === user.id}
												onclick={() => handleStatusChange(user.id, 'approved')}
												class="px-3 py-1.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer transition-all shadow-2xs disabled:opacity-50 flex items-center space-x-1"
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
												class="px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 text-xs font-semibold cursor-pointer transition-all border border-rose-200 disabled:opacity-50"
											>
												Reject
											</button>
										{/if}

										<!-- Delete Button (Cannot delete self) -->
										{#if user.id !== clinicStore.currentUser.id}
											<button
												type="button"
												disabled={deletingUserId === user.id}
												onclick={() => handleDeleteUser(user.id, user.name)}
												title="Delete account"
												class="p-2 rounded-xl text-gray-400 hover:text-red-600 hover:bg-red-50 cursor-pointer transition-colors"
											>
												<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
													<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
												</svg>
											</button>
										{/if}
									</div>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		{/if}
	</div>

</div>

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
									? 'Student cannot log in until approved by clinic staff.'
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

				<!-- Section: Academic Details -->
				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-3 flex items-center space-x-2">
						<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
						</svg>
						<span>Academic & Account Information</span>
					</h4>
					<div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Student ID</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.studentId}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Program / Strand</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.programStrand || 'N/A'}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Year & Section</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.yearSection || 'N/A'}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Role</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.role}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">CRRMU Responder</span>
							<span class="text-xs font-bold text-gray-800">{selectedUser.isCrrmuMember ? 'Yes' : 'No'}</span>
						</div>
						<div class="p-3 bg-gray-50 rounded-xl">
							<span class="text-[10px] text-gray-400 font-bold uppercase block">Contact Number</span>
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

				<!-- Section: Legal & Terms and Conditions Consent -->
				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-3 flex items-center space-x-2">
						<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
						</svg>
						<span>Legal & Terms Acceptance Record</span>
					</h4>
					<div class="p-4 bg-gray-50 rounded-2xl border border-gray-200/70 space-y-2">
						<div class="flex items-center justify-between">
							<div class="flex items-center space-x-2">
								<svg class="w-4 h-4 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
								</svg>
								<span class="font-bold text-gray-800">Terms & Conditions & Privacy Agreement</span>
							</div>
							<span class="px-2 py-0.5 rounded-full text-[10px] font-semibold bg-emerald-100 text-emerald-800">
								Consented
							</span>
						</div>
						<p class="text-gray-500 leading-relaxed text-[11px]">
							User agreed to comply with CELTECH School Clinic Health Management System rules and authorized emergency notification protocol under RA 10173 (Philippine Data Privacy Act).
						</p>
					</div>
				</div>
			</div>

			<!-- Modal Footer -->
			<div class="p-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
				<span class="text-[11px] text-gray-500">ID: {selectedUser.id}</span>
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
{/if}
