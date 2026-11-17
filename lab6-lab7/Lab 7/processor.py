import math

MENU_PRICES = {
    "LAT": 4.50,
    "CAP": 4.00,
    "ESP": 3.00,
    "AME": 3.50,
    "MOC": 5.00,  # fixed: was "MOc", which could never match an uppercased prefix
}


def lookup_drink_code(code_string):
    """Return the base price for a drink code, or None if the input is invalid/unknown."""
    if not isinstance(code_string, str):
        return None
    code_prefix = code_string.strip().upper()[:3]
    return MENU_PRICES.get(code_prefix)


def calculate_average_shot_cost(pricing_csv):
    """Return the average of comma-separated prices, or None if input is invalid."""
    if not isinstance(pricing_csv, str) or not pricing_csv.strip():
        return None
    prices = []
    for p in pricing_csv.split(','):
        p = p.strip()
        if not p:
            return None  # empty element, e.g. "1.0,,2.0"
        try:
            value = float(p)
        except (ValueError, OverflowError):
            return None
        if not math.isfinite(value) or value < 0:  # rejects nan, inf, negatives
            return None
        prices.append(value)
    if not prices:
        return None
    avg = sum(prices) / len(prices)
    return avg if math.isfinite(avg) else None  # guards against overflow to inf


def parse_order_modifiers(order_spec):
    """Parse 'key:value;key:value' into a dict. Malformed pairs are skipped."""
    modifier_dict = {}
    if not isinstance(order_spec, str):
        return modifier_dict
    for item in order_spec.split(';'):
        if ':' not in item:
            continue  # no separator -> skip
        key, value = item.split(':', 1)  # maxsplit=1 so values may contain ':'
        key, value = key.strip(), value.strip()
        if key:
            modifier_dict[key] = value
    return modifier_dict


def main():
    print("==== Running lookup_drink_code ====")
    drink_input = input("Enter drink code prefix (e.g. LAT, CAP, ESP): ")
    price = lookup_drink_code(drink_input)
    print("Base Price: $", price if price is not None else "Invalid drink code")

    print("\n==== Running calculate_average_shot_cost ====")
    shots_input = input("Enter CSV of shot prices (e.g. 1.0, 1.5, 2.0): ")
    avg_price = calculate_average_shot_cost(shots_input)
    print("Average Shot Price: $", avg_price if avg_price is not None else "Invalid price list")

    print("\n==== Running parse_order_modifiers ====")
    spec_input = input("Enter modifiers (e.g. milk:oat;syrup:vanilla): ")
    mods = parse_order_modifiers(spec_input)
    print("Parsed Modifiers:", mods)


if __name__ == "__main__":
    main()
