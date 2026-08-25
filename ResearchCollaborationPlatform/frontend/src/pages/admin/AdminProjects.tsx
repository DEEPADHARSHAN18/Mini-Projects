import { useState, useEffect } from 'react';
import axios from 'axios';

export const AdminProjects = () => {
    const [projects, setProjects] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchProjects = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:8080/api/admin/projects', { headers: { Authorization: `Bearer ${token}` } });
                setProjects(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchProjects();
    }, []);

    if (loading) return <div className="p-8">Loading projects...</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Projects Overview</h1>
                <p className="text-sm text-gray-500">View all research projects</p>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Domain</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Faculty ID</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {projects.map(p => (
                            <tr key={p.projectId}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{p.projectId}</td>
                                <td className="px-6 py-4 text-sm font-medium text-gray-900">{p.title}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.domain}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.facultyId}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
