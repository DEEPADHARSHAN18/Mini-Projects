import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const CollaborationRequests = () => {
    const [requests, setRequests] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    
    useEffect(() => {
        fetchRequests();
    }, []);

    const fetchRequests = () => {
        apiClient.get('/faculty/collaboration-requests').then(res => {
            setRequests(res.data);
            setLoading(false);
        });
    };

    const handleUpdate = (id: number, status: string) => {
        const endpoint = status === 'ACCEPTED' ? `/collaborations/${id}/accept` : `/collaborations/${id}/reject`;
        apiClient.put(endpoint).then(() => fetchRequests());
    };

    if (loading) return <div>Loading...</div>;

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Collaboration Requests</h1>
            <div className="grid gap-4">
                {requests.map((r: any) => (
                    <Card key={r.collaborationId} className="hover:shadow-md transition-shadow">
                        <CardContent className="pt-6 flex flex-col md:flex-row justify-between items-start gap-4">
                            <div className="flex-1">
                                <h3 className="font-bold text-lg text-gray-900">{r.projectTitle || `Project ID: ${r.projectId}`}</h3>
                                <p className="text-sm text-gray-700 mt-1 mb-2 bg-gray-50 p-3 rounded-md border border-gray-100">{r.projectDescription}</p>
                                <div className="flex flex-wrap gap-2 mb-3">
                                    <span className="px-2.5 py-0.5 rounded bg-blue-50 text-blue-700 text-xs font-medium border border-blue-100">Domain: {r.projectDomain}</span>
                                </div>
                                <div className="flex items-center text-sm text-gray-600 bg-white border border-gray-200 rounded p-2 inline-block">
                                    <span className="font-semibold mr-1">Student:</span> 
                                    <span className="text-gray-900">{r.studentName}</span> 
                                    <span className="text-gray-400 ml-1">({r.studentEmail})</span>
                                </div>
                                <p className="text-xs text-gray-400 mt-3">Requested on: {new Date(r.createdAt).toLocaleDateString()}</p>
                            </div>
                            <div className="flex flex-col items-start md:items-end space-y-3 w-full md:w-auto mt-4 md:mt-0">
                                {r.status === 'PENDING' && <span className="px-3 py-1 rounded-full text-xs font-bold tracking-wide bg-yellow-100 text-yellow-700 border border-yellow-200">PENDING</span>}
                                {r.status === 'ACCEPTED' && <span className="px-3 py-1 rounded-full text-xs font-bold tracking-wide bg-green-100 text-green-700 border border-green-200">ACCEPTED</span>}
                                {r.status === 'REJECTED' && <span className="px-3 py-1 rounded-full text-xs font-bold tracking-wide bg-red-100 text-red-700 border border-red-200">REJECTED</span>}
                                
                                {r.status === 'PENDING' && (
                                    <div className="flex space-x-2 w-full md:w-auto">
                                        <Button onClick={() => handleUpdate(r.collaborationId, 'ACCEPTED')} className="bg-emerald-600 hover:bg-emerald-700 flex-1 md:flex-none">Accept</Button>
                                        <Button variant="outline" className="text-red-600 border-red-200 hover:bg-red-50 hover:text-red-700 flex-1 md:flex-none" onClick={() => handleUpdate(r.collaborationId, 'REJECTED')}>Reject</Button>
                                    </div>
                                )}
                            </div>
                        </CardContent>
                    </Card>
                ))}
                {requests.length === 0 && (
                    <Card>
                        <CardContent className="pt-10 pb-10 flex flex-col items-center justify-center text-gray-500">
                            <p className="text-lg">No collaboration requests yet.</p>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
};
