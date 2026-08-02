import re

# =====================================================
# BONUS SCORE
# =====================================================

KEYWORD_SCORE = {

    "cvt": {
        "cvt": 60,
        "roller": 40,
        "v belt": 35,
        "vbelt": 35,
        "kampas": 25,
        "mangkok": 25,
        "gredek": 25,
        "klotok": 20,
        "dengung": 15,
        "bearing": 15
    },

    "engine": {
        "mesin": 50,
        "klep": 45,
        "kruk as": 45,
        "krukas": 45,
        "piston": 40,
        "ring": 35,
        "ngebul": 30,
        "oli mesin": 25,
        "knocking": 25
    },

    "cooling": {
        "radiator": 60,
        "coolant": 55,
        "overheat": 50,
        "kipas": 25,
        "waterpump": 30
    },

    "brakes": {
        "rem": 60,
        "cakram": 35,
        "kampas": 30,
        "pedal": 25,
        "kaliper": 30,
        "master rem": 40,
        "minyak rem": 40
    },

    "transmission": {
        "matic": 45,
        "transmisi": 45,
        "gearbox": 40,
        "persneling": 35,
        "gigi": 30,
        "jedug": 35,
        "slip": 30
    },

    "electrical": {
        "aki": 50,
        "starter": 45,
        "alternator": 40,
        "dinamo": 35,
        "lampu": 20
    },

    "suspension": {
        "shock": 45,
        "tie rod": 40,
        "rack steer": 40,
        "bearing": 30,
        "cv joint": 40,
        "ball joint": 30
    }

}


# =====================================================
# SCORE
# =====================================================

def score_keywords(text: str, system: str):

    text = text.lower()

    total = 0

    if system not in KEYWORD_SCORE:
        return 0

    rules = KEYWORD_SCORE[system]

    for keyword, score in rules.items():

        if keyword in text:
            total += score

    return total
