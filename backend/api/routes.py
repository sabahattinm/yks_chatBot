
# api/routes.py
from fastapi import FastAPI, Depends, HTTPException
from backend.database.connection import DatabaseConnection
from backend.database.repository import StudentRepository, ExamResultRepository, AssignmentRepository
from backend.services.program_service import ProgramService
from backend.services.assignment_service import AssignmentService
from backend.services.agent_service import AgentService
from backend.models.pydantic_models import ExamResultInput, AssignmentUpdate, ChatInput, StudentInput
import logging

logger = logging.getLogger(__name__)


def get_db_connection():
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()


def get_repositories(db: DatabaseConnection = Depends(get_db_connection)):
    conn = db.connect()
    return {
        'student_repo': StudentRepository(conn),
        'exam_result_repo': ExamResultRepository(conn),
        'assignment_repo': AssignmentRepository(conn)
    }


def get_services(repos=Depends(get_repositories)):
    program_service = ProgramService(
        repos['student_repo'],
        repos['exam_result_repo'],
        repos['assignment_repo']
    )
    assignment_service = AssignmentService(repos['assignment_repo'])
    agent_service = AgentService(program_service, assignment_service)
    return {
        'program_service': program_service,
        'assignment_service': assignment_service,
        'agent_service': agent_service
    }


app = FastAPI()


@app.get("/", summary="Hoş Geldin Mesajı")
async def root():
    return {"message": "YKS Chatbot’a hoş geldin, kanka! 💪 Program oluşturmak için /docs’a göz at!"}


@app.post("/add_student", summary="Yeni öğrenci ekle")
async def add_student(input_data: StudentInput, repos=Depends(get_repositories)):
    try:
        student_id = repos['student_repo'].add(input_data.dict())
        logger.info(f"Yeni öğrenci eklendi: name={input_data.name}, goal={input_data.goal}, student_id={student_id}")
        return {"message": f"Öğrenci eklendi, kanka! ID: {student_id}"}
    except Exception as e:
        logger.error(f"Öğrenci eklenirken hata: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Öğrenci eklenirken hata: {str(e)}")


@app.post("/chat", summary="YKS chatbot ile sohbet et")
async def chat(input_data: ChatInput, services=Depends(get_services), repos=Depends(get_repositories)):
    try:
        # Öğrenci varlığını kontrol et
        student = repos['student_repo'].get(input_data.student_id)
        if not student:
            logger.warning(f"Öğrenci bulunamadı: student_id={input_data.student_id}")
            raise HTTPException(status_code=404,
                                detail=f"Öğrenci ID {input_data.student_id} bulunamadı, kanka! Önce öğrenci ekle.")

        response = await services['agent_service'].process_message(input_data.student_id, input_data.message)
        logger.info(f"Chat endpoint başarılı: student_id={input_data.student_id}, message={input_data.message}")
        return {"response": response}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Chat endpoint hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat işlemi sırasında hata: {str(e)}")


@app.post("/add_exam_result", summary="Deneme sonucu ekle")
async def add_exam_result(input_data: ExamResultInput, repos=Depends(get_repositories)):
    try:
        # Öğrenci varlığını kontrol et
        student = repos['student_repo'].get(input_data.student_id)
        if not student:
            logger.warning(f"Öğrenci bulunamadı: student_id={input_data.student_id}")
            raise HTTPException(status_code=404,
                                detail=f"Öğrenci ID {input_data.student_id} bulunamadı, kanka! Önce öğrenci ekle.")

        repos['exam_result_repo'].add(input_data.dict())
        logger.info(f"Deneme sonucu eklendi: student_id={input_data.student_id}, exam_type={input_data.exam_type}")
        return {"message": "Deneme sonucu ve yanlış konular eklendi."}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Add exam result endpoint hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Deneme sonucu eklenirken hata: {str(e)}")


@app.post("/update_assignment", summary="Ödev durumunu güncelle")
async def update_assignment(input_data: AssignmentUpdate, services=Depends(get_services),
                            repos=Depends(get_repositories)):
    try:
        # Ödevin ait olduğu öğrenciyi kontrol et
        assignments = repos['assignment_repo'].get(input_data.assignment_id)
        if not assignments:
            logger.warning(f"Ödev bulunamadı: assignment_id={input_data.assignment_id}")
            raise HTTPException(status_code=404, detail=f"Ödev ID {input_data.assignment_id} bulunamadı.")

        await services['assignment_service'].update_assignment_status(input_data.assignment_id, input_data.status)
        logger.info(f"Ödev güncellendi: assignment_id={input_data.assignment_id}, status={input_data.status}")
        return {"message": f"Ödev durumu '{input_data.status}' olarak güncellendi."}
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Update assignment endpoint hatası: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Ödev güncellenirken hata: {str(e)}")

