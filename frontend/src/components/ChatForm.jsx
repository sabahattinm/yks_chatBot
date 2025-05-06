// frontend/src/components/ChatForm.jsx
import { useState } from 'react';
import axios from 'axios';

function ChatForm() {
    const [studentId, setStudentId] = useState('');
    const [message, setMessage] = useState('');
    const [response, setResponse] = useState(null);
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setResponse(null);
        setError('');

        try {
            const res = await axios.post('http://localhost:8000/chat', {
                student_id: parseInt(studentId),
                message,
            });
            setResponse(res.data.response);
            setMessage('');
        } catch (err) {
            setError(err.response?.data?.detail || 'Bir şeyler ters gitti, kanka! ID’yi kontrol et.');
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="studentId" className="block text-sm font-medium text-gray-700">
                        Öğrenci ID
                    </label>
                    <input
                        type="number"
                        id="studentId"
                        value={studentId}
                        onChange={(e) => setStudentId(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                        placeholder="Örn: 1"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="message" className="block text-sm font-medium text-gray-700">
                        Mesajın
                    </label>
                    <input
                        type="text"
                        id="message"
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                        placeholder="Örn: Koç, program yap!"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
                >
                    Gönder, Haydi!
                </button>
            </form>
            {response && (
                <div className="mt-4">
                    <h3 className="text-lg font-semibold text-gray-800">Çalışma Programın:</h3>
                    <pre className="bg-gray-100 p-4 rounded-md overflow-auto text-sm">{JSON.stringify(response, null, 2)}</pre>
                    <p className="text-gray-600 text-center mt-2">Programı aldın, kanka! Şimdi çalışmaya başla! 🚀</p>
                </div>
            )}
            {error && (
                <div className="mt-4 text-center">
                    <p className="text-red-600 font-semibold">{error}</p>
                </div>
            )}
        </div>
    );
}

export default ChatForm;