from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
import requests
from app.diagnosis import analyze_symptom
from app.vision import analyze_image_with_ai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MontirPintarAPIV2")

app = FastAPI(title="MontirPintar AI v2")

class KeluhanInput(BaseModel):
    keluhan: str

class ErrorReportInput(BaseModel):
    keluhan: str
    diagnosa_ai: str

@app.get("/")
def home():
    return {"status": "aktif", "version": "v2.0", "pesan": "MontirPintar API v2 (Modular) Berjalan!"}

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
        logger.info(f"Menerima file gambar untuk analisis: {file.filename}")
        result = await analyze_image_with_ai(file)
        return result
    except Exception as e:
        logger.error(f"Error AI Kamera: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/lapor_error")
def lapor_error(data: ErrorReportInput):
    try:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN","8739496643:AAFRM2JtXrPe2s5DRwTPM-sceC6ctah2Jsg")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID","8875393494")
        
        if bot_token and chat_id:
            text = f"🚨 LAPORAN V2 MELESET\n\nKeluhan: {data.keluhan}\nDiagnosa AI: {data.diagnosa_ai}"
            telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
            requests.post(telegram_url, json={"chat_id": chat_id, "text": text}, timeout=3)
            
        return {"status": "success", "pesan": "Laporan terkirim!"}
    except Exception as e:
        return {"status": "error", "pesan": str(e)}
