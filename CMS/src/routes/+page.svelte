<script lang="ts">
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import { loginWithApi, checkBackendHealth } from '#lib/api';
	import { onMount } from 'svelte';

	let studentIdInput = $state('');
	let passwordInput = $state('');
	let showPassword = $state(false);
	let errorMessage = $state('');
	let isSubmitting = $state(false);
	let backendOnline = $state<boolean | null>(null);

	onMount(async () => {
		const health = await checkBackendHealth();
		backendOnline = health !== null;
	});

	async function handleSignIn(e: SubmitEvent) {
		e.preventDefault();
		if (!studentIdInput.trim()) {
			errorMessage = 'Please enter your Student ID or Email.';
			return;
		}

		if (!passwordInput.trim()) {
			errorMessage = 'Please enter your password.';
			return;
		}

		isSubmitting = true;
		errorMessage = '';

		try {
			// Attempt login via FastAPI backend with SQLite
			const authRes = await loginWithApi(studentIdInput.trim(), passwordInput);
			clinicStore.setCurrentUser(authRes.user);
			goto('/dashboard');
		} catch (err: any) {
			if (err?.message && (err.message.includes('Failed to fetch') || err.message.includes('NetworkError'))) {
				errorMessage = 'Cannot connect to authentication service. Please ensure the backend server is running.';
			} else {
				errorMessage = err?.message || 'Failed to sign in. Please check your credentials.';
			}
		} finally {
			isSubmitting = false;
		}
	}
</script>

<svelte:head>
	<title>Sign in to CSHMS - CELTECH School Clinic</title>
</svelte:head>

