import os
import json
import google.generativeai as genai

from fastapi import UploadFile, HTTPException

# ==========================================================
# Konfigurasi Gemini
# ==========================================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY belum dikonfigurasi.")

genai.configure(api_key=GEMINI_API_KEY)

# Gunakan model yang memang tersedia pada API Key Anda
MODEL_NAME = "gemini-3.5-flash"

GENERATION_CONFIG = {
    "response_mime_type": "application/json",
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048
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
# Prompt Pakar
# ==========================================================

PROMPT = """
Anda adalah Kepala Mekanik Mobil dan Motor profesional dengan pengalaman lebih dari 20 tahun.

Tugas Anda adalah menganalisis foto kendaraan yang diupload pengguna.

PERIKSA:

- Kebocoran oli mesin
- Kebocoran oli transmisi
- Kebocoran coolant
- Kebocoran minyak rem
- Kebocoran power steering
- Seal shock bocor
- CV Joint
- Gardan
- Boot As roda
- Selang radiator
- Selang rem
- Master rem
- Kaliper
- Water pump
- Kompresor AC
- Oli gardan
- Oli differential
- Oli gearbox
- Oli mesin
- Oli matic
- Kerusakan fisik
- Baut hilang
- Retak
- Pecah
- Aus

LOGIKA PAKAR:

1.
Jika terlihat oli merah pada sambungan mesin dan transmisi
=
Seal Input Transmisi Bocor.

2.
Jika terlihat oli hitam pekat pada sambungan mesin
=
Rear Main Seal Bocor.

3.
Jika terlihat cairan bening kekuningan di area rem
=
Brake Fluid Bocor.

Severity = DANGER

4.
Jika coolant merah/hijau/biru keluar dari radiator
=
Radiator Bocor.

5.
Jika shock basah oli
=
Seal Shock Bocor.

6.
Jika grease berceceran di CV Joint
=
Boot CV Joint Sobek.

7.
Jika power steering basah oli
=
Seal Rack Steer Bocor.

8.
Jika gardan basah gear oil
=
Seal Gardan Bocor.

Jawab HANYA JSON.

Format:

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

Jika foto blur, gelap, atau bukan kendaraan maka isi diagnosa_ai:

"Foto tidak dapat diidentifikasi sebagai komponen kendaraan. Harap foto ulang bagian yang bermasalah secara lebih jelas."

JANGAN menggunakan markdown.

JANGAN menggunakan ```json.

Output HARUS JSON valid.
"""


# ==========================================================
# Analisis AI Vision
# ==========================================================

async def analyze_image_with_ai(file: UploadFile):

    try:

        image_bytes = await file.read()

        if not image_bytes:
            raise HTTPException(
                status_code=400,
                detail="File gambar kosong."
            )

        mime_type = file.content_type or "image/jpeg"

        model = genai.GenerativeModel(MODEL_NAME)

generation_config = {
    "response_mime_type": "application/json",
    "temperature": 0.2,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048
}

response = model.generate_content(
    [
        PROMPT,
        {
            "mime_type": mime_type,
            "data": image_bytes
        }
    ],
    generation_config=generation_config
    safety_settings=SAFETY_SETTINGS
)

        raw = response.text.strip()

        if raw.startswith("```json"):
            raw = raw.replace("```json", "", 1)

        if raw.startswith("```"):
            raw = raw.replace("```", "", 1)

        if raw.endswith("```"):
            raw = raw[:-3]

        raw = raw.strip()

        result = json.loads(raw)

        return result

    except json.JSONDecodeError:

        raise HTTPException(
            status_code=500,
            detail="AI tidak mengembalikan JSON yang valid."
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Vision AI Error : {str(e)}"
        )
