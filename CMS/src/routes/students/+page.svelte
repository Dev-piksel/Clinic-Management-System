<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';
	import { fetchAdminUsers } from '#lib/api';
	import type { DemoAccount } from '#lib/types';
	import { onMount } from 'svelte';

	let searchQuery = $state('');
	let studentsList = $state<DemoAccount[]>([]);
	let selectedStudentId = $state('');
	let isLoading = $state(true);

	onMount(async () => {
		try {
			const users = await fetchAdminUsers('approved');
			studentsList = users.filter((a) => a.category === 'student');
			if (studentsList.length > 0) {
				selectedStudentId = studentsList[0].id;
			}
		} catch (err) {
			console.warn('Failed to load students', err);
		} finally {
			isLoading = false;
		}
	});

	let activeStudent = $derived(
		studentsList.find((a) => a.id === selectedStudentId) || (studentsList.length > 0 ? studentsList[0] : null)
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
</script>

<svelte:head>
	<title>Student Search - Clinic Portal - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Page Header -->
	<div>
		<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
			STUDENT DIRECTORY
		</p>
		<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
			Student search
		</h1>
		<p class="text-sm text-gray-500 mt-1">
			Find an active registered student by name or student number.
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
	</div>

	{#if isLoading}
		<div class="bg-white rounded-3xl p-12 text-center border border-gray-100 shadow-xs space-y-3">
			<div class="w-8 h-8 border-2 border-[#1b522f] border-t-transparent rounded-full animate-spin mx-auto"></div>
			<p class="text-xs text-gray-400">Loading student directory...</p>
		</div>
	{:else if studentsList.length === 0 || !activeStudent}
		<div class="bg-white rounded-3xl p-12 text-center border border-gray-100 shadow-xs space-y-3">
			<div class="w-12 h-12 bg-gray-100 text-gray-400 rounded-2xl mx-auto flex items-center justify-center">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
				</svg>
			</div>
			<h3 class="text-base font-bold text-gray-800">No registered students yet</h3>
			<p class="text-xs text-gray-500 max-w-sm mx-auto">
				When students register and their accounts are approved by clinic administration, they will appear in this directory.
			</p>
			<a href="/register" class="inline-block mt-2 px-5 py-2.5 rounded-xl bg-[#1b522f] text-white text-xs font-semibold hover:bg-[#154225] transition-colors">
				Register New Student
			</a>
		</div>
	{:else}
		<!-- Student Pills Selection Bar -->
		<div class="flex items-center space-x-2 overflow-x-auto pb-1">
			{#each studentsList as s (s.id)}
				<button
					type="button"
					onclick={() => (selectedStudentId = s.id)}
					class="px-4 py-2 rounded-xl text-xs font-semibold whitespace-nowrap transition-all cursor-pointer {selectedStudentId === s.id
						? 'bg-[#1b522f] text-white shadow-xs'
						: 'bg-white text-gray-600 hover:bg-gray-50 border border-gray-100'}"
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
							style="background-color: {activeStudent.avatarBg || '#edf7f0'}; color: {activeStudent.avatarColor || '#1b522f'};"
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
						<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.programStrand || 'N/A'}</p>
					</div>
					<div>
						<p class="text-gray-400 font-medium">Year & Section</p>
						<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.yearSection || 'N/A'}</p>
					</div>
					<div>
						<p class="text-gray-400 font-medium">Email</p>
						<p class="text-sm font-bold text-gray-800 mt-1 truncate">{activeStudent.email}</p>
					</div>
					<div>
						<p class="text-gray-400 font-medium">Contact</p>
						<p class="text-sm font-bold text-gray-800 mt-1">{activeStudent.contactNumber || 'N/A'}</p>
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
							<p class="text-sm font-bold text-gray-800 mt-0.5">{activeStudent.emergencyPerson || 'None specified'}</p>
							<p class="text-xs text-gray-400 font-mono mt-0.5">{activeStudent.emergencyContact || 'No number'}</p>
						</div>
					</div>

					{#if activeStudent.emergencyContact}
						<a
							href="tel:{activeStudent.emergencyContact}"
							class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold flex items-center space-x-2 transition-colors cursor-pointer shadow-2xs"
						>
							<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
							</svg>
							<span>Call</span>
						</a>
					{/if}
				</div>
			</div>

			<!-- Right Card: Clinic Timeline -->
			<div class="lg:col-span-5 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
				<div class="flex items-center justify-between">
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">CLINIC RECORD</p>
					<a href="/medical-records" class="text-xs font-semibold text-[#1b522f] hover:underline">
						View full record
					</a>
				</div>

				<h3 class="text-xl font-bold text-gray-800">Clinic status</h3>
				<div class="p-6 bg-gray-50/70 rounded-2xl border border-gray-100 text-center space-y-1">
					<p class="text-xs font-semibold text-gray-700">Records on File</p>
					<p class="text-[11px] text-gray-400">Student is cleared for campus health attendance.</p>
				</div>
			</div>

		</div>
	{/if}
</div>
