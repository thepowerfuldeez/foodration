import re
from utils import find_line, normalize_measurement, ITEMS_CODE, KILOGRAMM_CODE
from purchase import Purchase


def parse_receipt(raw_text):
    purchases = []
    raw_text_lines = raw_text.split("\n")
    items = [" ".join(a.split()[1:]) for a in re.findall("(?=\d+\. ).*", raw_text)]

    for i, it in enumerate(items):
        weight_search_result = re.search("\d+(\.d+)?\ ?(к?гр?|м?л|шт)", it)
        if weight_search_result:
            weight_start, weight_end = weight_search_result.span()
            name = it[:weight_start].strip()
            *_, weight, measurement = re.split("(\d+)", it[weight_start:weight_end])
            weight = float(weight.strip())
            try:
                measurement, to_divide = normalize_measurement(measurement.strip())
                weight /= to_divide
            except UnrecognizedMeasurement as e:
                print(e)
                measurement = ITEMS_CODE
        else:
            # weighted item, but ask user
            name = it
            measurement = KILOGRAMM_CODE
            weight = None

        if i < len(items)-1:
            i1, i2 = find_line(raw_text_lines, items[i]), find_line(raw_text_lines, items[i+1])
        else:
            i1, i2 = find_line(raw_text_lines, items[i]), len(raw_text_lines)
        if i1 is not None and i2 is not None:
            metadata = list(filter(lambda x: x, raw_text_lines[i1+1:i2]))
            quantity_line = metadata[0].split('x')[1].strip()
            full_price = float(quantity_line.split('=')[1].strip().replace(",", "."))
            quantity = float(quantity_line.split('=')[0].strip().replace(",", "."))
            if len(metadata) > 1:
                full_price -= float(metadata[1].split(":")[1].strip().replace(",", "."))

            if weight is None:
                if quantity == 1:
                    # TODO: suspicious, possibly it's pieces and it might not be one, ask user
                    measurement = ITEMS_CODE
                weight = quantity
                full_weight = weight
            else:
                if measurement == ITEMS_CODE:
                    # TODO: multiply by weight of one piece
                    pass
                full_weight = quantity * weight
#             print(f"Name: {name}, Weight: {weight} {code2name[measurement]}, "
#                   f"Quantity: {quantity}, Full weight: {full_weight} {code2name[measurement]} Full price: {full_price}")
            purchases.append(Purchase(name, weight, measurement, quantity, full_weight, full_price))
    return purchases
    