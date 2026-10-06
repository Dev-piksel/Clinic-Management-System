<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { goto } from '$app/navigation';

	let isStaff = $derived(clinicStore.currentUser.category === 'staff');

	// ================= STAFF MODE STATE =================
	let activeDay = $state('04');
	let activeTab = $state<'Today' | 'Pending' | 'Confirmed' | 'Completed'>('Today');
	let searchFilter = $state('');

	const staffDays = [
		{ dayName: 'Sun', dayNumber: '03', isClosed: true },
		{ dayName: 'Mon', dayNumber: '04', isClosed: false },
		{ dayName: 'Tue', dayNumber: '05', isClosed: false },
		{ dayName: 'Wed', dayNumber: '06', isClosed: false },
		{ dayName: 'Thu', dayNumber: '07', isClosed: false },
		{ dayName: 'Fri', dayNumber: '08', isClosed: false },
		{ dayName: 'Sat', dayNumber: '09', isClosed: false }
	];

	let filteredStaffAppointments = $derived.by(() => {
		let list = clinicStore.appointments;
		if (activeTab === 'Pending') {
			list = list.filter((a) => a.status === 'Pending');
		} else if (activeTab === 'Confirmed') {
			list = list.filter((a) => a.status === 'Confirmed');
		} else if (activeTab === 'Completed') {
			list = list.filter((a) => a.status === 'Completed');
		}
		if (searchFilter.trim()) {
			const q = searchFilter.toLowerCase();
			list = list.filter(
				(a) =>
					a.studentName?.toLowerCase().includes(q) ||
					a.studentId?.includes(q) ||
					a.title.toLowerCase().includes(q)
			);
		}
		return list;
	});

	// ================= STUDENT MODE STATE =================
	let currentStep = $state<number>(1);
	let selectedDate = $state<number>(8);
	let selectedMonth = $state('October 2026');
	let selectedTime = $state('10:30 AM');
	let selectedReason = $state('Follow-up');
	let additionalNotes = $state('');
	let isBooked = $state(false);

	const timeSlots = [
		'08:30 AM',
		'09:15 AM',
		'10:30 AM',
		'11:15 AM',
		'01:30 PM',
		'02:15 PM',
		'03:00 PM',
		'03:45 PM'
	];

	const reasonOptions = [
		'Follow-up',
		'General consultation',
		'First aid / Injury assessment',
		'Medical certificate request',
		'Routine health check'
	];

	const emptyDaysStart = [null, null, null, null];
	const daysInOctober = Array.from({ length: 31 }, (_, i) => i + 1);

	function isSunday(day: number): boolean {
		return (day + 3) % 7 === 0;
	}

	function handleDayClick(day: number) {
		if (isSunday(day)) return;
		selectedDate = day;
	}

	function handleNextStep() {
		if (currentStep < 4) {
			currentStep += 1;
		} else {
			clinicStore.addAppointment({
				title: selectedReason,
				type: selectedReason,
				date: `2026-10-${selectedDate.toString().padStart(2, '0')}`,
				day: selectedDate.toString().padStart(2, '0'),
				month: 'OCT',
				time: selectedTime,
				location: 'School Clinic',
				reason: selectedReason,
				studentName: clinicStore.currentUser.name,
				studentId: clinicStore.currentUser.studentId,
				studentInitials: clinicStore.currentUser.initials
			});
			isBooked = true;
			setTimeout(() => {
				goto('/dashboard');
			}, 1800);
		}
	}
</script>

<svelte:head>
	<title>{isStaff ? 'Clinic Schedule - Appointments' : 'Book Clinic Appointment - CSHMS'}</title>
</svelte:head>

