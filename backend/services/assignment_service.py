import logging
from backend.database.repository import BaseRepository  # Doğru içe aktarma

logger = logging.getLogger(__name__)

class AssignmentService:
    """Manages assignment creation and status updates."""
    def __init__(self, assignment_repo: BaseRepository):
        self.assignment_repo = assignment_repo

    async def check_assignments(self, student_id: int) -> str:
        """Checks pending assignments for a student."""
        try:
            assignments = self.assignment_repo.get(student_id)
            if not assignments:
                logger.info(f"No pending assignments for student ID: {student_id}")
                return "Tamamlanmış veya bekleyen ödev yok, kanka! Yeni program için hazırız!"
            response = "Bekleyen ödevlerin:\n"
            for assignment in assignments:
                response += f"- {assignment['subject']} ({assignment['topic']}): {assignment['task']} (Son tarih: {assignment['due_date']})\n  Video: {assignment['youtube_link']}\n"
            logger.info(f"Retrieved pending assignments for student ID: {student_id}")
            return response
        except Exception as e:
            logger.error(f"Error checking assignments: {e}")
            raise

    async def update_assignment_status(self, assignment_id: int, status: str):
        """Updates the status of an assignment."""
        try:
            self.assignment_repo.update_status(assignment_id, status)
            logger.info(f"Updated assignment ID: {assignment_id} to status: {status}")
        except Exception as e:
            logger.error(f"Error updating assignment status: {e}")
            raise