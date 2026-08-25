import { useState, useEffect } from 'react';
import axios from 'axios';

export const AdminPublications = () => {
    const [publications, setPublications] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchPublications = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:8080/api/admin/publications', { headers: { Authorization: `Bearer ${token}` } });
                setPublications(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchPublications();
    }, []);

    if (loading) return <div className="p-8">Loading publications...</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Publications Overview</h1>
                <p className="text-sm text-gray-500">View all research publications</p>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Title</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Journal/Year</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Domain</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Faculty ID</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {publications.map(p => (
                            <tr key={p.publicationId}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{p.publicationId}</td>
                                <td className="px-6 py-4 text-sm font-medium text-gray-900">{p.title}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">{p.journal} ({p.year})</td>
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
