import type { DemoAccount, Appointment, ClinicVisit, NotificationItem, FirstAidReport, QueueItem } from './types';

export const defaultEmptyUser: DemoAccount = {
	id: '',
	name: '',
	firstName: '',
	role: 'Student',
	category: 'student',
	isCrrmuMember: false,
	initials: '',
	studentId: '',
	programStrand: '',
	yearSection: '',
	email: '',
	contactNumber: '',
	address: '',
	avatarBg: '#edf7f0',
	avatarColor: '#1b522f',
	emergencyPerson: '',
	emergencyRelationship: '',
	emergencyContact: '',
	preferredContactMethod: 'Phone call',
	status: 'pending'
};

// Zero preset / demo accounts
export const demoAccounts: DemoAccount[] = [];

export const initialAppointments: Appointment[] = [];
export const initialVisits: ClinicVisit[] = [];
export const initialNotifications: NotificationItem[] = [];
export const initialFirstAidReports: FirstAidReport[] = [];
export const initialQueueItems: QueueItem[] = [];

// App global reactive state store using Svelte 5 runes
class ClinicStore {
	currentUser = $state<DemoAccount>(defaultEmptyUser);
	selectedAccountId = $state<string>('');
	isLoggedIn = $state<boolean>(false);
	appointments = $state<Appointment[]>(initialAppointments);
	visits = $state<ClinicVisit[]>(initialVisits);
	notifications = $state<NotificationItem[]>(initialNotifications);
	firstAidReports = $state<FirstAidReport[]>(initialFirstAidReports);
	queue = $state<QueueItem[]>(initialQueueItems);
	activeNav = $state<string>('dashboard');

	crrmuReportApproved = $state<boolean>(false);

	// Unread notification count
	get unreadNotificationsCount(): number {
		return this.notifications.filter((n) => !n.read).length;
	}

	get pendingCrrmuCount(): number {
		return this.crrmuReportApproved ? 0 : 0;
	}

	pendingUsersCount = $state<number>(0);

	setPendingUsersCount(count: number) {
		this.pendingUsersCount = count;
	}

	approvePendingCrrmuReport() {
		this.crrmuReportApproved = true;
	}

	selectAccount(id: string) {
		this.selectedAccountId = id;
		const found = demoAccounts.find((a) => a.id === id);
		if (found) {
			this.currentUser = { ...found };
		}
	}

	login(id: string) {
		this.selectAccount(id);
		this.isLoggedIn = true;
	}

	setCurrentUser(user: DemoAccount) {
		this.currentUser = { ...user };
		this.selectedAccountId = user.id;
		this.isLoggedIn = true;
	}

	logout() {
		this.isLoggedIn = false;
		this.currentUser = { ...defaultEmptyUser };
		this.selectedAccountId = '';
		if (typeof window !== 'undefined') {
			localStorage.removeItem('cshms_token');
		}
	}

	addAppointment(app: Omit<Appointment, 'id' | 'status'>) {
		const newApp: Appointment = {
			...app,
			id: `app-${Date.now()}`,
			status: 'Confirmed'
		};
		this.appointments = [newApp, ...this.appointments];
		
		this.notifications = [
			{
				id: `notif-${Date.now()}`,
				title: 'Appointment booked',
				message: `Your ${app.title} on ${app.date} at ${app.time} is registered.`,
				time: 'Just now',
				type: 'confirmation',
				read: false,
				actionText: 'View appointments',
				actionHref: '/appointments',
				category: 'appointment'
			},
			...this.notifications
		];
	}

	updateProfile(updated: Partial<DemoAccount>) {
		this.currentUser = {
			...this.currentUser,
			...updated
		};
	}

	markAllNotificationsRead() {
		this.notifications = this.notifications.map((n) => ({ ...n, read: true }));
	}

	addFirstAidReport(report: Omit<FirstAidReport, 'id' | 'status'>) {
		const newReport: FirstAidReport = {
			...report,
			id: `far-${Date.now()}`,
			status: 'Submitted'
		};
		this.firstAidReports = [newReport, ...this.firstAidReports];
		
		this.notifications = [
			{
				id: `notif-${Date.now()}`,
				title: 'First aid report submitted',
				message: `Report for ${report.patientName} (${report.incidentType}) submitted to school clinic.`,
				time: 'Just now',
				type: 'confirmation',
				read: false,
				actionText: 'View details',
				actionHref: '/first-aid-reports',
				category: 'message'
			},
			...this.notifications
		];
	}

	advanceQueue(id: string) {
		this.queue = this.queue.map((q) => {
			if (q.id === id) {
				if (q.status === 'Waiting') return { ...q, status: 'In Consultation', actionText: 'Open visit' };
				if (q.status === 'In Consultation') return { ...q, status: 'Under Observation', actionText: 'Open visit' };
				return { ...q, status: 'Completed', actionText: 'Open' };
			}
			return q;
		});
	}

	addQueueItem(item: Omit<QueueItem, 'id' | 'queueNumber'>) {
		const qNum = (this.queue.length + 1).toString().padStart(2, '0');
		const newItem: QueueItem = {
			...item,
			id: `q-${Date.now()}`,
			queueNumber: qNum
		};
		this.queue = [...this.queue, newItem];
	}
}

export const clinicStore = new ClinicStore();
