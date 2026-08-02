import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE = {}


def _load_json(path: Path):

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load():

    global CACHE

    if CACHE:
        return CACHE

    CACHE = {

        "cars":
            _load_json(BASE_DIR / "dataset" / "cars.json"),

        "motorcycles":
            _load_json(BASE_DIR / "dataset" / "motorcycles.json"),

        "slang":
            _load_json(BASE_DIR / "dataset" / "slang.json"),

        "symptoms":
            _load_json(BASE_DIR / "v2" / "symptoms.json"),

        "faults":
            _load_json(BASE_DIR / "v2" / "faults.json"),

        "components":
            _load_json(BASE_DIR / "v2" / "components.json"),

        "repairs":
            _load_json(BASE_DIR / "v2" / "repairs.json"),

        "costs":
            _load_json(BASE_DIR / "v2" / "costs.json"),

        "aliases":
            _load_json(BASE_DIR / "v2" / "aliases.json"),

        "translation_id":
            _load_json(BASE_DIR / "translations" / "id.json"),

        "translation_en":
            _load_json(BASE_DIR / "translations" / "en.json"),
    }

    return CACHE


def reload():
    global CACHE
    CACHE = {}
    return load()
