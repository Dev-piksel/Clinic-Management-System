<script lang="ts">
	import { clinicStore } from '#lib/state.svelte';

	let isStaff = $derived(clinicStore.currentUser.category === 'staff');
	let isEditing = $state(false);

	// Profile fields
	let fullName = $state(clinicStore.currentUser.name);
	let role = $state(clinicStore.currentUser.role);
	let schoolEmail = $state(clinicStore.currentUser.email);
	let contactNumber = $state(clinicStore.currentUser.contactNumber);

	// Student specific
	let studentNumber = $state(clinicStore.currentUser.studentId);
	let programStrand = $state(clinicStore.currentUser.programStrand);
	let yearSection = $state(clinicStore.currentUser.yearSection);
	let address = $state(clinicStore.currentUser.address);
	let emergencyPerson = $state(clinicStore.currentUser.emergencyPerson);
	let emergencyRelationship = $state(clinicStore.currentUser.emergencyRelationship);
	let emergencyContact = $state(clinicStore.currentUser.emergencyContact);
	let preferredContactMethod = $state(clinicStore.currentUser.preferredContactMethod);

	// Clinic Staff Workflow Settings
	let appointmentAlerts = $state(true);
	let crrmuAlerts = $state(true);
	let followUpReminders = $state(true);

	let saveSuccess = $state(false);

	$effect(() => {
		if (!isEditing) {
			fullName = clinicStore.currentUser.name;
			role = clinicStore.currentUser.role;
			schoolEmail = clinicStore.currentUser.email;
			contactNumber = clinicStore.currentUser.contactNumber;
			studentNumber = clinicStore.currentUser.studentId;
			programStrand = clinicStore.currentUser.programStrand;
			yearSection = clinicStore.currentUser.yearSection;
			address = clinicStore.currentUser.address;
			emergencyPerson = clinicStore.currentUser.emergencyPerson;
			emergencyRelationship = clinicStore.currentUser.emergencyRelationship;
			emergencyContact = clinicStore.currentUser.emergencyContact;
			preferredContactMethod = clinicStore.currentUser.preferredContactMethod;
		}
	});

	function toggleEdit() {
		if (isEditing) {
			clinicStore.updateProfile({
				name: fullName,
				role,
				email: schoolEmail,
				contactNumber,
				studentId: studentNumber,
				programStrand,
				yearSection,
				address,
				emergencyPerson,
				emergencyRelationship,
				emergencyContact,
				preferredContactMethod
			});
			saveSuccess = true;
			setTimeout(() => {
				saveSuccess = false;
			}, 3000);
		}
		isEditing = !isEditing;
	}
</script>

<svelte:head>
	<title>{isStaff ? 'Profile & Preferences - Clinic Portal - CSHMS' : 'My Profile - CSHMS'}</title>
</svelte:head>

