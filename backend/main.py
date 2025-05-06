from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import app as fastapi_app
from database.connection import DatabaseConnection
from database.schema import initialize_schema
from dotenv import load_dotenv
import os
import logging

# Günlükleme yapılandırması
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env dosyasını yükle
load_dotenv()
logger.info("Çevre değişkenleri yüklendi.")

def init_app():
    db = DatabaseConnection()
    conn = db.connect()
    initialize_schema(conn)
    db.close()

    # CORS ayarları
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],  # React frontend’in çalıştığı adres
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return fastapi_app

app = init_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)