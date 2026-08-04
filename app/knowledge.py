from app.loader import load

db = load()

# ==========================================================
# BUILD CACHE
# ==========================================================

_COMPONENTS = {
    item["id"]: item
    for item in db.get("components", [])
    if "id" in item
}

_FAULTS = {
    item["id"]: item
    for item in db.get("faults", [])
    if "id" in item
}

_REPAIRS = {
    item["component"]: item
    for item in db.get("repairs", [])
    if "component" in item
}

_COSTS = {
    item["component"]: item
    for item in db.get("costs", [])
    if "component" in item
}

_SYMPTOMS = {
    item["id"]: item
    for item in db.get("symptoms", [])
    if "id" in item
}

_ALIASES = {}

for item in db.get("aliases", []):

    word = item.get("word", "").lower().strip()

    replace = item.get("replace", "").lower().strip()

    if word:
        _ALIASES[word] = replace

# ==========================================================
# COMPONENT
# ==========================================================

def get_component(component_id: str):

    return _COMPONENTS.get(component_id)

# ==========================================================
# FAULT
# ==========================================================

def get_fault(fault_id: str):

    return _FAULTS.get(fault_id)

# ==========================================================
# REPAIR
# ==========================================================

def get_repair(component_id: str):

    return _REPAIRS.get(component_id)

# ==========================================================
# COST
# ==========================================================

def get_cost(component_id: str):

    return _COSTS.get(component_id)

# ==========================================================
# SYMPTOM
# ==========================================================

def get_symptom(symptom_id: str):

    return _SYMPTOMS.get(symptom_id)

# ==========================================================
# ALIAS
# ==========================================================

def get_alias(word: str):

    if not word:
        return ""

    word = word.lower().strip()

    return _ALIASES.get(
        word,
        word
    )

# ==========================================================
# COMPONENT SCORE
# ==========================================================

def component_score(user_input: str, item: dict):

    score = 0

    text = user_input.lower()

    component = item.get("component")

    if not component:
        return 0

    component_data = get_component(component)

    if not component_data:
        return 0

    names = []

    if "name" in component_data:
        names.append(component_data["name"])

    if "aliases" in component_data:
        names.extend(component_data["aliases"])

    for name in names:

        if name.lower() in text:

            score += 12

    return score
