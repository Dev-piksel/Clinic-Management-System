<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { fetchAdminUsers } from '#lib/api';
	import type { DemoAccount } from '#lib/types';
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	let isStaff = $derived(clinicStore.currentUser.category === 'staff');

	// ================= STAFF NEW CLINIC VISIT STATE =================
	let staffView = $state<'new' | 'history'>('new');
	let studentsList = $state<DemoAccount[]>([]);

	let selectedStudentName = $state('Walk-in Student');
	let selectedStudentId = $state('Unassigned');

	onMount(async () => {
		try {
			const users = await fetchAdminUsers('approved');
			studentsList = users.filter((u) => u.category === 'student');
			if (studentsList.length > 0) {
				selectedStudentName = studentsList[0].name;
				selectedStudentId = `${studentsList[0].studentId} · ${studentsList[0].programStrand} ${studentsList[0].yearSection}`;
			}
		} catch {
			// silent fallback
		}
	});
	let selectedVisitType = $state('Walk-in');
	let selectedConcern = $state('Headache');
	let selectedAssessment = $state('Mild');
	let selectedInterventions = $state<string[]>(['Rest', 'Hydration']);
	let selectedDisposition = $state('Returned to Class');
	let additionalRemarks = $state('');
	let isSaved = $state(false);

	const visitTypes = ['Appointment', 'Walk-in', 'Emergency'];
	const concernOptions = ['Headache', 'Fever', 'Stomachache', 'Dizziness', 'Minor Injury', 'Other'];
	const assessmentOptions = ['Mild', 'Moderate', 'Needs monitoring'];
	const interventionOptions = [
		'Rest',
		'Hydration',
		'First Aid',
		'Cold Compress',
		'Wound Cleaning',
		'Bandaging',
		'Observation',
		'Referral',
		'Other'
	];
	const dispositionOptions = [
		'Returned to Class',
		'Continue Observation',
		'Follow-up Required',
		'Sent Home',
		'Referred to Hospital',
		'Other'
	];

	function toggleIntervention(opt: string) {
		if (selectedInterventions.includes(opt)) {
			selectedInterventions = selectedInterventions.filter((i) => i !== opt);
		} else {
			selectedInterventions = [...selectedInterventions, opt];
		}
	}

	function handleSaveVisit() {
		// Save visit to clinic records
		clinicStore.visits = [
			{
				id: `visit-${Date.now()}`,
				date: '04',
				monthYear: 'OCT 2026',
				title: selectedConcern,
				type: selectedVisitType.toLowerCase() === 'walk-in' ? 'walk-in' : 'consultation',
				time: '10:45 AM',
				assessment: selectedAssessment,
				intervention: selectedInterventions.join(' + ') || 'Basic care',
				disposition: selectedDisposition,
				clinicNote: additionalRemarks || undefined,
				status: selectedDisposition === 'Follow-up Required' ? 'Follow-up needed' : 'Completed'
			},
			...clinicStore.visits
		];

		isSaved = true;
		setTimeout(() => {
			isSaved = false;
			goto('/dashboard');
		}, 2000);
	}

	// ================= STUDENT HISTORY VIEW STATE =================
	let activeFilter = $state<'all' | 'consultation' | 'first-aid'>('all');

	let filteredVisits = $derived(
		activeFilter === 'all'
			? clinicStore.visits
			: clinicStore.visits.filter((v) => v.type === activeFilter)
	);
</script>

<svelte:head>
	<title>{isStaff ? 'New Clinic Visit - Clinic Portal - CSHMS' : 'Clinic Visits - CSHMS'}</title>
</svelte:head>

