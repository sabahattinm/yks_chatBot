// frontend/src/pages/Home.jsx
import AddStudentForm from '../components/AddStudentForm';

function Home() {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
                YKS Chatbot’a Hoş Geldin, Kanka! 🚀
            </h1>
            <p className="text-center text-gray-600 mb-8">
                Aşağıdaki formu doldur, sana özel YKS çalışma programı oluşturalım!
            </p>
            <AddStudentForm />
        </div>
    );
}

export default Home;

// frontend/src/pages/ExamResultPage.jsx
import AddExamResultForm from '../components/AddExamResultForm';

function ExamResultPage() {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
                Deneme Sonucunu Ekle, Kanka! 📊
            </h1>
            <p className="text-center text-gray-600 mb-8">
                Son deneme sonuçlarını gir, yanlışlarını kapatalım!
            </p>
            <AddExamResultForm />
        </div>
    );
}

export default ExamResultPage;