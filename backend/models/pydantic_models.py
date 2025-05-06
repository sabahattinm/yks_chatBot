from pydantic import BaseModel
from typing import Dict, List, Optional

class Netler(BaseModel):
    matematik: Optional[int] = 0
    fizik: Optional[int] = 0
    kimya: Optional[int] = 0
    biyoloji: Optional[int] = 0
    turkce: Optional[int] = 0
    sosyal: Optional[int] = 0
    geometri: Optional[int] = 0

class WrongTopics(BaseModel):
    matematik: List[str] = []
    fizik: List[str] = []
    kimya: List[str] = []
    biyoloji: List[str] = []
    turkce: List[str] = []
    sosyal: List[str] = []
    geometri: List[str] = []

class ExamResultInput(BaseModel):
    student_id: int
    exam_date: str
    exam_type: str
    netler: Netler
    wrong_topics: WrongTopics

class AssignmentUpdate(BaseModel):
    assignment_id: int
    status: str

class ChatInput(BaseModel):
    student_id: int
    message: str

class StudentInput(BaseModel):
    name: str
    goal: str
    study_schedule: Optional[str] = ""