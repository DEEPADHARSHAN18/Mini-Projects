import { useState, useEffect } from 'react';
import axios from 'axios';
import { UserIcon } from 'lucide-react';

export const AdminFaculty = () => {
    const [faculty, setFaculty] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchFaculty = async () => {
            try {
                const token = localStorage.getItem('token');
                const res = await axios.get('http://localhost:8080/api/admin/faculty', { headers: { Authorization: `Bearer ${token}` } });
                setFaculty(res.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchFaculty();
    }, []);

    if (loading) return <div className="p-8">Loading faculty...</div>;

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Faculty Management</h1>
                <p className="text-sm text-gray-500">View and manage faculty profiles</p>
            </div>

            <div className="bg-white rounded-lg shadow overflow-hidden">
                <table className="min-w-full divide-y divide-gray-200">
                    <thead className="bg-gray-50">
                        <tr>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">User ID</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Department</th>
                            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Expertise</th>
                        </tr>
                    </thead>
                    <tbody className="bg-white divide-y divide-gray-200">
                        {faculty.map(f => (
                            <tr key={f.facultyId}>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{f.facultyId}</td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                                    <div className="flex items-center">
                                        <UserIcon className="w-4 h-4 mr-2" />
                                        {f.user?.name || `User ID: ${f.userId}`}
                                    </div>
                                </td>
                                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">{f.department}</td>
                                <td className="px-6 py-4 text-sm text-gray-500">{f.expertise}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};
