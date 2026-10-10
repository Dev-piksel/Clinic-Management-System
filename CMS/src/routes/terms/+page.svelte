<script lang="ts">
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';

	function handleBack() {
		if (clinicStore.isLoggedIn) {
			goto('/dashboard');
		} else {
			goto('/');
		}
	}
</script>

<svelte:head>
	<title>Terms and Conditions & Privacy Policy - CSHMS CELTECH</title>
</svelte:head>

<div class="min-h-screen bg-[#f8faf8] text-gray-800 antialiased selection:bg-[#1b522f]/10 selection:text-[#1b522f]">
	<!-- Top Navigation Header -->
	<header class="bg-white border-b border-gray-100 sticky top-0 z-20 shadow-2xs">
		<div class="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
			<div class="flex items-center space-x-3">
				<button
					type="button"
					onclick={handleBack}
					class="w-9 h-9 rounded-xl bg-gray-50 hover:bg-gray-100 text-gray-600 flex items-center justify-center cursor-pointer transition-colors"
					aria-label="Go back"
				>
					<svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
						<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
					</svg>
				</button>
				<div class="flex items-center space-x-2.5">
					<div class="w-8 h-8 bg-[#52ad69] rounded-xl flex items-center justify-center text-white shadow-2xs">
						<svg class="w-4 h-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
							<path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
							<polyline points="7 12 9 12 11 16 14 8 16 12 18 12"></polyline>
						</svg>
					</div>
					<div>
						<h1 class="font-bold text-sm text-[#1b522f] leading-none">CSHMS</h1>
						<p class="text-[10px] text-gray-400 font-medium mt-0.5">CELTECH School Clinic</p>
					</div>
				</div>
			</div>

			<div class="flex items-center space-x-2 text-xs">
				<a
					href="/register"
					class="px-3.5 py-1.5 rounded-xl border border-[#1b522f] text-[#1b522f] hover:bg-[#1b522f]/5 font-semibold transition-colors"
				>
					Register
				</a>
				<a
					href="/"
					class="px-3.5 py-1.5 rounded-xl bg-[#1b522f] text-white hover:bg-[#154225] font-semibold transition-colors shadow-2xs"
				>
					Sign In
				</a>
			</div>
		</div>
	</header>

	<!-- Main Content Container -->
	<main class="max-w-4xl mx-auto px-6 py-10 space-y-8">
		<!-- Hero Banner -->
		<div class="bg-gradient-to-br from-[#1b522f] to-[#123820] text-white rounded-3xl p-8 sm:p-10 shadow-sm relative overflow-hidden">
			<div class="absolute -right-12 -bottom-12 opacity-10 pointer-events-none">
				<svg class="w-72 h-72" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
					<path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
				</svg>
			</div>

			<div class="relative z-10 max-w-2xl">
				<span class="inline-block px-3 py-1 bg-white/15 backdrop-blur-xs text-[#8fd3a2] text-[11px] font-bold rounded-lg tracking-wider uppercase mb-3">
					LEGAL & DATA PRIVACY
				</span>
				<h2 class="text-3xl sm:text-4xl font-normal tracking-tight text-white mb-3">
					Terms and Conditions & Privacy Policy
				</h2>
				<p class="text-white/80 text-sm leading-relaxed">
					Governing use of the CELTECH School Clinic Health Management System (CSHMS), student health records handling, and emergency protocol notifications.
				</p>

				<div class="mt-6 flex flex-wrap gap-4 text-xs text-white/90 pt-2 border-t border-white/10">
					<div class="flex items-center space-x-2">
						<span class="w-2 h-2 rounded-full bg-[#52ad69]"></span>
						<span>Compliant with RA 10173 (Data Privacy Act of 2012)</span>
					</div>
					<div class="flex items-center space-x-2">
						<span class="w-2 h-2 rounded-full bg-[#52ad69]"></span>
						<span>Academic Year 2026–2027</span>
					</div>
				</div>
			</div>
		</div>

		<!-- Document Card Body -->
		<div class="bg-white rounded-3xl p-8 sm:p-10 border border-gray-100 shadow-xs space-y-8 leading-relaxed text-sm text-gray-600">

			<!-- Section 1 -->
			<section class="space-y-3 pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">1</span>
					<h3 class="text-lg font-bold text-gray-900">Acceptance of Terms and Eligibility</h3>
				</div>
				<p>
					By registering for, accessing, or utilizing the CELTECH School Clinic Health Management System (CSHMS), you affirm that you are an actively enrolled student, faculty member, or authorized clinic staff member of CELTECH College. If you do not agree with any of these terms, you must refrain from registering or using the online portal and seek direct offline consultation with the clinic office.
				</p>
			</section>

			<!-- Section 2 -->
			<section class="space-y-3 pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">2</span>
					<h3 class="text-lg font-bold text-gray-900">Compliance with Philippine Data Privacy Act (RA 10173)</h3>
				</div>
				<p>
					In full adherence to Republic Act No. 10173 (Data Privacy Act of 2012) of the Republic of the Philippines and relevant Department of Health (DOH) clinical record directives:
				</p>
				<ul class="list-disc pl-6 space-y-2 text-xs sm:text-sm text-gray-600">
					<li>
						<strong>Sensitive Personal Health Information:</strong> All clinical consultations, vital sign assessments, medication dispensed, first-aid reports, and medical histories recorded on this portal are strictly confidential.
					</li>
					<li>
						<strong>Access Limitation:</strong> Only registered school nurses, medical directors, and authorized emergency first-responders possess authorized clearance to inspect your diagnostic records.
					</li>
					<li>
						<strong>Data Encryption & Storage:</strong> Account passwords are encrypted using high-security bcrypt hashing and all records are safeguarded within secured institutional infrastructure.
					</li>
				</ul>
			</section>

			<!-- Section 3 -->
			<section class="space-y-3 pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">3</span>
					<h3 class="text-lg font-bold text-gray-900">Emergency Contact Designation and Protocol</h3>
				</div>
				<p>
					Every student registering for CSHMS is required to provide accurate, up-to-date emergency contact details (including primary guardian name, relationship, and active telephone/mobile number).
				</p>
				<div class="p-4 bg-[#f8faf9] rounded-2xl border border-gray-100 text-xs text-gray-600 space-y-1.5">
					<p class="font-semibold text-gray-800">By submitting this information, you explicitly authorize:</p>
					<p>• The school clinic staff to place urgent phone calls or SMS messages to your emergency contact during physical injury, loss of consciousness, fainting, or acute medical illness.</p>
					<p>• The school clinic to coordinate with emergency medical services (EMS) or tertiary medical centers should hospital transfer be recommended.</p>
				</div>
			</section>

			<!-- Section 4 -->
			<section class="space-y-3 pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">4</span>
					<h3 class="text-lg font-bold text-gray-900">Administrator Approval and Verification Gate</h3>
				</div>
				<p>
					To safeguard student privacy and prevent unauthorized access or impersonation:
				</p>
				<ul class="list-disc pl-6 space-y-2 text-xs sm:text-sm text-gray-600">
					<li>
						<strong>Pending Review State:</strong> All newly registered accounts are initially assigned a <span class="font-semibold text-amber-700">"Pending Approval"</span> status.
					</li>
					<li>
						<strong>Verification Criteria:</strong> Clinic administrators verify that the Student ID, full name, and academic program correspond with current institutional records before granting portal access.
					</li>
					<li>
						<strong>Rejection Policy:</strong> Any account created with false credentials, duplicate registrations, or fraudulent identities will be rejected and subject to administrative sanction.
					</li>
				</ul>
			</section>

			<!-- Section 5 -->
			<section class="space-y-3 pb-6 border-b border-gray-100">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">5</span>
					<h3 class="text-lg font-bold text-gray-900">Student and Patient Responsibilities</h3>
				</div>
				<p>
					As a user of the CSHMS portal, you agree to:
				</p>
				<ul class="list-disc pl-6 space-y-2 text-xs sm:text-sm text-gray-600">
					<li>Maintain the strict confidentiality of your authentication credentials and notify clinic administration immediately if you suspect unauthorized account access.</li>
					<li>Keep your medical conditions, drug allergies, contact numbers, and residential address updated via your student profile.</li>
					<li>Arrive promptly for scheduled consultations or cancel appointments in advance so other students may utilize clinic queue slots.</li>
				</ul>
			</section>

			<!-- Section 6 -->
			<section class="space-y-3">
				<div class="flex items-center space-x-3">
					<span class="w-7 h-7 rounded-lg bg-[#edf7f0] text-[#1b522f] text-xs font-bold flex items-center justify-center">6</span>
					<h3 class="text-lg font-bold text-gray-900">Modifications to Policy and Contact Information</h3>
				</div>
				<p>
					CELTECH College reserves the right to amend these Terms and Conditions in accordance with updated health guidelines or national statutory updates. Continued usage of the portal following published amendments signifies acceptance of the revised policies.
				</p>
				<div class="mt-4 p-4 bg-[#edf7f0] rounded-2xl border border-[#1b522f]/10 text-xs text-gray-700">
					<p class="font-bold text-[#1b522f]">CELTECH College School Clinic Office</p>
					<p class="text-gray-600 mt-0.5">Health Services Unit · Clinic Building Ground Floor · Bataan, Philippines</p>
					<p class="text-gray-500 mt-1">Direct inquiries to: <span class="font-medium text-gray-800">clinic@celtech.edu.ph</span></p>
				</div>
			</section>

		</div>

		<!-- Bottom Action Card -->
		<div class="flex items-center justify-between p-6 bg-white rounded-3xl border border-gray-100 shadow-2xs">
			<p class="text-xs text-gray-500">
				Ready to create your account or access the portal?
			</p>
			<div class="flex items-center space-x-3">
				<a
					href="/register"
					class="px-5 py-2.5 rounded-xl bg-[#1b522f] hover:bg-[#154225] text-white text-xs font-semibold shadow-xs transition-colors"
				>
					Proceed to Registration
				</a>
			</div>
		</div>
	</main>
</div>
