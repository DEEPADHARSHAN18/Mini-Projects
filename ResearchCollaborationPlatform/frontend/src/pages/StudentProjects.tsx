import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const StudentProjects = () => {
    const [projects, setProjects] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [showModal, setShowModal] = useState(false);
    
    const [formData, setFormData] = useState({
        title: '',
        description: '',
        domain: '',
        keywords: ''
    });

    useEffect(() => {
        fetchProjects();
    }, []);

    const fetchProjects = () => {
        apiClient.get('/projects/my').then(res => {
            setProjects(res.data);
            setLoading(false);
        });
    };

    const handleCreateProject = async (e: React.FormEvent) => {
        e.preventDefault();
        try {
            await apiClient.post('/projects', formData);
            setShowModal(false);
            setFormData({ title: '', description: '', domain: '', keywords: '' });
            fetchProjects();
        } catch (error) {
            console.error("Failed to create project", error);
            alert("Failed to create project.");
        }
    };

    if (loading) return <div>Loading projects...</div>;

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">My Projects</h1>
                <Button onClick={() => setShowModal(true)}>Create New Project</Button>
            </div>
            
            {showModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-md">
                        <h2 className="text-xl font-bold mb-4">Create New Project</h2>
                        <form onSubmit={handleCreateProject} className="space-y-4">
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Title</label>
                                <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Description</label>
                                <textarea required rows={3} className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Domain</label>
                                <input required type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" value={formData.domain} onChange={e => setFormData({...formData, domain: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Keywords (comma separated)</label>
                                <input type="text" className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2" value={formData.keywords} onChange={e => setFormData({...formData, keywords: e.target.value})} />
                            </div>
                            <div className="flex justify-end space-x-3 pt-4">
                                <Button type="button" variant="outline" onClick={() => setShowModal(false)}>Cancel</Button>
                                <Button type="submit">Create</Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <div className="grid gap-6">
                {projects.map((p: any) => (
                    <Card key={p.projectId}>
                        <CardHeader>
                            <CardTitle className="text-xl">{p.title}</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <p className="text-gray-600 mb-4">{p.description}</p>
                            <div className="flex space-x-4 text-sm text-gray-500">
                                <span>Domain: {p.domain}</span>
                                <span>Status: <span className="font-medium text-blue-600">{p.status}</span></span>
                            </div>
                        </CardContent>
                    </Card>
                ))}
                {projects.length === 0 && <p>No projects found.</p>}
            </div>
        </div>
    );
};
