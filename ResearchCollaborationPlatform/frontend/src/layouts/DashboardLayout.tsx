import { useAuth } from '../context/AuthContext';
import { Link, Outlet, useNavigate, useLocation } from 'react-router-dom';
import { LogOut, Home, FileText, Users, Bell, User as UserIcon, BookOpen, Briefcase } from 'lucide-react';

export const DashboardLayout = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const handleLogout = () => { logout(); navigate('/login'); };

    const navItems = {
        STUDENT: [
            { path: '/student/dashboard', label: 'Dashboard', icon: Home },
            { path: '/student/projects', label: 'My Projects', icon: FileText },
            { path: '/student/recommendations', label: 'Faculty Recommendations', icon: Users },
            { path: '/student/collaborations', label: 'My Collaborations', icon: Briefcase },
            { path: '/student/notifications', label: 'Notifications', icon: Bell },
        ],
        FACULTY: [
            { path: '/faculty/dashboard', label: 'Dashboard', icon: Home },
            { path: '/faculty/publications', label: 'My Publications', icon: BookOpen },
            { path: '/faculty/collaboration-requests', label: 'Requests', icon: Users },
            { path: '/faculty/collaborations', label: 'My Collaborations', icon: Briefcase },
            { path: '/faculty/notifications', label: 'Notifications', icon: Bell },
            { path: '/faculty/profile', label: 'Profile', icon: UserIcon },
        ],
        ADMIN: [
            { path: '/admin/dashboard', label: 'Dashboard', icon: Home },
            { path: '/admin/users', label: 'Users', icon: Users },
            { path: '/admin/faculty', label: 'Faculty', icon: UserIcon },
            { path: '/admin/students', label: 'Students', icon: Users },
            { path: '/admin/projects', label: 'Projects', icon: FileText },
            { path: '/admin/publications', label: 'Publications', icon: BookOpen },
            { path: '/admin/collaborations', label: 'Collaborations', icon: Briefcase },
            { path: '/admin/analytics', label: 'Analytics', icon: FileText },
            { path: '/admin/profile', label: 'Profile', icon: UserIcon },
        ]
    };

    const links = user ? navItems[user.role as keyof typeof navItems] : [];

    return (
        <div className="flex h-screen bg-gray-100">
            <aside className="w-64 bg-white border-r flex flex-col">
                <div className="h-16 flex items-center px-6 border-b">
                    <span className="text-xl font-bold text-blue-600">ResearchHub</span>
                </div>
                <nav className="flex-1 overflow-y-auto py-4">
                    {links.map(link => {
                        const Icon = link.icon;
                        const active = location.pathname.startsWith(link.path);
                        return (
                            <Link key={link.path} to={link.path} 
                                className={`flex items-center px-6 py-3 text-sm font-medium ${active ? 'text-blue-600 bg-blue-50' : 'text-gray-600 hover:bg-gray-50'}`}>
                                <Icon className="mr-3 h-5 w-5" />
                                {link.label}
                            </Link>
                        );
                    })}
                </nav>
                <div className="p-4 border-t">
                    <button onClick={handleLogout} className="flex items-center w-full px-2 py-2 text-sm font-medium text-red-600 hover:bg-red-50 rounded-md">
                        <LogOut className="mr-3 h-5 w-5" /> Logout
                    </button>
                </div>
            </aside>
            <main className="flex-1 overflow-y-auto">
                <header className="h-16 bg-white border-b flex items-center justify-end px-6">
                    <div className="flex items-center space-x-4">
                        <Bell className="h-5 w-5 text-gray-500" />
                        <div className="flex flex-col items-end">
                            <span className="text-sm font-medium text-gray-700">{user?.name}</span>
                            <span className="text-xs text-gray-500">{user?.role === 'ADMIN' ? 'Administrator' : user?.role}</span>
                        </div>
                    </div>
                </header>
                <div className="p-6">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};