{#if isStaff && staffView === 'new'}
	<!-- ================= CLINIC STAFF: NEW CLINIC VISIT (IMAGE 2) ================= -->
	<div class="space-y-6 max-w-6xl">
		<!-- Header -->
		<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
					CLICK, SELECT, CONFIRM
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					New clinic visit
				</h1>
				<p class="text-sm text-gray-500 mt-1">
					Faith's saved student details are already attached to this visit.
				</p>
			</div>

			<button
				type="button"
				onclick={() => (staffView = 'history')}
				class="text-xs font-semibold text-[#1b522f] hover:underline self-start sm:self-auto cursor-pointer"
			>
				View past visit logs &gt;
			</button>
		</div>

		{#if isSaved}
			<div class="bg-[#edf7f0] border border-[#1b522f]/20 rounded-3xl p-10 text-center max-w-xl mx-auto shadow-sm">
				<div class="w-16 h-16 rounded-full bg-[#1b522f] text-white flex items-center justify-center mx-auto mb-4">
					<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<h2 class="text-2xl font-bold text-gray-900 mb-2">Clinic Visit Recorded!</h2>
				<p class="text-sm text-gray-600 mb-4">
					Consultation for <strong>Faith Manada</strong> ({selectedConcern}) saved to medical history.
				</p>
				<p class="text-xs text-gray-400">Redirecting to Dashboard...</p>
			</div>
		{:else}
			<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
				
				<!-- Left Form Steps -->
				<div class="lg:col-span-8 space-y-6">
					
					<!-- STEP 1: Select Student & Visit Type -->
					<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-5">
						<div class="flex items-center space-x-3">
							<div class="w-7 h-7 rounded-full bg-[#1b522f] text-white flex items-center justify-center font-bold text-xs shrink-0">
								1
							</div>
							<div>
								<p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">STUDENT</p>
								<h3 class="text-base font-bold text-gray-800">Select student & visit type</h3>
							</div>
						</div>

						<!-- Student Selection -->
						{#if studentsList.length > 0}
							<div>
								<label for="visit-student-select" class="block text-xs font-semibold text-gray-700 mb-1.5">Select Enrolled Student</label>
								<select
									id="visit-student-select"
									onchange={(e) => {
										const found = studentsList.find((s) => s.id === e.currentTarget.value);
										if (found) {
											selectedStudentName = found.name;
											selectedStudentId = `${found.studentId} · ${found.programStrand} ${found.yearSection}`;
										}
									}}
									class="w-full px-3.5 py-3 rounded-2xl border border-gray-200 text-xs sm:text-sm bg-white font-medium text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20"
								>
									{#each studentsList as s}
										<option value={s.id}>{s.name} ({s.studentId} - {s.programStrand} {s.yearSection})</option>
									{/each}
								</select>
							</div>
						{:else}
							<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
								<div>
									<label for="visit-student-name-input" class="block text-xs font-semibold text-gray-700 mb-1">Student Name</label>
									<input
										id="visit-student-name-input"
										type="text"
										bind:value={selectedStudentName}
										placeholder="e.g. Student Name"
										class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs text-gray-800"
									/>
								</div>
								<div>
									<label for="visit-student-id-input" class="block text-xs font-semibold text-gray-700 mb-1">Student ID (Numbers only)</label>
									<input
										id="visit-student-id-input"
										type="text"
										inputmode="numeric"
										pattern="[0-9]*"
										bind:value={selectedStudentId}
										placeholder="e.g. 202611000"
										class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-xs text-gray-800"
									/>
								</div>
							</div>
						{/if}

						<!-- Visit Type Chips -->
						<div class="grid grid-cols-3 gap-3">
							{#each visitTypes as vt}
								{@const isSelected = selectedVisitType === vt}
								<button
									type="button"
									onclick={() => (selectedVisitType = vt)}
									class="p-3.5 rounded-xl border text-xs font-semibold flex items-center justify-center space-x-2 transition-all cursor-pointer {isSelected
										? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 shadow-2xs'
										: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
								>
									<span>{vt}</span>
									{#if isSelected}
										<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
										</svg>
									{/if}
								</button>
							{/each}
						</div>
					</div>

					<!-- STEP 2: Concern & Care (Record what happened) -->
					<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
						<div class="flex items-center space-x-3">
							<div class="w-7 h-7 rounded-full bg-[#1b522f] text-white flex items-center justify-center font-bold text-xs shrink-0">
								2
							</div>
							<div>
								<p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">CONCERN & CARE</p>
								<h3 class="text-base font-bold text-gray-800">Record what happened</h3>
							</div>
						</div>

						<!-- Chief Concern -->
						<div>
							<p class="text-xs font-semibold text-gray-700 mb-2">Chief concern</p>
							<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
								{#each concernOptions as opt}
									{@const isSelected = selectedConcern === opt}
									<button
										type="button"
										onclick={() => (selectedConcern = opt)}
										class="p-3 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
											? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs'
											: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
									>
										<span>{opt}</span>
										{#if isSelected}
											<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
											</svg>
										{/if}
									</button>
								{/each}
							</div>
						</div>

						<!-- Assessment -->
						<div>
							<p class="text-xs font-semibold text-gray-700 mb-2">Assessment</p>
							<div class="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
								{#each assessmentOptions as opt}
									{@const isSelected = selectedAssessment === opt}
									<button
										type="button"
										onclick={() => (selectedAssessment = opt)}
										class="p-3 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
											? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs'
											: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
									>
										<span>{opt}</span>
										{#if isSelected}
											<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
											</svg>
										{/if}
									</button>
								{/each}
							</div>
						</div>

						<!-- Intervention (Multi-select) -->
						<div>
							<p class="text-xs font-semibold text-gray-700 mb-2">Intervention</p>
							<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
								{#each interventionOptions as opt}
									{@const isSelected = selectedInterventions.includes(opt)}
									<button
										type="button"
										onclick={() => toggleIntervention(opt)}
										class="p-3 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
											? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs'
											: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
									>
										<span>{opt}</span>
										{#if isSelected}
											<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
											</svg>
										{/if}
									</button>
								{/each}
							</div>
						</div>
					</div>

					<!-- STEP 3: Outcome (Choose disposition) -->
					<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
						<div class="flex items-center space-x-3">
							<div class="w-7 h-7 rounded-full bg-[#1b522f] text-white flex items-center justify-center font-bold text-xs shrink-0">
								3
							</div>
							<div>
								<p class="text-[10px] font-bold text-gray-400 uppercase tracking-wider">OUTCOME</p>
								<h3 class="text-base font-bold text-gray-800">Choose disposition</h3>
							</div>
						</div>

						<!-- Disposition Chips -->
						<div class="grid grid-cols-2 sm:grid-cols-3 gap-2.5">
							{#each dispositionOptions as opt}
								{@const isSelected = selectedDisposition === opt}
								<button
									type="button"
									onclick={() => (selectedDisposition = opt)}
									class="p-3 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
										? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs'
										: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
								>
									<span>{opt}</span>
									{#if isSelected}
										<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
										</svg>
									{/if}
								</button>
							{/each}
						</div>

						<!-- Remarks -->
						<div>
							<div class="flex items-center justify-between mb-1.5">
								<label for="visit-remarks" class="text-xs font-semibold text-gray-700">Additional remarks</label>
								<span class="text-[11px] text-gray-400">Optional</span>
							</div>
							<textarea
								id="visit-remarks"
								bind:value={additionalRemarks}
								rows="3"
								placeholder="Only type details that are not captured above"
								class="w-full p-3.5 bg-white border border-gray-200 rounded-2xl text-xs focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
							></textarea>
						</div>
					</div>

				</div>

				<!-- Right Column: Live Summary Card -->
				<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-5 sticky top-28">
					<div>
						<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">LIVE SUMMARY</p>
						<h3 class="text-lg font-bold text-gray-800 mt-0.5">Clinic visit</h3>
					</div>

					<div class="space-y-3.5 text-xs pb-4 border-b border-gray-100">
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Student</span>
							<span class="font-bold text-gray-800">{selectedStudentName}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Type</span>
							<span class="font-semibold text-gray-800">{selectedVisitType}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Concern</span>
							<span class="font-semibold text-gray-800">{selectedConcern}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Assessment</span>
							<span class="font-semibold text-gray-800">{selectedAssessment}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Intervention</span>
							<span class="font-semibold text-gray-800">{selectedInterventions.join(' + ') || 'None'}</span>
						</div>
						<div class="flex justify-between items-center">
							<span class="text-gray-400">Disposition</span>
							<span class="font-semibold text-gray-800">{selectedDisposition}</span>
						</div>
					</div>

					<button
						type="button"
						onclick={handleSaveVisit}
						class="w-full bg-[#1b522f] hover:bg-[#154225] text-white font-medium py-3.5 rounded-xl text-xs flex justify-center items-center space-x-2 transition-colors cursor-pointer shadow-sm active:scale-[0.99]"
					>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
						<span>Save clinic visit</span>
					</button>
				</div>

			</div>
		{/if}
	</div>

{:else}
	<!-- ================= CLINIC VISITS HISTORY VIEW (STUDENTS OR STAFF TOGGLED) ================= -->
	<div class="space-y-8">
		<!-- Top Header & Action -->
		<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
					YOUR HEALTH HISTORY
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					Clinic visits
				</h1>
				<p class="text-sm text-gray-500 mt-1">
					A private, easy-to-scan record of care at the school clinic.
				</p>
			</div>

			{#if isStaff}
				<button
					type="button"
					onclick={() => (staffView = 'new')}
					class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors cursor-pointer"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
					</svg>
					<span>New clinic visit</span>
				</button>
			{:else}
				<a
					href="/appointments"
					class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors self-start md:self-auto cursor-pointer"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
					</svg>
					<span>Book appointment</span>
				</a>
			{/if}
		</div>

		<!-- Stats Row -->
		<div class="grid grid-cols-1 md:grid-cols-3 gap-5">
			<div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
				<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
					</svg>
				</div>
				<div>
					<h3 class="text-2xl font-bold text-gray-800">03</h3>
					<p class="text-xs text-gray-400 font-medium">Total visits this school year</p>
				</div>
			</div>

			<div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
				<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<div>
					<h3 class="text-2xl font-bold text-gray-800">02</h3>
					<p class="text-xs text-gray-400 font-medium">Returned to class</p>
				</div>
			</div>

			<div class="bg-white rounded-2xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
				<div class="w-12 h-12 rounded-xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
					</svg>
				</div>
				<div>
					<h3 class="text-2xl font-bold text-gray-800">01</h3>
					<p class="text-xs text-gray-400 font-medium">Follow-up completed</p>
				</div>
			</div>
		</div>

		<!-- Timeline Section -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
			<div class="lg:col-span-8 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
				<div class="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-gray-100 gap-4">
					<div>
						<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
							MOST RECENT FIRST
						</p>
						<h2 class="text-xl font-bold text-gray-800">Visit timeline</h2>
					</div>

					<div class="flex items-center space-x-2">
						{#each ['all', 'consultation', 'first-aid'] as f}
							<button
								type="button"
								onclick={() => (activeFilter = f as any)}
								class="px-3.5 py-1.5 rounded-full text-xs font-semibold capitalize transition-colors cursor-pointer {activeFilter === f
									? 'bg-[#1b522f] text-white shadow-2xs'
									: 'bg-gray-50 text-gray-600 hover:bg-gray-100'}"
							>
								{f === 'all' ? 'All' : f === 'first-aid' ? 'First aid' : 'Consultations'}
							</button>
						{/each}
					</div>
				</div>

				<div class="relative mt-8 space-y-8 pl-4 sm:pl-0">
					{#each filteredVisits as visit, idx (visit.id)}
						<div class="flex flex-col sm:flex-row items-start gap-5 relative">
							<div class="flex sm:flex-col items-center sm:items-end justify-between sm:justify-start w-full sm:w-24 shrink-0 sm:text-right pr-4 relative">
								<div class="flex items-baseline space-x-1 sm:block">
									<span class="text-2xl font-bold text-gray-800 leading-none">{visit.date}</span>
									<span class="text-[10px] font-semibold text-gray-400 tracking-wider uppercase block sm:mt-1">{visit.monthYear}</span>
								</div>
								<div class="w-3 h-3 rounded-full bg-[#1b522f] ring-4 ring-[#edf7f0] hidden sm:block absolute -right-1.5 top-2 z-10"></div>
							</div>

							{#if idx < filteredVisits.length - 1}
								<div class="hidden sm:block absolute left-[91px] top-6 bottom-[-32px] w-0.5 bg-gray-100"></div>
							{/if}

							<div class="flex-1 bg-white border border-gray-100 rounded-2xl p-5 shadow-2xs space-y-4 hover:border-[#1b522f]/20 transition-colors">
								<div class="flex items-start justify-between">
									<div>
										<h3 class="text-base font-bold text-gray-800">{visit.title}</h3>
										<p class="text-xs text-gray-400 capitalize mt-0.5">{visit.type} · {visit.time}</p>
									</div>
									<span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#e8f5ec] text-[#1b522f]">
										{visit.status}
									</span>
								</div>

								<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
									<div class="bg-[#f9fafb] rounded-xl p-3 border border-gray-100">
										<p class="text-[10px] font-semibold text-gray-400 uppercase">Assessment</p>
										<p class="text-xs font-semibold text-gray-800 mt-0.5">{visit.assessment}</p>
									</div>
									<div class="bg-[#f9fafb] rounded-xl p-3 border border-gray-100">
										<p class="text-[10px] font-semibold text-gray-400 uppercase">Intervention</p>
										<p class="text-xs font-semibold text-gray-800 mt-0.5">{visit.intervention}</p>
									</div>
									<div class="bg-[#f9fafb] rounded-xl p-3 border border-gray-100">
										<p class="text-[10px] font-semibold text-gray-400 uppercase">Disposition</p>
										<p class="text-xs font-semibold text-gray-800 mt-0.5">{visit.disposition}</p>
									</div>
								</div>

								{#if visit.clinicNote}
									<div class="bg-[#edf7f0] border border-[#1b522f]/10 rounded-xl p-3.5 flex items-start space-x-2.5 text-xs text-[#1b522f]">
										<svg class="w-4 h-4 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
										</svg>
										<span><strong>Clinic note:</strong> {visit.clinicNote}</span>
									</div>
								{/if}
							</div>
						</div>
					{/each}
				</div>
			</div>

			<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-4">
				<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center">
					<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
					</svg>
				</div>
				<h3 class="text-base font-bold text-gray-800">Your records stay private</h3>
				<p class="text-xs text-gray-500 leading-relaxed">
					Only authorized clinic personnel can view detailed assessments and official medical records.
				</p>
			</div>
		</div>
	</div>
{/if}
