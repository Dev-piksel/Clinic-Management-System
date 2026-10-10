export interface DemoAccount {
	id: string;
	name: string;
	firstName: string;
	role: string;
	category: 'student' | 'staff';
	isCrrmuMember?: boolean;
	initials: string;
	studentId: string;
	programStrand: string;
	yearSection: string;
	email: string;
	contactNumber: string;
	address: string;
	avatarBg: string;
	avatarColor: string;
	emergencyPerson: string;
	emergencyRelationship: string;
	emergencyContact: string;
	preferredContactMethod: string;
	status?: 'pending' | 'approved' | 'rejected';
	termsAccepted?: boolean;
	termsAcceptedAt?: string;
	createdAt?: string;
}

export interface FirstAidReport {
	id: string;
	date: string;
	time: string;
	patientName: string;
	patientRole: string;
	location: string;
	incidentType: string;
	treatment: string;
	responder: string;
	status: 'Submitted' | 'Reviewed';
}

export interface Appointment {
	id: string;
	type: string;
	title: string;
	date: string;
	day: string;
	month: string;
	time: string;
	location: string;
	reason: string;
	status: 'Confirmed' | 'Pending' | 'Completed' | 'Waiting';
	studentName?: string;
	studentId?: string;
	studentInitials?: string;
}

export interface ClinicVisit {
	id: string;
	date: string;
	monthYear: string;
	title: string;
	type: 'consultation' | 'first-aid' | 'walk-in';
	time: string;
	assessment: string;
	intervention: string;
	disposition: string;
	clinicNote?: string;
	status: 'Completed' | 'Follow-up needed';
}

export interface NotificationItem {
	id: string;
	title: string;
	message: string;
	time: string;
	type: 'confirmation' | 'reminder' | 'announcement';
	read: boolean;
	actionText?: string;
	actionHref?: string;
	category?: 'appointment' | 'visit' | 'reminder' | 'message';
}

export interface QueueItem {
	id: string;
	queueNumber: string;
	studentName: string;
	studentId: string;
	studentInitials: string;
	complaint: string;
	timeInClinic: string;
	status: 'Waiting' | 'In Consultation' | 'Under Observation' | 'Completed';
	actionText: 'Start visit' | 'Open' | 'Open visit';
}
