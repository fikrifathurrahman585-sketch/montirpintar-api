from app.matcher import match_symptoms
from app.scorer import calculate_confidence


def semantic_search(
    user_input,
    database=None,
    lang="id"
):

    matches = match_symptoms(user_input)

    if not matches:
        return None, 0

    best = matches[0]

    confidence = calculate_confidence(
        best["score"]
    )

    return best["symptom"], confidence
