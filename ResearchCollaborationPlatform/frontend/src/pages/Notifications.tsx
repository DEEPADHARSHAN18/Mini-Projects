import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent } from '../components/ui/Card';
import { Bell } from 'lucide-react';

export const Notifications = () => {
    const [notifications, setNotifications] = useState<any[]>([]);
    
    useEffect(() => {
        apiClient.get('/notifications').then(res => setNotifications(res.data));
    }, []);

    const markAsRead = (id: number) => {
        apiClient.put(`/notifications/${id}/read`).then(() => {
            setNotifications(notifications.map((n: any) => n.notificationId === id ? { ...n, status: 'READ' } : n));
        });
    };

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Notifications</h1>
            <div className="grid gap-4">
                {notifications.map((n: any) => (
                    <Card key={n.notificationId} className={n.status === 'UNREAD' ? 'border-l-4 border-l-blue-500 bg-blue-50/50' : ''}>
                        <CardContent className="pt-6 flex items-start justify-between cursor-pointer" onClick={() => markAsRead(n.notificationId)}>
                            <div className="flex items-start">
                                <Bell className={`mr-4 h-5 w-5 ${n.status === 'UNREAD' ? 'text-blue-500' : 'text-gray-400'}`} />
                                <div>
                                    <p className={`text-sm ${n.status === 'UNREAD' ? 'font-semibold text-gray-900' : 'text-gray-600'}`}>{n.message}</p>
                                    <p className="text-xs text-gray-400 mt-1">{new Date(n.createdAt).toLocaleString()}</p>
                                </div>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};
