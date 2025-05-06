from abc import ABC, abstractmethod
import json
from typing import Optional, Dict, Any, List

class BaseRepository(ABC):
    @abstractmethod
    def add(self, data: Dict[str, Any]) -> int:
        pass

    @abstractmethod
    def get(self, identifier: int) -> Optional[Dict[str, Any]]:
        pass

class StudentRepository(BaseRepository):
    def __init__(self, conn):
        self.conn = conn

    def add(self, data: Dict[str, Any]) -> int:
        c = self.conn.cursor()
        c.execute("INSERT INTO students (name, goal, study_schedule) VALUES (?, ?, ?)",
                  (data['name'], data['goal'], data['study_schedule']))
        self.conn.commit()
        return c.lastrowid

    def get(self, student_id: int) -> Optional[Dict[str, Any]]:
        c = self.conn.cursor()
        c.execute("SELECT name, goal, study_schedule FROM students WHERE id = ?", (student_id,))
        result = c.fetchone()
        if result:
            return {'name': result[0], 'goal': result[1], 'study_schedule': result[2]}
        return None

    def update_study_schedule(self, student_id: int, study_schedule: str):
        c = self.conn.cursor()
        c.execute("UPDATE students SET study_schedule = ? WHERE id = ?",
                  (study_schedule, student_id))
        self.conn.commit()

class ExamResultRepository(BaseRepository):
    def __init__(self, conn):
        self.conn = conn

    def add(self, data: Dict[str, Any]) -> int:
        c = self.conn.cursor()
        wrong_topics = data.get('wrong_topics', {})
        c.execute('''INSERT INTO exam_results (
                     student_id, exam_date, exam_type, matematik, fizik, kimya, biyoloji, turkce, sosyal, geometri,
                     matematik_wrong_topics, fizik_wrong_topics, kimya_wrong_topics, biyoloji_wrong_topics,
                     turkce_wrong_topics, sosyal_wrong_topics, geometri_wrong_topics)
                     VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (data['student_id'], data['exam_date'], data['exam_type'],
                   data['netler'].get('matematik', 0), data['netler'].get('fizik', 0), data['netler'].get('kimya', 0),
                   data['netler'].get('biyoloji', 0), data['netler'].get('turkce', 0), data['netler'].get('sosyal', 0),
                   data['netler'].get('geometri', 0),
                   json.dumps(wrong_topics.get('matematik', [])),
                   json.dumps(wrong_topics.get('fizik', [])),
                   json.dumps(wrong_topics.get('kimya', [])),
                   json.dumps(wrong_topics.get('biyoloji', [])),
                   json.dumps(wrong_topics.get('turkce', [])),
                   json.dumps(wrong_topics.get('sosyal', [])),
                   json.dumps(wrong_topics.get('geometri', []))))
        self.conn.commit()
        return c.lastrowid

    def get(self, student_id: int) -> Optional[Dict[str, Any]]:
        c = self.conn.cursor()
        c.execute('''SELECT exam_type, matematik, fizik, kimya, biyoloji, turkce, sosyal, geometri,
                            matematik_wrong_topics, fizik_wrong_topics, kimya_wrong_topics,
                            biyoloji_wrong_topics, turkce_wrong_topics, sosyal_wrong_topics, geometri_wrong_topics
                     FROM exam_results
                     WHERE student_id = ?
                     ORDER BY exam_date DESC LIMIT 1''', (student_id,))
        result = c.fetchone()
        if result:
            return {
                'exam_type': result[0],
                'netler': {
                    'matematik': result[1], 'fizik': result[2], 'kimya': result[3], 'biyoloji': result[4],
                    'turkce': result[5], 'sosyal': result[6], 'geometri': result[7]
                },
                'wrong_topics': {
                    'matematik': json.loads(result[8]), 'fizik': json.loads(result[9]), 'kimya': json.loads(result[10]),
                    'biyoloji': json.loads(result[11]), 'turkce': json.loads(result[12]), 'sosyal': json.loads(result[13]),
                    'geometri': json.loads(result[14])
                }
            }
        return None

class AssignmentRepository(BaseRepository):
    def __init__(self, conn):
        self.conn = conn

    def add(self, data: Dict[str, Any]) -> int:
        c = self.conn.cursor()
        c.execute('''INSERT INTO assignments (student_id, subject, topic, task, youtube_link, due_date, status)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (data['student_id'], data['subject'], data['topic'], data['task'],
                   data['youtube_link'], data['due_date'], 'pending'))
        self.conn.commit()
        return c.lastrowid

    def get(self, student_id: int) -> List[Dict[str, Any]]:
        c = self.conn.cursor()
        c.execute("SELECT id, subject, topic, task, youtube_link, due_date FROM assignments WHERE student_id = ? AND status = 'pending'", (student_id,))
        return [{'id': row[0], 'subject': row[1], 'topic': row[2], 'task': row[3], 'youtube_link': row[4], 'due_date': row[5]} for row in c.fetchall()]

    def update_status(self, assignment_id: int, status: str):
        c = self.conn.cursor()
        c.execute("UPDATE assignments SET status = ? WHERE id = ?", (status, assignment_id))
        self.conn.commit()
