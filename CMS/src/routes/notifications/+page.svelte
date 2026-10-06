<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';

	let activeFilter = $state<'all' | 'unread' | 'appointment' | 'message'>('all');

	let filteredNotifications = $derived.by(() => {
		if (activeFilter === 'unread') {
			return clinicStore.notifications.filter((n) => !n.read);
		}
		if (activeFilter === 'appointment') {
			return clinicStore.notifications.filter((n) => n.category === 'appointment');
		}
		if (activeFilter === 'message') {
			return clinicStore.notifications.filter((n) => n.category === 'message' || n.category === 'visit');
		}
		return clinicStore.notifications;
	});

	let unreadCount = $derived(clinicStore.notifications.filter((n) => !n.read).length);
</script>

<svelte:head>
	<title>Notifications - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-5xl">
	<!-- Page Header -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				UPDATES FROM THE CLINIC
			</p>
			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				Notifications
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Appointment changes, follow-ups, and important clinic messages.
			</p>
		</div>

		<button
			type="button"
			onclick={() => clinicStore.markAllNotificationsRead()}
			class="inline-flex items-center space-x-1.5 px-4 py-2.5 rounded-xl bg-[#edf7f0] hover:bg-[#e2f2e6] border border-[#1b522f]/20 text-[#1b522f] text-xs font-semibold shadow-2xs transition-colors cursor-pointer self-start sm:self-auto"
		>
			<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
			</svg>
			<span>Mark all as read</span>
		</button>
	</div>

	<!-- Filter Pills -->
	<div class="flex flex-wrap items-center gap-2 pt-2">
		<button
			type="button"
			onclick={() => (activeFilter = 'all')}
			class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors cursor-pointer {activeFilter === 'all'
				? 'bg-[#1b522f] text-white shadow-2xs'
				: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
		>
			All {clinicStore.notifications.length}
		</button>
		<button
			type="button"
			onclick={() => (activeFilter = 'unread')}
			class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors cursor-pointer {activeFilter === 'unread'
				? 'bg-[#1b522f] text-white shadow-2xs'
				: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
		>
			Unread {unreadCount}
		</button>
		<button
			type="button"
			onclick={() => (activeFilter = 'appointment')}
			class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors cursor-pointer {activeFilter === 'appointment'
				? 'bg-[#1b522f] text-white shadow-2xs'
				: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
		>
			Appointments
		</button>
		<button
			type="button"
			onclick={() => (activeFilter = 'message')}
			class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition-colors cursor-pointer {activeFilter === 'message'
				? 'bg-[#1b522f] text-white shadow-2xs'
				: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
		>
			Clinic messages
		</button>
	</div>

	<!-- Notifications Card -->
	<div class="bg-white rounded-3xl border border-gray-100 shadow-xs divide-y divide-gray-100 overflow-hidden">
		{#if filteredNotifications.length === 0}
			<div class="py-12 text-center text-gray-400 text-sm">
				No notifications found in this category.
			</div>
		{:else}
			{#each filteredNotifications as notif (notif.id)}
				{@const isUnread = !notif.read}
				<div
					class="p-5 md:p-6 flex items-center justify-between transition-colors {isUnread
						? 'bg-[#f4f9f6]/90'
						: 'bg-white hover:bg-gray-50/50'}"
				>
					<!-- Left Icon & Content -->
					<div class="flex items-start space-x-4 min-w-0 pr-4">
						<div class="w-10 h-10 rounded-full bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 mt-0.5">
							{#if notif.category === 'appointment' && notif.type === 'confirmation'}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
								</svg>
							{:else if notif.category === 'visit'}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
								</svg>
							{:else if notif.category === 'appointment'}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
								</svg>
							{:else}
								<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
								</svg>
							{/if}
						</div>

						<div class="min-w-0">
							<div class="flex items-center space-x-1.5">
								<h3 class="text-sm font-bold text-gray-800 leading-snug">{notif.title}</h3>
								{#if isUnread}
									<span class="w-2 h-2 rounded-full bg-[#1b522f]"></span>
								{/if}
							</div>
							<p class="text-xs text-gray-600 mt-1 leading-relaxed">{notif.message}</p>
							<span class="text-[11px] {isUnread ? 'text-[#1b522f] font-semibold' : 'text-gray-400'} mt-1 block">
								{notif.time}
							</span>
						</div>
					</div>

					<!-- Right Action Link -->
					{#if notif.actionText && notif.actionHref}
						<a
							href={notif.actionHref}
							class="text-xs font-semibold text-gray-700 hover:text-[#1b522f] flex items-center space-x-1 shrink-0 whitespace-nowrap transition-colors py-2 px-3 rounded-lg hover:bg-white/80"
						>
							<span>{notif.actionText}</span>
							<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
							</svg>
						</a>
					{/if}
				</div>
			{/each}
		{/if}
	</div>
</div>
