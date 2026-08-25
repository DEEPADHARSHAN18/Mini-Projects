import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts';
import { Briefcase, Activity, Clock, CheckCircle } from 'lucide-react';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

export const StudentDashboard = () => {
    const [stats, setStats] = useState<any>(null);

    useEffect(() => {
        apiClient.get('/student/dashboard').then(res => setStats(res.data));
    }, []);

    if (!stats) return <div className="p-8 text-center text-gray-500">Loading dashboard...</div>;

    const domainData = Object.keys(stats.projectsByDomain || {}).map(key => ({
        name: key,
        value: stats.projectsByDomain[key]
    }));

    const statusData = Object.keys(stats.projectsByStatus || {}).map(key => ({
        name: key,
        value: stats.projectsByStatus[key]
    }));

    return (
        <div className="space-y-6 animate-fade-in">
            <h1 className="text-3xl font-bold text-gray-900 tracking-tight">Good morning, Student</h1>
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Total Projects</div>
                            <div className="text-3xl font-bold text-gray-900">{stats.totalProjects}</div>
                        </div>
                        <Briefcase className="h-10 w-10 text-blue-100 fill-blue-500" />
                    </CardContent>
                </Card>
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Active Projects</div>
                            <div className="text-3xl font-bold text-blue-600">{stats.activeProjects}</div>
                        </div>
                        <Activity className="h-10 w-10 text-blue-100 fill-blue-500" />
                    </CardContent>
                </Card>
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Pending Requests</div>
                            <div className="text-3xl font-bold text-amber-500">{stats.pendingCollaborations}</div>
                        </div>
                        <Clock className="h-10 w-10 text-amber-100 fill-amber-500" />
                    </CardContent>
                </Card>
                <Card className="hover:shadow-md transition-shadow">
                    <CardContent className="pt-6 flex items-center justify-between">
                        <div>
                            <div className="text-sm font-medium text-gray-500">Active Collaborations</div>
                            <div className="text-3xl font-bold text-emerald-600">{stats.acceptedCollaborations}</div>
                        </div>
                        <CheckCircle className="h-10 w-10 text-emerald-100 fill-emerald-500" />
                    </CardContent>
                </Card>
            </div>
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <Card className="lg:col-span-2 hover:shadow-md transition-shadow">
                    <CardHeader>
                        <CardTitle className="text-gray-800">Projects by Domain</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {domainData.length > 0 ? (
                            <div className="h-72 w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <BarChart data={domainData}>
                                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#E5E7EB" />
                                        <XAxis dataKey="name" tick={{fill: '#6B7280'}} axisLine={false} tickLine={false} />
                                        <YAxis allowDecimals={false} tick={{fill: '#6B7280'}} axisLine={false} tickLine={false} />
                                        <Tooltip cursor={{fill: '#F3F4F6'}} contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'}} />
                                        <Bar dataKey="value" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                                    </BarChart>
                                </ResponsiveContainer>
                            </div>
                        ) : (
                            <div className="h-72 flex items-center justify-center text-gray-400">No project data available</div>
                        )}
                    </CardContent>
                </Card>
                
                <Card className="hover:shadow-md transition-shadow">
                    <CardHeader>
                        <CardTitle className="text-gray-800">Project Status</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {statusData.length > 0 ? (
                            <div className="h-72 w-full">
                                <ResponsiveContainer width="100%" height="100%">
                                    <PieChart>
                                        <Pie
                                            data={statusData}
                                            cx="50%"
                                            cy="50%"
                                            innerRadius={60}
                                            outerRadius={80}
                                            paddingAngle={5}
                                            dataKey="value"
                                        >
                                            {statusData.map((_entry, index) => (
                                                <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                            ))}
                                        </Pie>
                                        <Tooltip contentStyle={{borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'}} />
                                        <Legend verticalAlign="bottom" height={36} iconType="circle" />
                                    </PieChart>
                                </ResponsiveContainer>
                            </div>
                        ) : (
                            <div className="h-72 flex items-center justify-center text-gray-400">No status data available</div>
                        )}
                    </CardContent>
                </Card>
            </div>
            
            <div className="grid grid-cols-1 gap-6">
                <Card className="hover:shadow-md transition-shadow">
                    <CardHeader><CardTitle className="text-gray-800">Recent Projects</CardTitle></CardHeader>
                    <CardContent>
                        {stats.recentProjects && stats.recentProjects.length === 0 ? <p className="text-sm text-gray-500 py-4 text-center">No projects yet.</p> : (
                            <div className="overflow-hidden rounded-md border border-gray-100">
                                <ul className="divide-y divide-gray-100">
                                    {stats.recentProjects?.map((p: any) => (
                                        <li key={p.projectId} className="py-4 px-4 flex justify-between items-center hover:bg-gray-50 transition-colors">
                                            <div>
                                                <span className="font-semibold text-gray-800 block">{p.title}</span>
                                                <span className="text-xs text-gray-500">{p.domain}</span>
                                            </div>
                                            <span className={`px-2.5 py-1 rounded-full text-xs font-medium
                                                ${p.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-800' : 
                                                  p.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-800' : 
                                                  'bg-gray-100 text-gray-800'}`}>
                                                {p.status}
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
