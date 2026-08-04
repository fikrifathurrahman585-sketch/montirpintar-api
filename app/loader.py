import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

CACHE = {}


# ==========================================================
# LOAD JSON
# ==========================================================

def _load_json(path: Path):

    if not path.exists():
        return []

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ==========================================================
# LOAD FOLDER
# ==========================================================

def _load_folder(folder: Path):

    data = []

    if not folder.exists():
        return data

    for file in sorted(folder.glob("*.json")):

        try:

            content = _load_json(file)

            if isinstance(content, list):
                data.extend(content)

            elif isinstance(content, dict):
                data.append(content)

        except Exception:
            continue

    return data


# ==========================================================
# LOAD
# ==========================================================

def load():

    global CACHE

    if CACHE:
        return CACHE

    dataset_dir = BASE_DIR / "dataset"

    CACHE = {

        # --------------------------------------------------
        # Legacy Dataset (tetap dipakai)
        # --------------------------------------------------

        "cars":
            _load_json(dataset_dir / "cars.json"),

        "motorcycles":
            _load_json(dataset_dir / "motorcycles.json"),

        # --------------------------------------------------
        # Modular Dataset (baru)
        # --------------------------------------------------

        "car":
            _load_folder(dataset_dir / "car"),

        "motorcycle":
            _load_folder(dataset_dir / "motorcycle"),

        # --------------------------------------------------
        # Knowledge Base Lama
        # --------------------------------------------------

        "slang":
            _load_json(dataset_dir / "slang.json"),

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


# ==========================================================
# RELOAD
# ==========================================================

def reload():

    global CACHE

    CACHE = {}

    return load()
