// frontend/src/pages/AssignmentPage.jsx
import UpdateAssignmentForm from '../components/UpdateAssignmentForm';

function AssignmentPage() {
    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold text-center text-blue-600 mb-6">
                Ödevlerini Güncelle, Kanka! ✅
            </h1>
            <p className="text-center text-gray-600 mb-8">
                Ödevlerini kontrol et, tamamladıklarını işaretle!
            </p>
            <UpdateAssignmentForm />
        </div>
    );
}

export default AssignmentPage;