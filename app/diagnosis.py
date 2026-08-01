import logging
from app.language import normalize_slang, detect_language
from app.search import semantic_search
from app.formatter import format_response
from app.loader import load_cars, load_motorcycles

logger = logging.getLogger("MontirPintarDiagnosis")

# ==========================================
# INISIALISASI DATABASE AMAN
# ==========================================
try:
    # Memuat data (Fallback ke list kosong [] jika None)
    DATABASE_CARS = load_cars() or []
    DATABASE_MOTORCYCLES = load_motorcycles() or []
    
    # Validasi tipe data (Mencegah TypeError jika JSON berupa Dictionary)
    if isinstance(DATABASE_CARS, dict):
        DATABASE_CARS = list(DATABASE_CARS.values())
    if isinstance(DATABASE_MOTORCYCLES, dict):
        DATABASE_MOTORCYCLES = list(DATABASE_MOTORCYCLES.values())
        
    # Penggabungan List yang aman
    FULL_DATABASE = list(DATABASE_CARS) + list(DATABASE_MOTORCYCLES)

except Exception as e:
    logger.error(f"Kritis: Gagal memuat atau menggabungkan dataset di diagnosis.py -> {e}")
    # Jika gagal, API tetap hidup dengan database kosong, bukan crash!
    FULL_DATABASE = []

# ==========================================
# FUNGSI UTAMA DIAGNOSA
# ==========================================
def analyze_symptom(user_input: str):
    lang = detect_language(user_input)
    normalized_input = normalize_slang(user_input)
    
    # Proses pencarian semantik (NLP)
    best_match, score = semantic_search(normalized_input, FULL_DATABASE, lang)
    
    return format_response(best_match, score, lang)
