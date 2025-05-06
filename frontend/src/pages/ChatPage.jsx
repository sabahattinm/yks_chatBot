// frontend/src/pages/ChatPage.jsx
import ChatForm from '../components/ChatForm';

function ChatPage() {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
                Çalışma Programı Al, Kanka! 💪
            </h1>
            <p className="text-center text-gray-600 mb-8">
                “Koç, program yap!” de, sana özel 7 günlük plan çıkaralım!
            </p>
            <ChatForm />
        </div>
    );
}

export default ChatPage;