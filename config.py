from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_DIR = BASE_DIR / "dataset"

CARS_FILE = DATASET_DIR / "cars.json"
MOTORCYCLES_FILE = DATASET_DIR / "motorcycles.json"
SLANG_FILE = DATASET_DIR / "slang.json"

STANDARDS_DIR = DATASET_DIR / "standards"

SYSTEMS_FILE = STANDARDS_DIR / "systems.json"
SEVERITY_FILE = STANDARDS_DIR / "severity.json"
DRIVEABILITY_FILE = STANDARDS_DIR / "driveability.json"
VALIDATION_FILE = STANDARDS_DIR / "validation.json"
TAXONOMY_FILE = STANDARDS_DIR / "taxonomy.json"
