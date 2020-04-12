KILOGRAMM_CODE = 1
LITRES_CODE = 2
ITEMS_CODE = 3

code2name = {
    KILOGRAMM_CODE: "kg",
    LITRES_CODE: "litres",
    ITEMS_CODE: "items",
}


class UnrecognizedMeasurement(Exception):
    pass


def find_line(lines, substr):
    for i, line in enumerate(lines):
        if substr in line:
            return i
    return None


def normalize_measurement(msr):
    if msr in {"г", "гр", "грамм"}:
        return KILOGRAMM_CODE, 1000
    elif msr in {"кг",} or "килограмм" in msr:
        return KILOGRAMM_CODE, 1
    elif msr in {"л", } or "литр" in msr:
        return LITRES_CODE, 1
    elif msr in {"мл", } or "миллилитр" in msr:
        return LITRES_CODE, 1000
    elif msr in {"шт", } or "штук" in msr:
        # TODO: ask how much weigh one piece (with measurement)
        return ITEMS_CODE, 1
    else:
        raise UnrecognizedMeasurement(f"Cannot recognize measurement {msr}!")