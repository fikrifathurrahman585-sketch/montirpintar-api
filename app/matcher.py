from app.loader import load
from app.knowledge import get_alias

db = load()


# ==========================================================
# NORMALIZE
# ==========================================================

def normalize(text):

    text = text.lower()

    chars = [
        ",",
        ".",
        "-",
        "/",
        "\\",
        "(",
        ")",
        ":",
        ";",
        "?",
        "!"
    ]

    for c in chars:
        text = text.replace(c, " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


# ==========================================================
# TOKENIZE
# ==========================================================

def tokenize(text):
    return normalize(text).split()


# ==========================================================
# EXPAND ALIAS
# ==========================================================

def expand_alias(tokens):

    output = []

    for token in tokens:
        output.append(get_alias(token))

    return output


# ==========================================================
# SCORE
# ==========================================================

def score_keywords(normalized, tokens, keywords):

    score = 0
    matched = []

    for keyword in keywords:

        keyword = normalize(keyword)

        if keyword in tokens:

            score += 3
            matched.append(keyword)

        elif keyword in normalized:

            score += 2
            matched.append(keyword)

    return score, matched


# ==========================================================
# MATCH MODERN DATASET
# ==========================================================

def match_modern_dataset(normalized, tokens):

    ranking = []

    datasets = []

    datasets.extend(db.get("motorcycle", []))
    datasets.extend(db.get("car", []))

    for item in datasets:

        language = item.get("language", {})

        for lang in ("id", "en"):

            if lang not in language:
                continue

            keywords = language[lang].get("symptoms", [])

            score, matched = score_keywords(
                normalized,
                tokens,
                keywords
            )

            if score == 0:
                continue

            ranking.append({

                "symptom": item,

                "score": score,

                "matched_keywords": matched

            })

    return ranking


# ==========================================================
# MATCH LEGACY DATASET
# ==========================================================

def match_legacy_dataset(normalized, tokens):

    ranking = []

    for symptom in db.get("symptoms", []):

        keywords = symptom.get("keywords", [])

        score, matched = score_keywords(
            normalized,
            tokens,
            keywords
        )

        if score == 0:
            continue

        ranking.append({

            "symptom": symptom,

            "score": score,

            "matched_keywords": matched

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
            tokens
        )
    )

    ranking.extend(
        match_legacy_dataset(
            normalized,
            tokens
        )
    )

    ranking.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return ranking
