// frontend/src/components/UpdateAssignmentForm.jsx
import { useState } from 'react';
import axios from 'axios';

function UpdateAssignmentForm() {
    const [assignmentId, setAssignmentId] = useState('');
    const [status, setStatus] = useState('completed');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        try {
            const response = await axios.post('http://localhost:8000/update_assignment', {
                assignment_id: parseInt(assignmentId),
                status,
            });
            setMessage(response.data.message);
            setAssignmentId('');
        } catch (err) {
            setError(err.response?.data?.detail || 'Bir şeyler ters gitti, kanka! Ödev ID’sini kontrol et.');
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="assignmentId" className="block text-sm font-medium text-gray-700">
                        Ödev ID
                    </label>
                    <input
                        type="number"
                        id="assignmentId"
                        value={assignmentId}
                        onChange={(e) => setAssignmentId(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                        placeholder="Örn: 1"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="status" className="block text-sm font-medium text-gray-700">
                        Durum
                    </label>
                    <select
                        id="status"
                        value={status}
                        onChange={(e) => setStatus(e.target.value)}
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                    >
                        <option value="completed">Tamamlandı</option>
                        <option value="pending">Bekliyor</option>
                    </select>
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
                >
                    Ödevi Güncelle
                </button>
            </form>
            {message && (
                <div className="mt-4 text-center">
                    <p className="text-green-600 font-semibold">{message}</p>
                    <p className="text-gray-600">Ödevi hallettin, kanka! Devam et! 💪</p>
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

export default UpdateAssignmentForm;
