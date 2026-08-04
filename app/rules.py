import re
from typing import List, Dict, Set

# ==========================================================
# VERSION
# ==========================================================

RULE_ENGINE_VERSION = "MontirPintar Rules Engine V4"

# ==========================================================
# VEHICLE KEYWORDS
# ==========================================================

CAR_KEYWORDS: Set[str] = {

    "mobil",
    "car",
    "sedan",
    "hatchback",
    "wagon",
    "estate",
    "suv",
    "mpv",
    "pickup",
    "pick-up",
    "truck",
    "truk",
    "van",
    "minibus"

}

MOTOR_KEYWORDS: Set[str] = {

    "motor",
    "motorcycle",
    "bike",
    "matic",
    "skutik",
    "bebek",
    "sport",
    "trail",
    "scooter"

}

# ==========================================================
# USER INTENT
# ==========================================================

INTENT_KEYWORDS: Dict[str, Set[str]] = {

    "diagnosis": {

        "kenapa",
        "mengapa",
        "why",
        "rusak",
        "problem",
        "diagnosa",
        "diagnosis"

    },

    "repair": {

        "service",
        "servis",
        "repair",
        "perbaiki",
        "ganti",
        "bengkel"

    },

    "maintenance": {

        "maintenance",
        "rawat",
        "tune up",
        "service berkala"

    },

    "cost": {

        "harga",
        "biaya",
        "cost",
        "price"

    }

}

# ==========================================================
# REGEX
# ==========================================================

TOKEN_REGEX = re.compile(

    r"[a-zA-Z0-9\-]+"

)

# ==========================================================
# CLEAN TEXT
# ==========================================================

def clean_text(text: str) -> str:

    if not text:

        return ""

    text = text.lower()

    text = re.sub(

        r"[^a-z0-9\s\-]",

        " ",

        text

    )

    text = re.sub(

        r"\s+",

        " ",

        text

    )

    return text.strip()

# ==========================================================
# TOKENIZE
# ==========================================================

def tokenize(text: str) -> List[str]:

    return TOKEN_REGEX.findall(

        clean_text(text)

    )

# ==========================================================
# REMOVE DUPLICATE
# ==========================================================

def unique(items: List[str]) -> List[str]:

    return list(

        dict.fromkeys(items)

    )

# ==========================================================
# EXTRACT PHRASES
# ==========================================================

def extract_phrases(text: str) -> List[str]:

    words = tokenize(text)

    phrases = []

    for i in range(len(words)):

        phrases.append(words[i])

        if i + 1 < len(words):

            phrases.append(

                words[i]
                + " "
                + words[i + 1]

            )

        if i + 2 < len(words):

            phrases.append(

                words[i]
                + " "
                + words[i + 1]
                + " "
                + words[i + 2]

            )

    return unique(phrases)

# ==========================================================
# PUBLIC
# ==========================================================

def extract_keywords(text: str) -> List[str]:

    return extract_phrases(text)


# ==========================================================
# VEHICLE SCORE
# ==========================================================

def vehicle_scores(text: str) -> Dict[str, int]:

    text = clean_text(text)

    scores = {
        "car": 0,
        "motorcycle": 0
    }

    for keyword in CAR_KEYWORDS:

        if keyword in text:
            scores["car"] += 1

    for keyword in MOTOR_KEYWORDS:

        if keyword in text:
            scores["motorcycle"] += 1

    return scores


# ==========================================================
# DETECT VEHICLE
# ==========================================================

def detect_vehicle(text: str):

    scores = vehicle_scores(text)

    if (
        scores["car"] == 0
        and
        scores["motorcycle"] == 0
    ):
        return None

    if scores["car"] >= scores["motorcycle"]:
        return "car"

    return "motorcycle"


# ==========================================================
# INTENT SCORE
# ==========================================================

def intent_scores(text: str):

    text = clean_text(text)

    scores = {}

    for intent, keywords in INTENT_KEYWORDS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[intent] = score

    return scores


# ==========================================================
# DETECT INTENT
# ==========================================================

def detect_intent(text: str):

    scores = intent_scores(text)

    best_intent = None
    highest_score = 0

    for intent, score in scores.items():

        if score > highest_score:

            highest_score = score
            best_intent = intent

    if highest_score == 0:
        return "diagnosis"

    return best_intent


# ==========================================================
# KEYWORD WEIGHT
# ==========================================================

def keyword_weight(keyword: str) -> int:

    keyword = keyword.strip()

    if not keyword:
        return 0

    words = keyword.split()

    if len(words) >= 3:
        return 6

    if len(words) == 2:
        return 4

    return 2


# ==========================================================
# BUILD KEYWORD MAP
# ==========================================================

def build_keyword_map(text: str):

    keywords = extract_keywords(text)

    result = {}

    for keyword in keywords:

        result[keyword] = keyword_weight(keyword)

    return result


# ==========================================================
# CONTAINS PHRASE
# ==========================================================

def contains_phrase(
    text: str,
    phrase: str
) -> bool:

    text = clean_text(text)

    phrase = clean_text(phrase)

    return phrase in text


# ==========================================================
# EXACT MATCH BONUS
# ==========================================================

def exact_match_bonus(
    user_input: str,
    phrase: str
):

    if contains_phrase(
        user_input,
        phrase
    ):
        return 8

    return 0


# ==========================================================
# PARTIAL MATCH BONUS
# ==========================================================

def partial_match_bonus(
    user_input: str,
    phrase: str
):

    tokens = tokenize(user_input)

    words = tokenize(phrase)

    matched = 0

    for word in words:

        if word in tokens:
            matched += 1

    if matched == len(words):
        return 6

    if matched >= len(words) * 0.7:
        return 4

    if matched > 0:
        return 2

    return 0
