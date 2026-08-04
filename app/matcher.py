from app.loader import load
from app.knowledge import get_alias
from app.rules import (
    clean_text,
    tokenize,
    extract_keywords,
    keyword_weight,
    exact_match_bonus,
    partial_match_bonus
)

db = load()


# ==========================================================
# NORMALIZE
# ==========================================================

def normalize(text: str):

    return clean_text(text)


# ==========================================================
# EXPAND ALIAS
# ==========================================================

def expand_alias(tokens):

    output = []

    for token in tokens:

        token = get_alias(token)

        if not isinstance(token, str):
            continue

        token = normalize(token)

        output.extend(

            token.split()

        )

    return output

# ==========================================================
# BUILD SEARCH TEXT
# ==========================================================

def build_search_text(tokens):

    return " ".join(tokens)


# ==========================================================
# GET DATASET KEYWORDS
# ==========================================================

def dataset_keywords(item, lang):

    keywords = []

    # ---------- Modern Dataset ----------

    language = item.get("language", {})

    if lang in language:

        keywords.extend(

            language[lang].get(
                "symptoms",
                []
            )

        )

    # ---------- Legacy Dataset ----------

    keywords.extend(

        item.get(
            "keywords",
            []
        )

    )

    return list(

        dict.fromkeys(keywords)

    )

# ==========================================================
# SCORE KEYWORDS V5
# ==========================================================

def score_keywords(

    user_input,
    normalized,
    tokens,
    keywords

):

    score = 0

    matched = []

    matched_words = set()

    for keyword in keywords:

        keyword = normalize(keyword)

        if not keyword:

            continue

        # ------------------------------
        # Exact Phrase Bonus
        # ------------------------------

        bonus = exact_match_bonus(

            user_input,

            keyword

        )

        if bonus > 0:

            score += bonus

            matched.append(keyword)

            matched_words.update(

                keyword.split()

            )

            continue

        # ------------------------------
        # Partial Phrase Bonus
        # ------------------------------

        bonus = partial_match_bonus(

            user_input,

            keyword

        )

        if bonus > 0:

            score += bonus

            matched.append(keyword)

            matched_words.update(

                keyword.split()

            )

            continue

        # ------------------------------
        # Single Keyword
        # ------------------------------

        if keyword in tokens:

            score += keyword_weight(

                keyword

            )

            matched.append(keyword)

            matched_words.add(keyword)

    # ----------------------------------
    # COVERAGE BONUS
    # ----------------------------------

    if keywords:

        coverage = (

            len(matched_words)

            /

            max(

                1,

                len(

                    set(

                        " ".join(keywords).split()

                    )

                )

            )

        )

        score += int(

            coverage * 10

        )

    return (

        score,

        matched

    )


# ==========================================================
# MATCH MODERN DATASET
# ==========================================================

def match_modern_dataset(
    user_input,
    normalized,
    tokens
):

    ranking = []

    datasets = []

    # Legacy JSON

    datasets.extend(
        db.get("cars", [])
    )

    datasets.extend(
        db.get("motorcycles", [])
    )

    # Modular JSON

    datasets.extend(
        db.get("car", [])
    )

    datasets.extend(
        db.get("motorcycle", [])
    )

    for item in datasets:

        language = item.get(
            "language",
            {}
        )

        languages = []

        if language:

            languages.extend(
                language.keys()
            )

        else:

            languages.append("id")

        for lang in languages:

            keywords = dataset_keywords(
                item,
                lang
            )

            if not keywords:
                continue

            score, matched = score_keywords(

                user_input,

                normalized,

                tokens,

                keywords

            )

            if score <= 0:
                continue

            ranking.append({

                "symptom": item,

                "score": score,

                "matched_keywords": matched,

                "language": lang

            })

    return ranking


# ==========================================================
# MATCH LEGACY DATASET
# ==========================================================

def match_legacy_dataset(
    user_input,
    normalized,
    tokens
):

    ranking = []

    for item in db.get(
        "symptoms",
        []
    ):

        keywords = dataset_keywords(
            item,
            "id"
        )

        if not keywords:
            continue

        score, matched = score_keywords(

            user_input,

            normalized,

            tokens,

            keywords

        )

        if score <= 0:
            continue

        ranking.append({

            "symptom": item,

            "score": score,

            "matched_keywords": matched,

            "language": "id"

        })

    return ranking

# ==========================================================
# MAIN MATCHER
# ==========================================================

def match_symptoms(text):

    normalized = normalize(text)

    tokens = expand_alias(

        tokenize(normalized)

    )

    ranking = []

    ranking.extend(

        match_modern_dataset(

            normalized,

            normalized,

            tokens

        )

    )

    ranking.extend(

        match_legacy_dataset(

            normalized,

            normalized,

            tokens

        )

    )

    ranking.sort(

        key=lambda item: (

            item["score"],

            len(

                item["matched_keywords"]

            )

        ),

        reverse=True

    )

    return ranking