{#if isStaff}
	<!-- ================= CLINIC STAFF APPOINTMENTS SCHEDULE ================= -->
	<div class="space-y-6 max-w-6xl">
		<!-- Header -->
		<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
					CLINIC SCHEDULE
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					Appointments
				</h1>
				<p class="text-sm text-gray-500 mt-1">
					Review requests and manage today's confirmed clinic schedule.
				</p>
			</div>

			<button
				type="button"
				class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors self-start sm:self-auto cursor-pointer"
			>
				<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
				</svg>
				<span>Block clinic date</span>
			</button>
		</div>

		<!-- Days of Week Selector Bar -->
		<div class="grid grid-cols-7 gap-2.5">
			{#each staffDays as d}
				{@const isCurrent = activeDay === d.dayNumber}
				<button
					type="button"
					onclick={() => !d.isClosed && (activeDay = d.dayNumber)}
					class="p-3 rounded-2xl flex flex-col items-center justify-center transition-all cursor-pointer border {d.isClosed
						? 'bg-gray-50/70 border-gray-100 text-gray-400 opacity-60 cursor-not-allowed'
						: isCurrent
						? 'bg-[#428859] border-[#428859] text-white shadow-xs font-bold'
						: 'bg-white border-gray-200/80 hover:bg-gray-50 text-gray-700 font-medium'}"
				>
					<span class="text-[11px] {isCurrent ? 'text-white/80' : 'text-gray-400'} font-semibold">{d.dayName}</span>
					<span class="text-lg font-bold leading-none mt-1">{d.dayNumber}</span>
					{#if d.isClosed}
						<span class="text-[9px] uppercase tracking-wider text-gray-400 mt-0.5">Closed</span>
					{/if}
				</button>
			{/each}
		</div>

		<!-- Filter Tabs & Search Bar -->
		<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pt-2">
			<div class="flex items-center space-x-2">
				{#each ['Today', 'Pending', 'Confirmed', 'Completed'] as tab}
					{@const isSelected = activeTab === tab}
					<button
						type="button"
						onclick={() => (activeTab = tab as any)}
						class="px-4 py-2 rounded-full text-xs font-semibold transition-colors cursor-pointer {isSelected
							? 'bg-[#1b522f] text-white shadow-2xs'
							: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
					>
						{tab}
					</button>
				{/each}
			</div>

			<div class="relative w-full sm:w-72">
				<div class="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none">
					<svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
					</svg>
				</div>
				<input
					type="text"
					bind:value={searchFilter}
					placeholder="Search appointments"
					class="w-full pl-10 pr-4 py-2 bg-white border border-gray-200/80 rounded-2xl text-xs focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
				/>
			</div>
		</div>

		<!-- Appointments Table Card -->
		<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
			<div class="overflow-x-auto">
				<table class="w-full text-left text-xs">
					<thead>
						<tr class="border-b border-gray-100 text-gray-400 uppercase text-[10px] font-bold tracking-wider">
							<th class="py-4 px-6">TIME</th>
							<th class="py-4 px-6">STUDENT</th>
							<th class="py-4 px-6">APPOINTMENT</th>
							<th class="py-4 px-6">STATUS</th>
							<th class="py-4 px-6 text-right">ACTION</th>
						</tr>
					</thead>
					<tbody class="divide-y divide-gray-50">
						{#each filteredStaffAppointments as app (app.id)}
							<tr class="hover:bg-gray-50/50 transition-colors">
								<!-- Time -->
								<td class="py-4 px-6 font-bold text-gray-800 whitespace-nowrap">
									{app.time}
								</td>

								<!-- Student -->
								<td class="py-4 px-6">
									<div class="flex items-center space-x-3">
										<div class="w-8 h-8 rounded-full bg-[#dcfce7] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0">
											{app.studentInitials || 'ST'}
										</div>
										<div>
											<p class="font-bold text-gray-800">{app.studentName || 'Student Patient'}</p>
											<p class="text-[11px] text-gray-400">{app.studentId || '202600000'}</p>
										</div>
									</div>
								</td>

								<!-- Appointment -->
								<td class="py-4 px-6">
									<p class="font-bold text-gray-800">{app.reason || app.title}</p>
									<p class="text-[11px] text-gray-400">{app.type}</p>
								</td>

								<!-- Status -->
								<td class="py-4 px-6">
									<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold {app.status === 'Waiting'
										? 'bg-amber-50 text-amber-700'
										: app.status === 'Confirmed'
										? 'bg-[#e8f5ec] text-[#1b522f]'
										: 'bg-emerald-50 text-emerald-700'}">
										{app.status}
									</span>
								</td>

								<!-- Action -->
								<td class="py-4 px-6 text-right">
									{#if app.status === 'Pending'}
										<button
											type="button"
											onclick={() => goto('/queue')}
											class="px-4 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer shadow-2xs transition-colors"
										>
											Review
										</button>
									{:else}
										<button
											type="button"
											onclick={() => goto('/queue')}
											class="px-4 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer shadow-2xs transition-colors"
										>
											Open
										</button>
									{/if}
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>

{:else}
	<!-- ================= STUDENT BOOK CLINIC APPOINTMENT ================= -->
	<div class="space-y-8">
		<!-- Page Header -->
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				BOOK CLINIC APPOINTMENT
			</p>
			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				Pick a time that works
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Your profile details are already attached—no need to type them again.
			</p>
		</div>

		<!-- Stepper Bar -->
		<div class="max-w-2xl py-2">
			<div class="relative flex items-center justify-between">
				<!-- Background Connecting Line -->
				<div class="absolute left-4 right-4 top-1/2 -translate-y-1/2 h-0.5 bg-gray-200 -z-0"></div>
				<div
					class="absolute left-4 top-1/2 -translate-y-1/2 h-0.5 bg-[#1b522f] transition-all duration-300 -z-0"
					style="width: {((currentStep - 1) / 3) * 100}%;"
				></div>

				<!-- Step 1 -->
				<button
					type="button"
					onclick={() => (currentStep = 1)}
					class="relative z-10 flex flex-col items-center group cursor-pointer"
				>
					<div
						class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors {currentStep >= 1
							? 'bg-[#1b522f] text-white'
							: 'bg-gray-100 text-gray-400'}"
					>
						1
					</div>
					<span class="text-[11px] font-semibold mt-1.5 {currentStep === 1 ? 'text-gray-900' : 'text-gray-400'}">Date</span>
				</button>

				<!-- Step 2 -->
				<button
					type="button"
					onclick={() => (currentStep = 2)}
					class="relative z-10 flex flex-col items-center group cursor-pointer"
				>
					<div
						class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors {currentStep >= 2
							? 'bg-[#1b522f] text-white'
							: 'bg-gray-100 text-gray-400'}"
					>
						2
					</div>
					<span class="text-[11px] font-semibold mt-1.5 {currentStep === 2 ? 'text-gray-900' : 'text-gray-400'}">Time</span>
				</button>

				<!-- Step 3 -->
				<button
					type="button"
					onclick={() => (currentStep = 3)}
					class="relative z-10 flex flex-col items-center group cursor-pointer"
				>
					<div
						class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors {currentStep >= 3
							? 'bg-[#1b522f] text-white'
							: 'bg-gray-100 text-gray-400'}"
					>
						3
					</div>
					<span class="text-[11px] font-semibold mt-1.5 {currentStep === 3 ? 'text-gray-900' : 'text-gray-400'}">Reason</span>
				</button>

				<!-- Step 4 -->
				<button
					type="button"
					onclick={() => (currentStep = 4)}
					class="relative z-10 flex flex-col items-center group cursor-pointer"
				>
					<div
						class="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold transition-colors {currentStep >= 4
							? 'bg-[#1b522f] text-white'
							: 'bg-gray-100 text-gray-400'}"
					>
						4
					</div>
					<span class="text-[11px] font-semibold mt-1.5 {currentStep === 4 ? 'text-gray-900' : 'text-gray-400'}">Confirm</span>
				</button>
			</div>
		</div>

		{#if isBooked}
			<div class="bg-[#edf7f0] border border-[#1b522f]/20 rounded-3xl p-8 text-center max-w-xl mx-auto shadow-sm">
				<div class="w-16 h-16 rounded-full bg-[#1b522f] text-white flex items-center justify-center mx-auto mb-4">
					<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<h2 class="text-2xl font-bold text-gray-900 mb-2">Appointment Confirmed!</h2>
				<p class="text-sm text-gray-600 mb-4">
					Your consultation on <strong>October {selectedDate}, 2026</strong> at <strong>{selectedTime}</strong> has been scheduled.
				</p>
				<p class="text-xs text-gray-400">Redirecting to Dashboard...</p>
			</div>
		{:else}
			<!-- Main Content Grid -->
			<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
				
				<!-- Left / Main Card -->
				<div class="lg:col-span-8 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
					<div class="flex items-center justify-between mb-4">
						<div>
							<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
								STEP {currentStep} OF 4
							</p>
							<h2 class="text-2xl font-bold text-gray-800">
								{#if currentStep === 1}
									Select date
								{:else if currentStep === 2}
									Select appointment time
								{:else if currentStep === 3}
									Reason for consultation
								{:else}
									Confirm your booking
								{/if}
							</h2>
						</div>

						{#if currentStep === 1}
							<div class="text-right">
								<span class="text-sm font-bold text-gray-800">{selectedMonth}</span>
							</div>
						{/if}
					</div>

					<!-- Step 1: Interactive Calendar -->
					{#if currentStep === 1}
						<div class="mt-6">
							<div class="grid grid-cols-7 gap-2 mb-2 text-center text-xs font-semibold text-gray-400">
								<div>Sun</div>
								<div>Mon</div>
								<div>Tue</div>
								<div>Wed</div>
								<div>Thu</div>
								<div>Fri</div>
								<div>Sat</div>
							</div>

							<div class="grid grid-cols-7 gap-2">
								{#each emptyDaysStart as _}
									<div class="h-14"></div>
								{/each}

								{#each daysInOctober as day}
									{@const closed = isSunday(day)}
									{@const selected = selectedDate === day}
									<button
										type="button"
										disabled={closed}
										onclick={() => handleDayClick(day)}
										class="h-14 rounded-2xl flex flex-col items-center justify-center transition-all cursor-pointer {closed
											? 'bg-gray-50 text-gray-300 cursor-not-allowed opacity-60'
											: selected
											? 'bg-[#1b522f] text-white shadow-sm ring-2 ring-[#1b522f]/20 font-bold'
											: 'bg-gray-50/70 hover:bg-[#edf7f0] text-gray-700 hover:text-[#1b522f] font-medium'}"
									>
										<span class="text-sm">{day}</span>
										{#if closed}
											<span class="text-[9px] uppercase tracking-wider font-semibold text-gray-400 mt-0.5">Closed</span>
										{/if}
									</button>
								{/each}
							</div>

							<div class="flex items-center space-x-6 mt-8 pt-4 border-t border-gray-100 text-xs text-gray-500">
								<div class="flex items-center space-x-2">
									<span class="w-3.5 h-3.5 rounded-md bg-gray-100 border border-gray-200"></span>
									<span>Available</span>
								</div>
								<div class="flex items-center space-x-2">
									<span class="w-3.5 h-3.5 rounded-md bg-[#1b522f]"></span>
									<span>Selected</span>
								</div>
								<div class="flex items-center space-x-2">
									<span class="w-3.5 h-3.5 rounded-md bg-gray-50 opacity-60 border border-gray-200"></span>
									<span>Unavailable / Sunday</span>
								</div>
							</div>
						</div>

					<!-- Step 2: Time Selection -->
					{:else if currentStep === 2}
						<div class="mt-6 space-y-4">
							<p class="text-xs text-gray-500">
								Available slots for <strong>October {selectedDate}, 2026</strong>:
							</p>
							<div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
								{#each timeSlots as slot}
									{@const isSelected = selectedTime === slot}
									<button
										type="button"
										onclick={() => (selectedTime = slot)}
										class="p-4 rounded-xl text-center text-sm font-semibold transition-all cursor-pointer border {isSelected
											? 'bg-[#1b522f] text-white border-[#1b522f] shadow-xs'
											: 'bg-white text-gray-700 border-gray-200 hover:border-[#1b522f]/40 hover:bg-gray-50'}"
									>
										{slot}
									</button>
								{/each}
							</div>
						</div>

					<!-- Step 3: Reason Selection -->
					{:else if currentStep === 3}
						<div class="mt-6 space-y-4">
							<p class="text-xs text-gray-500">Choose primary reason for this clinic visit:</p>
							<div class="space-y-2.5">
								{#each reasonOptions as reason}
									{@const isSelected = selectedReason === reason}
									<button
										type="button"
										onclick={() => (selectedReason = reason)}
										class="w-full text-left p-4 rounded-xl flex items-center justify-between text-sm font-semibold transition-all cursor-pointer border {isSelected
											? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 shadow-2xs'
											: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
									>
										<span>{reason}</span>
										{#if isSelected}
											<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
											</svg>
										{/if}
									</button>
								{/each}
							</div>

							<div class="pt-3">
								<label for="additional-notes" class="block text-xs font-semibold text-gray-700 mb-1.5">
									Additional notes for the nurse (optional)
								</label>
								<textarea
									id="additional-notes"
									bind:value={additionalNotes}
									rows="3"
									placeholder="e.g. slight headache since morning, recurring allergy..."
									class="w-full p-3.5 bg-white border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
								></textarea>
							</div>
						</div>

					<!-- Step 4: Confirmation Overview -->
					{:else}
						<div class="mt-6 space-y-5">
							<div class="bg-[#f8faf9] border border-gray-100 rounded-2xl p-5 space-y-3">
								<div class="flex justify-between items-center text-sm pb-2 border-b border-gray-100">
									<span class="text-gray-500">Patient</span>
									<span class="font-semibold text-gray-800">{clinicStore.currentUser.name}</span>
								</div>
								<div class="flex justify-between items-center text-sm pb-2 border-b border-gray-100">
									<span class="text-gray-500">Student ID</span>
									<span class="font-semibold text-gray-800">{clinicStore.currentUser.studentId}</span>
								</div>
								<div class="flex justify-between items-center text-sm pb-2 border-b border-gray-100">
									<span class="text-gray-500">Date</span>
									<span class="font-semibold text-gray-800">October {selectedDate}, 2026</span>
								</div>
								<div class="flex justify-between items-center text-sm pb-2 border-b border-gray-100">
									<span class="text-gray-500">Time</span>
									<span class="font-semibold text-[#1b522f]">{selectedTime}</span>
								</div>
								<div class="flex justify-between items-center text-sm">
									<span class="text-gray-500">Reason</span>
									<span class="font-semibold text-gray-800">{selectedReason}</span>
								</div>
							</div>
						</div>
					{/if}

					<!-- Controls -->
					<div class="mt-8 pt-4 border-t border-gray-100 flex items-center justify-between">
						{#if currentStep > 1}
							<button
								type="button"
								onclick={() => (currentStep -= 1)}
								class="px-5 py-2.5 rounded-xl border border-gray-200 hover:bg-gray-50 text-xs font-semibold text-gray-700 transition-colors cursor-pointer"
							>
								Back
							</button>
						{:else}
							<div></div>
						{/if}

						<button
							type="button"
							onclick={handleNextStep}
							class="px-6 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold flex items-center space-x-1.5 transition-colors cursor-pointer shadow-xs"
						>
							<span>{currentStep === 4 ? 'Confirm & Book Appointment' : 'Continue'}</span>
							<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
							</svg>
						</button>
					</div>
				</div>

				<!-- Right Info Card -->
				<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-4">
					<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
						</svg>
					</div>
					<h3 class="text-base font-bold text-gray-800">Choose an available day</h3>
					<p class="text-xs text-gray-500 leading-relaxed">
						Sundays, past dates, clinic closures, and fully booked days are unavailable automatically.
					</p>
				</div>

			</div>
		{/if}
	</div>
{/if}
