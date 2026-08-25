import { useAuth } from '../context/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';

export const Profile = () => {
    const { user } = useAuth();
    
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">My Profile</h1>
            <Card className="max-w-2xl">
                <CardHeader>
                    <CardTitle>Personal Information</CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                    <div>
                        <label className="text-sm font-medium text-gray-500">Name</label>
                        <p className="text-gray-900 font-medium">{user?.name}</p>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-500">Email</label>
                        <p className="text-gray-900 font-medium">{user?.email}</p>
                    </div>
                    <div>
                        <label className="text-sm font-medium text-gray-500">Role</label>
                        <p className="text-gray-900 font-medium">{user?.role}</p>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
};
