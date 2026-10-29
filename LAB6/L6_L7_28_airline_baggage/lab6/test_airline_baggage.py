import pytest
from airline_baggage import baggage_fee, carry_on_ok, check_in_status

def test_within_allowance():
    assert baggage_fee("economy", 10, "domestic", False) == 0


def test_carry_on_ok():
    assert carry_on_ok(5, 1, False) is True
