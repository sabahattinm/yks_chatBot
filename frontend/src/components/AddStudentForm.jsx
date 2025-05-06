// frontend/src/components/AddStudentForm.jsx
import { useState } from 'react';
import axios from 'axios';

function AddStudentForm() {
    const [name, setName] = useState('');
    const [goal, setGoal] = useState('');
    const [message, setMessage] = useState('');
    const [error, setError] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setMessage('');
        setError('');

        try {
            const response = await axios.post('http://localhost:8000/add_student', {
                name,
                goal,
                study_schedule: '',
            });
            setMessage(response.data.message);
            setName('');
            setGoal('');
        } catch (err) {
            setError(err.response?.data?.detail || 'Bir şeyler ters gitti, kanka! Backend çalıştığından emin ol.');
        }
    };

    return (
        <div className="max-w-md mx-auto bg-white p-6 rounded-lg shadow-md">
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                        Adın
                    </label>
                    <input
                        type="text"
                        id="name"
                        value={name}
                        onChange={(e) => setName(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                        placeholder="Örn: Sude"
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="goal" className="block text-sm font-medium text-gray-700">
                        Hedefin (Bölüm/Hedef)
                    </label>
                    <input
                        type="text"
                        id="goal"
                        value={goal}
                        onChange={(e) => setGoal(e.target.value)}
                        required
                        className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50"
                        placeholder="Örn: Tıp"
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition duration-200"
                >
                    Kaydol, Haydi!
                </button>
            </form>
            {message && (
                <div className="mt-4 text-center">
                    <p className="text-green-600 font-semibold">{message}</p>
                    <p className="text-gray-600">Şimdi deneme sonucu ekleyip program oluşturabilirsin! 💪</p>
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

export default AddStudentForm;