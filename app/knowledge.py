# ==========================================================
# KNOWLEDGE ENGINE V4
# ==========================================================

COMPONENT_GROUPS = {

    "engine": [
        "mesin",
        "klep",
        "camshaft",
        "kruk",
        "noken",
        "bearing",
        "connecting rod",
        "piston",
        "ring piston",
        "head"
    ],

    "cvt": [
        "roller",
        "v belt",
        "vbelt",
        "kampas ganda",
        "clutch",
        "torque driver",
        "bearing cvt"
    ],

    "transmission": [
        "transmisi",
        "gear",
        "kopling",
        "synchromesh",
        "input shaft",
        "output shaft"
    ],

    "brake": [
        "cakram",
        "kampas rem",
        "kaliper",
        "master rem",
        "selang rem"
    ],

    "suspension": [
        "shock",
        "tie rod",
        "rack steer",
        "ball joint",
        "bushing"
    ],

    "cooling": [
        "radiator",
        "waterpump",
        "thermostat",
        "coolant",
        "kipas"
    ]

}

# ==========================================================
# DETEKSI KOMPONEN
# ==========================================================

def detect_component(text):

    text = text.lower()

    result = []

    for system, components in COMPONENT_GROUPS.items():

        for component in components:

            if component in text:

                result.append(component)

    return result

# ==========================================================
# SKOR KOMPONEN
# ==========================================================

def component_score(user_input, item):

    score = 0

    components = detect_component(user_input)

    dataset_components = item.get(
        "components",
        []
    )

    for component in components:

        if component in dataset_components:

            score += 20

    return score
