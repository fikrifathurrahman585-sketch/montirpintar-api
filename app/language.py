import json
import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ==========================================================
# LOAD SLANG DICTIONARY
# ==========================================================

try:
    with open(
        os.path.join(BASE_DIR, "dataset", "slang.json"),
        "r",
        encoding="utf-8"
    ) as f:
        SLANG_DICT = json.load(f)

except Exception:
    SLANG_DICT = {}


# ==========================================================
# MANUAL NORMALIZATION
# ==========================================================

MANUAL_NORMALIZATION = {

    # ---------- Mesin ----------
    "klotok": "bunyi ketukan",
    "tektek": "bunyi ketukan",
    "tek-tek": "bunyi ketukan",
    "ketrok": "bunyi ketukan",

    "ngorok": "bunyi dengung",

    "ngelitik": "detonasi",

    "ngelitiknya": "detonasi",

    "jedug": "hentakan transmisi",

    "jeduk": "hentakan transmisi",

    "gredek": "kampas ganda selip",

    "ngempos": "tenaga hilang",

    "loyo": "tenaga lemah",

    "brebet": "mesin tersendat",

    "mbrebet": "mesin tersendat",

    "nyendat": "mesin tersendat",

    "ngebul": "asap knalpot",

    "ngasep": "asap knalpot",

    "mbul": "asap knalpot",

    "ngoroknya": "bunyi dengung",

    "ngorok2": "bunyi dengung",

    "ngorok-ngorok": "bunyi dengung",

    # ---------- CVT ----------

    "vbelt": "v belt",

    "vbelt": "v belt",

    "belt": "v belt",

    "cvt": "cvt",

    "roller": "roller cvt",

    "mangkok": "clutch outer",

    "kampasganda": "kampas ganda",

    # ---------- Rem ----------

    "blong": "rem blong",

    "pedal": "pedal rem",

    # ---------- Cooling ----------

    "overheat": "mesin panas",

    "panas": "mesin panas",

    # ---------- English ----------

    "gearbox": "transmission",

    "brakes": "brake",

    "tyres": "tire",

    "motorbike": "motorcycle",

    "oil": "engine oil",

    "coolant": "radiator coolant"
}


# ==========================================================
# STOP WORDS
# ==========================================================

STOPWORDS = {

    "nih",
    "dong",
    "bang",
    "bro",
    "gan",
    "pak",
    "mas",
    "mba",
    "mbak",
    "tolong",
    "please",
    "gua",
    "gue",
    "aku",
    "saya",
    "punya",
    "nihh",
    "dongg"
}


# ==========================================================
# NORMALIZE
# ==========================================================

def normalize_slang(text: str) -> str:

    text = text.lower()

    text = re.sub(r"[^a-z0-9\s\-]", " ", text)

    words = text.split()

    normalized = []

    for word in words:

        if word in STOPWORDS:
            continue

        if word in SLANG_DICT:
            word = SLANG_DICT[word]

        if word in MANUAL_NORMALIZATION:
            word = MANUAL_NORMALIZATION[word]

        normalized.append(word)

    return " ".join(normalized)


# ==========================================================
# LANGUAGE DETECTION
# ==========================================================

ENGLISH_WORDS = {

    "car",
    "engine",
    "noise",
    "sound",
    "gear",
    "transmission",
    "brake",
    "coolant",
    "oil",
    "battery",
    "starter",
    "steering",
    "radiator",
    "motorcycle",
    "clutch",
    "automatic",
    "manual"
}

INDONESIAN_WORDS = {

    "mobil",
    "motor",
    "mesin",
    "bunyi",
    "suara",
    "rem",
    "oli",
    "radiator",
    "aki",
    "starter",
    "setir",
    "kopling",
    "matic",
    "manual",
    "rusak",
    "brebet",
    "gredek",
    "klotok",
    "jedug",
    "ngempos"
}


def detect_language(text: str) -> str:

    text = text.lower()

    words = set(re.findall(r"[a-z]+", text))

    en_score = len(words.intersection(ENGLISH_WORDS))

    id_score = len(words.intersection(INDONESIAN_WORDS))

    if en_score > id_score:
        return "en"

    return "id"
