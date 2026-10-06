<script lang="ts">
	import { demoAccounts, clinicStore } from '#lib/state.svelte';

	let searchQuery = $state('');
	let selectedStudentId = $state('faith-manada');

	let studentsList = $derived(demoAccounts.filter((a) => a.category === 'student'));

	let activeStudent = $derived(
		demoAccounts.find((a) => a.id === selectedStudentId) || studentsList[0]
	);

	function handleSearchInput(e: Event) {
		const q = searchQuery.toLowerCase().trim();
		if (!q) return;
		const found = studentsList.find(
			(s) => s.name.toLowerCase().includes(q) || s.studentId.includes(q)
		);
		if (found) {
			selectedStudentId = found.id;
		}
	}
</script>

<svelte:head>
	<title>Student Search - Clinic Portal - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Page Header -->
	<div>
		<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
			ENTER ONCE. REUSE EVERYWHERE.
		</p>
		<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
			Student search
		</h1>
		<p class="text-sm text-gray-500 mt-1">
			Find a student by name or student number.
		</p>
	</div>

	<!-- Big Search Input -->
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

	<!-- Student Switcher Chips (when searching or previewing) -->
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

	<!-- Main Details & Timeline Grid -->
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
					<p class="text-gray-400 font-medium">Email</p>
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
				<a href="/medical-records" class="text-xs font-semibold text-[#1b522f] hover:underline">
					View full record
				</a>
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
			</div>
		</div>

	</div>
</div>
