import logging

from rapidfuzz import fuzz

from app.rules import detect_system
from app.scorer import score_keywords

logger = logging.getLogger("MontirPintarSearch")


# =====================================================
# Semantic Search V2
# =====================================================

def semantic_search(user_input, database, lang="id"):

    system = detect_system(user_input)

    # =====================================================
    # FILTER BERDASARKAN SYSTEM
    # =====================================================

    candidates = []

    if system:

        for item in database:

            item_system = (
                item.get("system")
                or item.get("system_name")
                or ""
            ).lower()

            if item_system == system:
                candidates.append(item)

    # jika tidak ada hasil, gunakan semua dataset
    if len(candidates) == 0:
        candidates = database

    logger.info(
        "System=%s Candidate=%d",
        system,
        len(candidates)
    )

    # =====================================================
    # RANKING
    # =====================================================

    best_item = None
    best_score = -1

    for item in candidates:

        symptom_list = []

        if lang == "en":

            symptom_list.extend(
                item.get("symptoms", {}).get("en", [])
            )

        else:

            symptom_list.extend(
                item.get("symptoms", {}).get("id", [])
            )

        semantic_score = 0

        for symptom in symptom_list:

            semantic_score = max(
                semantic_score,
                fuzz.token_sort_ratio(
                    user_input.lower(),
                    symptom.lower()
                )
            )

        keyword_bonus = score_keywords(
            user_input,
            system if system else ""
        )

        priority_bonus = item.get("priority", 0) * 2

        final_score = (
            semantic_score
            + keyword_bonus
            + priority_bonus
        )

        if final_score > best_score:

            best_score = final_score
            best_item = item

    logger.info(
        "BEST SCORE = %s",
        best_score
    )

    return best_item, best_score
