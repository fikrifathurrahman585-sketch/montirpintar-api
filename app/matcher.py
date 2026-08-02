from rapidfuzz import fuzz

from app.rules import (
    detect_system,
    detect_vehicle
)

from app.scorer import score_bonus


# ==========================================================
# HITUNG SEMANTIC SCORE
# ==========================================================

def semantic_score(user_input, symptoms):

    highest = 0

    for symptom in symptoms:

        score = fuzz.token_set_ratio(
            user_input.lower(),
            symptom.lower()
        )

        if score > highest:
            highest = score

    return highest


# ==========================================================
# RANKING ENGINE
# ==========================================================

def rank_candidates(
    user_input,
    database,
    lang="id"
):

    detected_system = detect_system(user_input)
    detected_vehicle = detect_vehicle(user_input)

    ranking = []

    for item in database:

        # ---------------------------------
        # FILTER VEHICLE
        # ---------------------------------

        vehicle = item.get(
            "vehicle",
            ""
        ).lower()

        if detected_vehicle:

            if vehicle != detected_vehicle:
                continue

        # ---------------------------------
        # FILTER SYSTEM
        # ---------------------------------

        system = item.get(
            "system",
            ""
        ).lower()

        if detected_system:

            if system != detected_system:
                continue

        # ---------------------------------
        # AMBIL GEJALA
        # ---------------------------------

        language = item.get("language", {})

        if lang not in language:
            continue

        symptoms = language[lang].get(
            "symptoms",
            []
        )

        semantic = semantic_score(
            user_input,
            symptoms
        )

        bonus = score_bonus(
            user_input,
            item
        )

        final_score = semantic + bonus

        ranking.append(
            {
                "item": item,
                "semantic": semantic,
                "bonus": bonus,
                "score": final_score
            }
        )

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking


# ==========================================================
# BEST MATCH
# ==========================================================

def best_match(
    user_input,
    database,
    lang="id"
):

    ranking = rank_candidates(
        user_input,
        database,
        lang
    )

    if len(ranking) == 0:
        return None, 0

    best = ranking[0]

    return (
        best["item"],
        best["score"]
    )


# ==========================================================
# TOP MATCHES
# ==========================================================

def top_matches(
    user_input,
    database,
    lang="id",
    limit=5
):

    ranking = rank_candidates(
        user_input,
        database,
        lang
    )

    return ranking[:limit]
