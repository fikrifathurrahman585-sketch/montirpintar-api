import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Muat Kamus Slang
try:
    with open(os.path.join(BASE_DIR, "dataset", "slang.json"), "r") as f:
        SLANG_DICT = json.load(f)
except Exception:
    SLANG_DICT = {}

def normalize_slang(text: str) -> str:
    """Mengubah kata gaul (slang) menjadi bahasa standar mesin"""
    words = text.lower().split()
    normalized = [SLANG_DICT.get(w, w) for w in words]
    return " ".join(normalized)

def detect_language(text: str) -> str:
    """Auto-detect bahasa berdasarkan kata kunci sederhana"""
    en_keywords = {"is", "my", "car", "engine", "when", "the", "noise", "jerks", "stalls"}
    id_keywords = {"mobil", "saya", "mesin", "saat", "bunyi", "jedug", "rusak", "kalau"}
    
    text_words = set(text.lower().split())
    en_score = len(text_words.intersection(en_keywords))
    id_score = len(text_words.intersection(id_keywords))
    
    return "en" if en_score > id_score else "id"
