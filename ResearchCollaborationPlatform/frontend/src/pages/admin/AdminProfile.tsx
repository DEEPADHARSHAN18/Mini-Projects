import { useAuth } from '../../context/AuthContext';

export const AdminProfile = () => {
    const { user } = useAuth();

    return (
        <div className="space-y-6 max-w-2xl">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Admin Profile</h1>
                <p className="text-sm text-gray-500">Your administrator account details</p>
            </div>

            <div className="bg-white rounded-lg shadow p-6 space-y-4 border border-gray-100">
                <div className="flex items-center space-x-4">
                    <div className="h-16 w-16 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center text-2xl font-bold">
                        {user?.name?.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h2 className="text-xl font-bold text-gray-900">{user?.name}</h2>
                        <p className="text-gray-500">{user?.email}</p>
                    </div>
                </div>

                <div className="pt-4 border-t border-gray-100">
                    <div className="grid grid-cols-2 gap-4">
                        <div>
                            <p className="text-sm font-medium text-gray-500">Role</p>
                            <p className="mt-1 font-medium text-gray-900">Administrator</p>
                        </div>
                        <div>
                            <p className="text-sm font-medium text-gray-500">Account ID</p>
                            <p className="mt-1 font-medium text-gray-900">{user?.id}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
