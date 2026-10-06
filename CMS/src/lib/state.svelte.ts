import type { DemoAccount, Appointment, ClinicVisit, NotificationItem, FirstAidReport, QueueItem } from './types';

export const demoAccounts: DemoAccount[] = [
	{
		id: 'faith-manada',
		name: 'Faith Manada',
		firstName: 'Faith',
		role: 'Student',
		category: 'student',
		isCrrmuMember: false,
		initials: 'FM',
		studentId: '202611399',
		programStrand: 'BSIT',
		yearSection: '4A',
		email: 'faithmanada@gmail.com',
		contactNumber: '09XX XXX XXXX',
		address: 'Bataan, Philippines',
		avatarBg: '#8fd3a2',
		avatarColor: '#1b522f',
		emergencyPerson: 'Parent / Guardian',
		emergencyRelationship: 'Parent',
		emergencyContact: '09XX XXX XXXX',
		preferredContactMethod: 'Phone call'
	},
	{
		id: 'vergel-suniga',
		name: 'Vergel Suniga Jr.',
		firstName: 'Vergel',
		role: 'Student - CRRMU Member',
		category: 'student',
		isCrrmuMember: true,
		initials: 'VS',
		studentId: '202211542',
		programStrand: 'BSCRIM',
		yearSection: '4C',
		email: 'vergelsuniga@gmail.com',
		contactNumber: '09XX XXX XXXX',
		address: 'Zambales, Philippines',
		avatarBg: '#dcfce7',
		avatarColor: '#1b522f',
		emergencyPerson: 'Parent / Guardian',
		emergencyRelationship: 'Parent',
		emergencyContact: '09XX XXX XXXX',
		preferredContactMethod: 'Phone call'
	},
	{
		id: 'alma-lontoc',
		name: 'Alma A. Lontoc',
		firstName: 'Alma',
		role: 'Head Nurse',
		category: 'staff',
		isCrrmuMember: false,
		initials: 'AL',
		studentId: 'CN-1002',
		programStrand: 'School Clinic Admin',
		yearSection: 'Healthcare Services',
		email: 'alma.lontoc@celtech.edu.ph',
		contactNumber: '09XX XXX XXXX',
		address: 'Bataan, Philippines',
		avatarBg: '#dcfce7',
		avatarColor: '#1b522f',
		emergencyPerson: 'Roberto Lontoc',
		emergencyRelationship: 'Spouse',
		emergencyContact: '09XX XXX XXXX',
		preferredContactMethod: 'SMS'
	},
	{
		id: 'elijah-delos-santos',
		name: 'Elijah Rheisan M. Delos Santos',
		firstName: 'Elijah',
		role: 'Assistant Nurse',
		category: 'staff',
		isCrrmuMember: false,
		initials: 'ED',
		studentId: 'CN-1005',
		programStrand: 'School Clinic Operations',
		yearSection: 'Healthcare Services',
		email: 'elijah.delossantos@celtech.edu.ph',
		contactNumber: '09XX XXX XXXX',
		address: 'Bataan, Philippines',
		avatarBg: '#dcfce7',
		avatarColor: '#1b522f',
		emergencyPerson: 'Maria Delos Santos',
		emergencyRelationship: 'Mother',
		emergencyContact: '09XX XXX XXXX',
		preferredContactMethod: 'Phone call'
	}
];

export const initialAppointments: Appointment[] = [
	{
		id: 'app-staff-1',
		type: 'Walk-in',
		title: 'Minor Injury Walk-in',
		date: '2026-10-04',
		day: '04',
		month: 'OCT',
		time: '8:30 AM',
		location: 'School Clinic',
		reason: 'Minor Injury',
		status: 'Waiting',
		studentName: 'Rovic De Guia',
		studentId: '202511854',
		studentInitials: 'RD'
	},
	{
		id: 'app-staff-2',
		type: 'General Consultation',
		title: 'Follow-up General Consultation',
		date: '2026-10-04',
		day: '04',
		month: 'OCT',
		time: '10:30 AM',
		location: 'School Clinic',
		reason: 'Follow-up',
		status: 'Confirmed',
		studentName: 'Faith Manada',
		studentId: '202611399',
		studentInitials: 'FM'
	},
	{
		id: 'app-staff-3',
		type: 'Medical Concern',
		title: 'Dizziness Medical Concern',
		date: '2026-10-04',
		day: '04',
		month: 'OCT',
		time: '1:00 PM',
		location: 'School Clinic',
		reason: 'Dizziness',
		status: 'Pending',
		studentName: 'Vergel Suniga Jr.',
		studentId: '202211542',
		studentInitials: 'VS'
	}
];

