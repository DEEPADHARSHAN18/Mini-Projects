import { useEffect, useState } from 'react';
import apiClient from '../services/apiClient';
import { Card, CardContent, } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const FacultyRecommendations = () => {
    const [projects, setProjects] = useState<any[]>([]);
    const [selectedProject, setSelectedProject] = useState('');
    const [recommendations, setRecommendations] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    
    // Modal state
    const [showPubModal, setShowPubModal] = useState(false);
    const [selectedFacultyPubs, setSelectedFacultyPubs] = useState<any[]>([]);
    const [loadingPubs, setLoadingPubs] = useState(false);
    const [selectedFacultyName, setSelectedFacultyName] = useState('');

    useEffect(() => {
        apiClient.get('/projects/my').then(res => {
            setProjects(res.data);
            setLoading(false);
        });
    }, []);

    const fetchRecommendations = () => {
        if (!selectedProject) return;
        setLoading(true);
        apiClient.get(`/projects/${selectedProject}/recommendations`).then(res => {
            setRecommendations(res.data);
            setLoading(false);
        });
    };

    const requestCollaboration = (facultyId: number) => {
        apiClient.post('/collaborations', { projectId: parseInt(selectedProject), facultyId }).then(() => {
            alert('Request sent!');
            setRecommendations(recommendations.map(r => r.faculty.facultyId === facultyId ? { ...r, collaborationStatus: 'PENDING' } : r));
        }).catch(() => {
            alert('Failed to send request.');
        });
    };
    
    const viewPublications = (facultyId: number, facultyName: string) => {
        setLoadingPubs(true);
        setSelectedFacultyName(facultyName);
        setShowPubModal(true);
        apiClient.get(`/student/faculty/${facultyId}/publications`).then(res => {
            setSelectedFacultyPubs(res.data);
            setLoadingPubs(false);
        }).catch(() => {
            alert('Failed to fetch publications.');
            setLoadingPubs(false);
        });
    };

    if (loading && projects.length === 0) return <div>Loading...</div>;

    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-gray-900">Faculty Recommendations</h1>
            <Card>
                <CardContent className="pt-6 flex space-x-4">
                    <select 
                        className="flex-1 rounded-md border-gray-300 shadow-sm px-4 py-2 border focus:ring-blue-500"
                        value={selectedProject} onChange={e => setSelectedProject(e.target.value)}>
                        <option value="">Select a Project...</option>
                        {projects.map((p: any) => <option key={p.projectId} value={p.projectId}>{p.title}</option>)}
                    </select>
                    <Button onClick={fetchRecommendations} disabled={!selectedProject || loading}>Get Recommendations</Button>
                </CardContent>
            </Card>
            
            {showPubModal && (
                <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
                    <div className="bg-white p-6 rounded-lg shadow-xl w-full max-w-2xl max-h-[80vh] flex flex-col">
                        <div className="flex justify-between items-center mb-4">
                            <h2 className="text-xl font-bold">Publications: {selectedFacultyName}</h2>
                            <Button variant="outline" onClick={() => setShowPubModal(false)}>Close</Button>
                        </div>
                        <div className="overflow-y-auto flex-1 pr-2">
                            {loadingPubs ? (
                                <p className="text-gray-500">Loading publications...</p>
                            ) : selectedFacultyPubs.length === 0 ? (
                                <p className="text-gray-500">No publications found for this faculty.</p>
                            ) : (
                                <ul className="space-y-4">
                                    {selectedFacultyPubs.map(pub => (
                                        <li key={pub.publicationId} className="border p-4 rounded-md">
                                            <h4 className="font-semibold text-gray-900">{pub.title}</h4>
                                            <p className="text-sm text-gray-600">{pub.journal} ({pub.year})</p>
                                            <div className="mt-2 flex items-center space-x-2 text-xs">
                                                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded">{pub.domain}</span>
                                                <span className="text-gray-500">{pub.keywords}</span>
                                            </div>
                                        </li>
                                    ))}
                                </ul>
                            )}
                        </div>
                    </div>
                </div>
            )}

            <div className="grid gap-6">
                {recommendations.map((r: any, idx: number) => (
                    <Card key={idx}>
                        <CardContent className="pt-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                            <div className="flex-1">
                                <h3 className="text-lg font-bold text-gray-900">{r.facultyName}</h3>
                                <p className="text-sm text-gray-500">{r.faculty.department}</p>
                                <div className="mt-2 text-sm text-gray-700 bg-blue-50 p-3 rounded-md">
                                    <span className="font-semibold text-blue-700">Score: {r.score.totalScore}%</span>
                                    <p className="mt-1">{r.explanation}</p>
                                </div>
                            </div>
                            <div className="flex flex-col space-y-2 w-full md:w-auto">
                                {r.collaborationStatus?.toUpperCase() === 'PENDING' && <span className="text-yellow-600 font-medium whitespace-nowrap">Collaboration request pending</span>}
                                {r.collaborationStatus?.toUpperCase() === 'ACCEPTED' && <span className="text-green-600 font-medium whitespace-nowrap">Collaboration accepted</span>}
                                {r.collaborationStatus?.toUpperCase() === 'REJECTED' && <span className="text-red-600 font-medium whitespace-nowrap">Collaboration rejected</span>}
                                {(!r.collaborationStatus || (r.collaborationStatus?.toUpperCase() !== 'PENDING' && r.collaborationStatus?.toUpperCase() !== 'ACCEPTED' && r.collaborationStatus?.toUpperCase() !== 'REJECTED')) && 
                                    <Button onClick={() => requestCollaboration(r.faculty.facultyId)}>Request Collaboration</Button>
                                }
                                <Button variant="outline" onClick={() => viewPublications(r.faculty.facultyId, r.facultyName)}>
                                    View Publications
                                </Button>
                            </div>
                        </CardContent>
                    </Card>
                ))}
            </div>
        </div>
    );
};
