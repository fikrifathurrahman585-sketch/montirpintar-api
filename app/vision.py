import os
import json
import logging

import google.generativeai as genai

from fastapi import UploadFile, HTTPException

# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger("MontirPintarVision")

# ==========================================================
# GEMINI CONFIG
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# GANTI sesuai model yang benar-benar muncul di endpoint /models
MODEL_NAME = "gemini-3.5-flash-lite"

GENERATION_CONFIG = {
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json"
}

SAFETY_SETTINGS = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE"
    }
]

# ==========================================================
# PROMPT
# ==========================================================

PROMPT = """
Anda adalah Kepala Mekanik Senior Mobil dan Motor dengan pengalaman lebih dari 20 tahun.

Tugas Anda adalah menganalisis foto kendaraan.

Periksa kemungkinan:

- Kebocoran oli mesin
- Kebocoran oli transmisi
- Kebocoran coolant
- Kebocoran minyak rem
- Kebocoran power steering
- Seal shock bocor
- CV Joint
- Boot CV
- Gardan
- Differential
- Gearbox
- Waterpump
- Radiator
- Selang radiator
- Selang rem
- Kaliper
- Master rem
- Kompresor AC
- Baut hilang
- Retak
- Pecah
- Korosi
- Keausan
- Komponen patah

LOGIKA PAKAR

1. Oli merah pada sambungan mesin dan transmisi
= Seal Input Transmisi Bocor

2. Oli hitam pekat
= Rear Main Seal Bocor

3. Cairan bening kekuningan pada area rem
= Brake Fluid Bocor
Severity=DANGER
Driveability=STOP

4. Coolant merah/hijau/biru
= Radiator Bocor

5. Shock basah oli
= Seal Shock Bocor

6. Grease berceceran
= Boot CV Joint Sobek

7. Rack steer basah oli
= Seal Rack Steer Bocor

8. Gardan basah gear oil
= Seal Gardan Bocor

Jawab HANYA JSON.

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

Jika gambar blur, gelap, tidak fokus, atau bukan kendaraan maka isi diagnosa_ai:

"Foto tidak dapat diidentifikasi sebagai komponen kendaraan. Harap foto ulang bagian yang bermasalah secara lebih jelas."

JANGAN menggunakan markdown.
JANGAN menggunakan ```json.
Output WAJIB JSON VALID.
"""

# ==========================================================
# ANALISIS
# ==========================================================

async def analyze_image_with_ai(file: UploadFile):

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY belum dikonfigurasi."
        )

    try:

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="File gambar kosong."
            )

        filename = (file.filename or "").lower()

        if filename.endswith(".png"):
            mime_type = "image/png"
        elif filename.endswith(".webp"):
            mime_type = "image/webp"
        elif filename.endswith(".jpg") or filename.endswith(".jpeg"):
            mime_type = "image/jpeg"
        else:
            mime_type = "image/jpeg"

        logger.info("===== GEMINI VISION =====")
        logger.info("Filename : %s", filename)
        logger.info("MimeType : %s", mime_type)
        logger.info("Size     : %d bytes", len(image_bytes))

        model = genai.GenerativeModel(MODEL_NAME)

        response = model.generate_content(
            [
                PROMPT,
                {
                    "mime_type": mime_type,
                    "data": image_bytes
                }
            ],
            generation_config=GENERATION_CONFIG,
            safety_settings=SAFETY_SETTINGS
        )

        raw = (response.text or "").strip()

        logger.info("RAW RESPONSE:")
        logger.info(raw)

        if raw.startswith("```json"):
            raw = raw.replace("```json", "", 1)

        if raw.startswith("```"):
            raw = raw.replace("```", "", 1)

        if raw.endswith("```"):
            raw = raw[:-3]

        raw = raw.strip()

        result = json.loads(raw)

        required = [
            "status",
            "bahasa",
            "akurasi",
            "diagnosa_ai",
            "solusi",
            "saran_tindakan",
            "tips_bengkel",
            "estimasi_biaya",
            "severity",
            "driveability"
        ]

        for key in required:
            if key not in result:
                result[key] = ""

        return result

    except json.JSONDecodeError:

        logger.exception("JSON Decode Error")

        raise HTTPException(
            status_code=500,
            detail="AI tidak mengembalikan JSON yang valid."
        )

    except Exception as e:

        logger.exception("Vision Error")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
