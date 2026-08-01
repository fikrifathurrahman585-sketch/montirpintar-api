import json
from pathlib import Path
from collections import Counter


BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"

CARS_FILE = DATASET_DIR / "cars.json"
MOTORCYCLES_FILE = DATASET_DIR / "motorcycles.json"

STANDARD_DIR = DATASET_DIR / "standards"

SYSTEM_FILE = STANDARD_DIR / "systems.json"
SEVERITY_FILE = STANDARD_DIR / "severity.json"
DRIVEABILITY_FILE = STANDARD_DIR / "driveability.json"
VALIDATION_FILE = STANDARD_DIR / "validation.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


class DatasetValidator:

    def __init__(self):

        self.systems = load_json(SYSTEM_FILE)

        self.severity = load_json(SEVERITY_FILE)

        self.driveability = load_json(DRIVEABILITY_FILE)

        self.rules = load_json(VALIDATION_FILE)

    def validate(self, dataset):

        errors = []

        ids = []

        required = self.rules["required_fields"]

        for item in dataset:

            ids.append(item["id"])

            for field in required:

                if field not in item:
                    errors.append(
                        f'{item.get("id","UNKNOWN")} missing "{field}"'
                    )

            if item["system"] not in self.systems:
                errors.append(
                    f'{item["id"]} invalid system'
                )

            if item["severity"] not in self.severity:
                errors.append(
                    f'{item["id"]} invalid severity'
                )

            if item["driveability"] not in self.driveability:
                errors.append(
                    f'{item["id"]} invalid driveability'
                )

            if "id" not in item["language"]:
                errors.append(
                    f'{item["id"]} missing language.id'
                )

            if "en" not in item["language"]:
                errors.append(
                    f'{item["id"]} missing language.en'
                )

            if "cost" not in item:
                errors.append(
                    f'{item["id"]} missing cost'
                )

            if len(item["language"]["id"]["symptoms"]) < self.rules["minimum_symptoms"]:
                errors.append(
                    f'{item["id"]} Indonesian symptoms below minimum'
                )

            if len(item["language"]["en"]["symptoms"]) < self.rules["minimum_symptoms"]:
                errors.append(
                    f'{item["id"]} English symptoms below minimum'
                )

        dup = Counter(ids)

        for key, value in dup.items():

            if value > 1:
                errors.append(f"Duplicate ID : {key}")

        return errors


def run_validation():

    validator = DatasetValidator()

    cars = load_json(CARS_FILE)

    motorcycles = load_json(MOTORCYCLES_FILE)

    errors = []

    errors.extend(validator.validate(cars))

    errors.extend(validator.validate(motorcycles))

    return errors


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
