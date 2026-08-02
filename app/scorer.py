from app.rules import (
    detect_vehicle,
    detect_system,
    extract_keywords
)

# ==========================================================
# BOBOT SKOR
# ==========================================================

KEYWORD_WEIGHT = 8
SYSTEM_WEIGHT = 20
VEHICLE_WEIGHT = 15
SEVERITY_WEIGHT = {
    "INFO": 0,
    "WARNING": 5,
    "DANGER": 10
}

# ==========================================================
# HITUNG SKOR KEYWORD
# ==========================================================

def score_keywords(user_input: str, item: dict):

    score = 0

    keywords = extract_keywords(user_input)

    dataset_keywords = item.get("keywords", [])

    aliases = item.get("aliases", [])

    all_keywords = set()

    for k in dataset_keywords:
        all_keywords.add(k.lower())

    for k in aliases:
        all_keywords.add(k.lower())

    for word in keywords:
        if word in all_keywords:
            score += KEYWORD_WEIGHT

    return score


# ==========================================================
# SKOR SISTEM
# ==========================================================

def score_system(user_input: str, item: dict):

    detected = detect_system(user_input)

    if not detected:
        return 0

    dataset_system = item.get("system", "").lower()

    if detected == dataset_system:
        return SYSTEM_WEIGHT

    return 0


# ==========================================================
# SKOR VEHICLE
# ==========================================================

def score_vehicle(user_input: str, item: dict):

    detected = detect_vehicle(user_input)

    if not detected:
        return 0

    vehicle = item.get("vehicle", "").lower()

    if detected == vehicle:
        return VEHICLE_WEIGHT

    return 0


# ==========================================================
# SKOR PRIORITAS
# ==========================================================

def score_priority(item: dict):

    priority = item.get("priority", 0)

    return priority * 3


# ==========================================================
# SKOR SEVERITY
# ==========================================================

def score_severity(item: dict):

    severity = item.get(
        "severity",
        "INFO"
    )

    return SEVERITY_WEIGHT.get(
        severity,
        0
    )


# ==========================================================
# TOTAL BONUS
# ==========================================================

def score_bonus(user_input: str, item: dict):

    total = 0

    total += score_keywords(
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

    total += score_priority(item)

    total += score_severity(item)

    return total