{#if isStaff}
	<!-- ================= CLINIC STAFF: PROFILE & PREFERENCES (NEW SCREENSHOT) ================= -->
	<div class="space-y-6 max-w-6xl">
		<!-- Top Eyebrow, Title and Edit Profile Button -->
		<div class="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
					CLINIC ACCOUNT
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					Profile & preferences
				</h1>
				<p class="text-sm text-gray-500 mt-1">
					Manage your CELTECH clinic account and workflow preferences.
				</p>
			</div>

			<div class="flex items-center space-x-3 self-start sm:self-auto">
				{#if saveSuccess}
					<span class="text-xs font-semibold text-[#1b522f] flex items-center space-x-1">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
						<span>Saved!</span>
					</span>
				{/if}

				<button
					type="button"
					onclick={toggleEdit}
					class="inline-flex items-center space-x-2 px-5 py-2.5 rounded-2xl border border-gray-200 bg-white hover:bg-gray-50 text-gray-700 text-xs font-semibold shadow-2xs transition-all cursor-pointer active:scale-[0.98]"
				>
					<svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
					</svg>
					<span>{isEditing ? 'Save changes' : 'Edit profile'}</span>
				</button>
			</div>
		</div>

		<!-- Main 2-Column Grid -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
			
			<!-- Left Card: User Profile Summary Card -->
			<div class="lg:col-span-5 bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs flex flex-col items-center text-center space-y-5">
				<!-- Large Squircle Avatar -->
				<div class="w-28 h-28 rounded-3xl bg-[#edf7f0] flex items-center justify-center p-3">
					<div
						class="w-full h-full rounded-2xl flex items-center justify-center font-bold text-2xl shadow-2xs"
						style="background-color: {clinicStore.currentUser.avatarBg}; color: {clinicStore.currentUser.avatarColor};"
					>
						{clinicStore.currentUser.initials}
					</div>
				</div>

				<!-- Name & Role -->
				<div>
					<h2 class="text-xl font-bold text-gray-900 leading-tight">
						{clinicStore.currentUser.name}
					</h2>
					<p class="text-xs text-gray-400 mt-1">
						{clinicStore.currentUser.role}
					</p>
				</div>

				<!-- Active Status Badge -->
				<span class="inline-block px-3.5 py-1 rounded-full text-xs font-medium bg-[#edf7f0] text-[#1b522f] border border-[#1b522f]/20">
					Clinic access active
				</span>

				<!-- Authorized Personnel Alert Box -->
				<div class="w-full bg-[#f4f9f6] border border-[#1b522f]/10 rounded-2xl p-4 flex items-start space-x-3 text-left">
					<div class="w-6 h-6 rounded-lg bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0 mt-0.5">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
						</svg>
					</div>
					<div>
						<h4 class="text-xs font-bold text-gray-800">Authorized personnel</h4>
						<p class="text-[11px] text-gray-500 mt-0.5 leading-snug">
							Medical record access is logged and protected.
						</p>
					</div>
				</div>
			</div>

			<!-- Right Column: Professional Profile & Workflow Settings -->
			<div class="lg:col-span-7 space-y-6">
				
				<!-- Card 1: Professional Profile -->
				<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-5">
					<div class="flex items-start justify-between">
						<div>
							<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
								ACCOUNT INFORMATION
							</p>
							<h3 class="text-lg font-bold text-gray-900 mt-1">
								Professional profile
							</h3>
						</div>
						<svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
						</svg>
					</div>

					<div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-1">
						<!-- Full name -->
						<div>
							<label for="staff-name" class="block text-xs font-semibold text-gray-700 mb-1.5">Full name</label>
							<input
								id="staff-name"
								type="text"
								disabled={!isEditing}
								bind:value={fullName}
								class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-xs transition-colors {isEditing
									? 'bg-white focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]'
									: 'bg-[#fbfcfc] text-gray-700 cursor-default'}"
							/>
						</div>

						<!-- Role -->
						<div>
							<label for="staff-role" class="block text-xs font-semibold text-gray-700 mb-1.5">Role</label>
							<input
								id="staff-role"
								type="text"
								disabled={!isEditing}
								bind:value={role}
								class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-xs transition-colors {isEditing
									? 'bg-white focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]'
									: 'bg-[#fbfcfc] text-gray-700 cursor-default'}"
							/>
						</div>

						<!-- School email -->
						<div>
							<label for="staff-email" class="block text-xs font-semibold text-gray-700 mb-1.5">School email</label>
							<input
								id="staff-email"
								type="email"
								disabled={!isEditing}
								bind:value={schoolEmail}
								class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-xs transition-colors {isEditing
									? 'bg-white focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]'
									: 'bg-[#fbfcfc] text-gray-700 cursor-default'}"
							/>
						</div>

						<!-- Contact number -->
						<div>
							<label for="staff-phone" class="block text-xs font-semibold text-gray-700 mb-1.5">Contact number</label>
							<input
								id="staff-phone"
								type="text"
								disabled={!isEditing}
								bind:value={contactNumber}
								class="w-full px-4 py-2.5 rounded-xl border border-gray-200 text-xs transition-colors {isEditing
									? 'bg-white focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]'
									: 'bg-[#fbfcfc] text-gray-700 cursor-default'}"
							/>
						</div>
					</div>
				</div>

				<!-- Card 2: Workflow Settings (Clinic preferences) -->
				<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs space-y-5">
					<div>
						<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
							WORKFLOW SETTINGS
						</p>
						<h3 class="text-lg font-bold text-gray-900 mt-1">
							Clinic preferences
						</h3>
					</div>

					<div class="divide-y divide-gray-100">
						<!-- Toggle 1: Appointment alerts -->
						<div class="py-4 first:pt-2 flex items-center justify-between">
							<div class="flex items-center space-x-3.5">
								<div class="w-10 h-10 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
									<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"></path>
									</svg>
								</div>
								<div>
									<h4 class="text-xs font-bold text-gray-800">Appointment alerts</h4>
									<p class="text-[11px] text-gray-400 mt-0.5">Notify me about new requests and changes</p>
								</div>
							</div>

							<!-- Custom Switch Toggle -->
							<button
								type="button"
								onclick={() => (appointmentAlerts = !appointmentAlerts)}
								aria-label="Toggle appointment alerts"
								class="w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-200 {appointmentAlerts
									? 'bg-[#52a368]'
									: 'bg-gray-200'}"
							>
								<div
									class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 {appointmentAlerts
										? 'translate-x-6'
										: 'translate-x-0'}"
								></div>
							</button>
						</div>

						<!-- Toggle 2: CRRMU report alerts -->
						<div class="py-4 flex items-center justify-between">
							<div class="flex items-center space-x-3.5">
								<div class="w-10 h-10 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
									<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
									</svg>
								</div>
								<div>
									<h4 class="text-xs font-bold text-gray-800">CRRMU report alerts</h4>
									<p class="text-[11px] text-gray-400 mt-0.5">Notify me when a first-aid report needs review</p>
								</div>
							</div>

							<button
								type="button"
								onclick={() => (crrmuAlerts = !crrmuAlerts)}
								aria-label="Toggle CRRMU report alerts"
								class="w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-200 {crrmuAlerts
									? 'bg-[#52a368]'
									: 'bg-gray-200'}"
							>
								<div
									class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 {crrmuAlerts
										? 'translate-x-6'
										: 'translate-x-0'}"
								></div>
							</button>
						</div>

						<!-- Toggle 3: Follow-up reminders -->
						<div class="py-4 last:pb-2 flex items-center justify-between">
							<div class="flex items-center space-x-3.5">
								<div class="w-10 h-10 rounded-2xl bg-[#edf7f0] text-[#1b522f] flex items-center justify-center shrink-0">
									<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
										<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"></path>
									</svg>
								</div>
								<div>
									<h4 class="text-xs font-bold text-gray-800">Follow-up reminders</h4>
									<p class="text-[11px] text-gray-400 mt-0.5">Show reminders for due student follow-ups</p>
								</div>
							</div>

							<button
								type="button"
								onclick={() => (followUpReminders = !followUpReminders)}
								aria-label="Toggle follow-up reminders"
								class="w-12 h-6 flex items-center rounded-full p-1 cursor-pointer transition-colors duration-200 {followUpReminders
									? 'bg-[#52a368]'
									: 'bg-gray-200'}"
							>
								<div
									class="bg-white w-4 h-4 rounded-full shadow-md transform transition-transform duration-200 {followUpReminders
										? 'translate-x-6'
										: 'translate-x-0'}"
								></div>
							</button>
						</div>
					</div>
				</div>

			</div>

		</div>
	</div>

