import { Link } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export const Landing = () => {
    return (
        <div className="min-h-screen bg-white">
            <header className="bg-white border-b px-6 py-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-blue-600">ResearchHub</h1>
                <Link to="/login"><Button variant="ghost">Sign in</Button></Link>
            </header>
            <main className="max-w-5xl mx-auto px-6 py-20 text-center">
                <h2 className="text-5xl font-extrabold text-gray-900 tracking-tight mb-6">
                    Connect Research Ideas with the Right Faculty
                </h2>
                <p className="text-xl text-gray-500 mb-10 max-w-3xl mx-auto">
                    ResearchHub intelligently matches student research projects with faculty expertise, 
                    using an advanced compatibility scoring algorithm.
                </p>
                <div className="flex justify-center space-x-4">
                    <Link to="/login"><Button className="px-8 py-4 text-lg">Get Started</Button></Link>
                </div>
            </main>
        </div>
    );
};
