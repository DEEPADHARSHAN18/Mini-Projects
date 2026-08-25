import { useState, useEffect } from 'react';
import axios from 'axios';
import { Users, User, BookOpen, FileText, CheckCircle, Clock, XCircle } from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

export const AdminDashboard = () => {
    const [stats, setStats] = useState<any>(null);
    const [analytics, setAnalytics] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const token = localStorage.getItem('token');
                const [statsRes, analyticsRes] = await Promise.all([
                    axios.get('http://localhost:8080/api/admin/dashboard', { headers: { Authorization: `Bearer ${token}` } }),
                    axios.get('http://localhost:8080/api/admin/analytics', { headers: { Authorization: `Bearer ${token}` } })
                ]);
                setStats(statsRes.data);
                setAnalytics(analyticsRes.data);
            } catch (err) {
                console.error(err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    if (loading) return <div className="p-8">Loading dashboard...</div>;
    if (!stats || !analytics) return <div className="p-8 text-red-600">Failed to load dashboard. <button onClick={() => window.location.reload()} className="underline ml-2">Retry</button></div>;

    const statCards = [
        { label: 'Total Users', value: stats.totalUsers, icon: Users, color: 'text-blue-600', bg: 'bg-blue-100' },
        { label: 'Total Students', value: stats.totalStudents, icon: User, color: 'text-indigo-600', bg: 'bg-indigo-100' },
        { label: 'Total Faculty', value: stats.totalFaculty, icon: User, color: 'text-purple-600', bg: 'bg-purple-100' },
        { label: 'Research Projects', value: stats.totalProjects, icon: FileText, color: 'text-teal-600', bg: 'bg-teal-100' },
        { label: 'Publications', value: stats.totalPublications, icon: BookOpen, color: 'text-orange-600', bg: 'bg-orange-100' },
        { label: 'Pending Requests', value: stats.pendingCollaborations, icon: Clock, color: 'text-yellow-600', bg: 'bg-yellow-100' },
        { label: 'Active Collaborations', value: stats.acceptedCollaborations, icon: CheckCircle, color: 'text-green-600', bg: 'bg-green-100' },
        { label: 'Rejected Requests', value: stats.rejectedCollaborations, icon: XCircle, color: 'text-red-600', bg: 'bg-red-100' }
    ];

    const pieColors = ['#0088FE', '#00C49F', '#FFBB28'];

    const userDistData = Object.keys(analytics.userDistribution || {}).map(k => ({ name: k, value: analytics.userDistribution[k] }));

    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
                <p className="text-sm text-gray-500">Overview of research collaboration activity</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                {statCards.map((card, idx) => {
                    const Icon = card.icon;
                    return (
                        <div key={idx} className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 flex items-center space-x-4 hover:shadow-md transition-shadow">
                            <div className={`p-3 rounded-full ${card.bg} ${card.color}`}>
                                <Icon className="w-6 h-6" />
                            </div>
                            <div>
                                <p className="text-sm font-medium text-gray-500">{card.label}</p>
                                <p className="text-2xl font-bold text-gray-900">{card.value}</p>
                            </div>
                        </div>
                    );
                })}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4">User Distribution</h2>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie data={userDistData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} fill="#8884d8" paddingAngle={5} dataKey="value" label>
                                    {userDistData.map((_entry, index) => <Cell key={`cell-${index}`} fill={pieColors[index % pieColors.length]} />)}
                                </Pie>
                                <Tooltip />
                            </PieChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
                    <h2 className="text-lg font-semibold mb-4">Publications by Year</h2>
                    <div className="h-64">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={analytics.publicationsByYear || []}>
                                <XAxis dataKey="year" />
                                <YAxis />
                                <Tooltip />
                                <Bar dataKey="count" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>
            </div>
        </div>
    );
};
