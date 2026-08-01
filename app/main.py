import time
import google.generativeai as genai
import logging
import os
import requests
import sys
from fastapi.responses import JSONResponse
from app.diagnosis import analyze_symptom
from app.vision import analyze_image_with_ai
from fastapi import FastAPI, UploadFile, File, HTTPException
from app.validator import run_validation
from app.loader import (
    load_cars,
    load_motorcycles,
)
from contextlib import asynccontextmanager
from pydantic import BaseModel
from datetime import datetime, timezone

"generated_at": datetime.now(timezone.utc).isoformat()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MontirPintarAPIV2")

app = FastAPI(
    title="MontirPintar AI",
    version="2.0",
    description="Bilingual Automotive AI Diagnosis API",
    lifespan=lifespan,
    contact={
        "name": "Fathurrahman"
    },
    license_info={
        "name": "MIT"
    }
)

class KeluhanInput(BaseModel):
    keluhan: str

class ErrorReportInput(BaseModel):
    keluhan: str
    diagnosa_ai: str


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "status":"error",
            "message":"Internal Server Error"
        }
    )

@asynccontextmanager
async def lifespan(app: FastAPI):
    errors = run_validation()
    if errors:
        logger.warning(
            f"Dataset Warning : {len(errors)}"
        )
    else:
        logger.info("Dataset OK")
    yield

@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time()-start
    logger.info(
        f"{request.method} {request.url.path} {duration:.3f}s"
    )
    return response


@app.get("/health")
def health():
    return {
"status":"healthy",
"cars":len(load_cars()),
"motorcycles":len(load_motorcycles()),
"validator":"OK"
}

@app.get("/qa")
def qa():
    errors = run_validation()
    return {
        "valid": len(errors) == 0,
        "error_count": len(errors),
        "errors": errors
    }

@app.get("/stats", tags=["System"])
def stats():
    cars = load_cars()
    motorcycles = load_motorcycles()
    return {
        "dataset": {
            "cars": len(cars),
            "motorcycles": len(motorcycles),
            "total": len(cars)+len(motorcycles)
        },
        "status":"ready"
    }

@app.get("/ping")
def ping():
    return {
        "message":"pong"
    }

@app.get("/languages")
def languages():
    return {
        "supported":[
            "id",
            "en"
        ]
    }

@app.get("/")
def home():
    return {"status": "aktif", "version": "v2.0", "pesan": "MontirPintar API v2 (Modular) Berjalan!"}


@app.get("/version")
def version():
    return {
    "api":"2.0",
    "gemini":genai.__version__,
    "python":sys.version.split()[0]
}

@app.get("/about", tags=["System"])
def about():
    cars = load_cars()
    motorcycles = load_motorcycles()
    return {
        "application": {
            "name": "MontirPintar AI",
            "version": "2.0",
            "engine": "Gemini"
        },
        "supported_language": [
            "id",
            "en"
        ],
        "supported_vehicle": [
            "car",
            "motorcycle"
        ],
        "knowledge": {
            "cars": len(cars),
            "motorcycles": len(motorcycles),
            "total": len(cars)+len(motorcycles)
        }
    }

@app.get("/models")
def list_models():
    try:
        api_key = os.environ.get("GEMINI_API_KEY")

        if not api_key:
            return {
                "status": "error",
                "message": "GEMINI_API_KEY tidak ditemukan."
            }
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models"
            f"?key={api_key}"
        )
        response = requests.get(url, timeout=20)
        return response.json()
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post("/diagnosa")
def diagnosa_ai(data: KeluhanInput):
    try:
        logger.info(f"Keluhan masuk: {data.keluhan}")
        result = analyze_symptom(data.keluhan)   
        if result:
            return result
        else:
            return {
                "status": "success",
                "bahasa": "unknown",
                "akurasi": 0.0,
                "severity": "UNKNOWN",
                "driveability": "UNKNOWN",
                "diagnosa_ai": "Kerusakan belum teridentifikasi.",
                "saran_tindakan": "Berhenti di tempat aman dan cek manual.",
                "tips_bengkel": "Bawa ke bengkel terdekat untuk dicek.",
                "estimasi_biaya": "Bervariasi"
            }
            
    except Exception as e:
        logger.error(f"Error AI: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# 🚀 ENDPOINT BARU UNTUK AI KAMERA / VISION
@app.post("/analisis_gambar")
async def analisis_gambar(file: UploadFile = File(...)):
    try:
        logger.info(
    f"Menerima file gambar: {file.filename}"
)
        result = await analyze_image_with_ai(file)
        return result
    except Exception as e:
        logger.error(f"Error AI Kamera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lapor_error")
def lapor_error(data: ErrorReportInput):
    try:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        
        if bot_token and chat_id:
            text = f"🚨 LAPORAN V2 MELESET\n\nKeluhan: {data.keluhan}\nDiagnosa AI: {data.diagnosa_ai}"
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(telegram_url, json={"chat_id": chat_id, "text": text}, timeout=3)
            
        return {"status": "success", "pesan": "Laporan terkirim!"}
    except Exception as e:
        return {"status": "error", "pesan": str(e)}
