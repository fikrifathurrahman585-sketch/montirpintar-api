from datetime import datetime


# ==========================================================
# NORMALIZE SCORE
# ==========================================================

def normalize_score(score):

    try:

        score = float(score)

    except Exception:

        score = 0

    # score semantic biasanya 0-100
    if score > 100:
        score = 100

    if score < 0:
        score = 0

    return round(score, 2)


# ==========================================================
# CONFIDENCE LEVEL
# ==========================================================

def confidence_level(score):

    if score >= 90:
        return "VERY_HIGH"

    if score >= 75:
        return "HIGH"

    if score >= 60:
        return "MEDIUM"

    if score >= 40:
        return "LOW"

    return "VERY_LOW"


# ==========================================================
# FORMAT RESPONSE
# ==========================================================

def format_response(match, score, lang):

    score = normalize_score(score)

    # ======================================================
    # DATA DITEMUKAN
    # ======================================================

    if match and score >= 45:

        lang_data = match["language"][lang]

        cost = (
            match["cost"]["idr"]
            if lang == "id"
            else match["cost"]["usd"]
        )

        solusi = (
            f"{lang_data['action']}\n\n"
            f"Tips Bengkel:\n"
            f"{lang_data['garage_tip']}"
        )

        return {

            "status": "success",

            "bahasa": lang,

            "akurasi": score,

            "confidence": score,

            "confidence_level": confidence_level(score),

            "diagnosa_ai": lang_data["problem"],

            "main_problem": lang_data["problem"],

            "solusi": solusi,

            "saran_tindakan": lang_data["action"],

            "recommended_action": lang_data["action"],

            "tips_bengkel": lang_data["garage_tip"],

            "garage_tip": lang_data["garage_tip"],

            "estimasi_biaya": cost,

            "estimated_cost": cost,

            "severity": match.get(
                "severity",
                "WARNING"
            ),

            "driveability": match.get(
                "driveability",
                "LIMITED"
            ),

            "language": lang,

            "engine": "MontirPintar Hybrid AI v2",

            "timestamp": datetime.utcnow().isoformat()

        }

    # ======================================================
    # FALLBACK
    # ======================================================

    if lang == "en":

        return {

            "status": "success",

            "bahasa": "en",

            "akurasi": 0,

            "confidence": 0,

            "confidence_level": "UNKNOWN",

            "diagnosa_ai": "The damage cannot yet be identified with sufficient confidence.",

            "main_problem": "Unknown issue.",

            "solusi": "Please visit the nearest repair shop for a manual inspection.",

            "saran_tindakan": "Drive carefully and have the vehicle inspected.",

            "recommended_action": "Manual inspection is recommended.",

            "tips_bengkel": "Ask the mechanic to perform a full diagnostic.",

            "garage_tip": "Request a complete inspection before replacing parts.",

            "estimasi_biaya": "Unknown",

            "estimated_cost": "Unknown",

            "severity": "UNKNOWN",

            "driveability": "UNKNOWN",

            "language": "en",

            "engine": "MontirPintar Hybrid AI v2",

            "timestamp": datetime.utcnow().isoformat()

        }

    # ======================================================
    # FALLBACK INDONESIA
    # ======================================================

    return {

        "status": "success",

        "bahasa": "id",

        "akurasi": 0,

        "confidence": 0,

        "confidence_level": "UNKNOWN",

        "diagnosa_ai": "Kerusakan belum dapat diidentifikasi secara akurat.",

        "main_problem": "Kerusakan belum dikenali.",

        "solusi": "Silakan lakukan pemeriksaan manual di bengkel terpercaya.",

        "saran_tindakan": "Hindari penggunaan kendaraan apabila muncul gejala yang membahayakan.",

        "recommended_action": "Lakukan pemeriksaan manual.",

        "tips_bengkel": "Minta mekanik melakukan pemeriksaan menyeluruh sebelum mengganti komponen.",

        "garage_tip": "Lakukan diagnosis manual.",

        "estimasi_biaya": "Belum diketahui",

        "estimated_cost": "Belum diketahui",

        "severity": "UNKNOWN",

        "driveability": "UNKNOWN",

        "language": "id",

        "engine": "MontirPintar Hybrid AI v2",

        "timestamp": datetime.utcnow().isoformat()

    }
