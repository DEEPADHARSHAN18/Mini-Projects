import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import { Login } from './pages/Login';
import { DashboardLayout } from './layouts/DashboardLayout';
import { StudentDashboard } from './pages/StudentDashboard';
import { FacultyDashboard } from './pages/FacultyDashboard';
import { AdminDashboard } from './pages/AdminDashboard';
import { AdminUsers } from './pages/admin/AdminUsers';
import { AdminFaculty } from './pages/admin/AdminFaculty';
import { AdminStudents } from './pages/admin/AdminStudents';
import { AdminProjects } from './pages/admin/AdminProjects';
import { AdminPublications } from './pages/admin/AdminPublications';
import { AdminCollaborations } from './pages/admin/AdminCollaborations';
import { AdminAnalytics } from './pages/admin/AdminAnalytics';
import { AdminProfile } from './pages/admin/AdminProfile';
import { Landing } from './pages/Landing';
import { StudentProjects } from './pages/StudentProjects';
import { FacultyRecommendations } from './pages/FacultyRecommendations';
import { MyCollaborations } from './pages/MyCollaborations';
import { FacultyPublications } from './pages/FacultyPublications';
import { CollaborationRequests } from './pages/CollaborationRequests';
import { Notifications } from './pages/Notifications';
import { Profile } from './pages/Profile';


const ProtectedRoute = ({ children, role }: { children: React.ReactNode, role?: string }) => {
    const { isAuthenticated, user } = useAuth();
    if (!isAuthenticated) return <Navigate to="/login" />;
    if (role && user?.role !== role) return <Navigate to={`/${user?.role.toLowerCase()}/dashboard`} />;
    return <>{children}</>;
};

function App() {
  return (
    <AuthProvider>
        <Router>
            <Routes>
                <Route path="/" element={<Landing />} />
                <Route path="/login" element={<Login />} />
                <Route element={<DashboardLayout />}>
                    <Route path="/student/*" element={
                        <ProtectedRoute role="STUDENT">
                            <Routes>
                                <Route path="dashboard" element={<StudentDashboard />} />
                                <Route path="projects" element={<StudentProjects />} />
                                <Route path="recommendations" element={<FacultyRecommendations />} />
                                <Route path="collaborations" element={<MyCollaborations />} />
                                <Route path="notifications" element={<Notifications />} />
                            </Routes>
                        </ProtectedRoute>
                    } />
                    <Route path="/faculty/*" element={
                        <ProtectedRoute role="FACULTY">
                            <Routes>
                                <Route path="dashboard" element={<FacultyDashboard />} />
                                <Route path="publications" element={<FacultyPublications />} />
                                <Route path="collaboration-requests" element={<CollaborationRequests />} />
                                <Route path="collaborations" element={<MyCollaborations />} />
                                <Route path="notifications" element={<Notifications />} />
                                <Route path="profile" element={<Profile />} />
                            </Routes>
                        </ProtectedRoute>
                    } />
                    <Route path="/admin/*" element={
                        <ProtectedRoute role="ADMIN">
                            <Routes>
                                <Route path="dashboard" element={<AdminDashboard />} />
                                <Route path="users" element={<AdminUsers />} />
                                <Route path="faculty" element={<AdminFaculty />} />
                                <Route path="students" element={<AdminStudents />} />
                                <Route path="projects" element={<AdminProjects />} />
                                <Route path="publications" element={<AdminPublications />} />
                                <Route path="collaborations" element={<AdminCollaborations />} />
                                <Route path="analytics" element={<AdminAnalytics />} />
                                <Route path="profile" element={<AdminProfile />} />
                            </Routes>
                        </ProtectedRoute>
                    } />
                </Route>
            </Routes>
        </Router>
    </AuthProvider>
  );
}

export default App;
