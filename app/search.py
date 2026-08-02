from app.matcher import rank_candidates


def semantic_search(
        user_input,
        database,
        lang="id"
):

    ranking = rank_candidates(
        user_input,
        database,
        lang
    )

    if not ranking:
        return None, 0

    score, item = ranking[0]

    return item, score
