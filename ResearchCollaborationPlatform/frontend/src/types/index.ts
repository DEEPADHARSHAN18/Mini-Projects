export interface User { id: number; name: string; email: string; role: string; }
export interface Project { projectId: number; title: string; description: string; domain: string; keywords: string; status: string; studentId: number; createdAt: string; }
export interface Faculty { facultyId: number; userId: number; department: string; expertise: string; researchInterests: string; availability: string; }
export interface Publication { publicationId: number; title: string; journal: string; year: number; domain: string; keywords: string; facultyId: number; }
export interface Collaboration { collaborationId: number; projectId: number; facultyId: number; studentId: number; status: string; createdAt: string; }
export interface Notification { notificationId: number; userId: number; message: string; status: string; createdAt: string; }
export interface Recommendation { faculty: Faculty; facultyName: string; score: any; explanation: string; }
