<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { goto } from '$app/navigation';

	let selectedIncident = $state('Minor Injury');
	let selectedAssistance = $state('Wound Cleaning');
	let selectedCondition = $state('Stable');
	let additionalNotes = $state('');
	let isSubmitted = $state(false);

	const incidentOptions = ['Minor Injury', 'Dizziness', 'Fainting', 'Minor Cut', 'Other'];
	const assistanceOptions = ['Wound Cleaning', 'Bandaging', 'Rest', 'Assistance to Clinic', 'Other'];
	const conditionOptions = ['Stable', 'Needs Clinic Assessment', 'Emergency'];

	function handleSubmitReport() {
		clinicStore.addFirstAidReport({
			date: '06 OCT 2026',
			time: '10:42 AM',
			patientName: 'Faith Manada',
			patientRole: 'Student - BSIT 4A',
			location: 'Campus Corridor',
			incidentType: selectedIncident,
			treatment: `${selectedAssistance}. Condition: ${selectedCondition}. ${additionalNotes ? 'Note: ' + additionalNotes : ''}`,
			responder: `${clinicStore.currentUser.name} (CRRMU)`
		});

		isSubmitted = true;
		setTimeout(() => {
			goto('/dashboard');
		}, 2000);
	}
</script>

<svelte:head>
	<title>Record First Aid Assistance - CSHMS</title>
</svelte:head>

