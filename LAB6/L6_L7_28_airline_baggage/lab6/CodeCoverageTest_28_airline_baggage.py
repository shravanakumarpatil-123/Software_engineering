import pytest

from airline_baggage import baggage_fee, carry_on_ok, check_in_status


def test_baggage_fee_rejects_unknown_cabin():
    with pytest.raises(ValueError, match="unknown cabin"):
        baggage_fee("first", 10, "domestic", False)


def test_baggage_fee_rejects_negative_weight():
    with pytest.raises(ValueError, match="invalid weight"):
        baggage_fee("economy", -1, "domestic", False)


@pytest.mark.parametrize(
    ("cabin", "weight", "route", "is_member", "expected"),
    [
        ("economy", 15, "domestic", False, 0),
        ("economy", 25, "domestic", True, 0),
        ("premium", 36, "domestic", True, 20),
        ("business", 41, "domestic", True, 20),
        ("economy", 36, "domestic", False, 840),
        ("premium", 26, "international", False, 45),
        ("economy", 36, "international", False, 2100),
        ("economy", 36, "other", False, 1890),
    ],
)
def test_baggage_fee_valid_cases(cabin, weight, route, is_member, expected):
    assert baggage_fee(cabin, weight, route, is_member) == expected


@pytest.mark.parametrize(
    ("weight", "items", "is_infant", "expected"),
    [
        (8, 2, True, True),
        (8, 3, True, False),
        (8, 1, False, False),
        (7, 1, False, True),
        (5, 2, False, False),
    ],
)
def test_carry_on_cases(weight, items, is_infant, expected):
    assert carry_on_ok(weight, items, is_infant) is expected


@pytest.mark.parametrize(
    ("minutes_before", "has_baggage", "is_international", "expected"),
    [
        (60, True, False, "open"),
        (45, True, False, "late"),
        (44, True, False, "closed"),
        (45, False, False, "open"),
        (90, False, True, "late"),
        (89, False, True, "closed"),
        (120, True, True, "open"),
    ],
)
def test_check_in_status_cases(minutes_before, has_baggage, is_international, expected):
    assert check_in_status(minutes_before, has_baggage, is_international) == expected
