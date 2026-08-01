import json
import os
from app.language import normalize_slang, detect_language
from app.search import semantic_search
from app.formatter import format_response
from app.loader import load_cars
from app.loader import load_motorcycles

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_json_db(filename):
    try:
        with open(os.path.join(BASE_DIR, "dataset", filename), "r") as f:
            return json.load(f)
    except Exception:
        return []

# Muat database mobil dan motor
DATABASE_CARS = load_cars()
DATABASE_MOTORCYCLES = load_motorcycles()
FULL_DATABASE = DATABASE_CARS + DATABASE_MOTORCYCLES

def analyze_symptom(user_input: str):
    lang = detect_language(user_input)
    normalized_input = normalize_slang(user_input)
    
    best_match, score = semantic_search(normalized_input, FULL_DATABASE, lang)
    
    return format_response(best_match, score, lang)
