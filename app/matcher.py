def match_symptoms(text: str):

    normalized = normalize(text)

    tokens = expand_alias(tokenize(normalized))

    hasil = []

    for symptom in db["symptoms"]:

        score = 0

        keywords = symptom.get("keywords", [])

        for keyword in keywords:

            keyword = normalize(keyword)

            if keyword in tokens:
                score += 3

            elif keyword in normalized:
                score += 2

        if score > 0:

            hasil.append({

                "symptom": symptom,

                "score": score,

                "matched_keywords": keywords

            })

    hasil.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return hasil
