import { useState, useEffect } from 'react';
import axios from 'axios';

export const AdminCollaborations = () => {
    const [collaborations, setCollaborations] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCollaborations = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:8080/api/admin/collaborations', { headers: { Authorization: `Bearer ${token}` } });
                setCollaborations(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchCollaborations();
    }, []);

    if (loading) return <div className="p-8">Loading collaborations...</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Collaborations Overview</h1>
                <p className="text-sm text-gray-500">View all collaboration requests and statuses</p>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Project Title</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Faculty ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Student ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {collaborations.map(c => (
                            <tr key={c.collaborationId}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{c.collaborationId}</td>
                                <td className="px-6 py-4 text-sm text-gray-900">{c.project?.title || `Project ID: ${c.projectId}`}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{c.facultyId}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{c.studentId}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm">
                                    <span className={`px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                        c.status === 'ACCEPTED' ? 'bg-green-100 text-green-800' :
                                        c.status === 'REJECTED' ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
                                    }`}>
                                        {c.status}
                                    </span>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
