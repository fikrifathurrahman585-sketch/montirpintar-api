from app.loader import load
from app.knowledge import get_alias

db = load()


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
        ";"
    ]

    for c in chars:
        text = text.replace(c, " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text.strip()


def tokenize(text):

    return normalize(text).split()


def expand_alias(tokens):

    output = []

    for token in tokens:

        output.append(get_alias(token))

    return output


def match_symptoms(text):

    normalized = normalize(text)

    tokens = expand_alias(tokenize(normalized))

    ranking = []

    for symptom in db["symptoms"]:

        keywords = symptom.get("keywords", [])

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

        if score > 0:

            ranking.append({

                "symptom": symptom,

                "score": score,

                "matched_keywords": matched

            })

    ranking.sort(

        key=lambda x: x["score"],

        reverse=True

    )

    return ranking