{:else}
	<!-- ================= STUDENT PROFILE VIEW ================= -->
	<div class="space-y-8 max-w-6xl">
		<!-- Page Header -->
		<div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
			<div>
				<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase mb-1">
					SAVED ONCE, REUSED SECURELY
				</p>
				<h1 class="text-3xl md:text-4xl font-normal text-gray-900 tracking-tight">
					My profile
				</h1>
				<p class="text-sm text-gray-500 mt-1">
					Keep your permitted personal and emergency details up to date.
				</p>
			</div>

			<div class="flex items-center space-x-3 self-start md:self-auto">
				{#if saveSuccess}
					<span class="text-xs font-semibold text-[#1b522f] flex items-center space-x-1">
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
						<span>Saved successfully!</span>
					</span>
				{/if}

				<button
					type="button"
					onclick={toggleEdit}
					class="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl border border-gray-200 hover:border-[#1b522f] text-gray-700 hover:text-[#1b522f] bg-white text-xs font-semibold shadow-2xs transition-colors cursor-pointer"
				>
					{#if isEditing}
						<svg class="w-3.5 h-3.5 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
						<span class="text-[#1b522f]">Save profile</span>
					{:else}
						<svg class="w-3.5 h-3.5 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"></path>
						</svg>
						<span>Edit profile</span>
					{/if}
				</button>
			</div>
		</div>

		<!-- Profile Main Grid -->
		<div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
			
			<!-- Left User Summary Card -->
			<div class="lg:col-span-4 bg-white rounded-3xl p-8 border border-gray-100 shadow-xs flex flex-col items-center text-center">
				<div
					class="w-24 h-24 rounded-3xl flex items-center justify-center font-bold text-2xl shadow-xs"
					style="background-color: {clinicStore.currentUser.avatarBg}; color: {clinicStore.currentUser.avatarColor};"
				>
					{clinicStore.currentUser.initials}
				</div>

				<h2 class="text-xl font-bold text-gray-800 mt-5">{clinicStore.currentUser.name}</h2>
				<p class="text-xs text-gray-400 font-medium mt-1">
					{clinicStore.currentUser.role} · {clinicStore.currentUser.programStrand} {clinicStore.currentUser.yearSection}
				</p>

				<span class="inline-block mt-4 px-3 py-1 rounded-lg bg-[#edf7f0] text-[#1b522f] text-[10px] font-bold tracking-wider">
					Profile complete
				</span>

				<div class="w-full mt-6 pt-6 border-t border-gray-100">
					<div class="w-full bg-gray-100 h-1.5 rounded-full overflow-hidden">
						<div class="bg-[#1b522f] h-full w-full rounded-full"></div>
					</div>
					<p class="text-[10px] text-gray-400 mt-2 font-medium">All required information is complete</p>
				</div>
			</div>

			<!-- Right Details Cards -->
			<div class="lg:col-span-8 space-y-6">
				
				<!-- School Information Card -->
				<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
					<div class="flex items-center justify-between mb-4">
						<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
							SCHOOL INFORMATION
						</p>
						<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
						</svg>
					</div>

					<h3 class="text-lg font-bold text-gray-800 mb-6">Student details</h3>

					<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
						<div>
							<label for="student-name" class="block text-xs font-semibold text-gray-700 mb-1.5">Full name</label>
							<input
								id="student-name"
								type="text"
								disabled={!isEditing}
								bind:value={fullName}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="student-number" class="block text-xs font-semibold text-gray-700 mb-1.5">Student number</label>
							<input
								id="student-number"
								type="text"
								disabled={!isEditing}
								bind:value={studentNumber}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="student-program" class="block text-xs font-semibold text-gray-700 mb-1.5">Program / Strand</label>
							<input
								id="student-program"
								type="text"
								disabled={!isEditing}
								bind:value={programStrand}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="student-year" class="block text-xs font-semibold text-gray-700 mb-1.5">Year & Section</label>
							<input
								id="student-year"
								type="text"
								disabled={!isEditing}
								bind:value={yearSection}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="student-email" class="block text-xs font-semibold text-gray-700 mb-1.5">Email</label>
							<input
								id="student-email"
								type="email"
								disabled={!isEditing}
								bind:value={schoolEmail}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="student-phone" class="block text-xs font-semibold text-gray-700 mb-1.5">Contact number</label>
							<input
								id="student-phone"
								type="text"
								disabled={!isEditing}
								bind:value={contactNumber}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div class="sm:col-span-2">
							<label for="student-address" class="block text-xs font-semibold text-gray-700 mb-1.5">Address</label>
							<input
								id="student-address"
								type="text"
								disabled={!isEditing}
								bind:value={address}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>
					</div>
				</div>

				<!-- Emergency / Responsible Person Card -->
				<div class="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-xs">
					<div class="flex items-center justify-between mb-4">
						<p class="text-[10px] font-bold tracking-[0.15em] text-gray-400 uppercase">
							USED WHEN ASSISTANCE IS NEEDED
						</p>
						<svg class="w-4 h-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"></path>
						</svg>
					</div>

					<h3 class="text-lg font-bold text-gray-800 mb-6">Emergency / Responsible Person</h3>

					<div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
						<div>
							<label for="emergency-person" class="block text-xs font-semibold text-gray-700 mb-1.5">Person</label>
							<input
								id="emergency-person"
								type="text"
								disabled={!isEditing}
								bind:value={emergencyPerson}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="emergency-rel" class="block text-xs font-semibold text-gray-700 mb-1.5">Relationship</label>
							<input
								id="emergency-rel"
								type="text"
								disabled={!isEditing}
								bind:value={emergencyRelationship}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="emergency-phone" class="block text-xs font-semibold text-gray-700 mb-1.5">Contact number</label>
							<input
								id="emergency-phone"
								type="text"
								disabled={!isEditing}
								bind:value={emergencyContact}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>

						<div>
							<label for="emergency-method" class="block text-xs font-semibold text-gray-700 mb-1.5">Preferred contact method</label>
							<input
								id="emergency-method"
								type="text"
								disabled={!isEditing}
								bind:value={preferredContactMethod}
								class="w-full px-3.5 py-2.5 rounded-xl border border-gray-200 text-sm {isEditing ? 'bg-white focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f]' : 'bg-gray-50/70 text-gray-700'}"
							/>
						</div>
					</div>

					<div class="mt-6 bg-[#edf7f0] border border-[#1b522f]/10 rounded-2xl p-4 flex items-start space-x-3.5">
						<div class="w-6 h-6 rounded-lg bg-[#1b522f] text-white flex items-center justify-center shrink-0 mt-0.5">
							<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
							</svg>
						</div>
						<div>
							<h4 class="text-xs font-bold text-[#1b522f]">Automatically available during clinic emergencies</h4>
							<p class="text-[11px] text-[#1b522f]/80 mt-0.5">
								You won't need to enter this information again during a visit.
							</p>
						</div>
					</div>
				</div>

			</div>
		</div>
	</div>
{/if}
