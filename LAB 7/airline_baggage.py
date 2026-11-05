import math
import re


_BOOKING_PATTERN = re.compile(
    r"(?P<airline>[A-Za-z]{2,3})-"
    r"(?P<flight>[0-9]+)-"
    r"(?P<row>[0-9]+)(?P<seat>[A-Za-z])"
)


def parse_booking(code):
    """Parse a booking code, returning None when its format is invalid."""
    if not isinstance(code, str):
        return None

    match = _BOOKING_PATTERN.fullmatch(code.strip())
    if match is None:
        return None

    try:
        flight = int(match.group("flight"))
        row = int(match.group("row"))
    except ValueError:
        # Very long digit strings may exceed Python's safe integer conversion limit.
        return None

    if flight <= 0 or row <= 0:
        return None

    return match.group("airline").upper(), flight, match.group("seat").upper()


def total_weight(weights_csv):
    """Sum comma-separated nonnegative finite weights; return None if invalid."""
    if not isinstance(weights_csv, str) or not weights_csv.strip():
        return None

    try:
        weights = [float(value.strip()) for value in weights_csv.split(",")]
    except ValueError:
        return None

    if not weights or any(not math.isfinite(weight) or weight < 0 for weight in weights):
        return None

    try:
        total = math.fsum(weights)
    except (OverflowError, ValueError):
        return None

    return total if math.isfinite(total) else None


def _valid_name_part(part):
    allowed_punctuation = {"'", "’", "-"}
    return (
        bool(part)
        and part[0].isalpha()
        and len(part[0].upper()) == 1
        and any(character.isalpha() for character in part)
        and all(character.isalpha() or character in allowed_punctuation for character in part)
    )


def tag_label(name):
    """Format a passenger label, returning None when a name is incomplete."""
    if not isinstance(name, str):
        return None

    parts = name.split()
    if len(parts) < 2:
        return None

    first, last = parts[0], parts[-1]
    if not _valid_name_part(first) or not _valid_name_part(last):
        return None

    return f"{first[0].upper()}. {last.upper()}"


def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter a booking code (e.g. AI-203-12A): ")
    result = parse_booking(user_input)
    print("Airline, Flight and Seat Letter:", result)

    print("\n==== Running total_weight ====")
    user_input = input("Enter bag weights in kg as CSV (e.g. 12.5,7,23): ")
    result = total_weight(user_input)
    print("Total Weight:", result)

    print("\n==== Running tag_label ====")
    user_input = input("Enter a passenger name (first and last): ")
    result = tag_label(user_input)
    print("Tag Label:", result)


if __name__ == "__main__":
    main()
