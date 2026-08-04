from app.matcher import match_symptoms
from app.scorer import score_bonus, confidence


# ==========================================================
# SEMANTIC SEARCH V3
# ==========================================================

def semantic_search(
    user_input,
    database=None,
    lang="id"
):
    matches = match_symptoms(user_input)

    if not matches:
        return None, 0

    ranking = []

    for candidate in matches:

        item = candidate["symptom"]

        base_score = candidate.get("score", 0)

        bonus_score = score_bonus(
            user_input,
            item
        )

        total_score = base_score + bonus_score

        ranking.append({
            "symptom": item,
            "score": total_score,
            "base_score": base_score,
            "bonus_score": bonus_score
        })

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    best = ranking[0]

    final_score = confidence(
        best["score"]
    )

    return (
        best["symptom"],
        final_score
    )
