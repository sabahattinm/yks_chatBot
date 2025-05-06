from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, Tool
from langchain.memory import ConversationBufferMemory
from typing import Optional
from dotenv import load_dotenv
import os
import logging

# Günlükleme yapılandırması
logger = logging.getLogger(__name__)

# .env dosyasını yükle
load_dotenv()

class AgentService:
    def __init__(self, program_service: 'ProgramService', assignment_service: 'AssignmentService'):
        self.program_service = program_service
        self.assignment_service = assignment_service
        self.agent = self._setup_agent()

    def _setup_agent(self):
        # GOOGLE_API_KEY kontrolü
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.error("GOOGLE_API_KEY çevre değişkeni bulunamadı.")
            raise ValueError("GOOGLE_API_KEY çevre değişkeni bulunamadı. Lütfen .env dosyasına ekleyin.")
        logger.info("Gemini API key başarıyla yüklendi.")

        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.7, google_api_key=api_key)
        memory = ConversationBufferMemory(memory_key="chat_history")
        tools = [
            Tool(
                name="StudyProgramGenerator",
                func=lambda x: self.program_service.generate_study_program(int(x.split(":")[1].strip())),
                description="Öğrenci ID’sine göre yanlış yapılan konulara, yüzdesel net eşiklerine ve YouTube kaynaklarına dayalı YKS çalışma programı oluşturur."
            ),
            Tool(
                name="CheckAssignments",
                func=lambda x: self.assignment_service.check_assignments(int(x.split(":")[1].strip())),
                description="Öğrencinin bekleyen ödevlerini kontrol eder."
            )
        ]
        return initialize_agent(
            tools=tools,
            llm=llm,
            agent_type="conversational-react-description",
            memory=memory,
            verbose=True
        )

    async def process_message(self, student_id: int, message: str) -> str:
        try:
            response = await self.agent.arun(
                input=f"""
                Öğrenci ID: {student_id}
                Mesaj: {message}
                Türkiye’deki gençlerin diline uygun, samimi ve YKS’ye özgü bir yanıt ver. 
                Yanlış yaptığı konulara, yüzdesel net eşiklerine ve YouTube kaynaklarına odaklanarak rehber ol.
                """
            )
            logger.info(f"Mesaj işlendi: {message}")
            return response
        except Exception as e:
            logger.error(f"Mesaj işlenirken hata: {str(e)}")
            raise
