from collections import Counter
import logging

from app.loader import (
    load_cars,
    load_motorcycles,
    load_systems,
    load_severity,
    load_driveability,
    load_validation,
)

logger = logging.getLogger("MontirPintarValidator")

class DatasetValidator:
    def __init__(self):
        # MENGGUNAKAN fungsi dari loader.py yang sudah di-import
        self.systems = load_systems() or []
        self.severity = load_severity() or []
        self.driveability = load_driveability() or []
        self.rules = load_validation() or {"required_fields": [], "minimum_symptoms": 1}

    def validate(self, dataset):
        errors = []
        if not dataset:
            return errors

        ids = []
        required = self.rules.get("required_fields", [])
        min_symptoms = self.rules.get("minimum_symptoms", 1)

        for item in dataset:
            # Gunakan .get() agar tidak crash (KeyError) jika JSON berantakan
            item_id = item.get("id", "UNKNOWN")
            ids.append(item_id)

            for field in required:
                if field not in item:
                    errors.append(f'{item_id} missing "{field}"')

            if item.get("system") not in self.systems:
                errors.append(f'{item_id} invalid system')

            if item.get("severity") not in self.severity:
                errors.append(f'{item_id} invalid severity')

            if item.get("driveability") not in self.driveability:
                errors.append(f'{item_id} invalid driveability')

            lang_data = item.get("language", {})

            if "id" not in lang_data:
                errors.append(f'{item_id} missing language.id')
            elif len(lang_data.get("id", {}).get("symptoms", [])) < min_symptoms:
                errors.append(f'{item_id} Indonesian symptoms below minimum')

            if "en" not in lang_data:
                errors.append(f'{item_id} missing language.en')
            elif len(lang_data.get("en", {}).get("symptoms", [])) < min_symptoms:
                errors.append(f'{item_id} English symptoms below minimum')

            if "cost" not in item:
                errors.append(f'{item_id} missing cost')

        dup = Counter(ids)
        for key, value in dup.items():
            if value > 1:
                errors.append(f"Duplicate ID : {key}")

        return errors


def run_validation():
    try:
        validator = DatasetValidator()

        # MENGGUNAKAN fungsi loader yang tepat
        cars = load_cars() or []
        motorcycles = load_motorcycles() or []

        errors = []
        errors.extend(validator.validate(cars))
        errors.extend(validator.validate(motorcycles))

        return errors
    except Exception as e:
        logger.error(f"Gagal menjalankan validasi dataset: {e}")
        # Kembalikan pesan error sebagai list agar tidak memicu crash di main.py
        return [f"System Error: {e}"]


if __name__ == "__main__":
    result = run_validation()

    print("=" * 60)
    print("MontirPintar Dataset Validator")
    print("=" * 60)

    if not result:
        print("Dataset VALID")
    else:
        print(f"{len(result)} Error ditemukan\n")
        for err in result:
            print("-", err)
