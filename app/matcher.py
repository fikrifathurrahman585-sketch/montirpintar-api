from app.rules import detect_system
from app.scorer import score_keywords
from rapidfuzz import fuzz


def rank_candidates(user_input, database, lang):

    system = detect_system(user_input)

    ranking = []

    for item in database:

        # -----------------------------------
        # Filter system
        # -----------------------------------

        if system:

            if item.get("system", "").lower() != system:
                continue

        # -----------------------------------
        # Ambil gejala
        # -----------------------------------

        symptoms = item["language"][lang]["symptoms"]

        semantic = 0

        for symptom in symptoms:

            semantic = max(
                semantic,
                fuzz.token_set_ratio(
                    user_input.lower(),
                    symptom.lower()
                )
            )

        keyword = score_keywords(
            user_input,
            system if system else ""
        )

        priority = item.get("priority", 0) * 3

        severity = item.get("severity", "")

        severity_bonus = {

            "INFO": 0,
            "WARNING": 5,
            "DANGER": 10

        }.get(severity, 0)

        total = (
            semantic
            + keyword
            + priority
            + severity_bonus
        )

        ranking.append(

            (
                total,
                item
            )

        )

    ranking.sort(
        key=lambda x: x[0],
        reverse=True
    )

    return ranking
