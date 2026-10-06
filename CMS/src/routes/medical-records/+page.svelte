<script lang="ts">
	import { demoAccounts, clinicStore } from '#lib/state.svelte';

	let searchQuery = $state('');
	let selectedStudentId = $state('faith-manada');
	let showExportModal = $state(false);
	let showFullRecordModal = $state(false);
	let isExporting = $state(false);

	let studentsList = $derived(demoAccounts.filter((a) => a.category === 'student'));

	let activeStudent = $derived(
		demoAccounts.find((a) => a.id === selectedStudentId) || studentsList[0]
	);

	function handleSearchInput() {
		const q = searchQuery.toLowerCase().trim();
		if (!q) return;
		const found = studentsList.find(
			(s) => s.name.toLowerCase().includes(q) || s.studentId.includes(q)
		);
		if (found) {
			selectedStudentId = found.id;
		}
	}

	function handleExportPdf() {
		showExportModal = true;
	}

	function triggerPrint() {
		isExporting = true;
		setTimeout(() => {
			window.print();
			isExporting = false;
		}, 600);
	}
</script>

<svelte:head>
	<title>Medical Records - Clinic Portal - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Top Eyebrow, Title and Export Button -->
	<div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				ENTER ONCE. REUSE EVERYWHERE.
			</p>
			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				Medical records
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Find a student by name or student number.
			</p>
		</div>

		<button
			type="button"
			onclick={handleExportPdf}
			class="inline-flex items-center space-x-2 px-5 py-3 rounded-2xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors cursor-pointer self-start sm:self-auto active:scale-[0.98]"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
			</svg>
			<span>Export medical record PDF</span>
		</button>
	</div>

	<!-- Big Search Bar -->
	<div class="relative w-full">
		<div class="absolute inset-y-0 left-0 pl-5 flex items-center pointer-events-none">
			<svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
			</svg>
		</div>
		<input
			type="text"
			bind:value={searchQuery}
			oninput={handleSearchInput}
			placeholder="Search by name or student number..."
			class="w-full pl-13 pr-16 py-4 bg-white border border-gray-200/90 rounded-2xl text-sm focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-xs transition-colors"
		/>
		<div class="absolute inset-y-0 right-0 pr-5 flex items-center pointer-events-none">
			<span class="px-2 py-1 bg-gray-100 border border-gray-200 text-gray-400 rounded-md text-[11px] font-mono font-medium">
				⌘ K
			</span>
		</div>
	</div>

	<!-- Student Switcher Chips -->
	<div class="flex items-center space-x-2 overflow-x-auto pb-1 text-xs">
		<span class="text-gray-400 shrink-0 font-medium">Quick switch:</span>
		{#each studentsList as s}
			<button
				type="button"
				onclick={() => { selectedStudentId = s.id; searchQuery = s.name; }}
				class="px-3 py-1.5 rounded-full border transition-colors cursor-pointer shrink-0 {selectedStudentId === s.id
					? 'bg-[#edf7f0] text-[#1b522f] border-[#1b522f]/30 font-semibold'
					: 'bg-white text-gray-600 border-gray-200 hover:bg-gray-50'}"
			>
				{s.name} ({s.studentId})
			</button>
		{/each}
	</div>

	<!-- Main Details & Timeline Grid (Matching Image 3) -->
	<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
		
		<!-- Left Card: Student Info -->
		<div class="lg:col-span-7 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
			<!-- Header -->
			<div class="flex items-start justify-between pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-4">
					<div
						class="w-14 h-14 rounded-2xl flex items-center justify-center font-bold text-base shrink-0 shadow-2xs"
						style="background-color: {activeStudent.avatarBg}; color: {activeStudent.avatarColor};"
					>
						{activeStudent.initials}
					</div>
					<div>
						<h2 class="text-xl font-bold text-gray-800">{activeStudent.name}</h2>
						<p class="text-xs text-gray-400 mt-0.5">Student No. {activeStudent.studentId}</p>
					</div>
				</div>

				<span class="px-3 py-1 rounded-full text-xs font-semibold bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
					Active
				</span>
			</div>

			<!-- Student Data Fields -->
			<div class="grid grid-cols-2 gap-y-5 gap-x-6 text-xs">
				<div>
					<p class="text-gray-400 font-medium">Program / Strand</p>
					<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.programStrand}</p>
				</div>
				<div>
					<p class="text-gray-400 font-medium">Year & Section</p>
					<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.yearSection}</p>
				</div>
				<div>
					<p class="text-gray-400 font-medium">School email</p>
					<p class="text-sm font-bold text-gray-800 mt-1 truncate">{activeStudent.email}</p>
				</div>
				<div>
					<p class="text-gray-400 font-medium">Contact</p>
					<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.contactNumber}</p>
				</div>
			</div>

			<!-- Emergency Contact Banner Box -->
			<div class="bg-[#edf7f0] border border-[#1b522f]/10 rounded-2xl p-5 flex items-center justify-between">
				<div class="flex items-center space-x-3.5">
					<div class="w-10 h-10 rounded-xl bg-white text-[#1b522f] flex items-center justify-center shrink-0 shadow-2xs">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
						</svg>
					</div>
					<div>
						<p class="text-[10px] font-semibold text-gray-400 uppercase tracking-wider">Emergency / Responsible Person</p>
						<p class="text-sm font-bold text-gray-800 mt-0.5">{activeStudent.emergencyPerson}</p>
						<p class="text-xs text-gray-400 font-mono mt-0.5">{activeStudent.emergencyContact}</p>
					</div>
				</div>

				<a
					href="tel:{activeStudent.emergencyContact}"
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold flex items-center space-x-2 transition-colors cursor-pointer shadow-2xs"
				>
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
					</svg>
					<span>Call</span>
				</a>
			</div>
		</div>

		<!-- Right Card: Clinic Timeline -->
		<div class="lg:col-span-5 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
			<div class="flex items-center justify-between">
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">EASY TO SCAN</p>
				<button
					type="button"
					onclick={() => (showFullRecordModal = true)}
					class="text-xs font-semibold text-[#1b522f] hover:underline cursor-pointer"
				>
					View full record
				</button>
			</div>

			<h3 class="text-xl font-bold text-gray-800">Clinic timeline</h3>

			<div class="relative pl-6 space-y-8 before:absolute before:left-2 before:top-2 before:bottom-2 before:w-0.5 before:bg-gray-100">
				<!-- Timeline 1 -->
				<div class="relative">
					<div class="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-[#1b522f] ring-4 ring-white"></div>
					<p class="text-[10px] font-bold tracking-wider text-gray-400 uppercase">OCTOBER 4, 2026</p>
					<h4 class="text-sm font-bold text-gray-800 mt-1">Headache</h4>
					<p class="text-xs text-gray-500 mt-0.5">
						<strong>Assessment:</strong> Mild · <strong>Intervention:</strong> Rest + Hydration
					</p>
					<p class="text-[11px] text-gray-400 mt-1">Returned to class · Follow-up not required</p>
				</div>

				<!-- Timeline 2 -->
				<div class="relative">
					<div class="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-[#1b522f] ring-4 ring-white"></div>
					<p class="text-[10px] font-bold tracking-wider text-gray-400 uppercase">SEPTEMBER 18, 2026</p>
					<h4 class="text-sm font-bold text-gray-800 mt-1">Minor injury</h4>
					<p class="text-xs text-gray-500 mt-0.5">
						<strong>Assessment:</strong> Superficial cut · <strong>Intervention:</strong> Wound cleaning
					</p>
					<p class="text-[11px] text-gray-400 mt-1">Returned to class</p>
				</div>

				{#if clinicStore.crrmuReportApproved}
					<!-- Additional entry if CRRMU report approved -->
					<div class="relative">
						<div class="absolute -left-6 top-1 w-2.5 h-2.5 rounded-full bg-[#1b522f] ring-4 ring-white"></div>
						<p class="text-[10px] font-bold tracking-wider text-gray-400 uppercase">OCTOBER 6, 2026</p>
						<h4 class="text-sm font-bold text-gray-800 mt-1">Minor injury (CRRMU)</h4>
						<p class="text-xs text-gray-500 mt-0.5">
							<strong>Assessment:</strong> Superficial cut · <strong>Intervention:</strong> Wound cleaning + Bandaging
						</p>
						<p class="text-[11px] text-gray-400 mt-1">Returned to class · Verified by Clinic</p>
					</div>
				{/if}
			</div>
		</div>

	</div>
</div>

<!-- ================= EXPORT PDF MODAL ================= -->
{#if showExportModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto space-y-6">
			<!-- Modal Header -->
			<div class="flex items-start justify-between pb-4 border-b border-gray-100">
				<div>
					<span class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">OFFICIAL HEALTH DOCUMENT</span>
					<h3 class="text-xl font-bold text-gray-800 mt-1">Medical Record Export Preview</h3>
				</div>
				<button
					type="button"
					onclick={() => (showExportModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-gray-100 text-gray-400 hover:text-gray-700 flex items-center justify-center transition-colors cursor-pointer"
				>
					✕
				</button>
			</div>

			<!-- Document Sheet Style Preview -->
			<div class="bg-[#fcfdfd] border border-gray-200 rounded-2xl p-6 space-y-5 text-xs text-gray-700 shadow-2xs font-sans">
				<!-- Header with Logo -->
				<div class="flex items-center justify-between border-b border-gray-200 pb-4">
					<div class="flex items-center space-x-3">
						<div class="w-10 h-10 bg-[#428859] rounded-xl flex items-center justify-center text-white font-bold">
							CS
						</div>
						<div>
							<h4 class="font-bold text-sm text-gray-900 tracking-tight">CELTECH SCHOOL CLINIC</h4>
							<p class="text-[11px] text-gray-400">Institutional Health & Medical Management System</p>
						</div>
					</div>
					<div class="text-right">
						<span class="inline-block px-2.5 py-0.5 rounded-full bg-[#edf7f0] text-[#1b522f] font-mono text-[10px] font-bold">
							CONFIDENTIAL
						</span>
						<p class="text-[10px] text-gray-400 mt-1">Date: Oct 06, 2026</p>
					</div>
				</div>

				<!-- Student Profile Summary -->
				<div class="grid grid-cols-2 sm:grid-cols-4 gap-4 bg-white p-4 rounded-xl border border-gray-100">
					<div>
						<p class="text-[10px] text-gray-400 font-semibold uppercase">Student Name</p>
						<p class="font-bold text-gray-900 mt-0.5">{activeStudent.name}</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 font-semibold uppercase">Student ID</p>
						<p class="font-bold text-gray-900 mt-0.5">{activeStudent.studentId}</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 font-semibold uppercase">Program / Year</p>
						<p class="font-bold text-gray-900 mt-0.5">{activeStudent.programStrand} - {activeStudent.yearSection}</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 font-semibold uppercase">Status</p>
						<p class="font-bold text-[#1b522f] mt-0.5">Cleared / Active</p>
					</div>
				</div>

				<!-- Incident & Clinical Records Table -->
				<div>
					<p class="font-bold text-xs text-gray-800 uppercase tracking-wider mb-2">Clinic Encounters & Consultations</p>
					<div class="border border-gray-200 rounded-xl overflow-hidden">
						<table class="w-full text-left text-[11px]">
							<thead class="bg-gray-50 border-b border-gray-200 text-gray-500">
								<tr>
									<th class="p-2.5 font-semibold">Date</th>
									<th class="p-2.5 font-semibold">Chief Concern</th>
									<th class="p-2.5 font-semibold">Assessment</th>
									<th class="p-2.5 font-semibold">Intervention</th>
									<th class="p-2.5 font-semibold">Disposition</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-100">
								<tr>
									<td class="p-2.5 font-mono">2026-10-04</td>
									<td class="p-2.5 font-bold">Headache</td>
									<td class="p-2.5">Mild cephalalgia</td>
									<td class="p-2.5">Rest + Oral Hydration</td>
									<td class="p-2.5">Returned to class</td>
								</tr>
								<tr>
									<td class="p-2.5 font-mono">2026-09-18</td>
									<td class="p-2.5 font-bold">Minor injury</td>
									<td class="p-2.5">Superficial abrasion</td>
									<td class="p-2.5">Wound cleaning</td>
									<td class="p-2.5">Returned to class</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<!-- Attestation Sign-off -->
				<div class="pt-4 border-t border-gray-200 flex justify-between items-end text-[11px] text-gray-500">
					<div>
						<p class="font-medium">Recorded by:</p>
						<p class="font-bold text-gray-800 mt-1">Alma A. Lontoc, RN</p>
						<p class="text-[10px] text-gray-400">Head Nurse · CELTECH Clinic</p>
					</div>
					<div class="text-right">
						<div class="w-32 border-b border-gray-300 pb-1 mb-1 text-center font-serif italic text-gray-400">A. Lontoc</div>
						<p class="text-[10px] text-gray-400">Authorized Clinic Signature</p>
					</div>
				</div>
			</div>

			<!-- Actions -->
			<div class="flex items-center justify-end space-x-3 pt-2">
				<button
					type="button"
					onclick={() => (showExportModal = false)}
					class="px-5 py-2.5 rounded-xl border border-gray-200 text-gray-600 hover:bg-gray-50 text-xs font-semibold transition-colors cursor-pointer"
				>
					Cancel
				</button>
				<button
					type="button"
					onclick={triggerPrint}
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold flex items-center space-x-2 transition-colors cursor-pointer shadow-xs"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"></path>
					</svg>
					<span>{isExporting ? 'Generating PDF...' : 'Print / Download PDF'}</span>
				</button>
			</div>
		</div>
	</div>
{/if}

<!-- ================= FULL CLINICAL RECORD MODAL ================= -->
{#if showFullRecordModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-xl w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto space-y-6">
			<div class="flex items-start justify-between pb-4 border-b border-gray-100">
				<div>
					<span class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">COMPLETE EHR PROFILE</span>
					<h3 class="text-xl font-bold text-gray-800 mt-1">{activeStudent.name}'s Medical Chart</h3>
				</div>
				<button
					type="button"
					onclick={() => (showFullRecordModal = false)}
					aria-label="Close modal"
					class="w-8 h-8 rounded-full bg-gray-100 text-gray-400 hover:text-gray-700 flex items-center justify-center transition-colors cursor-pointer"
				>
					✕
				</button>
			</div>

			<div class="space-y-4 text-xs">
				<div class="p-4 bg-[#f8faf9] rounded-2xl border border-gray-100 space-y-2">
					<h4 class="font-bold text-gray-800">Health Baseline & Allergies</h4>
					<p class="text-gray-600"><strong>Allergies:</strong> No known drug allergies (NKDA)</p>
					<p class="text-gray-600"><strong>Chronic Conditions:</strong> None reported</p>
					<p class="text-gray-600"><strong>Blood Type:</strong> O Positive</p>
					<p class="text-gray-600"><strong>Immunization Status:</strong> Complete (Tetanus booster 2024)</p>
				</div>

				<div class="p-4 bg-[#f8faf9] rounded-2xl border border-gray-100 space-y-2">
					<h4 class="font-bold text-gray-800">Vital Signs History</h4>
					<p class="text-gray-600"><strong>Last Recorded BP:</strong> 110/70 mmHg (Oct 4, 2026)</p>
					<p class="text-gray-600"><strong>Heart Rate:</strong> 74 bpm</p>
					<p class="text-gray-600"><strong>Body Temp:</strong> 36.6 °C</p>
				</div>
			</div>

			<div class="flex justify-end pt-2">
				<button
					type="button"
					onclick={() => (showFullRecordModal = false)}
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] text-white text-xs font-semibold cursor-pointer"
				>
					Close
				</button>
			</div>
		</div>
	</div>
{/if}
