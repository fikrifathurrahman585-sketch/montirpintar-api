import os
import json
import base64
import requests
from fastapi import UploadFile, HTTPException

# Konfigurasi API Key Gemini (Ambil dari Environment Variable Vercel)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

async def analyze_image_with_ai(file: UploadFile):
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="API Key Gemini belum dikonfigurasi di server."
        )
    
    try:
        # 1. Baca gambar dari Android dan ubah ke format Base64
        image_bytes = await file.read()
        base64_image = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = file.content_type or "image/jpeg"
        
        # 2. Prompt Logika Pakar
        prompt = """Anda adalah seorang Kepala Mekanik Mobil dan Motor dengan pengalaman 20 tahun. 
Analisis foto komponen kendaraan yang dikirimkan ini. Identifikasi apakah ada kerusakan, kebocoran, keausan, atau masalah lainnya.

GUNAKAN LOGIKA PAKAR BERIKUT JIKA MELIHAT KEBOCORAN CAIRAN ATAU KERUSAKAN:
1. Sambungan Mesin & Transmisi + Oli Warna Merah/Kemerahan = "Bocor Seal Input Transmisi (Seal Torque Converter)". (Oli Matic rembes).
2. Sambungan Mesin & Transmisi + Oli Warna Hitam/Coklat Pekat = "Bocor Seal Kruk As Belakang (Rear Main Seal)". (Oli Mesin rembes).
3. Area Velg/Piringan Cakram/Selang Rem/Master Rem + Cairan Bening/Kekuningan Agak Licin = "Bocor Minyak Rem (Brake Fluid)". (BAHAYA FATAL, Rem bisa blong).
4. Area Depan/Bawah Bumper/Radiator + Cairan Encer Merah/Hijau/Biru = "Bocor Air Radiator (Coolant)". (Bisa bikin mesin overheat).
5. Area Tabung/As Shockbreaker Depan/Belakang + Basah Oli = "Seal Shockbreaker Bocor/Jebol". (Suspensi mati/keras).
6. Area Karet As Roda (CV Joint) + Gemuk/Grease Hitam Berceceran = "Karet Boot CV Joint Sobek". (Bisa bikin as roda berbunyi kletek-kletek).
7. Area Rack Steer (Bawah Setir) + Oli Kemerahan/Kecoklatan = "Bocor Oli Power Steering". (Setir bisa jadi berat atau bunyi dengung).
8. Area Gardan (Roda Belakang RWD) + Oli Kental Bau Menyengat = "Bocor Seal Gardan".

Berdasarkan foto yang diupload, berikan diagnosa pasti menggunakan pedoman di atas jika cocok. Cermati warna cairan dan area komponennya!

Berikan jawaban dalam format JSON murni (tanpa teks lain di luar JSON) dengan struktur kunci berikut:
{
  "status": "success",
  "bahasa": "id",
  "akurasi": 98.0,
  "diagnosa_ai": "[Jelaskan secara spesifik bagian yang rusak atau bocor, misal: Kebocoran Minyak Rem pada Kaliper]",
  "solusi": "[Berikan tindakan perbaikan darurat dan tips penanganan di bengkel]",
  "saran_tindakan": "[Tindakan darurat untuk pengendara, misal: JANGAN JALANKAN KENDARAAN JIKA MINYAK REM BOCOR]",
  "tips_bengkel": "[Kalimat yang harus diucapkan ke mekanik bengkel]",
  "estimasi_biaya": "[Estimasi biaya perbaikan dalam Rupiah, misal: Rp 300.000 - Rp 1.000.000]",
  "severity": "WARNING",
  "driveability": "LIMITED"
}
Jika gambar tidak jelas atau bukan bagian kendaraan, berikan diagnosa_ai: "Foto tidak dapat diidentifikasi sebagai komponen kendaraan. Harap foto ulang bagian yang bermasalah secara lebih jelas."
"""
        
        # 3. Siapkan format Payload JSON standar Google REST API
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": base64_image
                        }
                    }
                ]
            }]
        }
        
        # 4. Tembak langsung ke Endpoint Gemini 1.5 Flash menggunakan Requests (PERBAIKAN URL DENGAN -latest)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        
        # Cek jika ada error dari Google
        if response.status_code != 200:
            raise Exception(f"API Error: {response_data}")
            
        # 5. Ambil teks hasil balasan AI
        raw_text = response_data['candidates'][0]['content']['parts'][0]['text'].strip()
        
        # Bersihkan text dari format markdown ```json jika AI menambahkannya
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
            
        result_json = json.loads(raw_text.strip())
        return result_json
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal memproses gambar dengan AI: {str(e)}")
