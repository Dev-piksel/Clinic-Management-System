<script lang="ts">
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import { fetchAuditLogs, checkBackendHealth } from '#lib/api';
	import type { AuditLogItem } from '#lib/types';

	let logs = $state<AuditLogItem[]>([]);
	let isLoading = $state(true);
	let isBackendOnline = $state<boolean | null>(null);
	let errorMessage = $state('');

	// Filters
	let selectedCategory = $state<'all' | 'USER_MANAGEMENT' | 'AUTHENTICATION' | 'SECURITY'>('all');
	let selectedAction = $state<string>('all');
	let searchQuery = $state('');

	async function loadLogs() {
		isLoading = true;
		errorMessage = '';
		try {
			const health = await checkBackendHealth();
			isBackendOnline = health !== null;

			if (isBackendOnline) {
				logs = await fetchAuditLogs({
					category: selectedCategory,
					action: selectedAction,
					search: searchQuery
				});
			} else {
				logs = [];
			}
		} catch (err: any) {
			console.error('Failed to load audit logs', err);
			errorMessage = err.message || 'Failed to retrieve system audit logs';
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		if (clinicStore.isLoggedIn && clinicStore.currentUser.category !== 'staff') {
			goto('/dashboard');
			return;
		}
		loadLogs();
	});

	let filteredLogs = $derived.by(() => {
		let list = logs;
		if (selectedCategory !== 'all') {
			list = list.filter((l) => l.category === selectedCategory);
		}
		if (selectedAction !== 'all') {
			list = list.filter((l) => l.action === selectedAction);
		}
		if (searchQuery.trim()) {
			const q = searchQuery.toLowerCase().trim();
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

	let stats = $derived.by(() => {
		const total = logs.length;
		const userMgmt = logs.filter((l) => l.category === 'USER_MANAGEMENT').length;
		const auth = logs.filter((l) => l.category === 'AUTHENTICATION').length;
		const security = logs.filter((l) => l.category === 'SECURITY').length;
		return { total, userMgmt, auth, security };
	});

	function formatTimestamp(isoStr: string) {
		try {
			const d = new Date(isoStr);
			return d.toLocaleString('en-US', {
				month: 'short',
				day: 'numeric',
				year: 'numeric',
				hour: '2-digit',
				minute: '2-digit',
				second: '2-digit'
			});
		} catch {
			return isoStr;
		}
	}

	function getActionBadgeStyle(action: string) {
		switch (action) {
			case 'ROLE_UPDATED':
				return 'bg-purple-50 text-purple-700 border-purple-200';
			case 'ADMIN_CREATED_USER':
				return 'bg-blue-50 text-blue-700 border-blue-200';
			case 'USER_STATUS_UPDATED':
				return 'bg-emerald-50 text-emerald-700 border-emerald-200';
			case 'PASSWORD_RESET':
				return 'bg-amber-50 text-amber-700 border-amber-200';
			case 'USER_DELETED':
				return 'bg-red-50 text-red-700 border-red-200';
			case 'USER_LOGIN':
				return 'bg-slate-50 text-slate-700 border-slate-200';
			case 'USER_SELF_REGISTERED':
				return 'bg-teal-50 text-teal-700 border-teal-200';
			default:
				return 'bg-gray-50 text-gray-700 border-gray-200';
		}
	}

	function exportCsv() {
		if (!filteredLogs.length) return;
		const headers = ['Timestamp', 'Actor Name', 'Actor Role', 'Action', 'Category', 'Target User', 'Target Role', 'Details'];
		const rows = filteredLogs.map((l) => [
			`"${l.timestamp}"`,
			`"${l.actorName}"`,
			`"${l.actorRole}"`,
			`"${l.action}"`,
			`"${l.category}"`,
			`"${l.targetUserName || ''}"`,
			`"${l.targetUserRole || ''}"`,
			`"${l.details.replace(/"/g, '""')}"`
		]);
		const csvContent = [headers.join(','), ...rows.map((r) => r.join(','))].join('\n');
		const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
		const url = URL.createObjectURL(blob);
		const link = document.createElement('a');
		link.setAttribute('href', url);
		link.setAttribute('download', `cshms_audit_logs_${new Date().toISOString().slice(0, 10)}.csv`);
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
	}
</script>

<svelte:head>
	<title>Security & Activity Audit Logs - Clinic Admin - CSHMS</title>
</svelte:head>

<div class="space-y-8">

	<!-- Top Header & Tabs -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
		<div>
			<div class="flex items-center space-x-2 mb-1">
				<p class="text-[10px] font-bold tracking-[0.18em] text-[#1b522f] uppercase">
					CLINIC SYSTEM GOVERNANCE
				</p>
				<span class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-[#1b522f]/10 text-[#1b522f]">
					Immutable Trail
				</span>
			</div>
			<h2 class="text-2xl font-bold tracking-tight text-gray-900">Security & Activity Audit Logs</h2>
			<p class="text-xs sm:text-sm text-gray-500 mt-0.5">
				Track user registrations, administrator role changes, password resets, account approvals, and portal logins.
			</p>
		</div>

		<div class="flex items-center space-x-2.5">
			<a
				href="/admin/users"
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl border border-gray-200 bg-white text-xs font-semibold text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors shadow-2xs"
			>
				<svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
				</svg>
				<span>Manage User Accounts</span>
			</a>

			<button
				type="button"
				onclick={exportCsv}
				disabled={filteredLogs.length === 0}
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl border border-gray-200 bg-white text-xs font-semibold text-gray-700 hover:bg-gray-50 hover:border-gray-300 transition-colors shadow-2xs disabled:opacity-50"
			>
				<svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
				</svg>
				<span>Export CSV</span>
			</button>

			<button
				type="button"
				onclick={loadLogs}
				disabled={isLoading}
				class="inline-flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-[#1b522f] text-white text-xs font-semibold hover:bg-[#154225] transition-colors shadow-xs cursor-pointer"
			>
				<svg class="w-4 h-4 {isLoading ? 'animate-spin' : ''}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
				</svg>
				<span>Refresh</span>
			</button>
		</div>
	</div>

	<!-- Top Metric Cards -->
	<div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
		<div class="p-4 sm:p-5 rounded-2xl bg-white border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
				</svg>
			</div>
			<div>
				<p class="text-xs font-medium text-gray-500">Total Audit Logs</p>
				<h3 class="text-xl sm:text-2xl font-bold text-gray-900 mt-0.5">{stats.total}</h3>
				<p class="text-[11px] text-gray-400">All recorded operations</p>
			</div>
		</div>

		<div class="p-4 sm:p-5 rounded-2xl bg-white border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-xl bg-purple-50 text-purple-700 flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
				</svg>
			</div>
			<div>
				<p class="text-xs font-medium text-gray-500">User Operations</p>
				<h3 class="text-xl sm:text-2xl font-bold text-purple-900 mt-0.5">{stats.userMgmt}</h3>
				<p class="text-[11px] text-purple-600 font-medium">Roles & approvals</p>
			</div>
		</div>

		<div class="p-4 sm:p-5 rounded-2xl bg-white border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-700 flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
				</svg>
			</div>
			<div>
				<p class="text-xs font-medium text-gray-500">Security Events</p>
				<h3 class="text-xl sm:text-2xl font-bold text-amber-900 mt-0.5">{stats.security}</h3>
				<p class="text-[11px] text-amber-600 font-medium">Password resets</p>
			</div>
		</div>

		<div class="p-4 sm:p-5 rounded-2xl bg-white border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 16l-4-4m0 0l4-4m-4 4h14m-5 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h7a3 3 0 013 3v1"></path>
				</svg>
			</div>
			<div>
				<p class="text-xs font-medium text-gray-500">Auth Sessions</p>
				<h3 class="text-xl sm:text-2xl font-bold text-blue-900 mt-0.5">{stats.auth}</h3>
				<p class="text-[11px] text-blue-600 font-medium">Logins & registrations</p>
			</div>
		</div>
	</div>

	<!-- Filter Controls & Search -->
	<div class="bg-white p-4 sm:p-5 rounded-3xl border border-gray-100 shadow-xs space-y-4">
		<div class="flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
			<!-- Search Bar -->
			<div class="relative flex-1">
				<svg class="w-4 h-4 text-gray-400 absolute left-3.5 top-1/2 -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
				</svg>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search audit trail by actor, target user, action, or details..."
					class="w-full pl-10 pr-4 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] transition-all"
				/>
			</div>

			<!-- Category Filter Dropdown -->
			<div class="flex items-center space-x-2">
				<select
					bind:value={selectedCategory}
					class="px-3.5 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] cursor-pointer"
				>
					<option value="all">All Categories</option>
					<option value="USER_MANAGEMENT">User Management</option>
					<option value="AUTHENTICATION">Authentication</option>
					<option value="SECURITY">Security</option>
				</select>

				<!-- Action Filter Dropdown -->
				<select
					bind:value={selectedAction}
					class="px-3.5 py-2.5 bg-gray-50/70 border border-gray-200/80 rounded-2xl text-xs font-medium text-gray-700 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] cursor-pointer"
				>
					<option value="all">All Action Types</option>
					<option value="ROLE_UPDATED">Role Updated</option>
					<option value="USER_STATUS_UPDATED">Status Updated</option>
					<option value="ADMIN_CREATED_USER">Admin Created User</option>
					<option value="PASSWORD_RESET">Password Reset</option>
					<option value="USER_DELETED">User Deleted</option>
					<option value="USER_LOGIN">User Sign In</option>
					<option value="USER_SELF_REGISTERED">User Self-Registered</option>
				</select>
			</div>
		</div>
	</div>

	<!-- Audit Trail Log Table -->
	<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
		{#if isLoading}
			<div class="p-12 text-center text-gray-400 space-y-3">
				<div class="w-8 h-8 border-3 border-[#1b522f] border-t-transparent rounded-full animate-spin mx-auto"></div>
				<p class="text-xs font-medium">Loading audit logs...</p>
			</div>
		{:else if filteredLogs.length === 0}
			<div class="p-14 text-center text-gray-400 space-y-3">
				<div class="w-14 h-14 bg-gray-50 text-gray-300 rounded-3xl mx-auto flex items-center justify-center">
					<svg class="w-7 h-7" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
					</svg>
				</div>
				<h4 class="text-sm font-semibold text-gray-700">No Audit Logs Found</h4>
				<p class="text-xs text-gray-400 max-w-sm mx-auto">
					No audit activity records matched the selected filters. New actions will automatically appear here.
				</p>
			</div>
		{:else}
			<div class="overflow-x-auto">
				<table class="w-full text-left border-collapse">
					<thead>
						<tr class="bg-gray-50/80 border-b border-gray-100 text-[11px] font-bold text-gray-500 uppercase tracking-wider">
							<th class="py-3.5 px-4 sm:px-6">Timestamp</th>
							<th class="py-3.5 px-4">Action</th>
							<th class="py-3.5 px-4">Performed By (Actor)</th>
							<th class="py-3.5 px-4">Target User</th>
							<th class="py-3.5 px-4 sm:px-6">Description & Details</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-100 text-xs">
						{#each filteredLogs as log (log.id)}
							<tr class="hover:bg-gray-50/60 transition-colors">
								<!-- Timestamp -->
								<td class="py-3.5 px-4 sm:px-6 font-mono text-[11px] text-gray-500 whitespace-nowrap">
									{formatTimestamp(log.timestamp)}
								</td>

								<!-- Action Badge -->
								<td class="py-3.5 px-4 whitespace-nowrap">
									<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold border {getActionBadgeStyle(log.action)}">
										{log.action.replace(/_/g, ' ')}
									</span>
								</td>

								<!-- Actor -->
								<td class="py-3.5 px-4 whitespace-nowrap">
									<div>
										<p class="font-bold text-gray-900">{log.actorName}</p>
										<p class="text-[10px] text-gray-400">{log.actorRole}</p>
									</div>
								</td>

								<!-- Target User -->
								<td class="py-3.5 px-4 whitespace-nowrap">
									{#if log.targetUserName}
										<div>
											<p class="font-semibold text-gray-800">{log.targetUserName}</p>
											{#if log.targetUserRole}
												<p class="text-[10px] text-gray-400">{log.targetUserRole}</p>
											{/if}
										</div>
									{:else}
										<span class="text-gray-400 italic text-[11px]">System / Self</span>
									{/if}
								</td>

								<!-- Details -->
								<td class="py-3.5 px-4 sm:px-6 text-gray-600 leading-relaxed min-w-[280px]">
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