<div class="space-y-8 max-w-6xl">
	<!-- Page Header -->
	<div>
		<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
			CRRMU ACCESS - MINIMUM NECESSARY
		</p>
		<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
			Record first aid assistance
		</h1>
		<p class="text-sm text-gray-500 mt-1">
			Submit a basic incident report for review by the school clinic.
		</p>
	</div>

	{#if isSubmitted}
		<div class="bg-[#edf7f0] border border-[#1b522f]/20 rounded-3xl p-10 text-center max-w-xl mx-auto shadow-sm">
			<div class="w-16 h-16 rounded-full bg-[#1b522f] text-white flex items-center justify-center mx-auto mb-4">
				<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
				</svg>
			</div>
			<h2 class="text-2xl font-bold text-gray-900 mb-2">First Aid Report Submitted!</h2>
			<p class="text-sm text-gray-600 mb-4">
				Your report for <strong>Faith Manada</strong> ({selectedIncident}) has been transmitted to Head Nurse Alma A. Lontoc.
			</p>
			<p class="text-xs text-gray-400">Redirecting to Dashboard...</p>
		</div>
	{:else}
		<!-- Main Form Layout -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
			
			<!-- Left Form Column -->
			<div class="lg:col-span-8 space-y-6">
				<!-- Privacy Protected Banner -->
				<div class="bg-[#edf7f0] border border-[#1b522f]/10 rounded-2xl p-4 flex items-center space-x-3.5">
					<div class="w-9 h-9 rounded-xl bg-white text-[#1b522f] flex items-center justify-center shrink-0 shadow-2xs">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
						</svg>
					</div>
					<div>
						<h3 class="text-xs font-bold text-[#1b522f]">Privacy-protected workflow</h3>
						<p class="text-[11px] text-[#1b522f]/80 mt-0.5">
							You can identify a student and report assistance, but cannot view medical history.
						</p>
					</div>
				</div>

				<!-- Student Assisted Card -->
				<div>
					<p class="text-xs font-semibold text-gray-700 mb-2">Student assisted</p>
					<div class="bg-[#f4f9f6] border border-[#1b522f]/20 rounded-2xl p-4 flex items-center justify-between cursor-pointer hover:border-[#1b522f]/40 transition-colors shadow-2xs">
						<div class="flex items-center space-x-3.5">
							<div class="w-10 h-10 rounded-full bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0 shadow-2xs">
								FM
							</div>
							<div>
								<p class="text-sm font-bold text-gray-800">Faith Manada</p>
								<p class="text-xs text-gray-400 mt-0.5">202611399 · BSIT 4A</p>
							</div>
						</div>
						<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
						</svg>
					</div>
				</div>

				<!-- Incident Selection -->
				<div>
					<p class="text-xs font-semibold text-gray-700 mb-2">Incident</p>
					<div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
						{#each incidentOptions as option}
							{@const isSelected = selectedIncident === option}
							<button
								type="button"
								onclick={() => (selectedIncident = option)}
								class="p-3.5 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
									? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs ring-1 ring-[#1b522f]/20'
									: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
							>
								<span>{option}</span>
								{#if isSelected}
									<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
									</svg>
								{/if}
							</button>
						{/each}
					</div>
				</div>

				<!-- Assistance Provided Selection -->
				<div>
					<p class="text-xs font-semibold text-gray-700 mb-2">Assistance provided</p>
					<div class="grid grid-cols-2 sm:grid-cols-3 gap-3">
						{#each assistanceOptions as option}
							{@const isSelected = selectedAssistance === option}
							<button
								type="button"
								onclick={() => (selectedAssistance = option)}
								class="p-3.5 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
									? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs ring-1 ring-[#1b522f]/20'
									: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
							>
								<span>{option}</span>
								{#if isSelected}
									<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
									</svg>
								{/if}
							</button>
						{/each}
					</div>
				</div>

				<!-- Condition Selection -->
				<div>
					<p class="text-xs font-semibold text-gray-700 mb-2">Condition</p>
					<div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
						{#each conditionOptions as option}
							{@const isSelected = selectedCondition === option}
							<button
								type="button"
								onclick={() => (selectedCondition = option)}
								class="p-3.5 rounded-xl border text-xs font-medium flex items-center justify-between transition-all cursor-pointer {isSelected
									? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold shadow-2xs ring-1 ring-[#1b522f]/20'
									: 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'}"
							>
								<span>{option}</span>
								{#if isSelected}
									<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
									</svg>
								{/if}
							</button>
						{/each}
					</div>
				</div>

				<!-- Additional Notes -->
				<div>
					<div class="flex items-center justify-between mb-1.5">
						<label for="crrmu-notes" class="text-xs font-semibold text-gray-700">Additional notes</label>
						<span class="text-[11px] text-gray-400">Optional</span>
					</div>
					<textarea
						id="crrmu-notes"
						bind:value={additionalNotes}
						rows="3"
						placeholder="Only add details the clinic needs"
						class="w-full p-3.5 bg-white border border-gray-200 rounded-2xl text-xs focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs"
					></textarea>
				</div>
			</div>

			<!-- Right Column: Report Summary -->
			<div class="lg:col-span-4 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-5 sticky top-28">
				<div>
					<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">READY TO SUBMIT</p>
					<h3 class="text-lg font-bold text-gray-800 mt-0.5">Report summary</h3>
				</div>

				<div class="space-y-3.5 text-xs pb-4 border-b border-gray-100">
					<div class="flex justify-between items-center">
						<span class="text-gray-400">Student</span>
						<span class="font-bold text-gray-800">Faith Manada</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-gray-400">Incident</span>
						<span class="font-semibold text-gray-800">{selectedIncident}</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-gray-400">Assistance</span>
						<span class="font-semibold text-gray-800">{selectedAssistance}</span>
					</div>
					<div class="flex justify-between items-center">
						<span class="text-gray-400">Condition</span>
						<span class="font-semibold text-gray-800">{selectedCondition}</span>
					</div>
				</div>

				<p class="text-[11px] text-gray-400 leading-relaxed">
					This report will be sent to the clinic for review. It does not directly modify the official medical record.
				</p>

				<button
					type="button"
					onclick={handleSubmitReport}
					class="w-full bg-[#1b522f] hover:bg-[#154225] text-white font-medium py-3.5 rounded-xl text-xs flex justify-center items-center space-x-2 transition-colors cursor-pointer shadow-sm active:scale-[0.99]"
				>
					<svg class="w-4 h-4 transform rotate-45 -mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8"></path>
					</svg>
					<span>Submit report</span>
				</button>
			</div>

		</div>
	{/if}
</div>
