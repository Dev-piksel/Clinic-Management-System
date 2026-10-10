<script lang="ts">
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import { registerWithApi, checkBackendHealth, type RegisterPayload } from '#lib/api';
	import { onMount } from 'svelte';

	let studentId = $state('');
	let name = $state('');
	let email = $state('');
	let contactNumber = $state('');
	let role = $state<'Student' | 'Staff'>('Student');
	let programStrand = $state('BSIT');
	let yearSection = $state('1A');
	let isCrrmuMember = $state(false);
	let password = $state('');
	let confirmPassword = $state('');
	let showPassword = $state(false);

	// Emergency Contact Details
	let emergencyPerson = $state('');
	let emergencyRelationship = $state('Parent');
	let emergencyContact = $state('');
	let preferredContactMethod = $state('Phone call');

	// Terms and Conditions
	let agreedToTerms = $state(false);
	let showTermsModal = $state(false);

	let errorMessage = $state('');
	let isSubmitting = $state(false);
	let backendOnline = $state<boolean | null>(null);
	let registrationSuccess = $state(false);
	let registeredName = $state('');
	let registeredId = $state('');

	onMount(async () => {
		const health = await checkBackendHealth();
		backendOnline = health !== null;
	});

	async function handleRegister(e: SubmitEvent) {
		e.preventDefault();
		errorMessage = '';

		// Validations
		if (!studentId.trim()) {
			errorMessage = role === 'Student' ? 'Please enter your Student ID (numbers only).' : 'Please enter your Staff ID.';
			return;
		}

		if (role === 'Student' && !/^\d+$/.test(studentId.trim())) {
			errorMessage = 'Student ID must contain numbers only.';
			return;
		}

		if (!name.trim()) {
			errorMessage = 'Please enter your Full Name.';
			return;
		}

		if (!email.trim() || !email.includes('@')) {
			errorMessage = 'Please enter a valid email address.';
			return;
		}

		if (!emergencyPerson.trim()) {
			errorMessage = 'Please provide an Emergency Contact Person name.';
			return;
		}

		if (!emergencyContact.trim()) {
			errorMessage = 'Please provide an Emergency Contact Number.';
			return;
		}

		if (password.length < 6) {
			errorMessage = 'Password must be at least 6 characters.';
			return;
		}

		if (password !== confirmPassword) {
			errorMessage = 'Passwords do not match.';
			return;
		}

		if (!agreedToTerms) {
			errorMessage = 'You must agree to the Terms & Conditions and Privacy Policy.';
			return;
		}

		isSubmitting = true;

		const payload: RegisterPayload = {
			student_id: studentId.trim(),
			name: name.trim(),
			email: email.trim().toLowerCase(),
			password,
			role: role === 'Staff' ? 'Clinic Staff' : (isCrrmuMember ? 'Student - CRRMU Member' : 'Student'),
			category: role === 'Staff' ? 'staff' : 'student',
			is_crrmu_member: isCrrmuMember,
			program_strand: role === 'Staff' ? 'School Clinic Operations' : programStrand,
			year_section: role === 'Staff' ? 'Healthcare Services' : yearSection,
			contact_number: contactNumber.trim() || '09XX XXX XXXX',
			emergency_person: emergencyPerson.trim(),
			emergency_relationship: emergencyRelationship.trim(),
			emergency_contact: emergencyContact.trim(),
			preferred_contact_method: preferredContactMethod,
			terms_accepted: true
		};

		try {
			// Register via SQLite FastAPI backend
			const authRes = await registerWithApi(payload);
			registeredName = authRes.user.name;
			registeredId = authRes.user.studentId;
			registrationSuccess = true;
		} catch (err: any) {
			if (err?.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError'))) {
				errorMessage = 'Cannot connect to authentication service. Please ensure the backend is running.';
				return;
			}

			errorMessage = err.message || 'Registration failed. Please try again.';
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Create Account - CSHMS CELTECH School Clinic</title>
</svelte:head>

<div class="w-full min-h-screen flex flex-col lg:flex-row bg-white">

	<!-- ================= LEFT COLUMN: HERO (DARK GREEN #1b522f) ================= -->
	<div class="w-full lg:w-1/2 bg-[#1b522f] relative text-white p-10 sm:p-14 lg:p-16 xl:p-20 flex flex-col justify-between overflow-hidden min-h-[500px] lg:min-h-screen">
		<!-- Background Watermark Graphics -->
		<div class="absolute inset-0 pointer-events-none opacity-10 flex items-center justify-center">
			<div class="absolute w-[800px] h-[800px] border border-white rounded-full -top-[10%] -left-[20%]"></div>
			<div class="absolute w-[600px] h-[600px] border border-white rounded-full top-[15%] left-[5%]"></div>
			<svg class="absolute -bottom-16 -right-16 w-[450px] h-[450px]" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="0.75" stroke-linecap="round" stroke-linejoin="round">
				<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
				<polyline points="4 12 8 12 10 16 14 8 16 12 20 12"></polyline>
			</svg>
		</div>

		<!-- Top: Logo Area -->
		<div class="relative z-10 flex items-center space-x-3.5">
			<div class="w-12 h-12 bg-[#52ad69] rounded-2xl flex items-center justify-center shadow-xs">
				<svg class="w-7 h-7 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
					<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
					<polyline points="7 12 9 12 11 16 14 8 16 12 18 12"></polyline>
				</svg>
			</div>
			<div>
				<h1 class="font-bold text-xl leading-tight tracking-tight text-white">CSHMS</h1>
				<p class="text-white/70 text-xs font-medium">CELTECH School Clinic</p>
			</div>
		</div>

		<!-- Middle: Statement -->
		<div class="relative z-10 my-12 lg:my-auto max-w-lg">
			<p class="text-[10px] sm:text-xs font-bold tracking-[0.2em] text-[#8fd3a2] uppercase mb-4">
				JOIN THE CLINIC PORTAL
			</p>
			<h2 class="text-3xl sm:text-4xl xl:text-5xl font-normal tracking-tight leading-tight text-white mb-6">
				Create your health portal account.
			</h2>
			<p class="text-white/80 text-sm sm:text-base leading-relaxed max-w-md">
				Register your Student ID, record your emergency contacts, and submit your request for clinic verification.
			</p>

			<div class="mt-8 space-y-3 max-w-md">
				<div class="flex items-center space-x-3 text-xs text-white/90">
					<div class="w-5 h-5 rounded-full bg-[#52ad69] flex items-center justify-center text-white shrink-0">
						<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
					</div>
					<span>Emergency contact on file for campus incidents</span>
				</div>
				<div class="flex items-center space-x-3 text-xs text-white/90">
					<div class="w-5 h-5 rounded-full bg-[#52ad69] flex items-center justify-center text-white shrink-0">
						<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
						</svg>
					</div>
					<span>Administrator approval protects student medical privacy</span>
				</div>
			</div>
		</div>

		<!-- Bottom: Pill Card -->
		<div class="relative z-10">
			<div class="bg-white/10 backdrop-blur-xs border border-white/15 rounded-2xl p-4 sm:p-5 flex items-center space-x-3.5 max-w-md shadow-xs">
				<div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center shrink-0">
					<svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<p class="text-xs sm:text-sm font-medium text-white/90 leading-snug">
					Compliant with Philippine Data Privacy Act (RA 10173).
				</p>
			</div>
		</div>
	</div>

	<!-- ================= RIGHT COLUMN: REGISTER FORM (WHITE) ================= -->
	<div class="w-full lg:w-1/2 bg-white p-6 sm:p-10 lg:p-12 xl:p-16 flex flex-col justify-center items-center relative min-h-screen overflow-y-auto">
		<div class="w-full max-w-lg space-y-6 my-auto py-6">

			<!-- Headers -->
			<div>
				<div class="flex items-center justify-between mb-1.5">
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
						NEW ACCOUNT REGISTRATION
					</p>
					{#if backendOnline === true}
						<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-2xs">
							<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
							SQLite Auth Online
						</span>
					{:else if backendOnline === false}
						<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">
							<span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
							Offline Mode
						</span>
					{/if}
				</div>
				<h3 class="text-3xl sm:text-4xl font-normal text-gray-900 tracking-tight">
					Register for CSHMS
				</h3>
				<p class="text-sm text-gray-500 mt-1.5">
					Fill out your academic and emergency details. Administrator review is required before access.
				</p>
			</div>

			<!-- Success Card: Awaiting Administrator Approval -->
			{#if registrationSuccess}
				<div class="bg-[#edf7f0] border border-[#1b522f]/20 rounded-3xl p-6 sm:p-8 text-center space-y-4 shadow-sm animate-fade-in">
					<div class="w-16 h-16 bg-[#1b522f] text-white rounded-3xl mx-auto flex items-center justify-center shadow-md">
						<svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
						</svg>
					</div>

					<div>
						<span class="inline-block px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 border border-amber-200 mb-2">
							Pending Administrator Approval
						</span>
						<h4 class="text-xl font-bold text-gray-900">Registration Submitted!</h4>
						<p class="text-xs sm:text-sm text-gray-600 mt-2 leading-relaxed max-w-md mx-auto">
							Thank you, <strong>{registeredName}</strong> ({registeredId}). Your account has been saved. To protect school clinic privacy, an administrator or nurse will review and approve your account before you can sign in.
						</p>
					</div>

					<div class="p-3.5 bg-white rounded-2xl border border-gray-200/80 text-left text-xs text-gray-600 space-y-1">
						<p class="font-semibold text-gray-800 flex items-center gap-1.5">
							<svg class="w-4 h-4 text-[#1b522f]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
							</svg>
							What happens next?
						</p>
						<p>Clinic staff can approve your account from the <strong>User Approvals</strong> portal. Once approved, you can immediately log in with your credentials.</p>
					</div>

					<div class="pt-2">
						<a
							href="/"
							class="inline-flex items-center justify-center space-x-2 w-full py-3.5 px-6 rounded-2xl bg-[#1b522f] hover:bg-[#154225] text-white text-sm font-semibold transition-colors shadow-xs"
						>
							<span>Back to Sign In</span>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path>
							</svg>
						</a>
					</div>
				</div>
			{:else}

				<!-- Error Alert -->
				{#if errorMessage}
					<div class="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center space-x-2">
						<svg class="w-4 h-4 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
						</svg>
						<span>{errorMessage}</span>
					</div>
				{/if}

				<!-- Registration Form -->
				<form class="space-y-4 pt-1" onsubmit={handleRegister}>

					<!-- Role Selector Pills -->
					<div>
						<span class="block text-xs font-semibold text-gray-700 mb-1.5">Account Type</span>
						<div class="grid grid-cols-2 gap-2 bg-gray-100 p-1 rounded-2xl">
							<button
								type="button"
								onclick={() => (role = 'Student')}
								class="py-2 text-xs font-semibold rounded-xl transition-all {role === 'Student' ? 'bg-white text-[#1b522f] shadow-xs' : 'text-gray-500 hover:text-gray-800'}"
							>
								Student
							</button>
							<button
								type="button"
								onclick={() => (role = 'Staff')}
								class="py-2 text-xs font-semibold rounded-xl transition-all {role === 'Staff' ? 'bg-white text-[#1b522f] shadow-xs' : 'text-gray-500 hover:text-gray-800'}"
							>
								Clinic Staff
							</button>
						</div>
					</div>

					<!-- Section 1: Academic / Personal Info -->
					<div class="border-b border-gray-100 pb-4 space-y-3.5">
						<p class="text-[10px] font-bold tracking-wider text-gray-400 uppercase">1. Personal & School Info</p>

						<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
							<div>
								<label for="reg-id" class="block text-xs font-semibold text-gray-700 mb-1.5">
									{role === 'Student' ? 'Student ID (Numbers only)' : 'Staff ID'} *
								</label>
								<input
									id="reg-id"
									type="text"
									inputmode={role === 'Student' ? 'numeric' : 'text'}
									pattern={role === 'Student' ? '[0-9]*' : undefined}
									bind:value={studentId}
									oninput={(e) => {
										if (role === 'Student') {
											studentId = e.currentTarget.value.replace(/\D/g, '');
										}
									}}
									placeholder={role === 'Student' ? 'e.g. 202611888 (numbers only)' : 'e.g. CN-1009'}
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>

							<div>
								<label for="reg-name" class="block text-xs font-semibold text-gray-700 mb-1.5">Full Name *</label>
								<input
									id="reg-name"
									type="text"
									bind:value={name}
									placeholder="e.g. Maria Santos"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>
						</div>

						<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
							<div>
								<label for="reg-email" class="block text-xs font-semibold text-gray-700 mb-1.5">Email Address *</label>
								<input
									id="reg-email"
									type="email"
									bind:value={email}
									placeholder="name@celtech.edu.ph"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>

							<div>
								<label for="reg-phone" class="block text-xs font-semibold text-gray-700 mb-1.5">Contact Number</label>
								<input
									id="reg-phone"
									type="text"
									bind:value={contactNumber}
									placeholder="0917 123 4567"
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>
						</div>

						{#if role === 'Student'}
							<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
								<div>
									<label for="reg-prog" class="block text-xs font-semibold text-gray-700 mb-1.5">Program / Strand</label>
									<select
										id="reg-prog"
										bind:value={programStrand}
										class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
									>
										<option value="BSIT">BSIT - Information Tech</option>
										<option value="BSCRIM">BSCRIM - Criminology</option>
										<option value="BSBA">BSBA - Business Admin</option>
										<option value="BSED">BSED - Education</option>
										<option value="BSN">BSN - Nursing</option>
										<option value="SHS">SHS - Senior High</option>
									</select>
								</div>

								<div>
									<label for="reg-sec" class="block text-xs font-semibold text-gray-700 mb-1.5">Year & Section</label>
									<input
										id="reg-sec"
										type="text"
										bind:value={yearSection}
										placeholder="e.g. 1A, 2B, 3C"
										class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
									/>
								</div>
							</div>

							<div class="flex items-center space-x-2 pt-0.5">
								<input
									id="reg-crrmu"
									type="checkbox"
									bind:checked={isCrrmuMember}
									class="w-4 h-4 rounded text-[#1b522f] focus:ring-[#1b522f] border-gray-300"
								/>
								<label for="reg-crrmu" class="text-xs text-gray-600 select-none">
									I am an active CRRMU responder (Campus Red Cross & Rescue Medical Unit)
								</label>
							</div>
						{/if}
					</div>

					<!-- Section 2: EMERGENCY CONTACT (MANDATORY FOR CLINIC CARE) -->
					<div class="border-b border-gray-100 pb-4 space-y-3.5">
						<div class="flex items-center justify-between">
							<p class="text-[10px] font-bold tracking-wider text-emerald-800 uppercase flex items-center gap-1.5">
								<svg class="w-3.5 h-3.5 text-emerald-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
								</svg>
								2. Emergency Contact Information
							</p>
							<span class="text-[10px] text-gray-400 font-medium">Used in clinic emergencies</span>
						</div>

						<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
							<div>
								<label for="reg-em-person" class="block text-xs font-semibold text-gray-700 mb-1.5">Contact Person *</label>
								<input
									id="reg-em-person"
									type="text"
									bind:value={emergencyPerson}
									placeholder="e.g. Maria Teresa Santos"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>

							<div>
								<label for="reg-em-rel" class="block text-xs font-semibold text-gray-700 mb-1.5">Relationship *</label>
								<select
									id="reg-em-rel"
									bind:value={emergencyRelationship}
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								>
									<option value="Parent">Parent</option>
									<option value="Mother">Mother</option>
									<option value="Father">Father</option>
									<option value="Guardian">Guardian</option>
									<option value="Spouse">Spouse</option>
									<option value="Sibling">Sibling</option>
									<option value="Relative">Relative</option>
								</select>
							</div>
						</div>

						<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
							<div>
								<label for="reg-em-phone" class="block text-xs font-semibold text-gray-700 mb-1.5">Emergency Phone *</label>
								<input
									id="reg-em-phone"
									type="text"
									bind:value={emergencyContact}
									placeholder="e.g. 0918 765 4321"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>

							<div>
								<label for="reg-em-method" class="block text-xs font-semibold text-gray-700 mb-1.5">Preferred Method</label>
								<select
									id="reg-em-method"
									bind:value={preferredContactMethod}
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								>
									<option value="Phone call">Phone call</option>
									<option value="SMS">SMS / Text message</option>
								</select>
							</div>
						</div>
					</div>

					<!-- Section 3: Passwords -->
					<div class="space-y-3.5">
						<p class="text-[10px] font-bold tracking-wider text-gray-400 uppercase">3. Account Password</p>

						<div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
							<div>
								<label for="reg-password" class="block text-xs font-semibold text-gray-700 mb-1.5">Password *</label>
								<input
									id="reg-password"
									type={showPassword ? 'text' : 'password'}
									bind:value={password}
									placeholder="Min. 6 characters"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>

							<div>
								<label for="reg-confirm" class="block text-xs font-semibold text-gray-700 mb-1.5">Confirm Password *</label>
								<input
									id="reg-confirm"
									type={showPassword ? 'text' : 'password'}
									bind:value={confirmPassword}
									placeholder="Re-enter password"
									required
									class="w-full px-3.5 py-3 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
								/>
							</div>
						</div>

						<div class="flex items-center justify-between text-xs">
							<button
								type="button"
								onclick={() => (showPassword = !showPassword)}
								class="text-xs text-gray-500 hover:text-gray-800 flex items-center space-x-1 cursor-pointer"
							>
								<span>{showPassword ? 'Hide passwords' : 'Show passwords'}</span>
							</button>
						</div>
					</div>

					<!-- Section 4: TERMS AND CONDITIONS CHECKBOX -->
					<div class="p-4 bg-gray-50 rounded-2xl border border-gray-200/70 space-y-2">
						<div class="flex items-start space-x-3">
							<input
								id="terms-check"
								type="checkbox"
								bind:checked={agreedToTerms}
								class="w-4 h-4 mt-0.5 rounded text-[#1b522f] focus:ring-[#1b522f] border-gray-300 cursor-pointer shrink-0"
							/>
							<label for="terms-check" class="text-xs text-gray-700 leading-snug cursor-pointer select-none">
								I agree to the
								<button
									type="button"
									onclick={() => (showTermsModal = true)}
									class="font-semibold text-[#1b522f] underline hover:text-[#154225] cursor-pointer inline"
								>
									Terms and Conditions
								</button>
								and consent to the collection of my emergency contact and health records under the CELTECH Clinic Data Privacy Policy.
							</label>
						</div>
					</div>

					<!-- Submit Button -->
					<button
						type="submit"
						disabled={isSubmitting}
						class="w-full bg-[#1b522f] hover:bg-[#154225] disabled:opacity-75 disabled:cursor-not-allowed text-white font-medium py-3.5 sm:py-4 rounded-2xl text-sm flex justify-center items-center space-x-2 transition-all cursor-pointer shadow-xs active:scale-[0.99] pt-2"
					>
						{#if isSubmitting}
							<svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
								<circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
								<path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
							</svg>
							<span>Submitting for Approval...</span>
						{:else}
							<span>Submit Registration</span>
							<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
							</svg>
						{/if}
					</button>

					<!-- Sign in Link -->
					<div class="text-center pt-2">
						<p class="text-xs text-gray-500">
							Already have an approved account?
							<a href="/" class="font-semibold text-[#1b522f] hover:underline ml-1">Sign in here</a>
						</p>
					</div>
				</form>
			{/if}

			<!-- Footer Notes -->
			<div class="space-y-3 pt-2 text-center">
				<div class="flex items-center justify-center space-x-1.5 text-gray-400 select-none text-[11px]">
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
					</svg>
					<span>Secure SQLite encrypted authentication & administrator approval gate.</span>
				</div>
			</div>

		</div>
	</div>

</div>

<!-- ================= TERMS AND CONDITIONS MODAL ================= -->
{#if showTermsModal}
	<div class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs animate-fade-in">
		<div class="bg-white rounded-3xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden border border-gray-100">
			<!-- Modal Header -->
			<div class="p-6 border-b border-gray-100 flex items-center justify-between bg-[#edf7f0]">
				<div class="flex items-center space-x-3">
					<div class="w-10 h-10 rounded-2xl bg-[#1b522f] text-white flex items-center justify-center">
						<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
						</svg>
					</div>
					<div>
						<h3 class="text-lg font-bold text-gray-900">Terms and Conditions</h3>
						<p class="text-xs text-gray-600">CELTECH School Clinic Health Management System (CSHMS)</p>
					</div>
				</div>

				<button
					type="button"
					onclick={() => (showTermsModal = false)}
					class="w-8 h-8 rounded-full bg-white/80 hover:bg-white text-gray-500 hover:text-gray-800 flex items-center justify-center cursor-pointer transition-colors"
					aria-label="Close modal"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
					</svg>
				</button>
			</div>

			<!-- Modal Body (Scrollable Policy Content) -->
			<div class="p-6 overflow-y-auto space-y-4 text-xs text-gray-600 leading-relaxed">
				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-1">1. Acceptance of Terms</h4>
					<p>
						By creating an account on the CELTECH School Clinic Health Management System (CSHMS), you acknowledge and agree to comply with the terms, rules, and privacy policies set forth by CELTECH College.
					</p>
				</div>

				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-1">2. Medical Data Privacy (RA 10173)</h4>
					<p>
						In compliance with the Data Privacy Act of 2012 (Republic Act No. 10173), all personal health information, clinical consultations, first-aid reports, and medical histories recorded on this platform are confidential and shall only be accessed by authorized clinic personnel, head nurses, and designated emergency medical responders.
					</p>
				</div>

				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-1">3. Emergency Contact Authorization</h4>
					<p>
						You verify that the emergency contact information provided during registration is accurate and up to date. You explicitly authorize CELTECH clinic staff to contact your designated emergency contact person in the event of an urgent medical situation, campus injury, or hospital referral.
					</p>
				</div>

				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-1">4. Administrator Review & Verification</h4>
					<p>
						All newly registered accounts are subject to administrative review. Access to the web application is granted only after a school clinic administrator or nurse verifies your Student ID / Staff credentials. Fraudulent or impersonated accounts will be rejected and reported to student affairs.
					</p>
				</div>

				<div>
					<h4 class="font-bold text-sm text-gray-900 mb-1">5. Student Responsibilities</h4>
					<p>
						You are responsible for keeping your login credentials confidential. You agree to promptly update your contact numbers, address, and medical conditions if any changes occur during the academic year.
					</p>
				</div>
			</div>

			<!-- Modal Footer -->
			<div class="p-4 bg-gray-50 border-t border-gray-100 flex items-center justify-between">
				<span class="text-[11px] text-gray-500">Effective Date: Academic Year 2026–2027</span>
				<button
					type="button"
					onclick={() => { agreedToTerms = true; showTermsModal = false; }}
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold cursor-pointer transition-colors shadow-xs"
				>
					I Agree & Understand
				</button>
			</div>
		</div>
	</div>
{/if}
