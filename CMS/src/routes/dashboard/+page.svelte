<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { goto } from '$app/navigation';

	let isStaff = $derived(clinicStore.currentUser.category === 'staff');
</script>

<svelte:head>
	<title>{isStaff ? 'Clinic Dashboard - CSHMS' : 'Student Portal Dashboard - CSHMS'}</title>
</svelte:head>

{#if isStaff}
	<!-- ================= CLINIC STAFF / HEAD NURSE DASHBOARD ================= -->
	<div class="space-y-8">
		<!-- Top Staff Header -->
		<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.18em] text-[#1b522f] uppercase mb-1">
					MONDAY, OCTOBER 4
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					Good afternoon, {clinicStore.currentUser.firstName}.
				</h1>
				<p class="text-sm text-gray-500 mt-0.5">
					Here's what needs your attention at the clinic today.
				</p>
			</div>

			<button
				type="button"
				onclick={() => goto('/queue')}
				class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors self-start sm:self-auto cursor-pointer"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
				</svg>
				<span>New clinic visit</span>
			</button>
		</div>

		<!-- 6 Metric Cards Row -->
		<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3.5">
			<!-- 1. Appointments -->
			<a href="/appointments" class="bg-white hover:bg-gray-50/80 p-4 rounded-2xl border border-gray-100 shadow-2xs group transition-all">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300 group-hover:text-[#1b522f] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">8</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Today's appointments</p>
				<p class="text-[10px] text-gray-400 mt-0.5">3 remaining</p>
			</a>

			<!-- 2. Waiting students -->
			<a href="/queue" class="bg-white hover:bg-gray-50/80 p-4 rounded-2xl border border-gray-100 shadow-2xs group transition-all">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300 group-hover:text-[#1b522f] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">3</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Waiting students</p>
				<p class="text-[10px] text-gray-400 mt-0.5">Longest: 12 min</p>
			</a>

			<!-- 3. Active clinic visits -->
			<div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-2xs">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M13 10V3L4 14h7v7l9-11h-7z"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">2</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Active clinic visits</p>
				<p class="text-[10px] text-gray-400 mt-0.5">1 under observation</p>
			</div>

			<!-- 4. Follow-ups -->
			<div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-2xs">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">4</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Follow-ups</p>
				<p class="text-[10px] text-gray-400 mt-0.5">2 due today</p>
			</div>

			<!-- 5. Sent home -->
			<div class="bg-white p-4 rounded-2xl border border-gray-100 shadow-2xs">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">1</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Sent home</p>
				<p class="text-[10px] text-gray-400 mt-0.5">Contact completed</p>
			</div>

			<!-- 6. Pending CRRMU -->
			<a href="/first-aid-reports" class="bg-white hover:bg-gray-50/80 p-4 rounded-2xl border border-gray-100 shadow-2xs group transition-all">
				<div class="flex items-center justify-between mb-2">
					<div class="w-8 h-8 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
						</svg>
					</div>
					<svg class="w-3.5 h-3.5 text-gray-300 group-hover:text-[#1b522f] transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</div>
				<p class="text-2xl font-bold text-gray-800">1</p>
				<p class="text-[11px] font-semibold text-gray-700 leading-tight mt-0.5">Pending CRRMU</p>
				<p class="text-[10px] text-gray-400 mt-0.5">Needs review</p>
			</a>
		</div>

		<!-- Live Flow Queue & CRRMU Review Card Grid -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
			
			<!-- Left: Clinic Queue -->
			<div class="lg:col-span-8 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
				<div class="flex items-center justify-between mb-4">
					<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">LIVE FLOW</p>
					<a href="/queue" class="text-xs font-semibold text-[#1b522f] hover:underline">
						Open queue
					</a>
				</div>

				<h2 class="text-xl font-bold text-gray-800 mb-6">Clinic queue</h2>

				<div class="space-y-4">
					{#each clinicStore.queue as item (item.id)}
						<div class="p-4 bg-[#f8faf9] border border-gray-100 rounded-2xl flex items-center justify-between hover:border-[#1b522f]/20 transition-colors">
							<div class="flex items-center space-x-4 min-w-0">
								<span class="text-sm font-bold text-[#1b522f] shrink-0">{item.queueNumber}</span>
								<div class="w-9 h-9 rounded-full bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0">
									{item.studentInitials}
								</div>
								<div class="truncate">
									<p class="text-sm font-bold text-gray-800 truncate">{item.studentName}</p>
									<p class="text-xs text-gray-400 truncate">{item.studentId} · {item.complaint}</p>
								</div>
							</div>

							<div class="flex items-center space-x-3 shrink-0 ml-4">
								<span class="px-2.5 py-1 rounded-full text-[11px] font-semibold {item.status === 'Waiting'
									? 'bg-amber-50 text-amber-700'
									: item.status === 'In Consultation'
									? 'bg-[#e8f5ec] text-[#1b522f]'
									: 'bg-blue-50 text-blue-700'}">
									{item.status === 'Waiting' ? 'Waiting · 8 min' : item.status}
								</span>

								{#if item.actionText === 'Start visit'}
									<button
										type="button"
										onclick={() => clinicStore.advanceQueue(item.id)}
										class="px-4 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer transition-colors shadow-2xs"
									>
										Start visit
									</button>
								{:else}
									<button
										type="button"
										onclick={() => clinicStore.advanceQueue(item.id)}
										class="px-4 py-2 rounded-xl bg-white border border-gray-200 text-gray-700 hover:text-[#1b522f] hover:border-[#1b522f] text-xs font-semibold cursor-pointer transition-colors"
									>
										Open
									</button>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			</div>

			<!-- Right: Needs Review CRRMU Report -->
			<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-4">
				<div class="flex items-center justify-between mb-1">
					<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">NEEDS REVIEW</p>
					<span class="px-2.5 py-0.5 rounded-full text-[10px] font-semibold bg-amber-50 text-amber-700">
						Pending
					</span>
				</div>

				<h3 class="text-xl font-bold text-gray-800">CRRMU report</h3>

				<div class="bg-[#f8faf9] border border-gray-100 rounded-2xl p-5 space-y-3">
					<div class="flex items-center space-x-2">
						<div class="flex -space-x-1.5 overflow-hidden">
							<div class="w-7 h-7 rounded-full bg-[#dcfce7] text-[#1b522f] flex items-center justify-center font-bold text-[10px] ring-2 ring-white">
								VS
							</div>
							<div class="w-7 h-7 rounded-full bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-[10px] ring-2 ring-white">
								FM
							</div>
						</div>
						<div class="text-xs">
							<span class="font-bold text-gray-800">Vergel Suniga Jr.</span>
							<span class="text-gray-400"> assisted </span>
							<span class="font-bold text-gray-800">Faith Manada</span>
						</div>
					</div>

					<div class="pt-2 border-t border-gray-100 text-xs space-y-1">
						<p class="font-bold text-gray-800">Minor injury</p>
						<p class="text-gray-500">Wound cleaning + bandaging</p>
						<p class="text-[10px] text-gray-400">10:42 AM</p>
					</div>
				</div>

				<a
					href="/first-aid-reports"
					class="block text-center w-full py-2.5 rounded-xl bg-[#edf7f0] hover:bg-[#e2f2e6] text-[#1b522f] text-xs font-semibold transition-colors mt-2"
				>
					Review report &gt;
				</a>
			</div>

		</div>

		<!-- Bottom: At A Glance Today's Activity -->
		<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
			<div class="flex items-center justify-between mb-4">
				<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">AT A GLANCE</p>
				<span class="text-[10px] text-gray-400">Updated just now</span>
			</div>

			<h3 class="text-xl font-bold text-gray-800 mb-6">Today's activity</h3>

			<div class="grid grid-cols-2 md:grid-cols-4 gap-6">
				<div class="space-y-1">
					<p class="text-3xl font-bold text-gray-800">12</p>
					<p class="text-xs text-gray-400">Total students assisted</p>
				</div>
				<div class="space-y-1">
					<p class="text-3xl font-bold text-gray-800">07</p>
					<p class="text-xs text-gray-400">Visits completed</p>
				</div>
				<div class="space-y-1">
					<p class="text-3xl font-bold text-gray-800">18m</p>
					<p class="text-xs text-gray-400">Average visit time</p>
				</div>
				<div class="space-y-1">
					<p class="text-3xl font-bold text-gray-800">02</p>
					<p class="text-xs text-gray-400">Follow-ups created</p>
				</div>
			</div>
		</div>

	</div>

{:else}
	<!-- ================= STUDENT PORTAL DASHBOARD ================= -->
	<div class="space-y-8">
		<!-- Hero Banner -->
		<div class="bg-[#1b522f] rounded-3xl p-8 md:p-12 relative overflow-hidden text-white shadow-md flex items-center justify-between">
			<!-- Decorative Background Curves -->
			<div class="absolute inset-0 pointer-events-none opacity-20">
				<div class="absolute w-[600px] h-[600px] rounded-full border-[60px] border-[#428859] -top-40 -right-20"></div>
				<div class="absolute w-[400px] h-[400px] rounded-full bg-[#428859]/30 bottom-[-100px] right-[200px] blur-2xl"></div>
			</div>

			<!-- Left Text Info -->
			<div class="relative z-10 max-w-xl">
				<p class="text-[10px] md:text-xs font-bold tracking-[0.18em] text-[#8fd3a2] mb-3 uppercase">
					MONDAY, OCTOBER 4
				</p>
				<h1 class="text-3xl md:text-4xl lg:text-5xl font-medium tracking-tight text-white mb-2 leading-tight">
					Good afternoon, {clinicStore.currentUser.firstName}!
				</h1>
				<p class="text-white/80 text-sm md:text-base font-normal">
					What can the clinic help you with today?
				</p>
			</div>

			<!-- Right Heartbeat Badge Icon -->
			<div class="relative z-10 hidden md:flex items-center justify-center w-28 h-28 bg-white/10 backdrop-blur-sm rounded-3xl border border-white/10 shrink-0">
				<svg class="w-14 h-14 text-white/90" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
					<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
					<polyline points="7 12 9 12 11 16 14 8 16 12 18 12"></polyline>
				</svg>
			</div>
		</div>

		<!-- Quick Actions Section -->
		<section>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				LESS TYPING, FASTER CARE
			</p>
			<h2 class="text-2xl font-bold text-gray-800 mb-5">Quick actions</h2>

			<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
				<!-- Action 1: Book Appointment -->
				<a
					href="/appointments"
					class="bg-white hover:bg-gray-50/80 border border-gray-100/90 rounded-2xl p-5 shadow-xs hover:shadow-md transition-all flex items-center justify-between group"
				>
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-sm font-semibold text-gray-800 group-hover:text-[#1b522f] transition-colors">Book clinic appointment</h3>
							<p class="text-xs text-gray-400 mt-0.5">Select a date and time</p>
						</div>
					</div>
					<svg class="w-4 h-4 text-gray-300 group-hover:text-[#1b522f] group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</a>

				<!-- Action 2: Clinic Visits -->
				<a
					href="/clinic-visits"
					class="bg-white hover:bg-gray-50/80 border border-gray-100/90 rounded-2xl p-5 shadow-xs hover:shadow-md transition-all flex items-center justify-between group"
				>
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-sm font-semibold text-gray-800 group-hover:text-[#1b522f] transition-colors">Clinic visit history</h3>
							<p class="text-xs text-gray-400 mt-0.5">View past care</p>
						</div>
					</div>
					<svg class="w-4 h-4 text-gray-300 group-hover:text-[#1b522f] group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</a>

				<!-- Action 3: My Profile -->
				<a
					href="/profile"
					class="bg-white hover:bg-gray-50/80 border border-gray-100/90 rounded-2xl p-5 shadow-xs hover:shadow-md transition-all flex items-center justify-between group"
				>
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-sm font-semibold text-gray-800 group-hover:text-[#1b522f] transition-colors">My profile</h3>
							<p class="text-xs text-gray-400 mt-0.5">Review saved details</p>
						</div>
					</div>
					<svg class="w-4 h-4 text-gray-300 group-hover:text-[#1b522f] group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</a>

				<!-- Action 4: Emergency Contact -->
				<a
					href="/profile#emergency"
					class="bg-white hover:bg-gray-50/80 border border-gray-100/90 rounded-2xl p-5 shadow-xs hover:shadow-md transition-all flex items-center justify-between group"
				>
					<div class="flex items-center space-x-4">
						<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform">
							<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
							</svg>
						</div>
						<div>
							<h3 class="text-sm font-semibold text-gray-800 group-hover:text-[#1b522f] transition-colors">Emergency contact</h3>
							<p class="text-xs text-gray-400 mt-0.5">Update responsible person</p>
						</div>
					</div>
					<svg class="w-4 h-4 text-gray-300 group-hover:text-[#1b522f] group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
					</svg>
				</a>

				<!-- Action 5: Record First Aid (CRRMU Member only) -->
				{#if clinicStore.currentUser.isCrrmuMember}
					<a
						href="/first-aid-reports"
						class="bg-[#edf7f0] hover:bg-[#e2f2e6] border border-[#1b522f]/20 rounded-2xl p-5 shadow-xs hover:shadow-md transition-all flex items-center justify-between group"
					>
						<div class="flex items-center space-x-4">
							<div class="w-12 h-12 rounded-xl bg-white text-[#1b522f] flex items-center justify-center shrink-0 group-hover:scale-105 transition-transform shadow-2xs">
								<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
								</svg>
							</div>
							<div>
								<h3 class="text-sm font-semibold text-gray-800 group-hover:text-[#1b522f] transition-colors">Record first aid</h3>
								<p class="text-xs text-[#1b522f] font-medium mt-0.5">Submit to the clinic</p>
							</div>
						</div>
						<svg class="w-4 h-4 text-gray-400 group-hover:text-[#1b522f] group-hover:translate-x-0.5 transition-all" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
						</svg>
					</a>
				{/if}
			</div>
		</section>

		<!-- Bottom Section: Current Appointment & Notifications -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
			
			<!-- Current Appointment Card -->
			<div class="lg:col-span-7 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
				<div class="flex items-center justify-between mb-4">
					<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">UP NEXT</p>
					<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#e8f5ec] text-[#1b522f]">
						Confirmed
					</span>
				</div>
				
				<h2 class="text-xl font-bold text-gray-800 mb-6">Current appointment</h2>

				{#if clinicStore.appointments.length > 0}
					{@const current = clinicStore.appointments[0]}
					<div class="bg-[#f8faf9] rounded-2xl p-5 mb-6 border border-gray-100/80 flex items-center space-x-5">
						<!-- Date Badge -->
						<div class="w-16 h-16 rounded-xl bg-[#1b522f] text-white flex flex-col items-center justify-center font-bold shrink-0 shadow-xs">
							<span class="text-xl leading-none">{current.day}</span>
							<span class="text-[10px] tracking-wider uppercase mt-0.5">{current.month}</span>
						</div>

						<!-- Details -->
						<div class="space-y-1">
							<h3 class="text-base font-semibold text-gray-800">{current.title}</h3>
							<div class="flex items-center space-x-1.5 text-xs text-gray-500">
								<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
								</svg>
								<span>{current.time} · {current.location}</span>
							</div>
							<p class="text-xs text-gray-400">Reason: {current.reason}</p>
						</div>
					</div>

					<a
						href="/appointments"
						class="inline-flex items-center space-x-1.5 px-5 py-2.5 rounded-xl bg-[#edf7f0] hover:bg-[#e2f2e6] text-[#1b522f] text-xs font-semibold transition-colors"
					>
						<span>View appointment</span>
						<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
						</svg>
					</a>
				{:else}
					<div class="py-8 text-center text-gray-400 text-sm">
						No upcoming appointments.
					</div>
				{/if}
			</div>

			<!-- Notifications Card -->
			<div class="lg:col-span-5 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
				<div class="flex items-center justify-between mb-4">
					<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">STAY UPDATED</p>
					<a href="/notifications" class="text-xs font-semibold text-[#1b522f] hover:underline">
						View all
					</a>
				</div>

				<h2 class="text-xl font-bold text-gray-800 mb-6">Notifications</h2>

				<div class="space-y-4">
					{#each clinicStore.notifications.slice(0, 2) as notif (notif.id)}
						<div class="flex items-start space-x-3.5 pb-4 border-b border-gray-50 last:border-0 last:pb-0">
							<div class="w-8 h-8 rounded-full bg-[#e8f5ec] text-[#1b522f] flex items-center justify-center shrink-0 mt-0.5">
								{#if notif.type === 'confirmation'}
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
									</svg>
								{:else}
									<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z"></path>
									</svg>
								{/if}
							</div>
							<div>
								<h3 class="text-xs font-semibold text-gray-800">{notif.title}</h3>
								<p class="text-xs text-gray-500 mt-0.5 leading-snug">{notif.message}</p>
								<span class="text-[10px] text-gray-400 mt-1 block">{notif.time}</span>
							</div>
						</div>
					{/each}
				</div>
			</div>

		</div>
	</div>
{/if}
