from app.matcher import match_symptoms


def semantic_search(
    user_input: str,
    database=None,
    lang: str = "id"
):
    """
    Search Engine V2

    Return:
        best_match,
        confidence
    """

    matches = match_symptoms(user_input)

    if not matches:
        return None, 0

    best = matches[0]

    symptom = best["symptom"]

    score = best["score"]

    confidence = min(100, score * 12)

    return symptom, confidence