<div class="w-full min-h-screen flex flex-col lg:flex-row bg-white">
	
	<!-- ================= LEFT COLUMN: HERO (DARK GREEN #1b522f) ================= -->
	<div class="w-full lg:w-1/2 bg-[#1b522f] relative text-white p-10 sm:p-14 lg:p-16 xl:p-20 flex flex-col justify-between overflow-hidden min-h-[600px] lg:min-h-screen">
		<!-- Background Watermark Graphics -->
		<div class="absolute inset-0 pointer-events-none opacity-10 flex items-center justify-center">
			<!-- Subtle concentric arcs -->
			<div class="absolute w-[800px] h-[800px] border border-white rounded-full -top-[10%] -left-[20%]"></div>
			<div class="absolute w-[600px] h-[600px] border border-white rounded-full top-[15%] left-[5%]"></div>
			
			<!-- Giant Heartbeat Icon Watermark in bottom right -->
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

		<!-- Middle: Hero Statement -->
		<div class="relative z-10 my-16 lg:my-auto max-w-lg">
			<p class="text-[10px] sm:text-xs font-bold tracking-[0.2em] text-[#8fd3a2] uppercase mb-4">
				ADVANCING STUDENT HEALTH SERVICES
			</p>
			<h2 class="text-4xl sm:text-5xl xl:text-6xl font-normal tracking-tight leading-tight text-white mb-6">
				Responsive care.<br />Reliable services.
			</h2>
			<p class="text-white/80 text-sm sm:text-base leading-relaxed max-w-md">
				A centralized platform designed to support efficient and organized healthcare services at CELTECH College.
			</p>
		</div>

		<!-- Bottom: Feature Pill Card -->
		<div class="relative z-10">
			<div class="bg-white/10 backdrop-blur-xs border border-white/15 rounded-2xl p-4 sm:p-5 flex items-center space-x-3.5 max-w-md shadow-xs">
				<div class="w-5 h-5 rounded-full bg-white/20 flex items-center justify-center shrink-0">
					<svg class="w-3.5 h-3.5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2.5" d="M5 13l4 4L19 7"></path>
					</svg>
				</div>
				<p class="text-xs sm:text-sm font-medium text-white/90 leading-snug">
					Accessible care. Organized records. Connected services.
				</p>
			</div>
		</div>
	</div>

	<!-- ================= RIGHT COLUMN: SIGN IN FORM (WHITE) ================= -->
	<div class="w-full lg:w-1/2 bg-white p-8 sm:p-14 lg:p-16 xl:p-20 flex flex-col justify-center items-center relative min-h-screen">
		<div class="w-full max-w-lg space-y-6">
			
			<!-- Headers -->
			<div>
				<div class="flex items-center justify-between mb-1.5">
					<p class="text-[10px] font-bold tracking-[0.15em] text-[#1b522f] uppercase">
						WELCOME BACK
					</p>
					{#if backendOnline === true}
						<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200 shadow-2xs">
							<span class="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
							SQLite Auth Online
						</span>
					{:else if backendOnline === false}
						<span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200" title="Start backend with npm run backend:dev">
							<span class="w-1.5 h-1.5 rounded-full bg-amber-400"></span>
							Demo Mode
						</span>
					{/if}
				</div>
				<h3 class="text-3xl sm:text-4xl font-normal text-gray-900 tracking-tight">
					Sign in to CSHMS
				</h3>
				<p class="text-sm text-gray-500 mt-1.5">
					Use your CELTECH Student ID to access your health services.
				</p>
			</div>

			{#if errorMessage}
				{#if errorMessage.toLowerCase().includes('pending')}
					<div class="p-4 bg-amber-50 border border-amber-200 text-amber-900 text-xs rounded-2xl flex items-start space-x-3 shadow-2xs">
						<svg class="w-5 h-5 text-amber-600 shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
						</svg>
						<div class="space-y-1">
							<p class="font-bold text-amber-900">Account Pending Administrator Approval</p>
							<p class="text-amber-800 leading-relaxed">{errorMessage}</p>
						</div>
					</div>
				{:else}
					<div class="p-3 bg-red-50 border border-red-200 text-red-700 text-xs rounded-xl flex items-center space-x-2">
						<svg class="w-4 h-4 text-red-500 shrink-0" fill="currentColor" viewBox="0 0 20 20">
							<path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd"></path>
						</svg>
						<span>{errorMessage}</span>
					</div>
				{/if}
			{/if}

			<!-- Form -->
			<form class="space-y-4 pt-1" onsubmit={handleSignIn}>
				
				<!-- Student ID Field -->
				<div>
					<label for="student-id-input" class="block text-xs font-semibold text-gray-700 mb-1.5">Student ID</label>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
							<svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"></path>
							</svg>
						</div>
						<input
							id="student-id-input"
							type="text"
							bind:value={studentIdInput}
							placeholder="Enter your Student ID"
							class="w-full pl-11 pr-4 py-3.5 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
						/>
					</div>
				</div>

				<!-- Password Field -->
				<div>
					<div class="flex justify-between items-center mb-1.5">
						<label for="password-input" class="block text-xs font-semibold text-gray-700">Password</label>
						<a href="#forgot" class="text-xs font-semibold text-[#1b522f] hover:underline">Forgot password?</a>
					</div>
					<div class="relative">
						<div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
							<svg class="h-4 w-4 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
								<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
							</svg>
						</div>
						<input
							id="password-input"
							type={showPassword ? 'text' : 'password'}
							bind:value={passwordInput}
							placeholder="Enter your password"
							class="w-full pl-11 pr-11 py-3.5 bg-white border border-gray-200/90 rounded-2xl text-xs sm:text-sm text-gray-800 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-[#1b522f]/20 focus:border-[#1b522f] shadow-2xs transition-colors"
						/>
						<button
							type="button"
							onclick={() => (showPassword = !showPassword)}
							class="absolute inset-y-0 right-0 pr-4 flex items-center text-gray-400 hover:text-gray-600 cursor-pointer"
							aria-label={showPassword ? 'Hide password' : 'Show password'}
						>
							{#if showPassword}
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"></path>
								</svg>
							{:else}
								<svg class="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
									<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
								</svg>
							{/if}
						</button>
					</div>
				</div>

				<!-- Submit Button (Sign in >) -->
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
						<span>Signing in...</span>
					{:else}
						<span>Sign in</span>
						<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
						</svg>
					{/if}
				</button>

				<!-- Register Link -->
				<div class="text-center pt-2">
					<p class="text-xs text-gray-500">
						Don't have an account?
						<a href="/register" class="font-semibold text-[#1b522f] hover:underline ml-1">Create an account</a>
					</p>
				</div>
			</form>

			<!-- Security Footer Note -->
			<div class="pt-6 text-center space-y-2">
				<div class="flex items-center justify-center space-x-1.5 text-gray-400 select-none text-[11px]">
					<svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.75" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path>
					</svg>
					<span>Your health information is private and protected.</span>
				</div>
				<div class="text-[11px] text-gray-400">
					By using this system, you agree to the
					<a href="/terms" class="font-semibold text-[#1b522f] hover:underline ml-0.5">Terms and Conditions</a>
				</div>
			</div>

		</div>
	</div>

</div>
