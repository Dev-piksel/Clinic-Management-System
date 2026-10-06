<script lang="ts">
	let showExportModal = $state(false);
	let isExporting = $state(false);

	const dailyVisits = [
		{ day: 'Mon', count: 5, heightPercent: 52 },
		{ day: 'Tue', count: 7, heightPercent: 74 },
		{ day: 'Wed', count: 4, heightPercent: 42 },
		{ day: 'Thu', count: 8, heightPercent: 85 },
		{ day: 'Fri', count: 6, heightPercent: 63 },
		{ day: 'Sat', count: 3, heightPercent: 32 }
	];

	const visitReasons = [
		{ reason: 'Headache', count: '14 visits', percent: 85 },
		{ reason: 'Minor injury', count: '10 visits', percent: 62 },
		{ reason: 'Dizziness', count: '07 visits', percent: 44 },
		{ reason: 'Stomachache', count: '05 visits', percent: 30 }
	];

	const outcomes = [
		{ count: '32', label: 'Returned to class', percent: '62%' },
		{ count: '08', label: 'Observation', percent: '15%' },
		{ count: '06', label: 'Follow-up required', percent: '12%' },
		{ count: '06', label: 'Sent home', percent: '11%' }
	];

	function triggerPrint() {
		isExporting = true;
		setTimeout(() => {
			window.print();
			isExporting = false;
		}, 600);
	}
</script>

