from app.loader import load
from app.knowledge import get_alias

db = load()


def normalize(text: str):

    text = text.lower().strip()

    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace("-", " ")

    while "  " in text:
        text = text.replace("  ", " ")

    return text


def tokenize(text: str):

    return normalize(text).split()


def expand_alias(tokens):

    hasil = []

    for token in tokens:

        hasil.append(get_alias(token))

    return hasil


def match_symptoms(text: str):

    tokens = expand_alias(tokenize(text))

    hasil = []

    for symptom in db["symptoms"]:

        score = 0

        keywords = symptom.get("keywords", [])

        for keyword in keywords:

            keyword = keyword.lower()

            if keyword in tokens:
                score += 2

            elif keyword in text.lower():
                score += 1

        if score > 0:

            hasil.append({
                "symptom": symptom,
                "score": score
            })

    hasil.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return hasil
