<script lang="ts">
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import { fetchAdminStats } from '#lib/api';
	import { onMount } from 'svelte';

	let currentPath = $derived(page.url.pathname);
	let isStaff = $derived(clinicStore.currentUser.category === 'staff');

	onMount(async () => {
		if (isStaff) {
			try {
				const stats = await fetchAdminStats();
				clinicStore.setPendingUsersCount(stats.pending);
			} catch {
				// Backend might be offline; silent fallback
			}
		}
	});

	const studentNavItems = [
		{
			id: 'dashboard',
			label: 'Dashboard',
			href: '/dashboard',
			icon: 'home'
		},
		{
			id: 'appointments',
			label: 'Appointments',
			href: '/appointments',
			icon: 'calendar'
		},
		{
			id: 'clinic-visits',
			label: 'Clinic Visits',
			href: '/clinic-visits',
			icon: 'clipboard'
		},
		{
			id: 'profile',
			label: 'Profile',
			href: '/profile',
			icon: 'user'
		},
		{
			id: 'notifications',
			label: 'Notifications',
			href: '/notifications',
			icon: 'bell',
			hasBadge: true
		}
	];

	const staffNavItems = [
		{
			id: 'dashboard',
			label: 'Dashboard',
			href: '/dashboard',
			icon: 'grid'
		},
		{
			id: 'appointments',
			label: 'Appointments',
			href: '/appointments',
			icon: 'calendar'
		},
		{
			id: 'queue',
			label: 'Queue',
			href: '/queue',
			icon: 'queue'
		},
		{
			id: 'students',
			label: 'Students',
			href: '/students',
			icon: 'search-user'
		},
		{
			id: 'admin-users',
			label: 'User Approvals',
			href: '/admin/users',
			icon: 'users-check',
			get badgeCount() {
				return clinicStore.pendingUsersCount;
			}
		},
		{
			id: 'clinic-visits',
			label: 'Clinic Visits',
			href: '/clinic-visits',
			icon: 'clipboard'
		},
		{
			id: 'medical-records',
			label: 'Medical Records',
			href: '/medical-records',
			icon: 'document'
		},
		{
			id: 'crrmu-reports',
			label: 'CRRMU Reports',
			href: '/crrmu-reports',
			icon: 'shield',
			get badgeCount() {
				return clinicStore.pendingCrrmuCount;
			}
		},
		{
			id: 'reports',
			label: 'Reports',
			href: '/reports',
			icon: 'chart'
		},
		{
			id: 'profile',
			label: 'Profile',
			href: '/profile',
			icon: 'user'
		}
	];

	let visibleNavItems = $derived.by(() => {
		if (isStaff) {
			return staffNavItems;
		}
		const items = [...studentNavItems];
		if (clinicStore.currentUser.isCrrmuMember) {
			items.push({
				id: 'first-aid-reports',
				label: 'First Aid Reports',
				href: '/first-aid-reports',
				icon: 'shield',
				hasBadge: false
			});
		}
		return items;
	});

	function handleSignOut() {
		clinicStore.logout();
		goto('/');
	}
</script>

