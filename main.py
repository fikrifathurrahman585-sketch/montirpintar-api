from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util
import requests
import os

app = FastAPI(title="MontirPintar API")

# Load model AI (Hanya dilakukan 1x saat server nyala)
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Database Bengkel (Bisa Anda tambahkan kasus-kasus sebelumnya di sini)
data_bengkel = [
    {"id": "MBL_MS_01", "gejala_masalah": "Mesin mobil bunyi tek-tek kencang saat digas...", "diagnosa_ai": "Metal Duduk/Jalan Aus", "solusi": "Turun mesin...", "estimasi_biaya": "Rp 3.000.000"},
    # ... (Copy paste semua data bengkel Anda dari Colab ke sini) ...
]

# Tanamkan Embeddings ke memori
gejala_list = [item["gejala_masalah"] for item in data_bengkel]
gejala_embeddings = model.encode(gejala_list, convert_to_tensor=True)

# Format Input dari Android
class KeluhanInput(BaseModel):
    keluhan: str

@app.get("/")
def home():
    return {"status": "aktif", "pesan": "Server MontirPintar siap melayani!"}

@app.post("/diagnosa")
def diagnosa_ai(data: KeluhanInput):
    try:
        keluhan_user = data.keluhan
        input_embedding = model.encode(keluhan_user, convert_to_tensor=True)
        cos_scores = util.cos_sim(input_embedding, gejala_embeddings)[0]
        
        import torch
        best_match_idx = torch.argmax(cos_scores).item()
        best_score = cos_scores[best_match_idx].item()
        
        if best_score > 0.4:
            hasil = data_bengkel[best_match_idx]
            return {
                "status": "success",
                "diagnosa_ai": hasil["diagnosa_ai"], # Sesuaikan dengan key Anda
                "solusi": hasil["solusi"],
                "estimasi_biaya": hasil["estimasi_biaya"],
                "akurasi": round(best_score * 100, 2)
            }
        else:
            return {"status": "error", "pesan": "Keluhan kurang spesifik."}
    except Exception as e:
        return {"status": "error", "pesan": str(e)}

# Endpoint Telegram (Jika Anda ingin pertahankan fitur laporan meleset)
@app.post("/lapor_error")
def lapor_error(data: dict):
    # Logika telegram Anda masukkan ke sini
    return {"status": "success"}