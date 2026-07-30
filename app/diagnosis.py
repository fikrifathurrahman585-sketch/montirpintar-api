import json
import os
from app.language import normalize_slang, detect_language
from app.search import semantic_search
from app.formatter import format_response

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load Database JSON
def load_json_db(filename):
    try:
        with open(os.path.join(BASE_DIR, "dataset", filename), "r") as f:
            return json.load(f)
    except Exception:
        return []

DATABASE_CARS = load_json_db("cars.json")
DATABASE_MOTORCYCLES = load_json_db("motorcycles.json")
FULL_DATABASE = DATABASE_CARS + DATABASE_MOTORCYCLES

def analyze_symptom(user_input: str):
    # 1. Deteksi Bahasa
    lang = detect_language(user_input)
    
    # 2. Normalisasi Slang (Ubah kata gaul)
    normalized_input = normalize_slang(user_input)
    
    # 3. Cari di Database menggunakan Semantic Search
    best_match, score = semantic_search(normalized_input, FULL_DATABASE, lang)
    
    # 4. Rapikan Output
    return format_response(best_match, score, lang)
