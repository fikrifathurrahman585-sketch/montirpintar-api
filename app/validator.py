import json

from app.loader import *

from app.utils import duplicate


class DatasetValidator:

    def __init__(self):

        self.systems = load_systems()

        self.severity = load_severity()

        self.driveability = load_driveability()

        self.rules = load_validation()

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

            if item["severity"] not in self.severity:

                errors.append(

                    f'{item["id"]} invalid severity'

                )

            if item["driveability"] not in self.driveability:

                errors.append(

                    f'{item["id"]} invalid driveability'

                )

            if item["system"] not in self.systems:

                errors.append(

                    f'{item["id"]} invalid system'

                )

            if "id" not in item["language"]:

                errors.append(

                    f'{item["id"]} missing Indonesian language'

                )

            if "en" not in item["language"]:

                errors.append(

                    f'{item["id"]} missing English language'

                )

            if len(item["language"]["id"]["symptoms"]) < self.rules["minimum_symptoms"]:

                errors.append(

                    f'{item["id"]} too few Indonesian symptoms'

                )

            if len(item["language"]["en"]["symptoms"]) < self.rules["minimum_symptoms"]:

                errors.append(

                    f'{item["id"]} too few English symptoms'

                )

        dup = duplicate(ids)

        for d in dup:

            errors.append(

                f'Duplicate ID : {d}'

            )

        return errors


if __name__ == "__main__":

    validator = DatasetValidator()

    cars = load_cars()

    motorcycles = load_motorcycles()

    print("=" * 60)

    print("MontirPintar Validator")

    print("=" * 60)

    print()

    errors = validator.validate(cars)

    errors += validator.validate(motorcycles)

    if not errors:

        print("✔ Dataset Valid")

    else:

        print()

        print(f"{len(errors)} Error Found")

        print()

        for e in errors:

            print("-", e)
