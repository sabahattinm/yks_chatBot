// frontend/src/components/AddExamResultForm.jsx
import { useState } from 'react';
import axios from 'axios';

function AddExamResultForm() {
    const [studentId, setStudentId] = useState('');
    const [examDate, setExamDate] = useState('');
    const [examType, setExamType] = useState('AYT');
    const [netler, setNetler] = useState({
        matematik: '',
        fizik: '',
        kimya: '',
        biyoloji: '',
        geometri: '',
        turkce: '',
        sosyal: '',
    });
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleNetChange = (subject, value) => {
        setNetler((prev) => ({ ...prev, [subject]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        const payload = {
            student_id: parseInt(studentId),
            exam_date: examDate,
            exam_type: examType,
            netler: {
                matematik: parseInt(netler.matematik) || 0,
                fizik: parseInt(netler.fizik) || 0,
                kimya: parseInt(netler.kimya) || 0,
                biyoloji: parseInt(netler.biyoloji) || 0,
                geometri: parseInt(netler.geometri) || 0,
                turkce: parseInt(netler.turkce) || 0,
                sosyal: parseInt(netler.sosyal) || 0,
            },
            wrong_topics: {
                matematik: [], // Kullanıcıdan alınabilir
                fizik: [],
                kimya: [],
                biyoloji: [],
                geometri: [],
                turkce: [],
                sosyal: [],
            },
        };

        try {
            const response = await axios.post('http://localhost:8000/add_exam_result', payload);
            setMessage(response.data.message);
            setStudentId('');
            setExamDate('');
            setNetler({ matematik: '', fizik: '', kimya: '', biyoloji: '', geometri: '', turkce: '', sosyal: '' });
        } catch (err) {
            setError(err.response?.data?.detail || 'Bir şeyler ters gitti, kanka! Verileri kontrol et.');
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
                    <label htmlFor="examDate" className="block text-sm font-medium text-gray-700">
                        Sınav Tarihi
                    </label>
                    <input
                        type="date"
                        id="examDate"
                        value={examDate}
                        onChange={(e) => setExamDate(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="examType" className="block text-sm font-medium text-gray-700">
                        Sınav Türü
                    </label>
                    <select
                        id="examType"
                        value={examType}
                        onChange={(e) => setExamType(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                    >
                        <option value="AYT">AYT</option>
                        <option value="TYT">TYT</option>
                    </select>
                </div>
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">Netler</label>
                    {['matematik', 'fizik', 'kimya', 'biyoloji', 'geometri', 'turkce', 'sosyal'].map((subject) => (
                        <div key={subject} className="flex items-center mb-2">
                            <label className="w-24 text-sm text-gray-600 capitalize">{subject}</label>
                            <input
                                type="number"
                                value={netler[subject]}
                                onChange={(e) => handleNetChange(subject, e.target.value)}
                                className="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                                placeholder="0"
                            />
                        </div>
                    ))}
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
                >
                    Sonuçları Ekle
                </button>
            </form>
            {message && (
                <div className="mt-4 text-center">
                    <p className="text-green-600 font-semibold">{message}</p>
                    <p className="text-gray-600">Şimdi çalışma programı alabilirsin! 🚀</p>
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

export default AddExamResultForm;
