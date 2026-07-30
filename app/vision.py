import os
import google.generativeai as genai
from fastapi import UploadFile, HTTPException
import json

# Konfigurasi API Key Gemini (Ambil dari Environment Variable Vercel)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

async def analyze_image_with_ai(file: UploadFile):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="API Key Gemini belum dikonfigurasi di server."
        )
    
    try:
        # Baca bytes dari file gambar yang dikirim Android
        image_bytes = await file.read()
        
        # Gunakan model Gemini Flash yang cepat dan gratis/murah untuk Multimodal
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt khusus agar AI bertindak sebagai mekanik senior
        prompt = """
        Anda adalah seorang mekanik mobil dan motor profesional yang ahli. Analisis foto komponen kendaraan yang dikirimkan ini.
        Identifikasi apakah ada kerusakan, kebocoran (oli/radiator/minyak rem), keausan, atau masalah lainnya.
        
        Berikan jawaban dalam format JSON murni (tanpa teks lain di luar JSON) dengan struktur kunci berikut:
        {
          "status": "success",
          "bahasa": "id",
          "akurasi": 95.0,
          "diagnosa_ai": "[Jelaskan secara spesifik bagian yang rusak atau bocor, misal: Kebocoran oli pada seal kruk as]",
          "solusi": "[Berikan tindakan perbaikan darurat dan tips penanganan di bengkel]",
          "saran_tindakan": "[Tindakan darurat untuk pengendara]",
          "tips_bengkel": "[Kalimat yang harus diucapkan ke mekanik bengkel]",
          "estimasi_biaya": "[Estimasi biaya perbaikan dalam Rupiah, misal: Rp 300.000 - Rp 1.000.000]",
          "severity": "WARNING",
          "driveability": "LIMITED"
        }
        Jika gambar tidak jelas atau bukan bagian kendaraan, berikan diagnosa_ai: "Foto tidak dapat diidentifikasi sebagai komponen kendaraan. Harap foto ulang bagian yang bermasalah."
        """
        
        # Kirim gambar dan prompt ke Gemini
        response = model.generate_content([
            prompt,
            {
                "mime_type": file.content_type,
                "data": image_bytes
            }
        ])
        
        # Bersihkan response text dari markdown block ```json ... ``` jika ada
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        result_json = json.loads(raw_text.strip())
        return result_json
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses gambar dengan AI: {str(e)}")
