import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import ExamResultPage from './pages/ExamResultPage';
import ChatPage from './pages/ChatPage';
import AssignmentPage from './pages/AssignmentPage';

function App() {
    return (
        <Router>
            <div className="min-h-screen bg-gray-100">
                <nav className="bg-blue-600 text-white p-4">
                    <div className="container mx-auto flex justify-between items-center">
                        <h1 className="text-xl font-bold">YKS Chatbot</h1>
                        <div className="space-x-4">
                            <Link to="/" className="hover:underline">Öğrenci Kaydı</Link>
                            <Link to="/add-exam" className="hover:underline">Deneme Sonucu</Link>
                            <Link to="/chat" className="hover:underline">Çalışma Programı</Link>
                            <Link to="/assignments" className="hover:underline">Ödevler</Link>
                        </div>
                    </div>
                </nav>
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/add-exam" element={<ExamResultPage />} />
                    <Route path="/chat" element={<ChatPage />} />
                    <Route path="/assignments" element={<AssignmentPage />} />
                </Routes>
            </div>
        </Router>
    );
}

export default App;
