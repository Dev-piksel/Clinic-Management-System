<script lang="ts">
	import './layout.css';
	import '../app.css';
	import { page } from '$app/state';
	import Sidebar from '#lib/components/Sidebar.svelte';
	import TopHeader from '#lib/components/TopHeader.svelte';
	import type { LayoutProps } from './$types';

	let { children }: LayoutProps = $props();

	// Check if on login/sign-in page
	let isAuthPage = $derived(
		page.url.pathname === '/' ||
		page.url.pathname.startsWith('/sign-in') ||
		page.url.pathname.startsWith('/login')
	);
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
