def format_response(match, score, lang):
    if match and score > 0.15:
        lang_data = match["language"][lang]
        cost = match["cost"]["idr"] if lang == "id" else match["cost"]["usd"]
        
        return {
            "status": "success",
            
            # 🛡️ FORMAT LAMA (V1) AGAR ANDROID TIDAK CRASH
            "bahasa": lang,
            "akurasi": round(score * 100, 2),
            "diagnosa_ai": lang_data["problem"],
            "saran_tindakan": lang_data["action"],
            "tips_bengkel": lang_data["garage_tip"],
            "estimasi_biaya": cost,
            
            # 🚀 FORMAT BARU (V2) UNTUK PENGEMBANGAN SELANJUTNYA
            "language": lang,
            "confidence": round(score * 100, 2),
            "severity": match.get("severity", "WARNING"),
            "driveability": match.get("driveability", "LIMITED"),
            "main_problem": lang_data["problem"],
            "recommended_action": lang_data["action"],
            "garage_tip": lang_data["garage_tip"],
            "estimated_cost": cost
        }
    else:
        return {
            "status": "success",
            
            # 🛡️ FORMAT LAMA (V1)
            "bahasa": lang,
            "akurasi": 0.0,
            "diagnosa_ai": "Kerusakan belum teridentifikasi secara spesifik.",
            "saran_tindakan": "Berhenti di tempat aman dan cek manual.",
            "tips_bengkel": "Bawa ke bengkel terdekat untuk dicek manual.",
            "estimasi_biaya": "Bervariasi",
            
            # 🚀 FORMAT BARU (V2)
            "language": lang,
            "confidence": 0.0,
            "severity": "UNKNOWN",
            "driveability": "UNKNOWN",
            "main_problem": "Kerusakan belum teridentifikasi / Unknown issue.",
            "recommended_action": "Berhenti di tempat aman dan cek manual.",
            "garage_tip": "Bawa ke bengkel terdekat untuk dicek manual.",
            "estimated_cost": "Bervariasi"
        }
