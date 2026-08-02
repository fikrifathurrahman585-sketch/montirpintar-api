import re

# ==========================================
# DETEKSI JENIS KENDARAAN
# ==========================================

CAR_KEYWORDS = {
    "mobil",
    "car",
    "sedan",
    "suv",
    "mpv",
    "pickup",
    "truck"
}

MOTOR_KEYWORDS = {
    "motor",
    "motorcycle",
    "bike",
    "matic",
    "bebek",
    "sport"
}


def detect_vehicle(text: str):

    text = text.lower()

    for word in CAR_KEYWORDS:
        if word in text:
            return "car"

    for word in MOTOR_KEYWORDS:
        if word in text:
            return "motorcycle"

    return None


# ==========================================
# DETEKSI SISTEM
# ==========================================

SYSTEM_RULES = {

    "engine": [
        "mesin",
        "engine",
        "klep",
        "valve",
        "piston",
        "kruk",
        "bearing",
        "connecting rod",
        "noken",
        "camshaft"
    ],

    "cvt": [
        "cvt",
        "roller",
        "vbelt",
        "v-belt",
        "kampas",
        "ganda",
        "gredek",
        "klotok"
    ],

    "transmission": [
        "transmisi",
        "gearbox",
        "kopling",
        "clutch",
        "matic",
        "manual",
        "gigi",
        "slip",
        "jedug"
    ],

    "brake": [
        "rem",
        "brake",
        "cakram",
        "disc",
        "kampas rem",
        "kaliper",
        "master rem"
    ],

    "suspension": [
        "shock",
        "shockbreaker",
        "tie rod",
        "rack steer",
        "ball joint",
        "bushing",
        "gluduk"
    ],

    "cooling": [
        "radiator",
        "coolant",
        "overheat",
        "kipas",
        "waterpump"
    ],

    "electrical": [
        "aki",
        "battery",
        "alternator",
        "starter",
        "dinamo"
    ]
}


def detect_system(text: str):

    text = text.lower()

    score = {}

    for system, keywords in SYSTEM_RULES.items():

        score[system] = 0

        for keyword in keywords:

            if keyword in text:

                score[system] += 1

    if not score:
        return None

    best = max(score, key=score.get)

    if score[best] == 0:
        return None

    return best


# ==========================================
# EKSTRAKSI KATA KUNCI
# ==========================================

def extract_keywords(text: str):

    text = text.lower()

    words = re.findall(r"[a-zA-Z0-9\-]+", text)

    return list(dict.fromkeys(words))
