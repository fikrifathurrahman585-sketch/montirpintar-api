from fastapi import FastAPI
from pydantic import BaseModel
import requests
import numpy as np

app = FastAPI(title="MontirPintar API Lite")

# ⚠️ PASTIKAN ANDA MENGISI TOKEN HUGGING FACE DI SINI
HF_TOKEN = "MASUKKAN_TOKEN_HUGGING_FACE_ANDA_DISINI" 
API_URL = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

# Database Kasus Bengkel
data_bengkel = [
    {"id": "MBL_MS_01", "gejala_masalah": "Mesin mobil bunyi tek-tek kencang saat digas...", "diagnosa_ai": "Metal Duduk/Jalan Aus", "solusi": "Turun mesin...", "estimasi_biaya": "Rp 3.000.000"},
    {"id": "MTR_KL_01", "gejala_masalah": "Motor mati mendadak di jalan atau lampu merah, tombol stater ditekan cuma bunyi cetek-cetek, dinamo starter diam tidak mau muter, dan klakson nyala redup.", "diagnosa_ai": "Aki Drop / Bendik Starter", "solusi": "Cek tegangan aki. Ganti bendik baru.", "estimasi_biaya": "Rp 60.000 - Rp 150.000"},
    # Silakan tambah/copy data bengkel Anda yang lain di bawah ini
]

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

# Variabel Global untuk menyimpan memori AI agar tidak memanggil HF berulang kali
GLOBAL_EMBEDDINGS = None

def get_embedding(text_list):
    response = requests.post(API_URL, headers=headers, json={"inputs": text_list})
    if response.status_code == 200:
        return np.array(response.json())
    else:
        raise Exception(f"Gagal memanggil HF API: {response.text}")

def cos_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

class KeluhanInput(BaseModel):
    keluhan: str

@app.get("/")
def home():
    return {"status": "aktif", "pesan": "Server MontirPintar siap melayani!"}

@app.post("/diagnosa")
def diagnosa_ai(data: KeluhanInput):
    global GLOBAL_EMBEDDINGS
    try:
        # LAZY LOADING: Minta data ke HF hanya saat ada user yang bertanya
        if GLOBAL_EMBEDDINGS is None:
            gejala_list = [item["gejala_masalah"] for item in data_bengkel]
            GLOBAL_EMBEDDINGS = get_embedding(gejala_list)

        # Dapatkan vektor dari keluhan user
        input_embedding = get_embedding([data.keluhan])[0]
        
        # Hitung kecocokan
        best_match_idx = -1
        best_score = -1.0
        
        for i, db_emb in enumerate(GLOBAL_EMBEDDINGS):
            score = cos_sim(input_embedding, db_emb)
            if score > best_score:
                best_score = score
                best_match_idx = i
                
        if best_score > 0.4:
            hasil = data_bengkel[best_match_idx]
            return {
                "status": "success",
                "diagnosa_ai": hasil["diagnosa_ai"],
                "solusi": hasil["solusi"],
                "estimasi_biaya": hasil["estimasi_biaya"],
                "akurasi": round(float(best_score) * 100, 2)
            }
        else:
            return {"status": "error", "pesan": "Keluhan belum dikenali."}
            
    except Exception as e:
        return {"status": "error", "pesan": str(e)}

# Endpoint Telegram untuk Laporan Error (Optional)
@app.post("/lapor_error")
def lapor_error(data: dict):
    return {"status": "success"}
