import json
from app.config import *

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

_CARS = None
_MOTOR = None

def load_cars():
    global _CARS
    if _CARS is None:
        _CARS = load_json(CARS_FILE)
    return _CARS

# 🚀 INI ADALAH FUNGSI YANG HILANG DAN MENYEBABKAN CRASH
def load_motorcycles():
    global _MOTOR
    if _MOTOR is None:
        _MOTOR = load_json(MOTORCYCLES_FILE)
    return _MOTOR
    
def load_slang():
    return load_json(SLANG_FILE)

def load_systems():
    return load_json(SYSTEMS_FILE)

def load_severity():
    return load_json(SEVERITY_FILE)

def load_driveability():
    return load_json(DRIVEABILITY_FILE)

def load_validation():
    return load_json(VALIDATION_FILE)

def load_taxonomy():
    return load_json(TAXONOMY_FILE)
