import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent } from '../components/ui/Card';

export const MyCollaborations = () => {
    const [collaborations, setCollaborations] = useState<any[]>([]);
    
    useEffect(() => {
        apiClient.get('/collaborations/my').then(res => setCollaborations(res.data));
    }, []);

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">My Collaborations</h1>
            <div className="grid gap-4">
                {collaborations.map((c: any) => (
                    <Card key={c.collaborationId}>
                        <CardContent className="pt-6 flex justify-between items-center">
                            <div>
                                <p className="font-semibold">Project ID: {c.projectId}</p>
                                <p className="text-sm text-gray-500">Started: {new Date(c.createdAt).toLocaleDateString()}</p>
                            </div>
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${c.status === 'ACCEPTED' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}`}>
                                {c.status}
                            </span>
                        </CardContent>
                    </Card>
                ))}
                {collaborations.length === 0 && <p className="text-gray-500">No collaborations yet.</p>}
            </div>
        </div>
    );
};
