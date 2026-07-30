import difflib
import json
import os

# Muat database dari folder dataset
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, "dataset", "cars.json"), "r") as f:
    DATABASE_CARS = json.load(f)

with open(os.path.join(BASE_DIR, "dataset", "slang.json"), "r") as f:
    SLANG_DICT = json.load(f)

def normalize_text(text: str) -> str:
    """Mengubah kata gaul (slang) menjadi bahasa standar"""
    words = text.lower().split()
    normalized_words = [SLANG_DICT.get(w, w) for w in words]
    return " ".join(normalized_words)

def analyze_symptom(user_input: str):
    normalized_input = normalize_text(user_input)
    
    best_match = None
    highest_score = 0.0
    detected_lang = "id"
    
    for case in DATABASE_CARS:
        # Cek Bahasa Indonesia
        for symptom in case["language"]["id"]["symptoms"]:
            score = difflib.SequenceMatcher(None, normalized_input, symptom).ratio()
            if score > highest_score:
                highest_score = score
                best_match = case
                detected_lang = "id"
                
        # Cek Bahasa Inggris
        for symptom in case["language"]["en"]["symptoms"]:
            score = difflib.SequenceMatcher(None, normalized_input, symptom).ratio()
            if score > highest_score:
                highest_score = score
                best_match = case
                detected_lang = "en"
                
    if highest_score > 0.15 and best_match:
        lang_data = best_match["language"][detected_lang]
        cost = best_match["cost"]["idr"] if detected_lang == "id" else best_match["cost"]["usd"]
        
        return {
            "status": "success",
            "bahasa": detected_lang,
            "akurasi": round(highest_score * 100, 2),
            "severity": best_match["severity"],
            "driveability": best_match["driveability"],
            # KOMPATIBILITAS ANDROID (Tetap gunakan key lama)
            "diagnosa_ai": lang_data["problem"],
            "saran_tindakan": lang_data["action"],
            "tips_bengkel": lang_data["garage_tip"],
            "estimasi_biaya": cost
        }
        
    return None
