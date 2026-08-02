import logging

from app.language import (
    normalize_slang,
    detect_language
)

from app.search import semantic_search
from app.formatter import format_response

logger = logging.getLogger("MontirPintarDiagnosis")


def analyze_symptom(
    user_input: str,
    forced_lang: str = "id"
):
    """
    Diagnosis Engine V2
    """

    if forced_lang in ["id", "en"]:
        lang = forced_lang
    else:
        lang = detect_language(user_input)

    normalized = normalize_slang(user_input)

    best_match, confidence = semantic_search(
        normalized,
        None,
        lang
    )

    return format_response(
        best_match,
        confidence,
        lang
    )
