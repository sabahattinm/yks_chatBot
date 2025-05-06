from datetime import datetime, timedelta
import json
from backend.config.config import QUESTION_COUNTS, NET_THRESHOLD_PERCENTAGE, YOUTUBE_RESOURCES, DEFAULT_TOPICS
import logging
from backend.database.repository import BaseRepository  # Doğru içe aktarma

logger = logging.getLogger(__name__)

class ProgramService:
    """Handles generation and updating of personalized YKS study programs."""
    def __init__(self, student_repo: BaseRepository, exam_result_repo: BaseRepository, assignment_repo: BaseRepository):
        self.student_repo = student_repo
        self.exam_result_repo = exam_result_repo
        self.assignment_repo = assignment_repo

    async def generate_study_program(self, student_id: int) -> str:
        """Generates a 7-day study program based on exam results and wrong topics."""
        try:
            student = self.student_repo.get(student_id)
            if not student:
                logger.warning(f"Student not found: {student_id}")
                return "Öğrenci bulunamadı, lütfen ID’yi kontrol et."

            exam_data = self.exam_result_repo.get(student_id)
            if not exam_data:
                logger.warning(f"No exam results for student: {student_id}")
                return "Henüz deneme sonucu yok, lütfen önce deneme girin."

            exam_type = exam_data['exam_type']
            netler = exam_data['netler']
            wrong_topics = exam_data['wrong_topics']

            # Identify weak subjects (<50% net)
            weak_subjects = []
            question_counts = QUESTION_COUNTS.get(exam_type, QUESTION_COUNTS['AYT'])
            for subject, net in netler.items():
                if net is None or net == 0:
                    continue
                max_questions = question_counts.get(subject, 40)
                net_percentage = net / max_questions
                if net_percentage < NET_THRESHOLD_PERCENTAGE:
                    weak_subjects.append((subject, net, net_percentage))

            # Generate 7-day program
            program = []
            today = datetime.now()
            for day in range(7):
                date = (today + timedelta(days=day)).strftime('%Y-%m-%d')
                daily_plan = {"date": date, "tasks": [], "assignments": []}

                # Focus on weak subjects
                for subject, net, net_percentage in weak_subjects[:2]:
                    topics = wrong_topics.get(subject, [])
                    topic = topics[day % len(topics)] if topics else DEFAULT_TOPICS[subject][day % len(DEFAULT_TOPICS[subject])]

                    youtube_channel = next((ch for ch in YOUTUBE_RESOURCES[subject] if topic in ch['topics']), YOUTUBE_RESOURCES[subject][0])
                    youtube_link = youtube_channel['link']
                    task = f"{subject}: {topic} konusunu çalış, {youtube_channel['channel']} kanalından videoyu izle: {youtube_link}"
                    daily_plan["tasks"].append(task)

                    assignment_task = f"{topic} konusundan 10 kolay soru çöz, 5 orta zorlukta deneme sorusu yap."
                    due_date = (today + timedelta(days=day + 1)).strftime('%Y-%m-%d')
                    self.assignment_repo.add({
                        'student_id': student_id,
                        'subject': subject,
                        'topic': topic,
                        'task': assignment_task,
                        'youtube_link': youtube_link,
                        'due_date': due_date
                    })
                    daily_plan["assignments"].append({
                        "subject": subject,
                        "topic": topic,
                        "task": assignment_task,
                        "youtube_link": youtube_link,
                        "due_date": due_date
                    })

                # General review for other subjects
                other_subjects = [s for s in netler.keys() if s not in [ws[0] for ws in weak_subjects]]
                if other_subjects:
                    other_subject = other_subjects[day % len(other_subjects)]
                    topics = wrong_topics.get(other_subject, [])
                    topic = topics[day % len(topics)] if topics else DEFAULT_TOPICS[other_subject][day % len(DEFAULT_TOPICS[other_subject])]
                    youtube_channel = next((ch for ch in YOUTUBE_RESOURCES[other_subject] if topic in ch['topics']), YOUTUBE_RESOURCES[other_subject][0])
                    youtube_link = youtube_channel['link']
                    task = f"{other_subject}: {topic} için {youtube_channel['channel']} kanalından video izle: {youtube_link}, 5 soru çöz."
                    daily_plan["tasks"].append(task)

                daily_plan["motivation"] = "Kanka, yanlışlarını kapatıyosun, süpersin! 💪 Bu tempoyla Haziran’da sınavı patlatırsın!"
                program.append(daily_plan)

            # Update student's study schedule
            self.student_repo.update_study_schedule(student_id, json.dumps(program, ensure_ascii=False))
            logger.info(f"Generated study program for student ID: {student_id}")
            return json.dumps(program, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error generating study program: {e}")
            raise
