import json
import logging
import re
from pathlib import Path
from typing import Any


# ==========================================================
# LOGGER
# ==========================================================

logger = logging.getLogger("MontirPintarLanguage")


# ==========================================================
# PATH
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"

LANGUAGE_DIR = DATASET_DIR / "language"


# ==========================================================
# LOAD JSON
# ==========================================================

def _load_json(
    path: Path,
    default: Any
):

    if not path.exists():

        logger.warning(
            "Language dataset tidak ditemukan: %s",
            path
        )

        return default

    try:

        with open(
            path,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    except Exception:

        logger.exception(
            "Gagal membaca language dataset: %s",
            path
        )

        return default


# ==========================================================
# LOAD DATASET
# ==========================================================

# Dataset slang lama.
# Tetap digunakan untuk backward compatibility.

SLANG_DICT = _load_json(
    DATASET_DIR / "slang.json",
    {}
)


# Stopwords baru.

STOPWORDS_DATA = _load_json(
    LANGUAGE_DIR / "stopwords.json",
    []
)


# Manual normalization baru.

MANUAL_NORMALIZATION = _load_json(
    LANGUAGE_DIR / "manual_normalization.json",
    {}
)


# Language detection dictionary.

LANGUAGE_DETECTION = _load_json(
    LANGUAGE_DIR / "language_detection.json",
    {}
)


# ==========================================================
# VALIDATE DATASET TYPES
# ==========================================================

if not isinstance(SLANG_DICT, dict):
    SLANG_DICT = {}

if not isinstance(STOPWORDS_DATA, list):
    STOPWORDS_DATA = []

if not isinstance(MANUAL_NORMALIZATION, dict):
    MANUAL_NORMALIZATION = {}

if not isinstance(LANGUAGE_DETECTION, dict):
    LANGUAGE_DETECTION = {}


# ==========================================================
# BUILD FAST LOOKUP CACHE
# ==========================================================

STOPWORDS = {
    str(word).lower().strip()
    for word in STOPWORDS_DATA
    if str(word).strip()
}


SLANG_LOOKUP = {

    str(key).lower().strip():
        str(value).lower().strip()

    for key, value in SLANG_DICT.items()

    if str(key).strip()
}


NORMALIZATION_LOOKUP = {

    str(key).lower().strip():
        str(value).lower().strip()

    for key, value in MANUAL_NORMALIZATION.items()

    if str(key).strip()
}


LANGUAGE_WORDS = {}

for language, words in LANGUAGE_DETECTION.items():

    if not isinstance(words, list):
        continue

    LANGUAGE_WORDS[
        str(language).lower().strip()
    ] = {

        str(word).lower().strip()

        for word in words

        if str(word).strip()
    }


# ==========================================================
# BASIC TEXT CLEANING
# ==========================================================

def clean_text(text: str) -> str:

    if not text:
        return ""

    text = str(text).lower()

    # Unicode apostrophe → normal apostrophe
    text = text.replace("’", "'")

    # Karakter non alphanumeric menjadi spasi.
    # Hyphen tetap dipertahankan untuk istilah seperti:
    # v-belt, tie-rod, dll.

    text = re.sub(
        r"[^a-z0-9\s\-']",
        " ",
        text
    )

    # Hilangkan whitespace berlebih

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================================
# NORMALIZE REPEATED CHARACTERS
# ==========================================================

def normalize_repeated_characters(
    word: str
) -> str:

    if not word:
        return ""

    # Contoh:
    #
    # matiiiiii -> matii
    # brebettttt -> brebett
    #
    # Kita tidak langsung mengubah menjadi satu karakter
    # karena beberapa kata memang memiliki huruf ganda.

    return re.sub(
        r"(.)\1{2,}",
        r"\1\1",
        word
    )


# ==========================================================
# LOOKUP NORMALIZATION
# ==========================================================

def _normalize_word(word: str) -> str:

    if not word:
        return ""

    original = word

    # ------------------------------------------------------
    # 1. Exact slang lookup
    # ------------------------------------------------------

    if original in SLANG_LOOKUP:

        original = SLANG_LOOKUP[original]


    # ------------------------------------------------------
    # 2. Exact manual normalization
    # ------------------------------------------------------

    if original in NORMALIZATION_LOOKUP:

        original = NORMALIZATION_LOOKUP[original]

        return original


    # ------------------------------------------------------
    # 3. Repeated-character normalization
    # ------------------------------------------------------

    reduced = normalize_repeated_characters(
        original
    )


    # Coba lagi setelah huruf berulang dibersihkan.

    if reduced in SLANG_LOOKUP:

        reduced = SLANG_LOOKUP[reduced]


    if reduced in NORMALIZATION_LOOKUP:

        reduced = NORMALIZATION_LOOKUP[reduced]


    return reduced


# ==========================================================
# MULTI-WORD NORMALIZATION
# ==========================================================

def _normalize_phrases(text: str) -> str:

    if not text:
        return ""

    result = text

    # Normalization dataset boleh memiliki key seperti:
    #
    # "ga ada tenaga": "tenaga hilang"
    # "tidak ada tenaga": "tenaga hilang"
    #
    # Phrase terpanjang diproses lebih dulu agar
    # phrase pendek tidak merusak phrase panjang.

    phrases = sorted(
        NORMALIZATION_LOOKUP.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for source, replacement in phrases:

        if " " not in source:
            continue

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(source)
            + r"(?![a-z0-9])"
        )

        result = re.sub(
            pattern,
            replacement,
            result
        )

    return result


# ==========================================================
# NORMALIZE SLANG
# ==========================================================

def normalize_slang(text: str) -> str:

    """
    Normalisasi utama input pengguna.

    Fungsi ini sengaja mempertahankan nama lama
    `normalize_slang()` karena diagnosis.py sudah
    menggunakannya.

    Pipeline:

    raw text
        ↓
    clean text
        ↓
    multi-word normalization
        ↓
    slang normalization
        ↓
    manual normalization
        ↓
    stopword removal
        ↓
    normalized text
    """

    text = clean_text(text)

    if not text:
        return ""

    # ------------------------------------------------------
    # PHRASE NORMALIZATION
    # ------------------------------------------------------

    text = _normalize_phrases(text)


    # ------------------------------------------------------
    # TOKEN NORMALIZATION
    # ------------------------------------------------------

    words = text.split()

    normalized = []

    for word in words:

        word = word.strip()

        if not word:
            continue


        # Stopword sebelum normalization.

        if word in STOPWORDS:
            continue


        normalized_word = _normalize_word(
            word
        )


        # Replacement dapat menghasilkan beberapa kata:
        #
        # gredek -> kampas ganda selip
        #
        # sehingga hasil perlu dipecah kembali.

        replacement_words = (
            normalized_word.split()
        )


        for replacement in replacement_words:

            replacement = replacement.strip()

            if not replacement:
                continue

            if replacement in STOPWORDS:
                continue

            normalized.append(
                replacement
            )


    # ------------------------------------------------------
    # REMOVE DUPLICATE WHITESPACE
    # ------------------------------------------------------

    result = " ".join(normalized)

    result = re.sub(
        r"\s+",
        " ",
        result
    )

    return result.strip()


# ==========================================================
# LANGUAGE SCORE
# ==========================================================

def _language_score(
    words: set,
    language: str
) -> int:

    dictionary = LANGUAGE_WORDS.get(
        language,
        set()
    )

    if not dictionary:
        return 0

    return len(
        words.intersection(
            dictionary
        )
    )


# ==========================================================
# LANGUAGE DETECTION
# ==========================================================

def detect_language(text: str) -> str:

    """
    Deteksi bahasa sederhana berbasis dictionary.

    Saat ini kontrak backend hanya menggunakan:
        id
        en

    Jika tidak cukup bukti,
    Indonesia tetap menjadi fallback agar
    backward compatible dengan aplikasi sekarang.
    """

    text = clean_text(text)

    if not text:
        return "id"

    words = set(
        re.findall(
            r"[a-z0-9\-']+",
            text
        )
    )


    # ------------------------------------------------------
    # SCORE
    # ------------------------------------------------------

    id_score = _language_score(
        words,
        "id"
    )

    en_score = _language_score(
        words,
        "en"
    )


    # ------------------------------------------------------
    # RESULT
    # ------------------------------------------------------

    if en_score > id_score:
        return "en"

    return "id"


# ==========================================================
# GET LANGUAGE SCORES
# ==========================================================

def get_language_scores(
    text: str
) -> dict:

    """
    Fungsi tambahan untuk debugging/testing.

    Tidak mengubah kontrak fungsi lama.
    """

    text = clean_text(text)

    words = set(
        re.findall(
            r"[a-z0-9\-']+",
            text
        )
    )

    result = {}

    for language in LANGUAGE_WORDS:

        result[language] = (
            _language_score(
                words,
                language
            )
        )

    return result


# ==========================================================
# RELOAD LANGUAGE DATA
# ==========================================================

def reload_language_data():

    """
    Catatan:
    Dataset bahasa saat ini dimuat ketika module
    pertama kali di-import.

    Pada Vercel/server production, deployment baru
    otomatis memuat ulang module sehingga perubahan
    JSON langsung aktif setelah redeploy.

    Fungsi ini disediakan untuk compatibility/debug.
    """

    return {
        "slang": len(SLANG_LOOKUP),
        "normalization": len(
            NORMALIZATION_LOOKUP
        ),
        "stopwords": len(STOPWORDS),
        "languages": {
            language: len(words)
            for language, words
            in LANGUAGE_WORDS.items()
        }
    }
