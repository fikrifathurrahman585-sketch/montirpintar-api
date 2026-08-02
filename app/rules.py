import re


SYSTEM_RULES = {

    "cvt": [
        "cvt",
        "roller",
        "v belt",
        "vbelt",
        "kampas ganda",
        "mangkok",
        "clutch",
        "pulley",
        "gredek",
        "klotok",
        "dengung gardan"
    ],

    "engine": [
        "mesin",
        "klep",
        "kruk as",
        "krukas",
        "piston",
        "ring piston",
        "ngebul",
        "oli mesin",
        "knocking",
        "metal"
    ],

    "cooling": [
        "radiator",
        "coolant",
        "overheat",
        "kipas",
        "waterpump",
        "air radiator"
    ],

    "brakes": [
        "rem",
        "cakram",
        "kampas rem",
        "pedal rem",
        "kaliper",
        "master rem",
        "minyak rem"
    ],

    "transmission": [
        "matic",
        "transmisi",
        "gearbox",
        "persneling",
        "gigi",
        "slip",
        "jedug"
    ],

    "electrical": [
        "aki",
        "starter",
        "alternator",
        "dinamo",
        "lampu",
        "kelistrikan"
    ],

    "suspension": [
        "shock",
        "tie rod",
        "rack steer",
        "bearing",
        "cv joint",
        "ball joint"
    ]
}


def detect_system(text: str):

    text = text.lower()

    scores = {}

    for system, keywords in SYSTEM_RULES.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[system] = score

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return None

    return best
