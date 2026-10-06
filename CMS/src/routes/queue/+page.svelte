<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';

	let activeFilter = $state<'All' | 'Waiting' | 'In consultation' | 'Observation' | 'Completed'>('All');
	let showWalkInModal = $state(false);

	let studentName = $state('');
	let studentId = $state('');
	let complaint = $state('Headache');

	let filteredQueue = $derived.by(() => {
		if (activeFilter === 'Waiting') return clinicStore.queue.filter((q) => q.status === 'Waiting');
		if (activeFilter === 'In consultation') return clinicStore.queue.filter((q) => q.status === 'In Consultation');
		if (activeFilter === 'Observation') return clinicStore.queue.filter((q) => q.status === 'Under Observation');
		if (activeFilter === 'Completed') return clinicStore.queue.filter((q) => q.status === 'Completed');
		return clinicStore.queue;
	});

	function handleAddWalkIn(e: SubmitEvent) {
		e.preventDefault();
		if (!studentName.trim()) return;

		const initials = studentName
			.split(' ')
			.map((n) => n[0])
			.join('')
			.slice(0, 2)
			.toUpperCase();

		clinicStore.addQueueItem({
			studentName,
			studentId: studentId || '2026' + Math.floor(10000 + Math.random() * 90000),
			studentInitials: initials || 'ST',
			complaint,
			timeInClinic: 'Just arrived',
			status: 'Waiting',
			actionText: 'Start visit'
		});

		studentName = '';
		studentId = '';
		showWalkInModal = false;
	}
</script>

<svelte:head>
	<title>Queue Management - Clinic Portal - CSHMS</title>
</svelte:head>

<div class="space-y-6 max-w-6xl">
	<!-- Page Header -->
	<div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
		<div>
			<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
				LIVE CLINIC FLOW
			</p>
			<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
				Queue management
			</h1>
			<p class="text-sm text-gray-500 mt-1">
				Update each student's status with one click.
			</p>
		</div>

		<button
			type="button"
			onclick={() => (showWalkInModal = true)}
			class="inline-flex items-center space-x-2 px-5 py-3 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors self-start sm:self-auto cursor-pointer"
		>
			<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
				<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
			</svg>
			<span>Add walk-in</span>
		</button>
	</div>

	<!-- Filter Tabs -->
	<div class="flex flex-wrap items-center gap-2 pt-2">
		{#each ['All', 'Waiting', 'In consultation', 'Observation', 'Completed'] as tab}
			{@const isSelected = activeFilter === tab}
			<button
				type="button"
				onclick={() => (activeFilter = tab as any)}
				class="px-4 py-2 rounded-full text-xs font-semibold transition-colors cursor-pointer {isSelected
					? 'bg-[#1b522f] text-white shadow-2xs'
					: 'bg-white border border-gray-200 text-gray-700 hover:bg-gray-50'}"
			>
				{tab === 'All' ? `All ${clinicStore.queue.length}` : tab}
			</button>
		{/each}
	</div>

	<!-- Queue Table Card -->
	<div class="bg-white rounded-3xl border border-gray-100 shadow-xs overflow-hidden">
		<div class="overflow-x-auto">
			<table class="w-full text-left text-xs">
				<thead>
					<tr class="border-b border-gray-100 text-gray-400 uppercase text-[10px] font-bold tracking-wider">
						<th class="py-4 px-6">QUEUE</th>
						<th class="py-4 px-6">STUDENT</th>
						<th class="py-4 px-6">VISIT</th>
						<th class="py-4 px-6">STATUS</th>
						<th class="py-4 px-6 text-right">ACTION</th>
					</tr>
				</thead>
				<tbody class="divide-y divide-gray-50">
					{#each filteredQueue as item (item.id)}
						<tr class="hover:bg-gray-50/50 transition-colors">
							<!-- Queue Number -->
							<td class="py-4 px-6 font-bold text-gray-800 text-sm whitespace-nowrap">
								{item.queueNumber}
							</td>

							<!-- Student Info -->
							<td class="py-4 px-6">
								<div class="flex items-center space-x-3">
									<div class="w-8 h-8 rounded-full bg-[#8fd3a2] text-[#1b522f] flex items-center justify-center font-bold text-xs shrink-0">
										{item.studentInitials}
									</div>
									<div>
										<p class="font-bold text-gray-800">{item.studentName}</p>
										<p class="text-[11px] text-gray-400">{item.studentId} · {item.complaint}</p>
									</div>
								</div>
							</td>

							<!-- Visit Reason & Time in clinic -->
							<td class="py-4 px-6">
								<p class="font-bold text-gray-800">{item.complaint}</p>
								<p class="text-[11px] text-gray-400">{item.timeInClinic}</p>
							</td>

							<!-- Status Badge -->
							<td class="py-4 px-6">
								<span class="inline-flex items-center px-2.5 py-1 rounded-full text-[11px] font-semibold {item.status === 'Waiting'
									? 'bg-amber-50 text-amber-700'
									: item.status === 'In Consultation'
									? 'bg-[#e8f5ec] text-[#1b522f]'
									: item.status === 'Under Observation'
									? 'bg-[#e8f5ec] text-[#1b522f]'
									: 'bg-gray-100 text-gray-600'}">
									{item.status}
								</span>
							</td>

							<!-- Action Button -->
							<td class="py-4 px-6 text-right">
								<button
									type="button"
									onclick={() => clinicStore.advanceQueue(item.id)}
									class="px-4 py-2 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer shadow-2xs transition-colors"
								>
									{item.actionText}
								</button>
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>

