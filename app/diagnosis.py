import logging

from app.language import (
    normalize_slang,
    detect_language
)

from app.search import semantic_search
from app.formatter import format_response
from app.loader import load_cars, load_motorcycles

logger = logging.getLogger("MontirPintarDiagnosis")


# =====================================================
# LOAD DATASET
# =====================================================

try:

    DATABASE_CARS = load_cars() or []
    DATABASE_MOTORCYCLES = load_motorcycles() or []

    if isinstance(DATABASE_CARS, dict):
        DATABASE_CARS = list(DATABASE_CARS.values())

    if isinstance(DATABASE_MOTORCYCLES, dict):
        DATABASE_MOTORCYCLES = list(DATABASE_MOTORCYCLES.values())

    FULL_DATABASE = DATABASE_CARS + DATABASE_MOTORCYCLES

    logger.info(
        "Dataset loaded : %d",
        len(FULL_DATABASE)
    )

except Exception as e:

    logger.exception(e)

    FULL_DATABASE = []


# =====================================================
# MAIN DIAGNOSIS
# =====================================================

def analyze_symptom(user_input: str, forced_lang: str = "id"):

    if forced_lang in ["id", "en"]:
        lang = forced_lang
    else:
        lang = detect_language(user_input)

    normalized_input = normalize_slang(user_input)

    best_match, score = semantic_search(
        normalized_input,
        FULL_DATABASE,
        lang
    )

    return format_response(
        best_match,
        score,
        lang
    )
