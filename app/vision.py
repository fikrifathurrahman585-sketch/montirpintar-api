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
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Prompt khusus agar AI bertindak sebagai mekanik senior dengan Logika Pakar
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