<svelte:head>
	<title>Clinic Reports & Analytics - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Page Eyebrow, Title and Export Summary Button -->
	<div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				CLINIC INSIGHTS
			</p>
			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				Reports
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				A compact operational summary for the CELTECH School Clinic.
			</p>
		</div>

		<button
			type="button"
			onclick={() => (showExportModal = true)}
			class="inline-flex items-center space-x-2 px-5 py-3 rounded-2xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors cursor-pointer self-start sm:self-auto active:scale-[0.98]"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path>
			</svg>
			<span>Export summary</span>
		</button>
	</div>

	<!-- Top Row: 4 Metric Cards (Matching Image 5) -->
	<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
		
		<!-- 1: Students Assisted -->
		<div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z"></path>
				</svg>
			</div>
			<div>
				<p class="text-[11px] font-medium text-gray-400">Students assisted</p>
				<h3 class="text-3xl font-bold text-gray-800 leading-tight">48</h3>
				<p class="text-[11px] text-gray-400 mt-0.5">This month</p>
			</div>
		</div>

		<!-- 2: Clinic Visits -->
		<div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
				</svg>
			</div>
			<div>
				<p class="text-[11px] font-medium text-gray-400">Clinic visits</p>
				<h3 class="text-3xl font-bold text-gray-800 leading-tight">52</h3>
				<p class="text-[11px] text-gray-400 mt-0.5">4 repeat visits</p>
			</div>
		</div>

		<!-- 3: Appointments -->
		<div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
				</svg>
			</div>
			<div>
				<p class="text-[11px] font-medium text-gray-400">Appointments</p>
				<h3 class="text-3xl font-bold text-gray-800 leading-tight">31</h3>
				<p class="text-[11px] text-gray-400 mt-0.5">92% completed</p>
			</div>
		</div>

		<!-- 4: Sent Home -->
		<div class="bg-white rounded-3xl p-6 border border-gray-100 shadow-xs flex items-center space-x-4">
			<div class="w-12 h-12 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
				<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
				</svg>
			</div>
			<div>
				<p class="text-[11px] font-medium text-gray-400">Sent home</p>
				<h3 class="text-3xl font-bold text-gray-800 leading-tight">06</h3>
				<p class="text-[11px] text-gray-400 mt-0.5">Contacts recorded</p>
			</div>
		</div>

	</div>

	<!-- Middle Row: Daily clinic visits (Chart) & Common concerns -->
	<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-stretch">
		
		<!-- Left Card: Daily Clinic Visits Bar Chart -->
		<div class="lg:col-span-7 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs flex flex-col justify-between">
			<!-- Header -->
			<div>
				<div class="flex items-center justify-between">
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
						LAST 7 DAYS
					</p>
					<span class="px-3 py-1 rounded-full text-xs font-semibold bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
						38 total
					</span>
				</div>
				<h3 class="text-xl font-bold text-gray-800 mt-1">
					Daily clinic visits
				</h3>
			</div>

			<!-- Vertical Bar Chart Visual -->
			<div class="pt-8 pb-2">
				<div class="grid grid-cols-6 gap-3 sm:gap-6 items-end h-48">
					{#each dailyVisits as item}
						<div class="flex flex-col items-center h-full justify-end group">
							<!-- Tall Track Pill -->
							<div class="w-full max-w-[42px] h-38 bg-[#e8f5ec]/70 rounded-2xl relative overflow-hidden flex items-end justify-center transition-transform group-hover:scale-[1.02]">
								<!-- Filled Solid Green Bar -->
								<div
									class="w-full bg-[#52a368] rounded-2xl transition-all duration-500 ease-out"
									style="height: {item.heightPercent}%;"
								></div>
							</div>

							<!-- Count & Day Labels -->
							<div class="mt-3 text-center">
								<p class="text-xs font-bold text-gray-800">{item.count}</p>
								<p class="text-[11px] font-medium text-gray-400 mt-0.5">{item.day}</p>
							</div>
						</div>
					{/each}
				</div>
			</div>
		</div>

		<!-- Right Card: Common Concerns / Visit Reasons -->
		<div class="lg:col-span-5 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs flex flex-col justify-between">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
					COMMON CONCERNS
				</p>
				<h3 class="text-xl font-bold text-gray-800 mt-1">
					Visit reasons
				</h3>
			</div>

			<!-- Horizontal Progress Rows -->
			<div class="space-y-5 pt-6 pb-2">
				{#each visitReasons as item}
					<div class="space-y-2">
						<div class="flex items-center justify-between text-xs">
							<span class="font-bold text-gray-800">{item.reason}</span>
							<span class="text-gray-400 font-medium">{item.count}</span>
						</div>
						<!-- Progress Bar -->
						<div class="w-full h-2 bg-[#e8f5ec] rounded-full overflow-hidden">
							<div
								class="h-full bg-[#52a368] rounded-full transition-all duration-500 ease-out"
								style="width: {item.percent}%;"
							></div>
						</div>
					</div>
				{/each}
			</div>
		</div>

	</div>

	<!-- Bottom Row: Disposition Summary / Outcomes this month -->
	<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-6">
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
				DISPOSITION SUMMARY
			</p>
			<h3 class="text-xl font-bold text-gray-800 mt-1">
				Outcomes this month
			</h3>
		</div>

		<div class="grid grid-cols-2 md:grid-cols-4 gap-6 pt-1">
			{#each outcomes as item}
				<div class="space-y-1">
					<h4 class="text-3xl font-bold text-gray-800">{item.count}</h4>
					<p class="text-xs font-semibold text-gray-800">{item.label}</p>
					<p class="text-xs text-gray-400">{item.percent}</p>
				</div>
			{/each}
		</div>
	</div>
</div>

<!-- ================= EXPORT OPERATIONAL SUMMARY MODAL ================= -->
{#if showExportModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl border border-gray-100 max-h-[90vh] overflow-y-auto space-y-6">
			<div class="flex items-start justify-between pb-4 border-b border-gray-100">
				<div>
					<span class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">CELTECH CLINIC OPERATIONS</span>
					<h3 class="text-xl font-bold text-gray-800 mt-1">Monthly Census & Operational Summary</h3>
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

			<div class="bg-[#fcfdfd] border border-gray-200 rounded-2xl p-6 space-y-5 text-xs text-gray-700 font-sans shadow-2xs">
				<div class="flex items-center justify-between border-b border-gray-200 pb-4">
					<div class="flex items-center space-x-3">
						<div class="w-10 h-10 bg-[#428859] rounded-xl flex items-center justify-center text-white font-bold">
							CS
						</div>
						<div>
							<h4 class="font-bold text-sm text-gray-900 tracking-tight">CELTECH SCHOOL CLINIC</h4>
							<p class="text-[11px] text-gray-400">Institutional Monthly Health Morbidity Report</p>
						</div>
					</div>
					<div class="text-right">
						<span class="inline-block px-2.5 py-0.5 rounded-full bg-[#edf7f0] text-[#1b522f] font-mono text-[10px] font-bold">
							OCTOBER 2026
						</span>
						<p class="text-[10px] text-gray-400 mt-1">Generated: Today, 10:42 AM</p>
					</div>
				</div>

				<div class="grid grid-cols-4 gap-3 text-center bg-white p-4 rounded-xl border border-gray-100">
					<div>
						<p class="text-[10px] text-gray-400 uppercase font-semibold">Patients</p>
						<p class="text-lg font-bold text-gray-900 mt-0.5">48</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 uppercase font-semibold">Total Visits</p>
						<p class="text-lg font-bold text-gray-900 mt-0.5">52</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 uppercase font-semibold">Appointments</p>
						<p class="text-lg font-bold text-gray-900 mt-0.5">31</p>
					</div>
					<div>
						<p class="text-[10px] text-gray-400 uppercase font-semibold">Sent Home</p>
						<p class="text-lg font-bold text-gray-900 mt-0.5">06</p>
					</div>
				</div>

				<div>
					<p class="font-bold text-xs text-gray-800 uppercase tracking-wider mb-2">Morbidity & Chief Complaints</p>
					<div class="border border-gray-200 rounded-xl overflow-hidden">
						<table class="w-full text-left text-[11px]">
							<thead class="bg-gray-50 border-b border-gray-200 text-gray-500">
								<tr>
									<th class="p-2.5 font-semibold">Category</th>
									<th class="p-2.5 font-semibold">Incidence Count</th>
									<th class="p-2.5 font-semibold">Percentage</th>
									<th class="p-2.5 font-semibold">Primary Disposition</th>
								</tr>
							</thead>
							<tbody class="divide-y divide-gray-100">
								<tr>
									<td class="p-2.5 font-bold">Headache / Cephalalgia</td>
									<td class="p-2.5 font-mono">14</td>
									<td class="p-2.5">26.9%</td>
									<td class="p-2.5">Rest + Return to class</td>
								</tr>
								<tr>
									<td class="p-2.5 font-bold">Minor Injury / Abrasion</td>
									<td class="p-2.5 font-mono">10</td>
									<td class="p-2.5">19.2%</td>
									<td class="p-2.5">First aid + Wound dressing</td>
								</tr>
								<tr>
									<td class="p-2.5 font-bold">Dizziness / Presyncope</td>
									<td class="p-2.5 font-mono">07</td>
									<td class="p-2.5">13.5%</td>
									<td class="p-2.5">Observation + Hydration</td>
								</tr>
								<tr>
									<td class="p-2.5 font-bold">Stomachache / Abdominal Pain</td>
									<td class="p-2.5 font-mono">05</td>
									<td class="p-2.5">9.6%</td>
									<td class="p-2.5">Rest + Antacid guidance</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>

				<div class="pt-4 border-t border-gray-200 flex justify-between items-end text-[11px] text-gray-500">
					<div>
						<p class="font-medium">Certified Accurate by:</p>
						<p class="font-bold text-gray-800 mt-1">Alma A. Lontoc, RN</p>
						<p class="text-[10px] text-gray-400">Head Nurse · CELTECH School Clinic</p>
					</div>
					<div class="text-right">
						<div class="w-32 border-b border-gray-300 pb-1 mb-1 text-center font-serif italic text-gray-400">A. Lontoc</div>
						<p class="text-[10px] text-gray-400">Signature on File</p>
					</div>
				</div>
			</div>

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
					<span>{isExporting ? 'Generating summary...' : 'Print / Download Report'}</span>
				</button>
			</div>
		</div>
	</div>
{/if}
