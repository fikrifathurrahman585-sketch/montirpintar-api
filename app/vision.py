import os
import json
import base64
import requests
from fastapi import UploadFile, HTTPException

# API Key Gemini
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Model Gemini (mudah diganti nanti)
GEMINI_MODEL = "gemini-2.5-flash"


async def analyze_image_with_ai(file: UploadFile):

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="API Key Gemini belum dikonfigurasi."
        )

    try:

        # ==========================
        # Baca gambar
        # ==========================

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="File gambar kosong."
            )

        mime_type = file.content_type or "image/jpeg"

        base64_image = base64.b64encode(image_bytes).decode("utf-8")

        # ==========================
        # Prompt
        # ==========================

        prompt = """
Anda adalah seorang Kepala Mekanik Mobil dan Motor dengan pengalaman 20 tahun.

Analisis foto komponen kendaraan ini.

Perhatikan:

- kebocoran oli
- kebocoran coolant
- kebocoran minyak rem
- kebocoran power steering
- kebocoran shock
- CV Joint
- seal gardan
- kerusakan mekanis
- keausan

Gunakan logika pakar berikut:

1. Sambungan Mesin + Transmisi + Oli Merah = Bocor Seal Input Transmisi
2. Sambungan Mesin + Transmisi + Oli Hitam = Bocor Rear Main Seal
3. Area Rem + Brake Fluid = Bocor Minyak Rem
4. Radiator + Coolant = Bocor Radiator
5. Shock + Oli = Seal Shock Bocor
6. CV Joint + Grease = Boot CV Sobek
7. Rack Steer + Oli = Bocor Power Steering
8. Gardan + Gear Oil = Bocor Seal Gardan

Jawaban WAJIB JSON.

{
  "status":"success",
  "bahasa":"id",
  "akurasi":95,
  "diagnosa_ai":"",
  "solusi":"",
  "saran_tindakan":"",
  "tips_bengkel":"",
  "estimasi_biaya":"",
  "severity":"INFO",
  "driveability":"NORMAL"
}

Jika gambar tidak jelas maka isi diagnosa_ai:

"Foto tidak dapat diidentifikasi sebagai komponen kendaraan. Harap foto ulang bagian yang bermasalah secara lebih jelas."

JANGAN memberikan markdown.
JANGAN memberikan penjelasan.
Hanya JSON.
"""

        # ==========================
        # Payload
        # ==========================

        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        },
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": base64_image
                            }
                        }
                    ]
                }
            ]
        }

        # ==========================
        # Request
        # ==========================

        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
        )

        response = requests.post(
            url,
            headers={
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=60
        )

        # ==========================
        # Error Google
        # ==========================

        if response.status_code != 200:

            try:
                error_json = response.json()
            except Exception:
                error_json = response.text

            raise Exception(error_json)

        response_data = response.json()

        # ==========================
        # Validasi response
        # ==========================

        if "candidates" not in response_data:
            raise Exception(
                f"Response Gemini tidak memiliki candidates.\n{response_data}"
            )

        raw_text = (
            response_data["candidates"][0]
            ["content"]["parts"][0]["text"]
            .strip()
        )

        # ==========================
        # Bersihkan markdown
        # ==========================

        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "", 1)

        if raw_text.startswith("```"):
            raw_text = raw_text.replace("```", "", 1)

        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        raw_text = raw_text.strip()

        # ==========================
        # Parse JSON
        # ==========================

        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError:
            raise Exception(
                f"AI tidak mengembalikan JSON.\n\n{raw_text}"
            )

        return result

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Gagal memproses gambar dengan AI: {str(e)}"
        )
