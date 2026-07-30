def format_response(match, score, lang):
    if match and score > 0.15:
        lang_data = match["language"][lang]
        cost = match["cost"]["idr"] if lang == "id" else match["cost"]["usd"]
        
        return {
            "status": "success",
            "language": lang,
            "confidence": round(score * 100, 2),
            "severity": match.get("severity", "WARNING"),
            "driveability": match.get("driveability", "LIMITED"),
            
            # 🚀 FORMAT BARU V2
            "main_problem": lang_data["problem"],
            "recommended_action": lang_data["action"],
            "garage_tip": lang_data["garage_tip"],
            "estimated_cost": cost,
            
            # 🛡️ FORMAT LAMA (Agar Android saat ini tidak crash)
            "diagnosa_ai": lang_data["problem"],
            "saran_tindakan": lang_data["action"],
            "tips_bengkel": lang_data["garage_tip"],
            "estimasi_biaya": cost
        }
    else:
        return {
            "status": "success",
            "language": lang,
            "confidence": 0.0,
            "severity": "UNKNOWN",
            "driveability": "UNKNOWN",
            "main_problem": "Kerusakan belum teridentifikasi / Unknown issue.",
            "diagnosa_ai": "Kerusakan belum teridentifikasi secara spesifik.",
            "saran_tindakan": "Berhenti di tempat aman dan cek manual.",
            "tips_bengkel": "Bawa ke bengkel terdekat untuk dicek manual.",
            "estimasi_biaya": "Bervariasi"
        }
