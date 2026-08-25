import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const FacultyPublications = () => {
    const [publications, setPublications] = useState<any[]>([]);
    const [showForm, setShowForm] = useState(false);
    const [editingId, setEditingId] = useState<number | null>(null);
    const [formData, setFormData] = useState({ title: '', journal: '', year: new Date().getFullYear(), domain: '', keywords: '' });
    
    useEffect(() => {
        fetchPublications();
    }, []);

    const fetchPublications = () => {
        apiClient.get('/faculty/publications').then(res => setPublications(res.data));
    };

    const handleSave = () => {
        if (editingId) {
            apiClient.put(`/faculty/publications/${editingId}`, formData).then(() => {
                fetchPublications();
                resetForm();
            });
        } else {
            apiClient.post('/faculty/publications', formData).then(() => {
                fetchPublications();
                resetForm();
            });
        }
    };

    const handleDelete = (id: number) => {
        apiClient.delete(`/faculty/publications/${id}`).then(() => fetchPublications());
    };

    const editPublication = (pub: any) => {
        setEditingId(pub.publicationId);
        setFormData({ title: pub.title, journal: pub.journal, year: pub.year, domain: pub.domain, keywords: pub.keywords });
        setShowForm(true);
    };

    const resetForm = () => {
        setShowForm(false);
        setEditingId(null);
        setFormData({ title: '', journal: '', year: new Date().getFullYear(), domain: '', keywords: '' });
    };

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-2xl font-bold text-gray-900">My Publications</h1>
                <Button onClick={() => setShowForm(!showForm)}>
                    {showForm ? 'Cancel' : 'Add Publication'}
                </Button>
            </div>

            {showForm && (
                <Card className="bg-white border border-blue-100 shadow-sm animate-fade-in">
                    <CardContent className="pt-6 space-y-4">
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div className="md:col-span-2">
                                <label className="block text-sm font-medium text-gray-700">Title</label>
                                <input type="text" className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 focus:border-blue-500 focus:ring-blue-500" 
                                    value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Journal/Conference</label>
                                <input type="text" className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 focus:border-blue-500 focus:ring-blue-500" 
                                    value={formData.journal} onChange={e => setFormData({...formData, journal: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Year</label>
                                <input type="number" className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 focus:border-blue-500 focus:ring-blue-500" 
                                    value={formData.year} onChange={e => setFormData({...formData, year: parseInt(e.target.value)})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Domain</label>
                                <input type="text" className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 focus:border-blue-500 focus:ring-blue-500" 
                                    value={formData.domain} onChange={e => setFormData({...formData, domain: e.target.value})} />
                            </div>
                            <div>
                                <label className="block text-sm font-medium text-gray-700">Keywords (comma-separated)</label>
                                <input type="text" className="mt-1 block w-full rounded-md border border-gray-300 shadow-sm px-3 py-2 focus:border-blue-500 focus:ring-blue-500" 
                                    value={formData.keywords} onChange={e => setFormData({...formData, keywords: e.target.value})} />
                            </div>
                        </div>
                        <div className="flex justify-end space-x-3 mt-6 pt-4 border-t border-gray-100">
                            <Button variant="outline" onClick={resetForm}>Cancel</Button>
                            <Button onClick={handleSave}>Save Publication</Button>
                        </div>
                    </CardContent>
                </Card>
            )}

            <div className="grid gap-4">
                {publications.map((p: any) => (
                    <Card key={p.publicationId} className="hover:shadow-md transition-shadow">
                        <CardContent className="pt-6 flex flex-col md:flex-row justify-between gap-4">
                            <div className="flex-1">
                                <h3 className="font-bold text-lg text-gray-900">{p.title}</h3>
                                <p className="text-sm font-medium text-blue-700 mt-1">{p.journal} <span className="text-gray-500 font-normal">({p.year})</span></p>
                                <div className="mt-3 flex flex-wrap gap-2">
                                    <span className="bg-blue-50 text-blue-700 border border-blue-100 px-2.5 py-0.5 rounded text-xs font-medium">Domain: {p.domain}</span>
                                    {p.keywords && <span className="bg-gray-100 text-gray-600 border border-gray-200 px-2.5 py-0.5 rounded text-xs">{p.keywords}</span>}
                                </div>
                            </div>
                            <div className="flex space-x-3 items-start mt-2 md:mt-0">
                                <Button variant="outline" onClick={() => editPublication(p)}>Edit</Button>
                                <Button variant="danger" className="text-red-600 bg-red-50 hover:bg-red-100 border-transparent" onClick={() => handleDelete(p.publicationId)}>Delete</Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
                {publications.length === 0 && !showForm && (
                    <Card>
                        <CardContent className="pt-10 pb-10 flex flex-col items-center justify-center text-gray-500">
                            <p className="text-lg">No publications added yet.</p>
                            <Button variant="outline" className="mt-4" onClick={() => setShowForm(true)}>Add your first publication</Button>
                        </CardContent>
                    </Card>
                )}
            </div>
        </div>
    );
};