export const initialVisits: ClinicVisit[] = [
	{
		id: 'visit-1',
		date: '04',
		monthYear: 'OCT 2026',
		title: 'Headache',
		type: 'consultation',
		time: '10:24 AM',
		assessment: 'Mild',
		intervention: 'Rest + Hydration',
		disposition: 'Returned to Class',
		clinicNote: 'Rest for 20 minutes and continue hydration.',
		status: 'Completed'
	},
	{
		id: 'visit-2',
		date: '18',
		monthYear: 'SEP 2026',
		title: 'Minor injury',
		type: 'first-aid',
		time: '1:15 PM',
		assessment: 'Superficial cut',
		intervention: 'Wound cleaning',
		disposition: 'Returned to Class',
		clinicNote: 'Cleaned with saline and antiseptic dressing applied.',
		status: 'Completed'
	},
	{
		id: 'visit-3',
		date: '02',
		monthYear: 'SEP 2026',
		title: 'Health checkup',
		type: 'consultation',
		time: '09:00 AM',
		assessment: 'Normal vitals',
		intervention: 'Vitals assessment',
		disposition: 'Returned to Class',
		status: 'Completed'
	}
];

export const initialNotifications: NotificationItem[] = [
	{
		id: 'notif-1',
		title: 'Appointment confirmed',
		message: 'Your General Consultation on October 8 at 10:30 AM is confirmed.',
		time: '12 minutes ago',
		type: 'confirmation',
		read: false,
		actionText: 'View appointment',
		actionHref: '/appointments',
		category: 'appointment'
	},
	{
		id: 'notif-2',
		title: 'Clinic follow-up',
		message: 'Remember to stay hydrated and visit the clinic if your headache returns.',
		time: 'Yesterday',
		type: 'reminder',
		read: false,
		actionText: 'View clinic visit',
		actionHref: '/clinic-visits',
		category: 'visit'
	},
	{
		id: 'notif-3',
		title: 'Appointment reminder',
		message: 'Your clinic appointment is tomorrow at 10:30 AM.',
		time: 'October 7',
		type: 'reminder',
		read: true,
		actionText: 'View details',
		actionHref: '/appointments',
		category: 'appointment'
	},
	{
		id: 'notif-4',
		title: 'Clinic message',
		message: 'The school clinic is available Monday to Saturday, 8:00 AM to 5:00 PM.',
		time: 'October 1',
		type: 'announcement',
		read: true,
		category: 'message'
	}
];

export const initialFirstAidReports: FirstAidReport[] = [
	{
		id: 'far-1',
		date: '05 OCT 2026',
		time: '02:15 PM',
		patientName: 'Faith Manada',
		patientRole: 'Student - BSIT 4A',
		location: 'Corridor 3rd Floor',
		incidentType: 'Minor Injury',
		treatment: 'Wound Cleaning and cold compress applied.',
		responder: 'Vergel Suniga Jr.',
		status: 'Reviewed'
	}
];

export const initialQueueItems: QueueItem[] = [
	{
		id: 'q-01',
		queueNumber: '01',
		studentName: 'Faith Manada',
		studentId: '202611399',
		studentInitials: 'FM',
		complaint: 'Headache',
		timeInClinic: '8 min in clinic',
		status: 'Waiting',
		actionText: 'Start visit'
	},
	{
		id: 'q-02',
		queueNumber: '02',
		studentName: 'Rovic De Guia',
		studentId: '202511854',
		studentInitials: 'RD',
		complaint: 'Minor injury',
		timeInClinic: '14 min in clinic',
		status: 'In Consultation',
		actionText: 'Open visit'
	},
	{
		id: 'q-03',
		queueNumber: '03',
		studentName: 'Vergel Suniga Jr.',
		studentId: '202211542',
		studentInitials: 'VS',
		complaint: 'Dizziness',
		timeInClinic: '22 min in clinic',
		status: 'Under Observation',
		actionText: 'Open visit'
	}
];

// App global reactive state store using Svelte 5 runes
class ClinicStore {
	currentUser = $state<DemoAccount>(demoAccounts[0]);
	selectedAccountId = $state<string>('faith-manada');
	isLoggedIn = $state<boolean>(true);
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
		return this.crrmuReportApproved ? 0 : 1;
	}

	approvePendingCrrmuReport() {
		this.crrmuReportApproved = true;
		this.visits = [
			{
				id: `visit-crrmu-${Date.now()}`,
				date: '06',
				monthYear: 'OCT 2026',
				title: 'Minor injury',
				type: 'first-aid',
				time: '10:42 AM',
				assessment: 'Superficial cut · Responder: Vergel Suniga Jr.',
				intervention: 'Wound cleaning + Bandaging',
				disposition: 'Returned to Class',
				clinicNote: 'Student was assisted to the clinic after first aid.',
				status: 'Completed'
			},
			...this.visits
		];
		this.notifications = [
			{
				id: `notif-${Date.now()}`,
				title: 'CRRMU report approved',
				message: 'Report for Faith Manada has been added to official clinic record.',
				time: 'Just now',
				type: 'confirmation',
				read: false,
				actionText: 'View timeline',
				actionHref: '/medical-records',
				category: 'visit'
			},
			...this.notifications
		];
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

	logout() {
		this.isLoggedIn = false;
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
				message: `Your appointment for ${app.title} on ${app.month} ${app.day} at ${app.time} is confirmed.`,
				time: 'Just now',
				type: 'confirmation',
				read: false,
				actionText: 'View appointment',
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
		const idx = demoAccounts.findIndex((a) => a.id === this.currentUser.id);
		if (idx !== -1) {
			demoAccounts[idx] = { ...this.currentUser };
		}
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
