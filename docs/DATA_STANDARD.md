# MontirPintar Data Standard

## Object Structure

Every diagnosis MUST follow this structure.

{
    id,
    vehicle,
    system,
    severity,
    driveability,
    language,
    cost
}

---

## ID Format

Cars

MBL_XXX_001

Motorcycles

MTR_XXX_001

---

## Vehicle

Allowed values

car

motorcycle

---

## Language

Must contain

id

en

---

## Cost

Must contain

idr

usd

---

## Severity

INFO

WARNING

DANGER

---

## Driveability

NORMAL

LIMITED

STOP

---

## JSON

UTF-8

No trailing comma

Valid JSON only
