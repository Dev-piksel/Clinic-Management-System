<script lang="ts">
	import './layout.css';
	import '../app.css';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { clinicStore } from '#lib/state.svelte';
	import { fetchCurrentUser, getStoredToken } from '#lib/api';
	import Sidebar from '#lib/components/Sidebar.svelte';
	import TopHeader from '#lib/components/TopHeader.svelte';
	import type { LayoutProps } from './$types';
	import { onMount } from 'svelte';

	let { children }: LayoutProps = $props();

	// Check if on public auth page
	let isAuthPage = $derived(
		page.url.pathname === '/' ||
		page.url.pathname.startsWith('/sign-in') ||
		page.url.pathname.startsWith('/login') ||
		page.url.pathname.startsWith('/register') ||
		page.url.pathname.startsWith('/terms')
	);

	let isCheckingAuth = $state(true);

	onMount(async () => {
		const token = getStoredToken();
		if (token) {
			try {
				const user = await fetchCurrentUser();
				if (user) {
					clinicStore.setCurrentUser(user);
					if (page.url.pathname === '/' || page.url.pathname === '/login' || page.url.pathname === '/register') {
						goto('/dashboard');
					}
				} else {
					clinicStore.logout();
					if (!isAuthPage) {
						goto('/');
					}
				}
			} catch {
				clinicStore.logout();
				if (!isAuthPage) {
					goto('/');
				}
			}
		} else {
			clinicStore.logout();
			if (!isAuthPage) {
				goto('/');
			}
		}
		isCheckingAuth = false;
	});

	$effect(() => {
		if (!isCheckingAuth && !clinicStore.isLoggedIn && !isAuthPage) {
			goto('/');
		}
	});
</script>

<svelte:head>
	<title>CSHMS - CELTECH School Clinic</title>
</svelte:head>

{#if isAuthPage}
	<div class="min-h-screen w-full bg-white text-gray-800 antialiased selection:bg-[#1b522f]/10 selection:text-[#1b522f]">
		{@render children()}
	</div>
{:else}
	<!-- Fixed Layout: Sidebar on left (fixed), Header on top (fixed), Only Main scrolls -->
	<div class="h-screen w-screen overflow-hidden flex bg-[#f8faf8] text-gray-800 antialiased selection:bg-[#1b522f]/10 selection:text-[#1b522f]">
		<!-- Persistent Left Sidebar: fixed height, independent scroll if needed -->
		<Sidebar />

		<!-- Main Workspace Area -->
		<div class="flex-1 flex flex-col h-screen min-w-0 overflow-hidden">
			<!-- Persistent Top Header: always fixed at the top -->
			<TopHeader />
			
			<!-- Scrollable Main Container: ONLY this area scrolls when user scrolls the page -->
			<main class="flex-1 overflow-y-auto p-6 md:p-10 w-full">
				<div class="max-w-7xl mx-auto">
					{@render children()}
				</div>
			</main>
		</div>
	</div>
{/if}