<!-- Add Walk-in Modal -->
{#if showWalkInModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-xs">
		<div class="bg-white rounded-3xl max-w-md w-full p-6 md:p-8 shadow-2xl border border-gray-100">
			<div class="flex items-center justify-between pb-4 border-b border-gray-100">
				<div>
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">CLINIC RECEPTION</p>
					<h3 class="text-xl font-bold text-gray-800">Add Walk-in Student</h3>
				</div>
				<button
					type="button"
					onclick={() => (showWalkInModal = false)}
					class="w-8 h-8 rounded-full bg-gray-100 hover:bg-gray-200 text-gray-500 flex items-center justify-center cursor-pointer"
				>
					✕
				</button>
			</div>

			<form onsubmit={handleAddWalkIn} class="space-y-4 mt-5">
				<div>
					<label for="walkin-name" class="block text-xs font-semibold text-gray-700 mb-1">Student Full Name</label>
					<input
						id="walkin-name"
						type="text"
						required
						bind:value={studentName}
						placeholder="e.g. Christian Paul Bautista"
						class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
					/>
				</div>

				<div>
					<label for="walkin-id" class="block text-xs font-semibold text-gray-700 mb-1">Student ID (optional)</label>
					<input
						id="walkin-id"
						type="text"
						bind:value={studentId}
						placeholder="e.g. 202611982"
						class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]"
					/>
				</div>

				<div>
					<label for="walkin-complaint" class="block text-xs font-semibold text-gray-700 mb-1">Chief Complaint</label>
					<select
						id="walkin-complaint"
						bind:value={complaint}
						class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] bg-white"
					>
						<option value="Headache">Headache</option>
						<option value="Minor injury">Minor injury</option>
						<option value="Dizziness">Dizziness</option>
						<option value="Stomach ache">Stomach ache</option>
						<option value="Feverish">Feverish</option>
						<option value="Allergic reaction">Allergic reaction</option>
					</select>
				</div>

				<div class="pt-3 flex items-center justify-end space-x-3 border-t border-gray-100">
					<button
						type="button"
						onclick={() => (showWalkInModal = false)}
						class="px-4 py-2.5 rounded-xl border border-gray-200 text-xs font-semibold text-gray-600 hover:bg-gray-50 cursor-pointer"
					>
						Cancel
					</button>
					<button
						type="submit"
						class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer shadow-xs"
					>
						Add to Queue
					</button>
				</div>
			</form>
		</div>
	</div>
{/if}
