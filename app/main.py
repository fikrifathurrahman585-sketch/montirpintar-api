import logging
import os
import sys
import time

import google.generativeai as genai
import requests

from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.responses import JSONResponse

from pydantic import BaseModel

from app.loader import (
    load_cars,
    load_motorcycles
)

from app.validator import run_validation
from app.diagnosis import analyze_symptom
from app.vision import analyze_image_with_ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MontirPintarAPIV2")

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
    lang: str = "id"

class ErrorReportInput(BaseModel):
    keluhan: str
    diagnosa_ai: str


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.exception(exc)

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": "Internal Server Error"
        }
    )


@app.middleware("http")
async def log_requests(request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start

    logger.info(
        "%s %s %.3fs",
        request.method,
        request.url.path,
        duration
    )
    return response


@app.get("/health", tags=["System"])
def health():
    errors = run_validation()

    return {
        "status": "healthy",
        "validator": "PASS" if not errors else "FAIL"
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

    errors = run_validation()

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
            "total": len(cars) + len(motorcycles)
        },
        "validator": {
            "status": "PASS" if len(errors) == 0 else "FAIL",
            "error_count": len(errors)
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
        
        # BARIS INI SUDAH DIPERBAIKI INDENTASINYA
        response.raise_for_status()
        return response.json()
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

@app.post(
    "/diagnosa",
    tags=["Diagnosis"]
)
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
@app.post(
    "/analisis_gambar",
    tags=["Vision"]
)
async def analisis_gambar(file: UploadFile = File(...)):
    try:
        logger.info(f"Menerima file gambar untuk analisis: {file.filename}")
        result = await analyze_image_with_ai(file)
        return result
    except Exception as e:
        logger.error(f"Error AI Kamera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post(
    "/lapor_error",
    tags=["System"]
)
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