<aside class="w-64 bg-white border-r border-gray-100 flex flex-col justify-between p-6 shrink-0 h-screen overflow-y-auto z-30">
	<div>
		<!-- Logo Area -->
		<a href="/dashboard" class="flex items-center space-x-3 group">
			<div class="w-11 h-11 bg-[#52ad69] rounded-2xl flex items-center justify-center shadow-xs transition-colors">
				<svg class="w-6 h-6 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
					<polyline points="7 12 9 12 11 16 14 8 16 12 18 12"></polyline>
				</svg>
			</div>
			<div>
				<h1 class="font-bold text-lg text-[#1b522f] leading-tight tracking-tight">CSHMS</h1>
				<p class="text-gray-400 text-[11px] font-medium">CELTECH School Clinic</p>
			</div>
		</a>

		<!-- Category Pill -->
		<div class="mt-7 mb-4">
			<span class="inline-block px-3 py-1 bg-[#e8f5ec] text-[#1b522f] text-[10px] font-bold rounded-lg tracking-wider uppercase">
				{isStaff ? 'CLINIC PORTAL' : 'STUDENT PORTAL'}
			</span>
		</div>

		<!-- Nav Links -->
		<nav class="space-y-1">
			{#each visibleNavItems as item (item.id)}
				{@const isActive = currentPath === item.href || (item.href !== '/dashboard' && currentPath.startsWith(item.href))}
				<a
					href={item.href}
					class="w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all {isActive
						? 'bg-[#edf7f0] text-[#1b522f] font-semibold shadow-xs'
						: 'text-gray-500 hover:text-gray-800 hover:bg-gray-50'}"
				>
					<div class="flex items-center space-x-3.5 min-w-0">
						{#if item.icon === 'home'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
							</svg>
						{:else if item.icon === 'grid'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"></path>
							</svg>
						{:else if item.icon === 'calendar'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
							</svg>
						{:else if item.icon === 'queue'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
							</svg>
						{:else if item.icon === 'search-user'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
							</svg>
						{:else if item.icon === 'clipboard'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
							</svg>
						{:else if item.icon === 'document'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
							</svg>
						{:else if item.icon === 'chart'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 17v-2m3 2v-4m3 4v-6m2 10H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
							</svg>
						{:else if item.icon === 'user'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
							</svg>
						{:else if item.icon === 'bell'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
							</svg>
						{:else if item.icon === 'shield'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
							</svg>
						{:else if item.icon === 'users-check'}
							<svg class="w-5 h-5 shrink-0 {isActive ? 'text-[#1b522f]' : 'text-gray-400'}" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"></path>
							</svg>
						{/if}
						<span class="truncate">{item.label}</span>
					</div>

					{#if 'badgeCount' in item && item.badgeCount}
						<span class="w-5 h-5 rounded-full bg-[#1b522f] text-white text-[11px] font-bold flex items-center justify-center shrink-0">
							{item.badgeCount}
						</span>
					{:else if 'hasBadge' in item && item.hasBadge && clinicStore.unreadNotificationsCount > 0}
						<span class="w-5 h-5 rounded-full bg-[#1b522f] text-white text-[11px] font-bold flex items-center justify-center shrink-0">
							{clinicStore.unreadNotificationsCount}
						</span>
					{/if}
				</a>
			{/each}
		</nav>
	</div>

	<!-- Bottom User & Sign Out -->
	<div class="pt-6 border-t border-gray-100">
		<div class="flex items-center space-x-3 mb-3">
			<div
				class="w-10 h-10 rounded-xl flex items-center justify-center font-bold text-xs shrink-0 shadow-xs"
				style="background-color: {clinicStore.currentUser.avatarBg}; color: {clinicStore.currentUser.avatarColor};"
			>
				{clinicStore.currentUser.initials}
			</div>
			<div class="truncate">
				<p class="text-xs font-semibold text-gray-800 truncate">{clinicStore.currentUser.name}</p>
				<p class="text-[11px] text-gray-400 truncate">{clinicStore.currentUser.role}</p>
			</div>
		</div>

		<div class="space-y-1 mb-2">
			<a
				href="/terms"
				class="w-full flex items-center space-x-2 text-[11px] font-medium text-gray-400 hover:text-[#1b522f] transition-colors py-1 px-1 rounded-lg hover:bg-gray-50"
			>
				<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
				</svg>
				<span>Terms & Conditions</span>
			</a>
		</div>

		<button
			type="button"
			onclick={handleSignOut}
			class="w-full flex items-center space-x-2 text-xs font-medium text-gray-400 hover:text-red-600 transition-colors py-1.5 px-1 rounded-lg hover:bg-red-50/50 cursor-pointer"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path>
			</svg>
			<span>Sign out</span>
		</button>
	</div>
</aside>
