<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { goto } from '$app/navigation';

	let showClarificationModal = $state(false);
	let clarificationMessage = $state('');
	let clarificationSent = $state(false);
	let showDismissConfirm = $state(false);

	function handleAddRecord() {
		clinicStore.approvePendingCrrmuReport();
	}

	function handleSendClarification() {
		if (!clarificationMessage.trim()) return;
		clinicStore.notifications = [
			{
				id: `notif-${Date.now()}`,
				title: 'Clarification requested on CRRMU report',
				message: `Head Nurse Alma A. Lontoc asked: "${clarificationMessage}"`,
				time: 'Just now',
				type: 'reminder',
				read: false,
				actionText: 'Reply in portal',
				actionHref: '/first-aid-reports',
				category: 'message'
			},
			...clinicStore.notifications
		];
		clarificationSent = true;
		setTimeout(() => {
			showClarificationModal = false;
			clarificationSent = false;
			clarificationMessage = '';
		}, 1500);
	}

	function handleDismiss() {
		clinicStore.crrmuReportApproved = true;
		showDismissConfirm = false;
	}
</script>

<svelte:head>
	<title>Pending CRRMU Report - Clinic Portal - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Page Eyebrow & Title -->
	<div>
		<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
			CLINIC REVIEW
		</p>
		<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
			Pending CRRMU report
		</h1>
		<p class="text-sm text-gray-500 mt-1">
			Verify the incident before incorporating it into the official record.
		</p>
	</div>

	{#if clinicStore.crrmuReportApproved}
		<!-- Approved Success State -->
		<div class="bg-white rounded-3xl p-8 border border-gray-100 shadow-xs space-y-4 max-w-2xl">
			<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
				</svg>
			</div>
			<h2 class="text-xl font-bold text-gray-900">Report processed</h2>
			<p class="text-sm text-gray-600">
				The first aid incident has been verified and added to Faith Manada's official clinic timeline.
			</p>
			<div class="pt-2 flex items-center space-x-3">
				<a
					href="/medical-records"
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold inline-flex items-center space-x-2 transition-colors cursor-pointer"
				>
					<span>View in Medical records</span>
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</a>
				<button
					type="button"
					onclick={() => (clinicStore.crrmuReportApproved = false)}
					class="px-4 py-2.5 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 text-xs font-medium cursor-pointer"
				>
					Reset review demo
				</button>
			</div>
		</div>
	{:else}
		<!-- Main Review Grid (Matching Image 4) -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
			
			<!-- Left Card: Pending Report Details -->
			<div class="lg:col-span-8 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
				<!-- Header Row -->
				<div class="flex items-center justify-between">
					<span class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
						SUBMITTED TODAY · 10:42 AM
					</span>
					<span class="px-3 py-1 rounded-full text-xs font-medium bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
						Pending review
					</span>
				</div>

				<!-- Section Title -->
				<h2 class="text-xl font-bold text-gray-900 tracking-tight">
					First aid assistance
				</h2>

				<!-- Participant Flow Pill / Card -->
				<div class="bg-[#f4f9f6] border border-[#1b522f]/10 rounded-2xl p-4 flex items-center justify-between">
					<!-- Responder -->
					<div class="flex items-center space-x-3">
						<div class="w-10 h-10 rounded-xl bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs">
							VS
						</div>
						<div>
							<p class="text-sm font-bold text-gray-900 leading-tight">Vergel Suniga Jr.</p>
							<p class="text-[11px] text-gray-400 mt-0.5">CRRMU Member</p>
						</div>
					</div>

					<!-- Chevron Arrow -->
					<div class="px-3 text-gray-400">
						<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
						</svg>
					</div>

					<!-- Student Assisted -->
					<div class="flex items-center space-x-3 text-right sm:text-left">
						<div class="w-10 h-10 rounded-xl bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs">
							FM
						</div>
						<div>
							<p class="text-sm font-bold text-gray-900 leading-tight">Faith Manada</p>
							<p class="text-[11px] text-gray-400 mt-0.5">Student assisted</p>
						</div>
					</div>
				</div>

				<!-- Incident Breakdown List -->
				<div class="divide-y divide-gray-100 text-xs">
					<div class="py-3.5 flex items-center justify-between">
						<span class="text-gray-400 font-medium">Incident</span>
						<span class="font-bold text-gray-800">Minor injury</span>
					</div>

					<div class="py-3.5 flex items-center justify-between">
						<span class="text-gray-400 font-medium">Assistance</span>
						<span class="font-bold text-gray-800">Wound cleaning + Bandaging</span>
					</div>

					<div class="py-3.5 flex items-center justify-between">
						<span class="text-gray-400 font-medium">Condition</span>
						<span class="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
							Stable
						</span>
					</div>

					<div class="py-3.5 flex flex-col sm:flex-row sm:items-start justify-between gap-2">
						<span class="text-gray-400 font-medium shrink-0">Notes</span>
						<span class="font-medium text-gray-700 sm:text-right leading-relaxed max-w-md">
							Student was assisted to the clinic after first aid.
						</span>
					</div>
				</div>
			</div>

			<!-- Right Card: Nurse Action (Review Decision) -->
			<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
				<div>
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
						NURSE ACTION
					</p>
					<h3 class="text-lg font-bold text-gray-900 mt-1">
						Review decision
					</h3>
					<p class="text-xs text-gray-500 mt-1.5 leading-relaxed">
						Confirm the report details before adding this event to Faith's clinic timeline.
					</p>
				</div>

				<div class="space-y-3 pt-2">
					<!-- Button 1: Add to clinic record -->
					<button
						type="button"
						onclick={handleAddRecord}
						class="w-full bg-[#1b522f] hover:bg-[#154225] text-white font-medium py-3.5 rounded-2xl text-xs flex justify-center items-center space-x-2 transition-all cursor-pointer shadow-xs active:scale-[0.99]"
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
						<span>Add to clinic record</span>
					</button>

					<!-- Button 2: Request clarification -->
					<button
						type="button"
						onclick={() => (showClarificationModal = true)}
						class="w-full bg-[#edf7f0] hover:bg-[#e2f2e6] text-[#1b522f] border border-[#1b522f]/20 font-medium py-3.5 rounded-2xl text-xs flex justify-center items-center space-x-2 transition-all cursor-pointer shadow-2xs"
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 10h.01M12 10h.01M16 10h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"></path>
						</svg>
						<span>Request clarification</span>
					</button>

					<!-- Button 3: Dismiss report -->
					<div class="pt-2 text-center">
						<button
							type="button"
							onclick={() => (showDismissConfirm = true)}
							class="text-xs text-gray-500 hover:text-red-600 transition-colors cursor-pointer py-1"
						>
							Dismiss report
						</button>
					</div>
				</div>
			</div>

		</div>
	{/if}
</div>

<!-- ================= REQUEST CLARIFICATION MODAL ================= -->
{#if showClarificationModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-lg w-full p-6 sm:p-8 shadow-2xl border border-gray-100 space-y-5">
			<div class="flex items-start justify-between pb-3 border-b border-gray-100">
				<div>
					<span class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">COMMUNICATION</span>
					<h3 class="text-lg font-bold text-gray-800 mt-1">Request Clarification</h3>
				</div>
				<button
					type="button"
					onclick={() => (showClarificationModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-gray-100 text-gray-400 hover:text-gray-700 flex items-center justify-center transition-colors cursor-pointer"
				>
					✕
				</button>
			</div>

			<p class="text-xs text-gray-600">
				Send a follow-up inquiry to responder <strong>Vergel Suniga Jr. (CRRMU)</strong> regarding incident report #FAR-2026-01:
			</p>

			{#if clarificationSent}
				<div class="p-4 bg-[#edf7f0] text-[#1b522f] rounded-2xl text-xs font-semibold text-center">
					✓ Clarification message sent to Vergel Suniga Jr.
				</div>
			{:else}
				<div class="space-y-3">
					<div class="flex flex-wrap gap-2 text-[11px]">
						<button
							type="button"
							onclick={() => (clarificationMessage = 'Was any topical antibiotic or ointment administered before bandaging?')}
							class="px-2.5 py-1 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-600 cursor-pointer"
						>
							+ Antibiotic inquiry
						</button>
						<button
							type="button"
							onclick={() => (clarificationMessage = 'Please confirm the exact location on campus where the injury occurred.')}
							class="px-2.5 py-1 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg text-gray-600 cursor-pointer"
						>
							+ Location detail
						</button>
					</div>

					<textarea
						bind:value={clarificationMessage}
						rows="3"
						placeholder="Type questions or instructions for the first aid responder..."
						class="w-full p-3.5 bg-white border border-gray-200 rounded-2xl text-xs focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
					></textarea>

					<div class="flex justify-end space-x-2 pt-2">
						<button
							type="button"
							onclick={() => (showClarificationModal = false)}
							class="px-4 py-2 rounded-xl border border-gray-200 text-gray-600 text-xs font-medium cursor-pointer"
						>
							Cancel
						</button>
						<button
							type="button"
							onclick={handleSendClarification}
							class="px-5 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer"
						>
							Send message
						</button>
					</div>
				</div>
			{/if}
		</div>
	</div>
{/if}

<!-- ================= DISMISS REPORT CONFIRM MODAL ================= -->
{#if showDismissConfirm}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border border-gray-100 space-y-4 text-center">
			<div class="w-12 h-12 rounded-full bg-red-50 text-red-600 flex items-center justify-center mx-auto">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
				</svg>
			</div>
			<h3 class="text-base font-bold text-gray-900">Dismiss this report?</h3>
			<p class="text-xs text-gray-500">
				The incident will not be appended to Faith's clinic record timeline.
			</p>
			<div class="flex justify-center space-x-3 pt-2">
				<button
					type="button"
					onclick={() => (showDismissConfirm = false)}
					class="px-4 py-2 rounded-xl border border-gray-200 text-gray-600 text-xs font-medium cursor-pointer"
				>
					Keep report
				</button>
				<button
					type="button"
					onclick={handleDismiss}
					class="px-4 py-2 rounded-xl bg-red-600 text-white text-xs font-semibold cursor-pointer"
				>
					Confirm dismiss
				</button>
			</div>
		</div>
	</div>
{/if}
