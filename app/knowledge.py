from app.loader import load

db = load()


# ==========================================================
# COMPONENT
# ==========================================================

def get_component(component_id: str):

    for item in db["components"]:
        if item.get("id") == component_id:
            return item

    return None


# ==========================================================
# FAULT
# ==========================================================

def get_fault(fault_id: str):

    for item in db["faults"]:
        if item.get("id") == fault_id:
            return item

    return None


# ==========================================================
# REPAIR
# ==========================================================

def get_repair(component_id: str):

    for item in db["repairs"]:
        if item.get("component") == component_id:
            return item

    return None


# ==========================================================
# COST
# ==========================================================

def get_cost(component_id: str):

    for item in db["costs"]:
        if item.get("component") == component_id:
            return item

    return None


# ==========================================================
# SYMPTOM
# ==========================================================

def get_symptom(symptom_id: str):

    for item in db["symptoms"]:
        if item.get("id") == symptom_id:
            return item

    return None


# ==========================================================
# ALIAS
# ==========================================================

def get_alias(word: str):

    word = word.lower()

    for item in db["aliases"]:

        if word == item.get("word", "").lower():

            return item.get("replace")

    return word
