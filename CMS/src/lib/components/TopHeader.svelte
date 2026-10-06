<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';

	let showNotifications = $state(false);
	let isStaff = $derived(clinicStore.currentUser.category === 'staff');
	let searchQuery = $state('');

	function toggleNotifications() {
		showNotifications = !showNotifications;
	}

	function closeNotifications() {
		showNotifications = false;
	}
</script>

<header class="h-20 bg-white border-b border-gray-100 px-8 flex items-center justify-between shrink-0 z-20 gap-4">
	<!-- Left Title -->
	<div class="shrink-0">
		<h2 class="text-sm font-bold text-gray-900 tracking-tight">
			{isStaff ? 'Clinic Portal' : 'Student Portal'}
		</h2>
		<p class="text-xs text-gray-400 font-medium">
			{isStaff ? 'Monday clinic overview' : 'Your health hub'}
		</p>
	</div>

	<!-- Center Search Bar (Staff / Clinic Portal) -->
	{#if isStaff}
		<div class="w-80 hidden md:block">
			<div class="relative w-full">
				<div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
					<svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
					</svg>
				</div>
				<input
					type="text"
					bind:value={searchQuery}
					placeholder="Search student or number"
					class="w-full pl-9 pr-4 py-2 bg-[#f4f7f4] border border-transparent rounded-2xl text-xs text-gray-700 placeholder-gray-400 focus:outline-none focus:ring-1 focus:ring-[#1b522f]/25 focus:bg-white focus:border-gray-200 transition-all shadow-2xs"
				/>
			</div>
		</div>
	{/if}

	<!-- Right Actions -->
	<div class="flex items-center space-x-4 shrink-0">
		<!-- Notification Bell -->
		<div class="relative">
			<button
				type="button"
				onclick={toggleNotifications}
				aria-label="View notifications"
				class="w-10 h-10 rounded-2xl bg-[#edf7f0] hover:bg-[#e2f2e6] text-[#1b522f] flex items-center justify-center transition-colors relative cursor-pointer"
			>
				<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
				</svg>
				{#if clinicStore.unreadNotificationsCount > 0}
					<span class="absolute top-2.5 right-2.5 w-2 h-2 rounded-full bg-[#48b469] ring-2 ring-[#edf7f0]"></span>
				{/if}
			</button>

			<!-- Dropdown Menu -->
			{#if showNotifications}
				<button
					type="button"
					tabindex="-1"
					aria-label="Close notifications menu"
					class="fixed inset-0 z-20 cursor-default bg-transparent border-0"
					onclick={closeNotifications}
					onkeydown={(e) => e.key === 'Escape' && closeNotifications()}
				></button>

				<div class="absolute right-0 mt-2 w-80 bg-white rounded-2xl shadow-xl border border-gray-100 p-4 z-30">
					<div class="flex items-center justify-between pb-3 border-b border-gray-100">
						<span class="font-bold text-xs text-gray-800">Notifications ({clinicStore.unreadNotificationsCount})</span>
						<button
							type="button"
							onclick={() => clinicStore.markAllNotificationsRead()}
							class="text-[11px] text-[#1b522f] font-semibold hover:underline cursor-pointer"
						>
							Mark all read
						</button>
					</div>

					<div class="divide-y divide-gray-50 max-h-72 overflow-y-auto mt-2">
						{#each clinicStore.notifications as notif (notif.id)}
							<div class="py-2.5 px-1 hover:bg-gray-50 rounded-lg transition-colors">
								<div class="flex items-start justify-between">
									<p class="text-xs font-semibold text-gray-800">{notif.title}</p>
									<span class="text-[10px] text-gray-400">{notif.time}</span>
								</div>
								<p class="text-[11px] text-gray-500 mt-0.5 leading-snug">{notif.message}</p>
							</div>
						{/each}
					</div>
				</div>
			{/if}
		</div>

		<!-- Vertical Divider Line (matching original design) -->
		<div class="h-6 w-px bg-gray-200"></div>

		<!-- User Avatar Profile (Unboxed: squircle avatar + name & role) -->
		<a
			href="/profile"
			class="flex items-center space-x-3 group cursor-pointer"
		>
			<div
				class="w-10 h-10 rounded-2xl flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs"
				style="background-color: {clinicStore.currentUser.avatarBg}; color: {clinicStore.currentUser.avatarColor};"
			>
				{clinicStore.currentUser.initials}
			</div>
			<div class="text-left pr-1">
				<p class="text-xs font-bold text-gray-800 leading-tight group-hover:text-[#1b522f] transition-colors">
					{clinicStore.currentUser.name}
				</p>
				<p class="text-[11px] text-gray-400 font-medium leading-none mt-0.5">
					{clinicStore.currentUser.role}
				</p>
			</div>
		</a>
	</div>
</header>
