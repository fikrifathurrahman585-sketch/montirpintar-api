import json
import os

BASE = os.path.dirname(__file__)

OLD_FILES = [
    "../cars.json",
    "../motorcycles.json"
]

components = []
faults = []
symptoms = []
repairs = []
costs = []

component_index = {}
fault_index = {}

component_counter = 1
fault_counter = 1


def save(name, data):
    with open(
        os.path.join(BASE, name),
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


for file_name in OLD_FILES:

    path = os.path.join(BASE, file_name)

    if not os.path.exists(path):
        continue

    with open(path, encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        continue

    for item in data:

        diagnosa = item.get("diagnosa_ai","").strip()

        solusi = item.get("solusi","").strip()

        biaya = item.get("estimasi_biaya","").strip()

        keywords = item.get("kata_kunci",[])

        if diagnosa == "":
            continue

        if diagnosa not in component_index:

            component_code = f"CMP_{component_counter:05d}"

            component_counter += 1

            component_index[diagnosa] = component_code

            components.append({
                "code":component_code,
                "id":diagnosa,
                "en":"",
                "category":"UNKNOWN"
            })

        component_code = component_index[diagnosa]

        fault_code = f"FLT_{fault_counter:05d}"

        fault_counter += 1

        faults.append({
            "code":fault_code,
            "component":component_code,
            "severity":"UNKNOWN",
            "driveability":"UNKNOWN"
        })

        symptoms.append({
            "fault":fault_code,
            "keywords":keywords
        })

        repairs.append({
            "fault":fault_code,
            "repair":solusi
        })

        costs.append({
            "fault":fault_code,
            "price":biaya
        })

save("components.json",components)
save("faults.json",faults)
save("symptoms.json",symptoms)
save("repairs.json",repairs)
save("costs.json",costs)

print("Selesai Migrasi Dataset.")
