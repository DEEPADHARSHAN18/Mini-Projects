import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { BookOpen, Clock, CheckCircle } from 'lucide-react';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export const FacultyDashboard = () => {
    const [stats, setStats] = useState<any>(null);

    useEffect(() => {
        apiClient.get('/faculty/dashboard').then(res => setStats(res.data));
    }, []);

    if (!stats) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>;

    const domainData = Object.keys(stats.publicationsByDomain || {}).map(key => ({
        name: key,
        value: stats.publicationsByDomain[key]
    }));

    const yearData = Object.keys(stats.publicationsByYear || {}).map(key => ({
        name: key,
        value: stats.publicationsByYear[key]
    })).sort((a, b) => a.name.localeCompare(b.name));

    return (
        <div className="space-y-6 animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Good morning, Faculty</h1>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Total Publications</div>
                            <div className="text-3xl font-bold text-gray-900">{stats.totalPublications}</div>
                        </div>
                        <BookOpen className="h-10 w-10 text-blue-100 fill-blue-500" />
                    </CardContent>
                </Card>
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Pending Requests</div>
                            <div className="text-3xl font-bold text-amber-500">{stats.pendingRequests}</div>
                        </div>
                        <Clock className="h-10 w-10 text-amber-100 fill-amber-500" />
                    </CardContent>
                </Card>
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Active Collaborations</div>
                            <div className="text-3xl font-bold text-emerald-600">{stats.activeCollaborations}</div>
                        </div>
                        <CheckCircle className="h-10 w-10 text-emerald-100 fill-emerald-500" />
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <Card className="hover:shadow-md transition-shadow">
                    <CardHeader>
                        <CardTitle className="text-gray-800">Publications by Year</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {yearData.length > 0 ? (
                            <div className="h-72 w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={yearData}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                        <XAxis dataKey="name" tick={{fill: '#6B7280'}} axisLine={false} tickLine={false} />
                                        <YAxis allowDecimals={false} tick={{fill: '#6B7280'}} axisLine={false} tickLine={false} />
                                        <Tooltip cursor={{fill: '#F3F4F6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'}} />
                                        <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        ) : (
                            <div className="h-72 flex items-center justify-center text-gray-400">No publication data</div>
                        )}
                    </CardContent>
                </Card>
                
                <Card className="hover:shadow-md transition-shadow">
                    <CardHeader>
                        <CardTitle className="text-gray-800">Publications by Domain</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {domainData.length > 0 ? (
                            <div className="h-72 w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={domainData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={80}
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {domainData.map((_entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'}} />
                                        <Legend verticalAlign="bottom" height={36} iconType="circle" />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        ) : (
                            <div className="h-72 flex items-center justify-center text-gray-400">No domain data</div>
                        )}
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 gap-6">
                <Card className="hover:shadow-md transition-shadow">
                    <CardHeader><CardTitle className="text-gray-800">Recent Publications</CardTitle></CardHeader>
                    <CardContent>
                        {stats.recentPublications && stats.recentPublications.length === 0 ? <p className="text-sm text-gray-500 py-4 text-center">No publications yet.</p> : (
                            <div className="overflow-hidden rounded-md border border-gray-100">
                                <ul className="divide-y divide-gray-100">
                                    {stats.recentPublications?.map((p: any) => (
                                        <li key={p.publicationId} className="py-4 px-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                                            <div>
                                                <span className="font-semibold text-gray-800 block">{p.title}</span>
                                                <span className="text-xs text-gray-500">{p.journal} • {p.year}</span>
                                            </div>
                                            <span className="px-2.5 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                                                {p.domain}
                                            </span>
                                        </li>
                                    ))}
                                </ul>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>
        </div>
    );
};
