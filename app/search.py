from app.matcher import match_symptoms
from app.scorer import confidence


def semantic_search(
    user_input,
    database=None,
    lang="id"
):

    matches = match_symptoms(user_input)

    if len(matches) == 0:
        return None, 0

    best = matches[0]

    final_score = confidence(best["score"])

    return best["symptom"], final_score
