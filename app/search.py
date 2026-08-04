from app.matcher import match_symptoms
from app.scorer import score_bonus, confidence


# ==========================================================
# SEMANTIC SEARCH V4
# ==========================================================

def semantic_search(
    user_input,
    database=None,
    lang="id"
):
    """
    database:
        Dipertahankan untuk backward compatibility.
    """

    matches = match_symptoms(user_input)

    if not matches:
        return None, 0

    best_item = None

    best_score = -1

    best_match_count = -1

    for candidate in matches:

        item = candidate["symptom"]

        base_score = candidate.get(
            "score",
            0
        )

        matched_keywords = candidate.get(
            "matched_keywords",
            []
        )

        bonus_score = score_bonus(
            user_input,
            item
        )

        final_score = (
            base_score
            +
            bonus_score
        )

        matched_count = len(
            matched_keywords
        )

        if (

            final_score > best_score

            or

            (
                final_score == best_score
                and
                matched_count > best_match_count
            )

        ):

            best_item = item

            best_score = final_score

            best_match_count = matched_count

    if best_item is None:

        return None, 0

    return (

        best_item,

        confidence(
            best_score
        )

    )
