from app.rules import (
    detect_vehicle,
    detect_system,
    extract_keywords
)

from app.knowledge import component_score

# ==========================================================
# WEIGHT CONFIG
# ==========================================================

KEYWORD_WEIGHT = 10
ALIAS_WEIGHT = 8
SYSTEM_WEIGHT = 20
VEHICLE_WEIGHT = 15
COMPONENT_WEIGHT = 12
PRIORITY_WEIGHT = 3

SEVERITY_WEIGHT = {
    "INFO": 0,
    "WARNING": 5,
    "DANGER": 10
}

# ==========================================================
# GET DATASET KEYWORDS
# ==========================================================

def dataset_keywords(item):

    keywords = set()

    # ---------- Legacy ----------
    for k in item.get("keywords", []):
        keywords.add(k.lower())

    for k in item.get("aliases", []):
        keywords.add(k.lower())

    # ---------- Modern ----------
    language = item.get("language", {})

    for lang in ("id", "en"):

        if lang not in language:
            continue

        for symptom in language[lang].get("symptoms", []):

            keywords.add(symptom.lower())

    return keywords


# ==========================================================
# KEYWORD SCORE
# ==========================================================

def score_keywords(user_input, item):

    score = 0

    keywords = extract_keywords(user_input)

    dataset = dataset_keywords(item)

    for word in keywords:

        if word in dataset:
            score += KEYWORD_WEIGHT

    return score


# ==========================================================
# ALIAS SCORE
# ==========================================================

def score_alias(user_input, item):

    score = 0

    aliases = item.get("aliases", [])

    text = user_input.lower()

    for alias in aliases:

        if alias.lower() in text:

            score += ALIAS_WEIGHT

    return score


# ==========================================================
# SYSTEM SCORE
# ==========================================================

def score_system(user_input, item):

    detected = detect_system(user_input)

    if not detected:
        return 0

    system = item.get("system", "").lower()

    if detected == system:
        return SYSTEM_WEIGHT

    return 0


# ==========================================================
# VEHICLE SCORE
# ==========================================================

def score_vehicle(user_input, item):

    detected = detect_vehicle(user_input)

    if not detected:
        return 0

    vehicle = item.get("vehicle", "").lower()

    if detected == vehicle:
        return VEHICLE_WEIGHT

    return 0


# ==========================================================
# PRIORITY SCORE
# ==========================================================

def score_priority(item):

    return item.get("priority", 0) * PRIORITY_WEIGHT


# ==========================================================
# SEVERITY SCORE
# ==========================================================

def score_severity(item):

    severity = item.get(
        "severity",
        "INFO"
    )

    return SEVERITY_WEIGHT.get(
        severity,
        0
    )


# ==========================================================
# COMPONENT SCORE
# ==========================================================

def score_component(user_input, item):

    try:
        return component_score(
            user_input,
            item
        )
    except Exception:
        return 0


# ==========================================================
# TOTAL SCORE
# ==========================================================

def score_bonus(user_input, item):

    total = 0

    total += score_keywords(
        user_input,
        item
    )

    total += score_alias(
        user_input,
        item
    )

    total += score_system(
        user_input,
        item
    )

    total += score_vehicle(
        user_input,
        item
    )

    total += score_component(
        user_input,
        item
    )

    total += score_priority(
        item
    )

    total += score_severity(
        item
    )

    return total


# ==========================================================
# CONFIDENCE ENGINE
# ==========================================================

def calculate_confidence(score):

    if score <= 0:
        return 0

    if score >= 100:
        return 99

    confidence = int(score)

    if confidence < 35:
        confidence = 35

    if confidence > 99:
        confidence = 99

    return confidence


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def confidence(score):

    return calculate_confidence(score)
